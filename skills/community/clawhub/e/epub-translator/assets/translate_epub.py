#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translate_epub.py — EPUB 英→中 段落级双语对照翻译器

用法：
    python translate_epub.py <input.epub> <output.epub> [--concurrency 16] [--resume]

行为：
    - 解包 EPUB，遍历所有 (x)html 章节
    - 跳过：<pre>/<code>/<math>/<svg>/<script>/<style>、公式段、装饰段
    - 翻译：<p>/<li>/<h1-6>/<blockquote>/<caption>/<figcaption>，在原节点紧下方
      插入同类型的中文节点（class="translated-zh"）
    - 表格：在原 <table> 下方追加一份整表翻译版（class="translated-zh table-zh"）
    - 并行调用 Deepseek API，带缓存与断点续传
    - 注入 translated.css，重新打包为合规 EPUB

依赖：pip install openai beautifulsoup4 lxml
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import sys
import threading
import time
import traceback
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, NavigableString, Tag
from openai import OpenAI

# ============ 配置加载 ============
# 优先级：命令行 --config > 环境变量 > 同目录 / 上级目录的 config.json > config.example.json
#
# 关键字段（来自 config.json）：
#   model_name   : OpenAI 兼容模型名，如 "deepseek-v4-flash" / "gpt-4o-mini"
#   api_key      : API key（可由环境变量 API_KEY 覆盖）
#   base_url     : OpenAI 兼容服务的根地址（不含 /chat/completions），可由环境变量 BASE_URL 覆盖
#   extra_body   : dict, 传给 OpenAI SDK 的 extra_body（DeepSeek 关闭思考: {"thinking":{"type":"disabled"}}）
#   system_prompt: 翻译用系统提示词
#
# 注意：API key 等敏感字段不应直接出现在脚本里。请使用同目录的 config.json
# （或 config.example.json）配置，或者通过环境变量传入。


def _default_config_path() -> Path:
    """按优先级查找 config.json：脚本同目录 → assets 上一级 → 当前工作目录。"""
    here = Path(__file__).resolve().parent
    candidates = [
        here / "config.json",
        here.parent / "config.json",
        Path.cwd() / "config.json",
        here / "config.example.json",
        here.parent / "config.example.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        "未找到 config.json。请在 skill 目录下创建 config.json（参考 config.example.json）。"
    )


def load_config(path: Optional[Path] = None) -> Dict[str, object]:
    """加载配置文件并允许环境变量覆盖。"""
    cfg_path = Path(path) if path else _default_config_path()
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    # 去掉以 _ 开头的注释字段
    cfg = {k: v for k, v in cfg.items() if not k.startswith("_")}

    # 环境变量覆盖（最高优先级，便于在 CI / 临时调试时切换）
    if os.environ.get("MODEL_NAME"):
        cfg["model_name"] = os.environ["MODEL_NAME"]
    if os.environ.get("API_KEY"):
        cfg["api_key"] = os.environ["API_KEY"]
    if os.environ.get("BASE_URL"):
        cfg["base_url"] = os.environ["BASE_URL"]
    if os.environ.get("SYSTEM_PROMPT"):
        cfg["system_prompt"] = os.environ["SYSTEM_PROMPT"]

    # 兜底默认值
    cfg.setdefault("model_name", "deepseek-v4-flash")
    cfg.setdefault("extra_body", {})
    cfg.setdefault(
        "system_prompt",
        "你是一位专业的英→中技术翻译。只输出译文，保留 ⟦KEEP_n⟧ 占位符与专有名词。",
    )

    for k in ("api_key", "base_url", "model_name"):
        if not cfg.get(k):
            raise ValueError(
                f"配置缺少必填项: {k}。请在 config.json 中设置，或通过环境变量 {k.upper()} 提供。"
            )

    # 规范化 base_url：去掉末尾的 /chat/completions 与多余斜杠
    bu = str(cfg["base_url"]).strip().rstrip("/")
    if bu.endswith("/chat/completions"):
        bu = bu[: -len("/chat/completions")].rstrip("/")
    cfg["base_url"] = bu

    return cfg


# 全局配置（在 main() 里完成初始化；模块导入时延迟加载）
CONFIG: Dict[str, object] = {}

# ============ 跳过翻译的标签与正则 ============
# 注意：code 不在 SKIP_TAGS 中，因为行内 <code> 需要保留原文。
# 块级 <pre><code> 会因 <pre> 在 SKIP_TAGS 中而被整体跳过。
SKIP_TAGS = {"pre", "math", "svg", "script", "style", "noscript", "kbd", "samp", "tt"}
TRANSLATE_TAGS = {
    "p", "li", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6",
    "caption", "figcaption", "dd", "dt",
}
# Springer/出版社把"段落"用 <div class="Para"> 标记，把"代码块"用 <div class="ProgramCode"> 标记。
# 也兼容 ePub3/各出版社常见的代码块 class 名。
TRANSLATE_DIV_CLASSES = {"Para"}
SKIP_DIV_CLASSES = {
    # Springer
    "ProgramCode", "LineGroup", "FixedLine",
    "EmphasisFontCategoryNonProportional",  # 等宽字体（行内代码）
    # O'Reilly / Apress / 通用
    "code", "Code", "code-block", "CodeBlock", "listing", "Listing",
    "informalexample", "programlisting", "screen", "literallayout",
    # MathJax / 公式相关
    "MathJax", "math", "equation", "Equation", "EquationContent",
}

# 段落内需要保护的"片段"：行内代码、公式、URL
PLACEHOLDER_RE = re.compile(
    r"(`[^`\n]+`"          # `inline code`
    r"|\$\$[^$]+\$\$"      # $$ block math $$
    r"|\$[^$\n]+\$"        # $ inline math $
    r"|\\\([^)]+\\\)"      # \( inline math \)
    r"|\\\[[^\]]+\\\]"     # \[ block math \]
    r"|https?://\S+"       # URLs
    r")"
)

# 一个段落"看起来只是公式 / 数字 / 符号"，跳过翻译
PURE_NON_TEXT_RE = re.compile(
    r"^[\s\d\W_]*$|^\$[^$]+\$$|^\\\([^)]+\\\)$|^\\\[[^\]]+\\\]$"
)

CACHE: Dict[str, str] = {}
CACHE_PATH: Optional[Path] = None
CACHE_LOCK = threading.Lock()


# ============ OpenAI 兼容客户端 ============
CLIENT: Optional[OpenAI] = None


def make_client() -> OpenAI:
    """根据 CONFIG 构造 OpenAI 兼容客户端（懒加载）。"""
    if not CONFIG:
        raise RuntimeError("CONFIG 未初始化，请先调用 load_config()。")
    return OpenAI(
        api_key=str(CONFIG["api_key"]),
        base_url=str(CONFIG["base_url"]),
    )


def _client() -> OpenAI:
    global CLIENT
    if CLIENT is None:
        CLIENT = make_client()
    return CLIENT


def call_llm(text: str, max_retry: int = 5) -> str:
    """单次翻译调用，带指数退避重试。使用 CONFIG 中的 model_name / extra_body。"""
    backoff = 2.0
    last_err: Optional[Exception] = None
    model_name = str(CONFIG["model_name"])
    system_prompt = str(CONFIG.get("system_prompt", ""))
    extra_body = CONFIG.get("extra_body") or {}
    for attempt in range(max_retry):
        try:
            kwargs = dict(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                stream=False,
            )
            if extra_body:
                kwargs["extra_body"] = extra_body
            resp = _client().chat.completions.create(**kwargs)
            out = (resp.choices[0].message.content or "").strip()
            if out:
                return out
            last_err = RuntimeError("empty response")
        except Exception as e:
            last_err = e
        time.sleep(backoff)
        backoff *= 2
    print(f"  [WARN] 翻译失败，保留原文: {text[:60]}... err={last_err}", file=sys.stderr)
    return ""


# ============ 占位符保护 ============
def protect(text: str) -> Tuple[str, List[str]]:
    keeps: List[str] = []

    def _sub(m: re.Match) -> str:
        keeps.append(m.group(0))
        return f"⟦KEEP_{len(keeps) - 1}⟧"

    masked = PLACEHOLDER_RE.sub(_sub, text)
    return masked, keeps


def restore(text: str, keeps: List[str]) -> str:
    for i, k in enumerate(keeps):
        text = text.replace(f"⟦KEEP_{i}⟧", k)
    return text


# ============ 翻译入口（带缓存） ============
def translate_text(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    if text in CACHE:
        return CACHE[text]
    masked, keeps = protect(text)
    raw = call_llm(masked)
    if not raw:
        CACHE[text] = ""
        return ""
    zh = restore(raw, keeps).strip()
    CACHE[text] = zh
    return zh


def flush_cache() -> None:
    if CACHE_PATH is None:
        return
    with CACHE_LOCK:
        snapshot = dict(CACHE)  # 拷贝快照避免在写盘期间发生 dict resize
    tmp = CACHE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(CACHE_PATH)


def load_cache(resume: bool) -> None:
    global CACHE
    if CACHE_PATH and resume and CACHE_PATH.exists():
        try:
            CACHE = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            print(f"  [INFO] 命中缓存条目: {len(CACHE)}")
        except Exception as e:
            print(f"  [WARN] 加载缓存失败: {e}", file=sys.stderr)
            CACHE = {}


# ============ HTML 解析与翻译单元收集 ============
def _classes_of(node: Tag) -> List[str]:
    c = node.get("class", [])
    if isinstance(c, str):
        return c.split()
    return list(c or [])


def is_skippable_node(node: Tag) -> bool:
    """节点本身或祖先含跳过标签 / 跳过 class 则跳过。"""
    cur = node
    while cur is not None and isinstance(cur, Tag):
        name = (cur.name or "").lower()
        if name in SKIP_TAGS:
            return True
        if name == "div":
            for c in _classes_of(cur):
                if c in SKIP_DIV_CLASSES:
                    return True
        # span/em 上的等宽类也算行内代码
        if name in ("span", "em", "i", "b", "strong"):
            for c in _classes_of(cur):
                if c in SKIP_DIV_CLASSES:
                    return True
        cur = cur.parent
    return False


def node_pure_text(node: Tag) -> str:
    """提取节点的纯文本，自动跳过 skippable 子树（代码块/公式/img/...）。

    行内 <code> 标签的内容会用反引号包裹（`...`），以便 LLM 在翻译时保留原文。
    行内公式 <img> 标签会被替换为 ⟦FORMULA⟧ 占位符，翻译后还原。
    """
    parts: List[str] = []
    for desc in node.descendants:
        if isinstance(desc, NavigableString):
            parent = desc.parent
            if parent is not None and is_skippable_node(parent):
                continue
            s = str(desc)
            if s.strip():
                # 如果父节点是 <code>，用反引号包裹内容，让 LLM 保留原文
                if parent is not None and parent.name == "code":
                    parts.append(f"`{s}`")
                else:
                    parts.append(s)
        elif isinstance(desc, Tag) and desc.name == "img":
            # 行内公式图片：插入占位符，翻译后还原
            parent = desc.parent
            if parent is not None and not is_skippable_node(parent):
                parts.append("⟦FORMULA⟧")
    return " ".join(" ".join(parts).split())


def node_text_excluding_block_children(node: Tag) -> str:
    """提取节点文本，但排除内部已经是"独立段落级"的子节点（避免重复翻译）。

    用于 div.Para 这种容器：如果内部嵌套 <p>/<figure>/<figcaption>/<h*>，
    那些将由各自的逻辑单独翻译；外层 div 只翻译散落在外的散文文本。
    """
    block_children_tags = TRANSLATE_TAGS | {"figure", "table", "ul", "ol"}
    parts: List[str] = []
    for desc in node.descendants:
        if isinstance(desc, NavigableString):
            parent = desc.parent
            # 跳过 skippable 子树
            anc = parent
            in_block_child = False
            while anc is not None and anc is not node and isinstance(anc, Tag):
                if is_skippable_node(anc):
                    in_block_child = True
                    break
                if anc.name in block_children_tags:
                    in_block_child = True
                    break
                anc = anc.parent
            if in_block_child:
                continue
            s = str(desc)
            if s.strip():
                parts.append(s)
    return " ".join(" ".join(parts).split())


def should_translate_text(text: str) -> bool:
    if not text or len(text.strip()) < 2:
        return False
    if PURE_NON_TEXT_RE.match(text):
        return False
    # 已经全部是 CJK 字符 → 跳过
    cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    if cjk > 0 and cjk / max(len(text), 1) > 0.5:
        return False
    return True


def collect_units_in_html(soup: BeautifulSoup) -> Tuple[List[Tag], Dict[int, str]]:
    """收集需要翻译的段落级节点。

    返回 (units, text_overrides)：
    - units：待翻译节点列表
    - text_overrides：dict[id(node) -> str]，对某些节点（如 div.Para 内含子段落的容器），
      要用"剥除子段落后的散文文本"作为翻译输入，而非默认的 node_pure_text。

    幂等性保证：
    - 跳过任何 class 已含 `translated-zh` 的节点。
    - 跳过任何已经有"紧邻 translated-zh 兄弟"的源节点。
    """
    units: List[Tag] = []
    text_overrides: Dict[int, str] = {}
    seen_ids: set = set()

    def _already_translated(node: Tag) -> bool:
        if "translated-zh" in _classes_of(node):
            return True
        nxt = node.find_next_sibling()
        if nxt is not None and isinstance(nxt, Tag) and "translated-zh" in _classes_of(nxt):
            return True
        return False

    # 1. 标准段落级标签
    for tag in soup.find_all(TRANSLATE_TAGS):
        if is_skippable_node(tag):
            continue
        if _already_translated(tag):
            continue
        if tag.name == "li" and tag.find(["p", "blockquote"]):
            continue
        if tag.find_parent("table") is not None:
            continue
        text = node_pure_text(tag)
        if should_translate_text(text):
            if id(tag) not in seen_ids:
                seen_ids.add(id(tag))
                units.append(tag)

    # 2. 出版社特有的 <div class="Para"> 等"段落 div"
    for tag in soup.find_all("div"):
        if is_skippable_node(tag):
            continue
        if _already_translated(tag):
            continue
        classes = _classes_of(tag)
        if not any(c in TRANSLATE_DIV_CLASSES for c in classes):
            continue

        # 内部含 figure/p/h*/li/ul/ol 等"块级子段落"时：
        # - 内部的子段落由各自的逻辑独立翻译
        # - 外层 div 仅翻译"剥除这些子段落之后"剩下的散文，避免重复
        has_block_child = bool(tag.find(TRANSLATE_TAGS | {"figure", "table", "ul", "ol"}))
        if has_block_child:
            residual = node_text_excluding_block_children(tag)
            if should_translate_text(residual) and id(tag) not in seen_ids:
                # 注意：因为 div 内部有子节点，append 译文兄弟也可能改变文档结构，
                # 但 BeautifulSoup 的 insert_after 是在 parent 内的同级位置插入，安全。
                seen_ids.add(id(tag))
                text_overrides[id(tag)] = residual
                units.append(tag)
            continue

        text = node_pure_text(tag)
        if should_translate_text(text) and id(tag) not in seen_ids:
            seen_ids.add(id(tag))
            units.append(tag)

    return units, text_overrides


def collect_tables(soup: BeautifulSoup) -> List[Tag]:
    return [t for t in soup.find_all("table") if not is_skippable_node(t)]


def collect_table_cell_texts(table: Tag) -> List[str]:
    texts: List[str] = []
    for cell in table.find_all(["th", "td"]):
        if is_skippable_node(cell):
            continue
        t = node_pure_text(cell)
        if should_translate_text(t):
            texts.append(t)
    return texts


# ============ 并行翻译 ============
def translate_batch(unique_texts: List[str], concurrency: int) -> Dict[str, str]:
    todo = [t for t in unique_texts if t not in CACHE]
    if not todo:
        return {t: CACHE.get(t, "") for t in unique_texts}

    total = len(todo)
    # 自适应 flush 间隔：总数大时拉大间隔，避免频繁写大 json 阻塞线程切换
    flush_every = max(50, total // 20)
    print(f"  [INFO] 待翻译 {total} 条 (并发 {concurrency}, flush 每 {flush_every} 条) ...")
    done = 0
    t_start = time.time()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(translate_text, t): t for t in todo}
        for fu in as_completed(futures):
            try:
                fu.result()
            except Exception as e:
                print(f"  [ERR] {e}", file=sys.stderr)
            done += 1
            if done % flush_every == 0 or done == total:
                elapsed = time.time() - t_start
                rate = done / elapsed if elapsed > 0 else 0
                eta = (total - done) / rate if rate > 0 else 0
                print(f"    ... {done}/{total}  {rate:.1f}/s  ETA {eta:.0f}s")
                flush_cache()
    flush_cache()
    return {t: CACHE.get(t, "") for t in unique_texts}


# ============ 写回 HTML ============
def insert_translation_node(soup: BeautifulSoup, node: Tag, zh: str) -> None:
    if not zh:
        return
    # 幂等性：避免在已经有 translated-zh 紧邻兄弟的情况下重复插入
    nxt = node.find_next_sibling()
    if nxt is not None and isinstance(nxt, Tag) and "translated-zh" in _classes_of(nxt):
        return
    new_tag = soup.new_tag(node.name)
    # 去重 class（避免 translated-zh translated-zh）
    classes = list(dict.fromkeys(_classes_of(node) + ["translated-zh"]))
    new_tag["class"] = classes

    # 收集源节点中的 <img> 标签（公式图片），用于还原 ⟦FORMULA⟧ 占位符
    source_imgs = list(node.find_all("img", recursive=True))
    img_idx = 0

    # 将反引号包裹的片段（`...`）转换为 <code> 标签，
    # 将 ⟦FORMULA⟧ 还原为源节点中的 <img> 标签
    _token_re = re.compile(r'`([^`]+)`|⟦FORMULA⟧')
    last_end = 0
    for m in _token_re.finditer(zh):
        pre_text = zh[last_end:m.start()]
        if pre_text:
            new_tag.append(NavigableString(pre_text))
        if m.group(1) is not None:
            # 反引号包裹的代码
            code_tag = soup.new_tag("code")
            code_tag.string = m.group(1)
            new_tag.append(code_tag)
        else:
            # ⟦FORMULA⟧ 占位符：从源节点复制对应的 <img>
            if img_idx < len(source_imgs):
                new_tag.append(copy.copy(source_imgs[img_idx]))
                img_idx += 1
        last_end = m.end()
    if last_end < len(zh):
        new_tag.append(NavigableString(zh[last_end:]))

    # 如果没有匹配到任何 token，使用原始方式
    if not list(new_tag.children):
        new_tag.string = zh

    node.insert_after(new_tag)


def translate_table_node(soup: BeautifulSoup, table: Tag) -> None:
    # 幂等性：如果下一个兄弟已经是 translated-zh 的翻译表，跳过
    nxt = table.find_next_sibling()
    if nxt is not None and isinstance(nxt, Tag):
        ncls = _classes_of(nxt)
        if "translated-zh" in ncls and "table-zh" in ncls:
            return
    cloned = copy.deepcopy(table)
    changed = False
    for cell in cloned.find_all(["th", "td"]):
        if is_skippable_node(cell):
            continue
        text = node_pure_text(cell)
        if not should_translate_text(text):
            continue
        zh = CACHE.get(text, "")
        if zh:
            # 简单替换：清空原内容，写入中文
            cell.clear()
            cell.append(NavigableString(zh))
            changed = True
    if changed:
        classes = list(dict.fromkeys(_classes_of(cloned) + ["translated-zh", "table-zh"]))
        cloned["class"] = classes
        table.insert_after(cloned)


# ============ EPUB 打包/解包 ============
def unpack_epub(epub_path: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(epub_path, "r") as zf:
        zf.extractall(dest)


def pack_epub(src_dir: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()
    # mimetype 必须 STORED 且为第一个条目
    with zipfile.ZipFile(out_path, "w") as zf:
        mt = src_dir / "mimetype"
        if mt.exists():
            zi = zipfile.ZipInfo("mimetype")
            zi.compress_type = zipfile.ZIP_STORED
            zf.writestr(zi, mt.read_bytes())
        for root, _, files in os.walk(src_dir):
            for name in files:
                p = Path(root) / name
                rel = p.relative_to(src_dir).as_posix()
                if rel == "mimetype":
                    continue
                zf.write(p, rel, compress_type=zipfile.ZIP_DEFLATED)


# ============ CSS 注入 ============
TRANSLATED_CSS = """
/* === translated-zh: 双语段落样式 === */
.translated-zh {
    color: #1a4d8c;
    font-family: "LXGW WenKai", "Source Han Serif SC", "Noto Serif CJK SC", "Microsoft YaHei", serif;
    line-height: 1.8;
    margin-top: 0.2em;
    margin-bottom: 1em;
    border-left: 3px solid #c5d6ec;
    padding-left: 0.6em;
}
.translated-zh.table-zh {
    margin-top: 0.5em;
    border-top: 2px dashed #888;
    border-left: none;
    padding-left: 0;
}
""".lstrip()


def inject_css(work_dir: Path) -> None:
    """把 translated.css 放到与 content.opf 同级的 styles 目录或 OEBPS 根，并写入引用。"""
    # 找到所有 xhtml/html 文件
    html_files = list(work_dir.rglob("*.xhtml")) + list(work_dir.rglob("*.html"))
    if not html_files:
        return

    # 把 css 文件放到第一个 html 同级目录
    base = html_files[0].parent
    css_path = base / "translated.css"
    css_path.write_text(TRANSLATED_CSS, encoding="utf-8")

    for hf in html_files:
        try:
            soup = BeautifulSoup(hf.read_text(encoding="utf-8"), "lxml-xml")
        except Exception:
            soup = BeautifulSoup(hf.read_text(encoding="utf-8"), "html.parser")
        head = soup.find("head")
        if head is None:
            continue
        # 已有则跳过
        already = any(
            (link.get("href", "") or "").endswith("translated.css")
            for link in head.find_all("link")
        )
        if already:
            continue
        rel = os.path.relpath(css_path, hf.parent).replace("\\", "/")
        link = soup.new_tag("link", rel="stylesheet", type="text/css", href=rel)
        head.append(link)
        hf.write_text(str(soup), encoding="utf-8")

    # 把 css 登记到 content.opf
    opfs = list(work_dir.rglob("*.opf"))
    for opf in opfs:
        try:
            soup = BeautifulSoup(opf.read_text(encoding="utf-8"), "lxml-xml")
        except Exception:
            continue
        manifest = soup.find("manifest")
        if manifest is None:
            continue
        if any(
            (it.get("href", "") or "").endswith("translated.css")
            for it in manifest.find_all("item")
        ):
            continue
        rel = os.path.relpath(css_path, opf.parent).replace("\\", "/")
        item = soup.new_tag(
            "item", id="translated-css", href=rel,
        )
        item["media-type"] = "text/css"
        manifest.append(item)
        opf.write_text(str(soup), encoding="utf-8")


# ============ 主流程 ============
def scan_html_file(hf: Path) -> Tuple[BeautifulSoup, List[Tag], Dict[int, str], List[Tag], List[str]]:
    """扫描单个 html 文件，返回 (soup, para_units, text_overrides, tables, unique_texts)。
    不调用 API，只解析 DOM 与抽取文本，可以多线程并行执行。
    """
    raw = hf.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    para_units, text_overrides = collect_units_in_html(soup)
    tables = collect_tables(soup)
    unique: List[str] = []
    seen = set()
    for n in para_units:
        t = text_overrides.get(id(n)) or node_pure_text(n)
        if t and t not in seen:
            seen.add(t)
            unique.append(t)
    for tb in tables:
        for t in collect_table_cell_texts(tb):
            if t and t not in seen:
                seen.add(t)
                unique.append(t)
    return soup, para_units, text_overrides, tables, unique


def writeback_html_file(hf: Path, soup: BeautifulSoup, para_units: List[Tag],
                        text_overrides: Dict[int, str], tables: List[Tag]) -> int:
    """把缓存中的译文写回 DOM，并保存文件。返回插入译文数。"""
    inserted = 0
    for n in para_units:
        t = text_overrides.get(id(n)) or node_pure_text(n)
        zh = CACHE.get(t, "")
        if zh:
            # insert_translation_node 内部有幂等检查
            before = id(n.find_next_sibling())
            insert_translation_node(soup, n, zh)
            after = id(n.find_next_sibling())
            if before != after:
                inserted += 1
    for tb in tables:
        translate_table_node(soup, tb)
    hf.write_text(str(soup), encoding="utf-8")
    return inserted


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="输入 EPUB 文件")
    ap.add_argument("output", help="输出 EPUB 文件")
    ap.add_argument("--config", default=None,
                    help="配置文件路径（默认按优先级查找 config.json）")
    ap.add_argument("--concurrency", type=int, default=64,
                    help="并发线程数 (默认 64；急速档 96)")
    ap.add_argument("--work-dir", default=None, help="工作目录 (默认在临时目录)")
    ap.add_argument("--resume", action="store_true",
                    help="复用 cache.json 断点续传；幂等：源 EPUB 重新解包，已写过的译文也会被检测跳过")
    args = ap.parse_args()

    # 加载配置（API key / base_url / model_name 等）
    global CONFIG
    try:
        CONFIG = load_config(Path(args.config) if args.config else None)
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERR] {e}", file=sys.stderr)
        return 2
    masked_key = (
        (str(CONFIG["api_key"])[:6] + "..." + str(CONFIG["api_key"])[-4:])
        if len(str(CONFIG["api_key"])) > 12 else "***"
    )
    print(f"[CONFIG] model={CONFIG['model_name']} base_url={CONFIG['base_url']} key={masked_key}")

    t0 = time.time()
    in_path = Path(args.input).resolve()
    out_path = Path(args.output).resolve()
    if not in_path.exists():
        print(f"[ERR] 输入文件不存在: {in_path}", file=sys.stderr)
        return 1

    work_dir = (
        Path(args.work_dir).resolve()
        if args.work_dir
        else Path.cwd() / f".epub-translate-{in_path.stem}"
    )
    if work_dir.exists() and not args.resume:
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    global CACHE_PATH
    CACHE_PATH = work_dir / "cache.json"
    load_cache(args.resume)

    extract_dir = work_dir / "extract"
    # 幂等关键：--resume 模式下也强制重新解包源 EPUB，避免在已含译文的 DOM 上重复插入
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    unpack_epub(in_path, extract_dir)
    print(f"[OK] 已解包到 {extract_dir}")

    html_files = sorted(
        list(extract_dir.rglob("*.xhtml")) + list(extract_dir.rglob("*.html"))
    )
    print(f"[OK] 发现 {len(html_files)} 个章节文件")

    # ---- 阶段 1：全局扫描所有章节，收集全部唯一翻译文本 ----
    print("[PHASE 1] 扫描所有章节，收集唯一文本 ...")
    scan_results: List[Tuple[Path, BeautifulSoup, List[Tag], Dict[int, str], List[Tag], List[str]]] = []
    global_unique: List[str] = []
    global_seen: set = set()
    for hf in html_files:
        try:
            soup, paras, overrides, tables, uniques = scan_html_file(hf)
        except Exception:
            print(f"[ERR] 扫描 {hf.name} 失败:\n{traceback.format_exc()}", file=sys.stderr)
            continue
        scan_results.append((hf, soup, paras, overrides, tables, uniques))
        for t in uniques:
            if t not in global_seen:
                global_seen.add(t)
                global_unique.append(t)
        print(f"  - {hf.name:<55s} paras={len(paras):4d} tables={len(tables):3d} unique={len(uniques):4d}")

    total_files = len(scan_results)
    total_unique = len(global_unique)
    todo = [t for t in global_unique if t not in CACHE]
    print(f"[PHASE 1 DONE] 章节={total_files} 全局唯一文本={total_unique} 已缓存={total_unique - len(todo)} 需翻译={len(todo)}")

    # ---- 阶段 2：一次性提交所有文本到全局线程池并行翻译 ----
    if todo:
        print(f"[PHASE 2] 全局并行翻译 (并发={args.concurrency}) ...")
        translate_batch(global_unique, concurrency=args.concurrency)
    else:
        print("[PHASE 2] 全部命中缓存，无需调用 API")

    # ---- 阶段 3：把译文写回所有章节 DOM ----
    print("[PHASE 3] 写回译文并保存章节文件 ...")
    total_inserted = 0
    for hf, soup, paras, overrides, tables, _ in scan_results:
        try:
            inserted = writeback_html_file(hf, soup, paras, overrides, tables)
            total_inserted += inserted
        except Exception:
            print(f"[ERR] 写回 {hf.name} 失败:\n{traceback.format_exc()}", file=sys.stderr)
    print(f"[PHASE 3 DONE] 共写入译文节点 {total_inserted} 个")

    inject_css(extract_dir)
    print("[OK] 已注入 translated.css")

    pack_epub(extract_dir, out_path)
    dt = time.time() - t0
    print(f"[DONE] 输出 EPUB: {out_path}  耗时 {dt:.1f}s")
    print("[NEXT] 请调用 epub-reader-optimizer skill 对成品做样式美化。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
