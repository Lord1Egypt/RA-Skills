#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-base 通用工作台 UI 细节自动检查引擎（C-detail-* 机检目录）。

零第三方依赖（仅标准库）。本文件是 **ct- 家族统一底座**里的通用引擎，供所有叶技能
"随包获得副本 + 提供 wb_detail_check.rules.json 扩展" 使用——引擎本身 **零叶子硬编码**：

  - 家族级默认词表（模糊名 / 泛词 / 承诺式 / i18n 白名单）已内置于此，全家族通用；
  - 叶子特定的词表追加、i18n 白名单覆盖、以及 C-detail-scope / C-detail-dupctl 的
    选择器 / scope 取值，全部经 `<root>/scripts/wb_detail_check.rules.json` 注入；
  - 因此同一份引擎可被 ct-literature / ct-registry / meta-analysis 等任意叶技能复用，
    不需每个技能复制一份写死自己选择器的大脚本。

覆盖的检查（全部可由 rules.json 配置，无浏览器即可判定）：
  C-detail-label       模糊名扫描（FAIL）—— 红线 3
  C-detail-placeholder 占位泛词扫描（FAIL，属性）/ 空态泛词（WARN，容器）—— 红线 4
  C-detail-claim       输入语法类承诺扫描（WARN→FAIL）—— 红线 1
  C-detail-i18n-ph     单语静态占位扫描（WARN）—— 红线 4
  C-detail-scope       表单态 scope 覆盖（FAIL，rules.scope 驱动）—— 红线 2
  C-detail-dupctl      相似/冗余控件（WARN，rules.dupctl 驱动）—— 红线 2
  C-detail-dupdst      写入目标重复（FAIL，结构冲突）—— 同一 data-dst/name 被 ≥2 控件占用
  C-detail-emptystate  空态引导（WARN，容器扫描版）—— 红线 4
  C-detail-escape      渲染层吞字符/未转义扫描（FAIL，红线 8）—— 2026-10-25 新增

  C-detail-dupctl / C-detail-dupdst 解决的是同一类缺陷家族的不同层级：
    - dupdst 是**结构层**：两个控件把值写进同一个 data-dst/name（取哪个由浏览器决定，
      互相覆盖）——纯机械、零配置即可判。
    - dupctl 是**语义层**：两个控件管「同一件事」但写法/标签不同（如 schema 渲染的
      n_sim 整数框 与 硬编码「蒙特卡洛精确功效带（模拟 2000 次）」复选框都控制 MC
      模拟），文本上毫不相干、data-dst 也不同，只能靠 rules.json 声明的「概念重叠」
      （concepts：字段名 + 关键词）识别。本检查器不做任何语义臆测，完全规则驱动。
  这类缺陷页面照常渲染、用户能操作，但行为冲突（改次数还是勾框？），属 §21.1 缺陷
  家族 G（控件语义冲突）——此前无法被任何 C-detail-* 抓到，本次新增。

  C-detail-escape 机制（沉淀自 ct-samplesize v5.13.4x「随机优势 φ = P(X<Y)」断裂实战）：
  拼 innerHTML 的 JS 字符串里含**裸 < 后跟字母且 < 前有非空白字符**（数学/逻辑文案，
  如 "P(X<Y)"、"n<5"），浏览器把 "<Y)" 当标签吞掉 → 用户看到断裂文案；**裸 < 后跟数字**
  在任何位置即危险（合法 HTML 标签名不可能数字开头）。这类缺陷页面照常渲染、控制台零
  error、截图静态查看也未必发现，属 §21.1 缺陷家族 F（渲染层未转义）。机检判据：
    - 字符串含 esc(/escapeHtml(/escHtml( 调用 → 视为已走转义，豁免；
    - "</" 闭合标签、"<!--" 注释不命中；
    - 裸 & 后紧跟字母且非 &entity; 形式 → WARN（与号通常原样显示，风险低于 <）；
    - rules.json 的 escape_allow_add 可追加豁免串（逐条白名单，防误伤）。

设计要点（降噪，详见 ct-base `references/workbench_ui.md` §21）：
  - claim 只盯"输入语法类承诺"（"可直接写 P:" / "支持…语法" 等后端可能不解析的
    输入格式声明），不把"会自动翻译"这类真实存在的自动行为误伤。
  - placeholder 属性扫描用泛词子串命中（高置信→FAIL）；空态容器扫描要求归一化后
    精确等于泛词（避免"暂无决策"被"暂无"误伤），且降为 WARN。
  - i18n-ph 排除"例：/例如：/如 "等示例前缀与常见单语字段（密码/备注/英文检索词），
    仅对"看起来是引导文案却单语"的占位报 WARN。
  - scope / dupctl 完全规则驱动：引擎不认识 `.picos-in` 或任何叶子的 class，全部从
    rules.json 读。

rules.json 字段（全部可选，缺省走家族默认）：
  fuzzy_labels_add:        []   追加模糊名
  placeholder_generics_add:[]  追加占位泛词
  emptystate_generics_add: []  追加空态泛词
  claim_patterns_add:      []  追加承诺式正则（字符串，引擎编译）
  i18n_whitelist_add:      []  追加单语字段白名单
  i18n_whitelist_force:    []  覆盖（而非追加）i18n 白名单
  scope: { "selectors": ["#center .picos-in", ".my-input"], "values": ["seed","result"] }
  dupctl: {
    "pairs": [["重新评估","确认 PICOS"]],
    "concepts": [{"names": ["n_sim"], "keywords": ["蒙特卡洛","monte carlo"], "owner": "schema"}],
    "generic_similarity": false
  }
  escape_allow_add:     []   追加吞字符豁免串（已验证安全的字面量，逐条白名单）
  escape_tag_allow_add: []   追加「非 HTML 但合法」的标签名（如 Define-XML 的
                             itemdef / itemref / odm；含命名空间前缀写 def:leaf）。
                             适用于生成 XML 文档的拼接代码，避免被当 innerHTML 误报。
  enable: { "scope": false, "dupctl": false, "dupdst": false }   # 三项默认关，需叶子显式开启

用法：
  python wb_detail_check.py                 # 自动定位同技能根的 workbench.html + rules.json
  python wb_detail_check.py --html <path>   # 指定文件（也接受目录：自动找 workbench.html/index.html）
  python wb_detail_check.py --root <dir>    # 技能根（自动找 workbench.html 与 scripts/rules.json）
  python wb_detail_check.py --rules <path>  # 显式指定规则文件

扫描范围（2026-10-30 改造）：
  入口 HTML **及其引用的本地外链资源**（`<link href>` / `<script src>`）会被合并扫描，
  因此同时兼容两种工作台形态：
    - 全内联单文件（ct-advisor：HTML 内含 <script>）——行为与改造前完全一致；
    - HTML + 外链 app.js（meta-analysis / ct-literature / ct-sdtm）——JS 模板里的
      `class="picos-in..."`、`placeholder="..."` 现在也能被 C-detail-* 看到。
  改造前引擎只读单个 HTML 文本，外链化后 C-detail-scope 恒判「覆盖到 0 个元素」假 FAIL。
  C-detail-escape 仍只扫 JS 字符串字面量（内联 script 体 + 外链 js 文件）。

退出码：0 = 全绿（无 FAIL）；非 0 = 存在 FAIL（用于阻断发布）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# —— 家族级默认词表（全 ct- 工作台通用；叶技能用 rules.json 扩展，不在此写死）——
DEFAULT_FUZZY_LABELS = [
    "中英对照", "高级", "更多", "设置", "其他", "自定义", "更多选项", "其它",
]
DEFAULT_PLACEHOLDER_GENERICS = [
    "待填", "to fill", "请输入", "无数据", "未填写",
]
DEFAULT_EMPTYSTATE_GENERICS = ["无数据", "待填", "未填写", "暂无"]
# 红线 1：输入语法类承诺（后端可能不解析的输入格式声明）—— 仅此类，避免误伤真实自动行为
# 注意：必须紧跟"写/Write"等输入动作，不单独用"可直接"（会误伤"可直接重试/上传"等合法指引）
DEFAULT_CLAIM_PATTERNS = [
    r"可直接写",
    r"请直接写",
    r"支持.+语法",
    r"write\s+[\"']P\s*:",
    r"写\s*[\"“]P\s*:",
]
# i18n-ph 排除：示例前缀 + 常见单语字段白名单
DEFAULT_I18N_PH_EXAMPLE_PREFIX = ("例：", "例如：", "如 ")
DEFAULT_I18N_PH_WHITELIST = ("密码", "备注", "英文检索词", "如 ")
# C-detail-escape：字符串内出现这些转义函数调用 → 视为已走转义，豁免裸 < 检查
DEFAULT_ESCAPE_FUNCS = ("esc(", "escapeHtml(", "escHtml(", "escapeHTML(",
                        # XML/通用转义（ct-adam 生成 Define-XML 用 escXML）
                        "escXML(", "escXml(", "escapeXml(", "escapeXML(", "xmlEsc(")

# 扫描"可见文案"的标签（其 inner text 参与 label 模糊名检查）
LABEL_TAGS = ["label", "button", "summary", "option"]

RULES_FILENAME = "wb_detail_check.rules.json"


# ———————————————————————————————————————————————————————
# 规则加载（合并家族默认 + 叶子 rules.json）
# ———————————————————————————————————————————————————————
def load_rules(rules_path: Path | None):
    cfg = {
        "fuzzy_labels": list(DEFAULT_FUZZY_LABELS),
        "placeholder_generics": list(DEFAULT_PLACEHOLDER_GENERICS),
        "emptystate_generics": list(DEFAULT_EMPTYSTATE_GENERICS),
        "claim_patterns": list(DEFAULT_CLAIM_PATTERNS),
        "i18n_ph_example_prefix": DEFAULT_I18N_PH_EXAMPLE_PREFIX,
        "i18n_ph_whitelist": list(DEFAULT_I18N_PH_WHITELIST),
        "scope": None,          # {"selectors": [...], "values": [...]}
        "dupctl": None,         # {"pairs": [[a,b],...], "concepts":[{names,kws,owner}], "generic_similarity": bool}
        "escape_funcs": list(DEFAULT_ESCAPE_FUNCS),
        "escape_allow": [],     # 逐条豁免的字符串字面量
        "escape_tag_allow": [],  # 追加「非 HTML 但合法的标签名」（如 Define-XML 的 ItemDef）
        "enable_scope": False,
        "enable_dupctl": False,
        "enable_dupdst": False,
    }
    if not rules_path or not rules_path.exists():
        return cfg
    try:
        raw = json.loads(rules_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("⚠ rules.json 解析失败，回退家族默认: %s" % e, file=sys.stderr)
        return cfg

    if isinstance(raw.get("fuzzy_labels_add"), list):
        cfg["fuzzy_labels"] += raw["fuzzy_labels_add"]
    if isinstance(raw.get("placeholder_generics_add"), list):
        cfg["placeholder_generics"] += raw["placeholder_generics_add"]
    if isinstance(raw.get("emptystate_generics_add"), list):
        cfg["emptystate_generics"] += raw["emptystate_generics_add"]
    if isinstance(raw.get("claim_patterns_add"), list):
        cfg["claim_patterns"] += [p for p in raw["claim_patterns_add"] if isinstance(p, str)]
    if isinstance(raw.get("i18n_whitelist_add"), list):
        cfg["i18n_ph_whitelist"] += raw["i18n_whitelist_add"]
    if isinstance(raw.get("i18n_whitelist_force"), list):
        cfg["i18n_ph_whitelist"] = list(raw["i18n_whitelist_force"])
    if isinstance(raw.get("escape_allow_add"), list):
        cfg["escape_allow"] += [s for s in raw["escape_allow_add"] if isinstance(s, str)]
    if isinstance(raw.get("escape_tag_allow_add"), list):
        cfg["escape_tag_allow"] += [s.lower() for s in raw["escape_tag_allow_add"] if isinstance(s, str)]

    scope = raw.get("scope")
    if isinstance(scope, dict) and isinstance(scope.get("selectors"), list) \
            and isinstance(scope.get("values"), list):
        cfg["scope"] = scope
        cfg["enable_scope"] = bool(raw.get("enable", {}).get("scope", True))
    dupctl = raw.get("dupctl")
    if isinstance(dupctl, dict) and (isinstance(dupctl.get("pairs"), list)
                                     or isinstance(dupctl.get("concepts"), list)):
        cfg["dupctl"] = dupctl
        cfg["enable_dupctl"] = bool(raw.get("enable", {}).get("dupctl", True))
    cfg["enable_dupdst"] = bool(raw.get("enable", {}).get("dupdst", False))
    return cfg


# ———————————————————————————————————————————————————————
# 通用 HTML 抽取
# ———————————————————————————————————————————————————————
def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _tag_text(html: str, tag: str):
    out = []
    for m in re.finditer(r"<%s\b[^>]*>(.*?)</%s>" % (tag, tag), html, re.S | re.I):
        txt = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if txt:
            out.append(txt)
    return out


def _attr_values(html: str, attr: str):
    return [m.group(2) for m in re.finditer(r"%s\s*=\s*([\"'])(.*?)\1" % attr, html, re.S)]


def _tag_openings(html: str):
    """yield 每个标签开标签的完整字符串（含属性）。"""
    for m in re.finditer(r"<[a-zA-Z][^>]*>", html):
        yield m.group(0)


# ———————————————————————————————————————————————————————
# 入口资源解析（HTML + 外链 JS/CSS 合并，兼容拆分形态）
# ———————————————————————————————————————————————————————
_LINK_RE = re.compile(r'<link\b[^>]*\bhref\s*=\s*["\']([^"\']+)["\']', re.I)
_SCRIPT_SRC_RE = re.compile(r'<script\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']', re.I)
_INLINE_SCRIPT_RE = re.compile(r"<script\b(?![^>]*\bsrc\s*=)[^>]*>(.*?)</script>", re.S | re.I)


def _is_local_ref(ref: str) -> bool:
    """本地相对引用才纳入扫描（跳过 http(s)://、//cdn、data:、blob:、#锚点）。"""
    r = ref.strip()
    if not r or r.startswith(("#", "data:", "blob:", "mailto:", "javascript:")):
        return False
    if re.match(r"^(?:https?:)?//", r, re.I):
        return False
    return True


def _resolve_asset(entry: Path, ref: str):
    """把入口里的相对引用解析成本地文件；越出入口目录或不存在则返回 None。"""
    ref = ref.split("?", 1)[0].split("#", 1)[0].strip()
    if not ref:
        return None
    base = entry.parent.resolve()
    try:
        p = (base / ref.lstrip("/")).resolve()
    except Exception:  # noqa: BLE001
        return None
    # 防目录穿越：只认入口同目录及其子目录
    try:
        p.relative_to(base)
    except ValueError:
        return None
    return p if p.is_file() else None


def _collect_assets(entry: Path, html: str):
    """返回 (js_paths, css_paths)。只收本地、存在、且未重复的资源。"""
    js, css = [], []
    seen = set()
    for ref in _SCRIPT_SRC_RE.findall(html):
        if not _is_local_ref(ref):
            continue
        p = _resolve_asset(entry, ref)
        if p and p not in seen:
            seen.add(p)
            js.append(p)
    for ref in _LINK_RE.findall(html):
        if not _is_local_ref(ref):
            continue
        p = _resolve_asset(entry, ref)
        if p and p not in seen and p.suffix.lower() == ".css":
            seen.add(p)
            css.append(p)
    return js, css


def _js_bodies(entry: Path, html: str, js_paths):
    """返回 [(显示名, JS 源码)]：内联 <script> 体 + 外链 js 文件。供 C-detail-escape 使用。"""
    out = []
    for i, m in enumerate(_INLINE_SCRIPT_RE.finditer(html)):
        body = m.group(1)
        if body.strip():
            out.append(("inline#%d" % (i + 1), body))
    for p in js_paths:
        try:
            out.append((p.name, _read(p)))
        except Exception:  # noqa: BLE001
            continue
    return out


_CJK_RE = re.compile(r"[一-鿿]")


def _fuzzy_hit(text: str, word: str) -> bool:
    """模糊名命中判定（2026-10-30 修子串误报）。

    - 归一化（去空白）后**整串等于**模糊名 → 命中（最典型的"按钮只写『高级』"）；
    - 子串命中但模糊名**前后紧邻中文** → 说明它只是更长词组的一部分（"不设置"里的
      "设置"、"高级路径"里的"高级"），语义已自解释，豁免；
    - 其余子串命中（如 "设置 面板"、单独的 "设置"）→ 命中。
    中文无词边界，故用"紧邻中文"作为词组内判定，避免把否定式与复合名误判为模糊。
    """
    t = re.sub(r"\s+", "", text)
    if t == word:
        return True
    start = 0
    while True:
        i = t.find(word, start)
        if i < 0:
            return False
        before = t[i - 1] if i > 0 else ""
        after = t[i + len(word)] if i + len(word) < len(t) else ""
        if not (_CJK_RE.match(before) or _CJK_RE.match(after)):
            return True
        start = i + 1


# ———————————————————————————————————————————————————————
# 检查项
# ———————————————————————————————————————————————————————
def _check_label(html: str, cfg):
    """C-detail-label：模糊名扫描（FAIL）。"""
    hits = []
    for tag in LABEL_TAGS:
        for txt in _tag_text(html, tag):
            for w in cfg["fuzzy_labels"]:
                if _fuzzy_hit(txt, w):
                    hits.append("%s 文案命中模糊名「%s」: %r" % (tag, w, txt[:40]))
    for v in _attr_values(html, "title"):
        for w in cfg["fuzzy_labels"]:
            if _fuzzy_hit(v, w):
                hits.append("title 命中模糊名「%s」: %r" % (w, v[:40]))
    return "C-detail-label", hits


def _check_placeholder_attr(html: str, cfg):
    """C-detail-placeholder（属性，FAIL）：placeholder="..." 命中泛词。"""
    hits = []
    for v in _attr_values(html, "placeholder"):
        for w in cfg["placeholder_generics"]:
            if w in v:
                hits.append("placeholder 命中泛词「%s」: %r" % (w, v[:40]))
    return "C-detail-placeholder", hits


def _check_placeholder_emptystate(html: str, cfg):
    """C-detail-placeholder（空态容器，WARN）：归一化后精确等于泛词。"""
    hits = []
    for m in re.finditer(
        r'class\s*=\s*([\"\'])([^\"\']*\b(empty|null|no-data|nodata)\b[^\"\']*)\1',
        html, re.I,
    ):
        seg = html[m.start(): m.start() + 400]
        inner = re.search(r">([^<]{0,40})<", seg)
        if not inner:
            continue
        norm = re.sub(r"[（）()\s]", "", inner.group(1))
        for w in cfg["emptystate_generics"]:
            if norm == w:
                hits.append("空态文案等于泛词「%s」: %r" % (w, inner.group(1)))
                break
    return "C-detail-placeholder(empty)", hits


def _check_claim(html: str, cfg):
    """C-detail-claim：输入语法类承诺扫描（WARN；无 claim-verified 闭环则 FAIL）。"""
    sources = []
    sources += _attr_values(html, "placeholder")
    sources += _attr_values(html, "title")
    sources += _tag_text(html, "p")
    sources += _tag_text(html, "span")
    sources += _tag_text(html, "div")
    warn_hits = []
    for s in sources:
        for pat in cfg["claim_patterns"]:
            if re.search(pat, s):
                warn_hits.append("承诺式表述 %r 命中模式 %s" % (s[:40], pat))
                break
    has_verified = "claim-verified:" in html
    return "C-detail-claim", warn_hits, (not has_verified)


def _check_i18n_placeholder(html: str, cfg):
    """C-detail-i18n-ph：单语静态占位扫描（WARN，已排除示例与常见单语字段）。

    三元绑定豁免：若含 placeholder 的同一标签内同时出现 data-i18n-ph="key",
    说明该占位文案由词典 JS 动态填充,属标准 i18n-ph 模式,不再报警。
    """
    warns = []
    for m in re.finditer(r"<[^>]*placeholder\s*=\s*\"([^\"]*)\"[^>]*>", html):
        tag = m.group(0)
        v = m.group(1)
        # 同一标签内若有 data-i18n-ph → 词典绑定,豁免
        if re.search(r'data-i18n-ph\s*=', tag):
            continue
        if not re.search(r"[一-鿿]", v):
            continue
        if v.startswith(cfg["i18n_ph_example_prefix"]) or v[:2] in cfg["i18n_ph_example_prefix"]:
            continue
        if any(w in v for w in cfg["i18n_ph_whitelist"]):
            continue
        if "zh ?" in v or v.startswith("T."):
            continue
        warns.append("静态占位含中文但未走 i18n 三元/T 键: %r" % v[:40])
    return "C-detail-i18n-ph", warns


_ENTITY_RE = re.compile(r"&(?:[A-Za-z][A-Za-z0-9]{1,10}|#\d{1,6}|#x[0-9A-Fa-f]{1,6});")
# C-detail-escape：已知 HTML 标签名集合。< 后标签名在集合内且名后是属性/闭合形态
# （空白 / > / / / = 或串尾）→ 合法拼接（含文案中嵌 <b>/<span> 强调与 "<button class="
# 这类无闭合拼接片段）；未知标签名（<Y) 的 Y、<5 已由数字规则覆盖）→ 吞字符，FAIL。
ESCAPE_KNOWN_TAGS = frozenset((
    "a abbr acronym address area article aside audio b base bdi bdo big blockquote body br "
    "button canvas caption center cite code col colgroup data datalist dd del details dfn "
    "dialog dir div dl dt em fieldset figcaption figure font footer form h1 h2 h3 h4 h5 h6 "
    "head header hgroup hr html i iframe img input ins kbd label legend li link main map mark "
    "menu meta meter nav ol optgroup option output p param picture pre progress q rp rt ruby "
    "s samp script section select small source span strike strong style sub summary sup table "
    "tbody td template textarea tfoot th thead time title tr track u ul var video wbr "
    # 内联 SVG 图标与滤镜（ct- 工作台常用）。注意：比较时用 .lower()，
    # 故此表必须全小写——原表里的 feGaussianBlur / animateTransform 因大小写
    # 永远匹配不上，2026-10-30 一并改正。
    "svg path circle rect g line polyline polygon ellipse text tspan defs use symbol "
    "clippath lineargradient radialgradient stop filter mask pattern marker "
    "fegaussianblur fedropshadow feblend fecolormatrix fecomponenttransfer fecomposite "
    "feconvolvematrix fediffuselighting fedisplacementmap feflood feimage femerge "
    "femergeNode femorphology feoffset fespecularlighting fetile feturbulence "
    "fedistantlight fepointlight fespotlight fefunca fefuncb fefuncg fefuncr "
    "animate animatetransform animatemotion animatecolor set mpath textpath transform "
    "foreignobject desc metadata view switch glyph "
    # Define-XML / ODM 标准标签（CDISC 领域通用，与 SVG 同理）：
    # ct-adam 等技能会拼接 Define-XML 文档（变量 ig/itemdefs 最终写成 .xml 文件，
    # 非 innerHTML），这些标签名合法，不应判为「吞字符」。2026-10-30 补。
    "odm study globalvariables studyname studydescription protocolname metadataversion "
    "defineversion standardname standardversion itemgroupdefs itemgroupdef itemdefs "
    "itemdef itemref alias description translatedtext methoddef codelist codelistitem "
    "enumerateditem externalcodelist def:leaf def:commentdef def:commentdefs def:commentoid "
    "def:archivelocationid def:pdfpageref"
).split())
# 统一小写规范化：匹配侧用 tm.group(1).lower()，集合侧必须同样小写，
# 否则 feGaussianBlur / animateTransform / feMergeNode 这类驼峰名永远匹配不上。
ESCAPE_KNOWN_TAGS = frozenset(x.lower() for x in ESCAPE_KNOWN_TAGS)
_ESCAPE_TAGNAME_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9._-]*(?::[A-Za-z][A-Za-z0-9._-]*)?)")
_ENTITY_RE = re.compile(r"&(?:[A-Za-z][A-Za-z0-9]{1,10}|#\d{1,6}|#x[0-9A-Fa-f]{1,6});")
_JS_STR_RE = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'')
_JS_TPL_RE = re.compile(r"`((?:[^`\\]|\\.)*)`", re.S)
# URL query 参数（&lang= / &ver= / &doc_index=）——fetch/拼接 URL 用，不进入 innerHTML，
# 与号原样保留是正确行为，不属「渲染层未转义」。2026-10-30 外链 js 合并扫描后补此豁免。
_QUERY_PARAM_RE = re.compile(r"&[A-Za-z_][A-Za-z0-9_]*=")
# JSON 数据值前缀：`"key":` / `'key':` —— 用于把内嵌配置/词典的文案排除在渲染层检查外
_JSON_VALUE_PREFIX_RE = re.compile(r"""["']\s*:\s*$""")


def _strip_js_comments(src: str) -> str:
    """把 JS 注释替换为等长空白（保留换行），使行号与原文一致。

    目的：注释里的引号会被 `_JS_STR_RE` 误当成字符串字面量（实证 ct-adam
    `/* 评级阈值：">=90"→90，"<50"→0 */` 被报成「裸 < 后跟数字」FAIL）。

    实现说明（2026-10-30）：初版用逐字符状态机跟踪 ' " ` 三种字符串，但遇到
    正则字面量（如 `replace(/['"]/g,'')`）会误入字符串态、导致后续注释识别失效
    （实测 ct-adam 行 259 未被剥离）。改为正则剥离，宁可宽松：
      - 块注释 `/* ... */`（非贪婪、可跨行）全部抹平；
      - 行注释只抹「整行以 // 开头」的，避免误伤 `https://` 这类 URL。
    误剥只会让检查偏宽松（可能漏报），不会造成误报。
    """
    def _blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))

    src = re.sub(r"/\*.*?\*/", _blank, src, flags=re.S)
    src = re.sub(r"(?m)^[ \t]*//[^\n]*", _blank, src)
    return src


def _iter_js_strings(body: str):
    """产出 (行号, 字符串字面量内容, 是否纯数据值)。单/双引号不跨行；模板串可跨行。

    第三个返回值标识「该字符串是 JSON 数据值」——即前文形如 `"key":` 的形式。
    典型来源：内嵌配置 `const WB_CONFIG_EMBED = {"desc":{"zh":"A(≥90)→D(<50)"}}`。
    这类字符串是**数据**（渲染时必然经文本节点或 esc()），不是拼 innerHTML 的代码，
    C-detail-escape 应跳过，否则每个含数学符号的配置文案都会误报 FAIL。
    JS 对象字面量（key 不带引号，如 `{html: "..."}`）不豁免，仍按代码检查。
    """
    for m in _JS_STR_RE.finditer(body):
        s = m.group(1) if m.group(1) is not None else m.group(2)
        lineno = body.count("\n", 0, m.start()) + 1
        is_data = bool(_JSON_VALUE_PREFIX_RE.search(body, max(0, m.start() - 200), m.start()))
        yield lineno, s, is_data
    for m in _JS_TPL_RE.finditer(body):
        yield body.count("\n", 0, m.start()) + 1, m.group(1), False


def _check_escape(sources, cfg):
    """C-detail-escape（红线 8，FAIL/WARN）：拼 innerHTML 的 JS 字符串裸 < / 裸 & 扫描。

    `sources` = [(显示名, JS 源码)]，由 `_js_bodies()` 提供（内联 script 体 + 外链 js），
    因此 HTML/JS 拆分后仍能扫到真实渲染代码。

    缺陷家族 F「渲染层未转义」——浏览器把文本中部的 "<Y)" 当标签吞掉，用户看到断裂
    文案（实证：ct-samplesize「随机优势 φ = P(X<Y)」显示成「φ = P(X」）。页面照常
    渲染、控制台零 error、静态 grep 与截图都难发现。
    判据：
      - 裸 < 后跟数字 → 任何位置 FAIL（合法 HTML 标签名不可能数字开头）；
      - 裸 < 后跟字母且 < 前有非空白字符 → FAIL（合法标签拼接通常以 < 开头或空白分隔，
        "P(X<Y)" 这类数学/逻辑文案的 < 必然夹在文本中部）。< 前邻若是标签边界符
        （> / " / ' / =，即"前一个标签刚结束"的签名）→ 合法拼接，豁免；
      - "</" / "<!--" / "<=" 等不命中；
      - 串内出现转义函数调用（esc( / escapeHtml( 等）→ 视为已走转义，整串豁免；
        esc("<Y)") 的函数名在串外，故按「该行出现转义函数调用」行级豁免（宁宽勿窄）；
      - rules.json escape_allow_add 逐条豁免；
      - 裸 & 后紧跟字母且非 &entity; → WARN（浏览器多数场景原样显示，风险低于 <）；
        URL query 形态（&name=）豁免——那是拼 URL，不进 innerHTML。
    """
    fails, warns = [], []
    for label, body in sources:
        body = _strip_js_comments(body)
        lines = body.split("\n")
        for lineno, s, is_data in _iter_js_strings(body):
            if is_data:
                continue  # 内嵌配置/词典的纯数据值，不参与渲染层判定
            if any(a in s for a in cfg["escape_allow"]):
                continue
            # 转义豁免：esc("<Y)") 的函数名在串外，故按「该行出现转义函数调用」行级豁免
            # （转义函数出现在该行 = 作者对该行字符串有转义意识，宁宽勿窄）
            line_txt = lines[lineno - 1] if lineno - 1 < len(lines) else ""
            if any(f in line_txt for f in cfg["escape_funcs"]):
                continue
            if any(f in s for f in cfg["escape_funcs"]):
                continue
            for m in re.finditer(r"<", s):
                i = m.start()
                nxt = s[i + 1:i + 2]
                if nxt.isdigit():
                    fails.append("%s 行%d: 裸 < 后跟数字 %r（合法标签名不可能数字开头，必被吞）"
                                 % (label, lineno, s[max(0, i - 14):i + 14]))
                    break
                if not nxt.isalpha():
                    continue  # "</" / "<!--" / "<=" / "< " 等
                tm = _ESCAPE_TAGNAME_RE.match(s, i)
                rest = s[tm.end():] if tm else "x"
                tagname = tm.group(1).lower() if tm else ""
                if tm and (tagname in ESCAPE_KNOWN_TAGS or tagname in cfg["escape_tag_allow"]) \
                        and (rest == "" or rest[0] in " \t\n/>="):
                    continue  # 已知标签名（HTML/SVG 或叶子声明的 XML 标签）+ 属性/闭合形态
                fails.append("%s 行%d: 未知形态裸 < %r（拼 innerHTML 会被浏览器当标签吞掉）"
                             % (label, lineno, s[max(0, i - 14):i + 14]))
                break
            for m in re.finditer(r"&[A-Za-z]", s):
                if _ENTITY_RE.match(s, m.start()):
                    continue
                # JS 逻辑与 `&&`（如 `${(a&&b)?...}`）不是 HTML 与号，两侧任一为 & 即跳过
                if (m.start() > 0 and s[m.start() - 1] == "&") \
                        or s[m.start() + 1:m.start() + 2] == "&":
                    continue
                if _QUERY_PARAM_RE.match(s, m.start()):
                    continue  # URL query 参数，不渲染 HTML
                warns.append("%s 行%d: 裸 & 未转实体 %r"
                             % (label, lineno, s[max(0, m.start() - 14):m.start() + 14]))
                break
    return "C-detail-escape", fails, warns


def _check_scope(html: str, cfg):
    """C-detail-scope（rules 驱动，FAIL）：收集函数覆盖的 data-scope 须含全部期望值。

    引擎不认识任何叶子 class——selectors/values 全部从 rules.json 的 scope 读。
    selectors 支持 ".class" 或 "#id" 形式（按属性子串匹配）。
    """
    scope = cfg.get("scope")
    if not scope:
        return "C-detail-scope", []
    selectors = scope.get("selectors", [])
    expected = set(scope.get("values", []))
    present = set()
    for opening in _tag_openings(html):
        cls = ""
        cm = re.search(r'class\s*=\s*[\"\']([^\"\']*)[\"\']', opening, re.I)
        if cm:
            cls = cm.group(1)
        idm = re.search(r'id\s*=\s*[\"\']([^\"\']*)[\"\']', opening, re.I)
        idv = idm.group(1) if idm else ""
        for sel in selectors:
            # 子串匹配：workbench.html 大量使用 JS 模板字面量（class="picos-in${...}"），
            # 单词切分会把 "picos-in" 拆成 "picos-in${miss" 而漏匹配；子串对模板字面量稳健。
            # 选择器由叶子在 rules.json 提供，是否过度匹配由叶子自负。
            if sel.startswith("."):
                if sel[1:] in cls:
                    break
            elif sel.startswith("#"):
                if sel[1:] in idv:
                    break
            else:
                if sel in cls:
                    break
        else:
            continue
        dsm = re.search(r'data-scope\s*=\s*[\"\']([^\"\']*)[\"\']', opening, re.I)
        if dsm:
            present.add(dsm.group(1))
    missing = expected - present
    if missing:
        return "C-detail-scope", [
            "selectors=%s 覆盖到的 data-scope=%s，缺期望值 %s"
            % (selectors, sorted(present), sorted(missing))
        ]
    return "C-detail-scope", []


def _check_dupdst(html: str, cfg):
    """C-detail-dupdst（结构冲突，FAIL）：写入目标（data-dst / name）被 ≥2 个控件占用。

    控件身份 = 其写入的「数据目标」。`<input data-dst="X">` 与 `<select name="X">` 把值
    交给同一个 X，浏览器/取值逻辑只认最后一个 → 互相覆盖，是确定性缺陷。

    实现要点（与 C-detail-* 家族口径一致，零浏览器、纯静态）：
      - 只扫 <input>/<select>/<textarea> 开标签里的 data-dst / name；
        `document.querySelector("[data-dst='x']")` 之类 JS 选择器不是控件，跳过；
      - 排除 `${...}` 模板表达式（schema 渲染写成 data-dst="${p.name}"，静态多次出现但
        运行时只展开一次，不算重复）；
      - **排除 radio / checkbox**：同名 radio 是单选组（同 name 仅一个可选）、同名 checkbox
        是多选组，同 name 是设计语义，不算冲突；
      - 同一控件同时带 data-dst 与 name 且值相同 → 只算一个目标，不误报。
    """
    counts = {}   # value -> [控件开标签片段, ...]
    for m in re.finditer(r"<(input|select|textarea)\b[^>]*>", html, re.I):
        tag = m.group(0)
        low = tag.lower()
        # radio/checkbox 同名是分组语义（单选/多选），不视为写入冲突
        if re.search(r'type\s*=\s*["\'](radio|checkbox)["\']', low):
            continue
        vals = []
        for attr in ("data-dst", "name"):
            am = re.search(r'%s\s*=\s*["\']([^"\']*)["\']' % attr, tag, re.I)
            if am:
                v = am.group(1)
                if re.match(r"^\$\{.+\}$", v):   # 模板表达式，跳过
                    continue
                if v:
                    vals.append(v)
        for v in vals:
            counts.setdefault(v, []).append(tag[:70])
    fails = []
    for v, tags in counts.items():
        if len(tags) >= 2:
            fails.append("写入目标 data-dst/name=%r 被 %d 个控件同时占用（取值互相覆盖）: %s"
                         % (v, len(tags), " | ".join(tags[:3])))
    return "C-detail-dupdst", fails


def _check_dupctl(html: str, cfg):
    """C-detail-dupctl（rules 驱动，WARN）：相似/冗余控件检测，两路：

    (1) pairs：明示的相似控件对（两个短语）均出现在 LABEL_TAGS 文案中、且无 `dup-verified:`
        闭环 → WARN（原有能力，向后兼容）。
    (2) concepts：概念重叠——某概念（如「蒙特卡洛 MC」）既由 schema 字段 <names> 提供，
        又被一个**硬编码控件**（label/button/summary/option/title 文本命中 keywords）驱动
        → 疑似冗余/冲突（两个控件管同一件事，但写法/标签不同、data-dst 也不同），
        须合并为单一控件，或确认非冗余后加 `dup-verified:` 闭环。

    引擎不预设任何控件名/概念——pairs 与 concepts 全部从 rules.json 的 dupctl 读。
    典型误报防线：schema 渲染字段（data-dst="${p.name}"）在静态文本里没有字面量标签，
    故硬编码控件的命中不会误伤 schema 字段自身；仅当确实存在「独立硬编码控件 + schema
    字段同概念」并存时才报警。
    """
    dupctl = cfg.get("dupctl")
    if not dupctl:
        return "C-detail-dupctl", []
    warns = []
    verified = "dup-verified:" in html

    # (1) pairs
    all_text = []
    for tag in LABEL_TAGS:
        all_text += _tag_text(html, tag)
    corpus = " \n ".join(all_text)
    for pair in dupctl.get("pairs", []):
        if not (isinstance(pair, list) and len(pair) == 2):
            continue
        a, b = pair
        if a in corpus and b in corpus and not verified:
            warns.append("相似控件对 %r / %r 均存在但未标 dup-verified:（疑似冗余/行为差异未证伪）"
                         % (a, b))

    # (2) concepts
    # 控件关联文本：LABEL_TAGS 文案 + title 属性（不含 div/p 等容器，避免结果区等误伤）。
    # 说明：schema 渲染字段（data-dst="${p.name}"）在静态文本里没有字面量标签，故本检查
    # 看到的「硬编码控件」天然就是独立于 schema 的实体；owner=schema 时叶子已断言该概念由
    # schema 字段提供，任何硬编码控件再碰同一关键词即冗余 —— 不需要（也无法）静态证明 schema 字段存在。
    ctrl_texts = []
    for tag in LABEL_TAGS:
        ctrl_texts += _tag_text(html, tag)
    ctrl_texts += _attr_values(html, "title")
    for c in dupctl.get("concepts", []):
        if not isinstance(c, dict):
            continue
        names = c.get("names") or []
        kws = c.get("keywords") or []
        owner = (c.get("owner") or "both").lower()
        if not kws:
            continue
        hits = []   # [(kw, text)]
        for t in ctrl_texts:
            for kw in kws:
                if kw in t:
                    hits.append((kw, t[:50]))
                    break
        if not hits:
            continue
        if owner == "schema":
            # 叶子断言：概念由 schema 字段 names 提供；硬编码控件再碰关键词 → 冗余/冲突
            if not verified:
                for kw, t in hits:
                    warns.append("概念「%s」已被硬编码控件 %r 驱动，但本工作台该概念由 schema "
                                 "字段 %s 提供（疑似冗余/冲突；合并为单一控件或确认后加 dup-verified:）"
                                 % (kw, t, names))
        else:
            # owner=both / 未指定：≥2 个硬编码控件都命中 → 冗余对
            uniq = {t for _, t in hits}
            if len(uniq) >= 2 and not verified:
                warns.append("概念 keywords=%s 被 ≥2 个硬编码控件同时引用（疑似冗余）: %s"
                             % (kws, " | ".join(sorted(uniq))[:120]))
    return "C-detail-dupctl", warns


# ———————————————————————————————————————————————————————
# 主流程
# ———————————————————————————————————————————————————————
def _find_entry(root: Path):
    """在技能根下定位工作台入口：workbench.html 优先，其次 index.html。

    跳过 publish / publish-dist / _archive / node_modules 等产物目录，
    避免扫到发布载荷里的副本（会导致同一问题重复报、且掩盖源码问题）。
    """
    skip = ("publish", "publish-dist", "_archive", "node_modules", ".git", "__pycache__")
    for name in ("workbench.html", "index.html"):
        cands = [p for p in root.rglob(name)
                 if not any(s in p.parts for s in skip)]
        if cands:
            # 取层级最浅的（入口通常在 workbench/ 或根）
            cands.sort(key=lambda p: (len(p.parts), str(p)))
            return cands[0]
    return None


def main():
    ap = argparse.ArgumentParser(description="ct-base 通用工作台 UI 细节机检 (C-detail-*)")
    ap.add_argument("--html", help="入口 HTML 路径（也接受目录：自动找 workbench.html/index.html）")
    ap.add_argument("--root", help="技能根目录（自动定位入口与 scripts/rules.json）")
    ap.add_argument("--rules", help="显式指定 wb_detail_check.rules.json 路径")
    args = ap.parse_args()

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[1]

    html_path = None
    if args.html:
        cand = Path(args.html)
        if cand.is_dir():
            html_path = _find_entry(cand)
            if not html_path:
                print("✕ 目录下未找到 workbench.html / index.html: %s" % cand, file=sys.stderr)
                return 2
        else:
            html_path = cand
    else:
        html_path = _find_entry(root)
        if not html_path:
            print("✕ 未找到 workbench.html / index.html（--html 指定 或 --root 指向技能根）",
                  file=sys.stderr)
            return 2

    if not html_path.exists():
        print("✕ 文件不存在: %s" % html_path, file=sys.stderr)
        return 2

    # rules.json：显式 > 技能根 scripts/ > 无（家族默认）
    rules_path = None
    if args.rules:
        rules_path = Path(args.rules)
    else:
        cand = root / "scripts" / RULES_FILENAME
        if cand.exists():
            rules_path = cand
    cfg = load_rules(rules_path)

    html = _read(html_path)
    js_paths, css_paths = _collect_assets(html_path, html)
    js_srcs = _js_bodies(html_path, html, js_paths)
    # 合并源：入口 HTML + 外链 JS 源码。JS 模板里的 class/placeholder/文案由此可见，
    # 从而兼容「HTML + app.js 外链」拆分形态（全内联单文件时 merged 等价于 html）。
    merged = html + "\n" + "\n".join(body for _, body in js_srcs)

    print("目标: %s  (%d 字符)" % (html_path, len(html)))
    if js_paths:
        print("外链 JS: %s  → 合并后 %d 字符"
              % (", ".join(p.name for p in js_paths), len(merged)))
    if css_paths:
        print("外链 CSS: %s" % ", ".join(p.name for p in css_paths))
    if not js_paths and not css_paths:
        print("外链资源: 无（全内联单文件形态）")
    if rules_path:
        print("规则: %s" % rules_path)
    else:
        print("规则: 家族默认（未找到 %s）" % RULES_FILENAME)

    fails = []   # (name, hits)
    warns = []   # (name, hits)

    name, hits = _check_label(merged, cfg)
    if hits:
        fails.append((name, hits))

    name, hits = _check_placeholder_attr(merged, cfg)
    if hits:
        fails.append((name, hits))

    name, hits = _check_placeholder_emptystate(merged, cfg)
    if hits:
        warns.append((name, hits))

    name, hits, escalate = _check_claim(merged, cfg)
    if hits:
        if escalate:
            fails.append((name, hits + ["  ↳ 无 claim-verified: 闭环，升级 FAIL"]))
        else:
            warns.append((name, hits))

    name, hits = _check_i18n_placeholder(merged, cfg)
    if hits:
        warns.append((name, hits))

    if cfg["enable_scope"]:
        name, hits = _check_scope(merged, cfg)
        if hits:
            fails.append((name, hits))

    if cfg["enable_dupctl"]:
        name, hits = _check_dupctl(merged, cfg)
        if hits:
            warns.append((name, hits))

    if cfg["enable_dupdst"]:
        name, hits = _check_dupdst(merged, cfg)
        if hits:
            fails.append((name, hits))

    name, hits, esc_warns = _check_escape(js_srcs, cfg)
    if hits:
        fails.append((name, hits))
    if esc_warns:
        warns.append((name + "(&)", esc_warns))

    print("\n--- C-detail-* 结果 ---")
    for name, hits in fails:
        print("[FAIL] %s (%d)" % (name, len(hits)))
        for h in hits:
            print("   - " + h)
    for name, hits in warns:
        print("[WARN] %s (%d)" % (name, len(hits)))
        for h in hits:
            print("   - " + h)

    if not fails and not warns:
        print("✓ C-detail-* 全绿（label / placeholder / claim / i18n-ph / escape"
              + (" / scope" if cfg["enable_scope"] else "")
              + (" / dupctl" if cfg["enable_dupctl"] else "")
              + (" / dupdst" if cfg["enable_dupdst"] else "") + "）")

    print("\n判据：任一 FAIL = 禁止交付。本次 FAIL=%d, WARN=%d" % (len(fails), len(warns)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
