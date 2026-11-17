#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""内容发布套件 - 各渠道输出格式合约校验器。

依据 references/channel-contracts.md 逐渠道检查生成的发布物料。
P0 阻断发布；P1 提示人工决定。
--enforce 时若存在 P0，进程退出码为 2。
"""
import argparse
import json
import os
import re
import subprocess
import sys

CONVO_TRACE = ["好的，", "我来", "，以下是", "本文档旨在", "下文将"]
CRED_PREFIX = ["ntn_", "sk-", "ghp_", "gho_", "ghu_", "ghs_", "ghr_"]

# 内部标记（发布物中不应出现）。作者内部笔名/代号不硬编码在通用引擎里，
# 由私有配置通过环境变量 PUBLISH_PEN_NAMES（逗号分隔）传入，默认为空。
INTERNAL_MARKERS = ["【内部】", "内部备注", "待定", "Gate", "审核过程"]
PEN_NAMES = [n.strip() for n in os.environ.get("PUBLISH_PEN_NAMES", "").split(",") if n.strip()]


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check_wechat(text, issues):
    if "<section" not in text:
        issues.append(("P0", "wechat", "缺少 <section> 包裹块"))
    if "<v2></v2>" not in text:
        issues.append(("P0", "wechat", "文末缺少 <v2></v2> 版本标记"))
    if re.search(r"<script|<style", text):
        issues.append(("P0", "wechat", "含 <script> 或 <style>"))
    if "position:fixed" in text or "position:absolute" in text:
        issues.append(("P0", "wechat", "含 position:fixed/absolute"))
    for m in re.finditer(r'class="([^"]*)"', text):
        if m.group(1) != "_135editor":
            issues.append(("P0", "wechat", "含外联 class=%r（可粘贴模式应无 class）" % m.group(1)))
            break
    if "font-size:16px" not in text and "line-height:1.8" not in text:
        issues.append(("P1", "wechat", "正文疑似未应用 16px/1.8 样式"))


def check_linkedin(text, issues):
    if re.search(r"^\s*#\s", text, re.M):
        issues.append(("P0", "linkedin", "含 Markdown 标题 #"))
    if "**" in text or "```" in text:
        issues.append(("P0", "linkedin", "含 Markdown 加粗 ** 或代码块 ```"))
    if re.search(r"^\s*-\s", text, re.M):
        issues.append(("P0", "linkedin", "含 Markdown 列表 - "))
    for marker in INTERNAL_MARKERS + PEN_NAMES:
        if marker in text:
            issues.append(("P0", "linkedin", "含内部备注标记/笔名 %r" % marker))
            break
    if len(text) > 3000:
        issues.append(("P1", "linkedin", "字符数 %d > 3000" % len(text)))
    if not re.search(r"#\w|#[\u4e00-\u9fff]", text):
        issues.append(("P1", "linkedin", "末尾未出现 #话题 标签"))


def check_standalone(text, issues):
    if not (text.lstrip().lower().startswith("<!doctype html") or "<html" in text.lower()):
        issues.append(("P0", "standalone", "非 HTML 文档结构"))
        return
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    if not m or not m.group(1).strip():
        issues.append(("P0", "standalone", "缺少非空 <title>"))
    for kw in ["circuit", "grid-glow", "neon", "linear-gradient"]:
        if kw in text.lower():
            issues.append(("P0", "standalone", "疑似科技电路风关键词 %r" % kw))
            break
    if "<nav" not in text and 'id="toc"' not in text:
        issues.append(("P1", "standalone", "缺少目录（<nav> 或 id=toc）"))


def check_ledger(text, issues):
    try:
        data = json.loads(text)
    except Exception as e:
        issues.append(("P0", "archive", "JSON 解析失败: %s" % e))
        return
    entries = data if isinstance(data, list) else data.get("entries", [])
    if not entries:
        issues.append(("P0", "archive", "台账为空"))
        return
    last = entries[-1]
    for field in ["title", "channels", "generated_at", "status"]:
        if field not in last:
            issues.append(("P0", "archive", "最新记录缺字段 %r" % field))
    if last.get("status") not in ["draft", "published", "archived"]:
        issues.append(("P1", "archive", "status=%r 取值异常" % last.get("status")))


def check_general(text, name, issues):
    for t in CONVO_TRACE:
        if t in text:
            issues.append(("P0", name, "含对话痕迹 %r" % t))
            break
    for p in CRED_PREFIX:
        if p in text:
            issues.append(("P0", name, "含疑似凭据前缀 %r" % p))
            break


def read_image_size(path):
    """读取 PNG/JPEG 尺寸，不依赖第三方图像库。"""
    with open(path, "rb") as f:
        head = f.read(32)
        if head.startswith(b"\x89PNG\r\n\x1a\n") and len(head) >= 24:
            w = int.from_bytes(head[16:20], "big")
            h = int.from_bytes(head[20:24], "big")
            return w, h
        if head[:2] == b"\xff\xd8":
            f.seek(2)
            sof_markers = set(range(0xC0, 0xC4)) | set(range(0xC5, 0xC8)) | set(range(0xC9, 0xCC)) | set(range(0xCD, 0xD0))
            while True:
                byte = f.read(1)
                if not byte:
                    break
                if byte != b"\xff":
                    continue
                while byte == b"\xff":
                    byte = f.read(1)
                if not byte:
                    break
                code = byte[0]
                if code in (0xD8, 0xD9) or 0xD0 <= code <= 0xD7:
                    continue
                length_bytes = f.read(2)
                if len(length_bytes) < 2:
                    break
                length = int.from_bytes(length_bytes, "big")
                data = f.read(length - 2)
                if code in sof_markers and len(data) >= 5:
                    return int.from_bytes(data[3:5], "big"), int.from_bytes(data[1:3], "big")
    raise ValueError("无法读取 PNG/JPEG 尺寸")


def check_wechat_layout_gate(args, pkg, issues):
    """任何微信片段默认执行唯一排版基线门禁。"""
    snippet = os.path.join(pkg, "wechat_snippet.html")
    if not os.path.isfile(snippet):
        return
    title = args.layout_title or ""
    manifest_path = os.path.join(pkg, "package-manifest.json")
    if not title and os.path.isfile(manifest_path):
        try:
            title = json.loads(read_text(manifest_path)).get("title", "")
        except Exception:
            title = ""
    command = [sys.executable, args.layout_checker, snippet, "--baseline", args.layout_baseline]
    if title:
        command.extend(["--title", title])
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        issues.append(("P0", "wechat", "未通过唯一排版基线：标题/小标题/正文字号、行高、颜色、间距或结构发生漂移"))


def check_root_layout(args, pkg, issues):
    """检查项目根目录排版别名存在且与发布包内容逐字一致。"""
    if not args.require_root_layout:
        return
    if not args.root_layout_dir or not args.root_layout_stem:
        issues.append(("P0", "root_layout", "启用根目录排版门禁时必须提供 --root-layout-dir 和 --root-layout-stem"))
        return
    root_dir = os.path.abspath(args.root_layout_dir)
    preview = os.path.join(root_dir, args.root_layout_stem + ".html")
    snippet = os.path.join(root_dir, args.root_layout_stem + "_snippet.html")
    package_preview = os.path.join(pkg, "wechat_preview.html")
    package_snippet = os.path.join(pkg, "wechat_snippet.html")
    for path in (preview, snippet):
        if not os.path.isfile(path):
            issues.append(("P0", "root_layout", "根目录排版文件不存在: %s" % path))
    if os.path.isfile(preview) and os.path.isfile(package_preview) and read_text(preview) != read_text(package_preview):
        issues.append(("P0", "root_layout", "根目录排版预览与发布包不一致"))
    if os.path.isfile(snippet) and os.path.isfile(package_snippet) and read_text(snippet) != read_text(package_snippet):
        issues.append(("P0", "root_layout", "根目录可粘贴排版与发布包不一致"))


def check_visual_chain(args, issues):
    """严格检查封面→摘要卡链路；未启用时保持旧版渠道校验兼容。"""
    required = {
        "cover_brief": args.cover_brief,
        "cover_prompt": args.cover_prompt,
        "cover_image": args.cover_image,
        "summary_card": args.summary_card,
        "summary_card_html": args.summary_card_html,
        "summary_contract": args.summary_contract,
        "summary_copy": args.summary_copy,
        "summary_baseline": args.summary_baseline,
        "summary_checker": args.summary_checker,
    }
    missing_args = [name for name, path in required.items() if not path]
    if missing_args:
        issues.append(("P0", "visual", "--require-visual-chain 缺少参数: %s" % ", ".join(missing_args)))
        return
    for name, path in required.items():
        if not os.path.isfile(path):
            issues.append(("P0", "visual", "%s 不存在: %s" % (name, path)))
    if any(not os.path.isfile(path) for path in required.values()):
        return

    try:
        w, h = read_image_size(args.cover_image)
        ratio = w / h
        if abs(ratio - 2.35) > 0.02:
            issues.append(("P0", "visual", "长文封面比例异常: %dx%d = %.3f，要求 2.35:1" % (w, h, ratio)))
    except Exception as e:
        issues.append(("P0", "visual", "长文封面尺寸读取失败: %s" % e))

    try:
        w, h = read_image_size(args.summary_card)
        if (w, h) != (810, 1080):
            issues.append(("P0", "visual", "摘要卡尺寸异常: %dx%d，要求 810x1080" % (w, h)))
    except Exception as e:
        issues.append(("P0", "visual", "摘要卡尺寸读取失败: %s" % e))

    result = subprocess.run(
        [sys.executable, args.summary_checker, args.summary_card_html, "--baseline", args.summary_baseline,
         "--contract", args.summary_contract, "--copy", args.summary_copy],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        issues.append(("P0", "visual", "摘要卡 6.1/baseline 校验失败；详见 checker 输出"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True, help="发布产物目录")
    ap.add_argument("--enforce", action="store_true", help="存在 P0 时退出码 2")
    ap.add_argument("--layout-baseline", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "references", "wechat_layout_baseline.json")), help="公众号排版唯一基线 JSON")
    ap.add_argument("--layout-checker", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "validate_wechat_layout.py")), help="公众号排版基线校验器")
    ap.add_argument("--layout-title", default="", help="定稿标题；缺省时从 package-manifest.json 读取")
    ap.add_argument("--require-root-layout", action="store_true", help="强制检查项目根目录排版别名")
    ap.add_argument("--root-layout-dir", default=None, help="项目根目录")
    ap.add_argument("--root-layout-stem", default=None, help="根目录排版文件 stem")
    ap.add_argument("--require-visual-chain", action="store_true", help="强制检查封面 brief/prompt→2.35:1 封面→摘要卡 6.1 baseline 链路")
    ap.add_argument("--cover-brief", help="封面 brief 路径")
    ap.add_argument("--cover-prompt", help="封面 prompt 路径")
    ap.add_argument("--cover-image", help="最终 2.35:1 长文封面路径")
    ap.add_argument("--summary-card", help="810x1080 摘要卡成品路径")
    ap.add_argument("--summary-card-html", help="摘要卡 HTML 源文件路径")
    ap.add_argument("--summary-contract", help="摘要卡文章级内容契约 JSON")
    ap.add_argument("--summary-copy", help="摘要卡配文路径")
    ap.add_argument("--summary-baseline", help="摘要卡 6.1 baseline HTML/JSON 路径")
    ap.add_argument("--summary-checker", help="check_summary_card_6_1.py 路径")
    args = ap.parse_args()

    pkg = args.package
    issues = []
    files = {
        "wechat": os.path.join(pkg, "wechat_snippet.html"),
        "linkedin": os.path.join(pkg, "linkedin-post.md"),
        "standalone": os.path.join(pkg, "standalone.html"),
        "archive": os.path.join(pkg, "archive-ledger.json"),
    }
    present = {k: v for k, v in files.items() if os.path.exists(v)}
    if not present:
        print("[FAIL] 目录 %s 无任何渠道产物" % pkg, file=sys.stderr)
        return 2

    for name, path in present.items():
        text = read_text(path)
        if name == "wechat":
            check_wechat(text, issues)
        elif name == "linkedin":
            check_linkedin(text, issues)
        elif name == "standalone":
            check_standalone(text, issues)
        elif name == "archive":
            check_ledger(text, issues)
        check_general(text, name, issues)

    if "wechat" in present:
        check_wechat_layout_gate(args, pkg, issues)
        check_root_layout(args, pkg, issues)

    if args.require_visual_chain:
        check_visual_chain(args, issues)

    result = {"package": pkg, "issues": [{"severity": s, "channel": c, "detail": d} for s, c, d in issues]}
    out_path = os.path.join(pkg, "publish-gate.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    p0 = [i for i in issues if i[0] == "P0"]
    p1 = [i for i in issues if i[0] == "P1"]
    print("== 发布物料门禁 ==")
    print("检查渠道: %s" % ", ".join(sorted(present)))
    if not issues:
        print("结果: 通过（P0=0, P1=0）")
    else:
        for s, c, d in issues:
            print("  [%s] %s: %s" % (s, c, d))
        print("汇总: P0=%d, P1=%d" % (len(p0), len(p1)))
    print("报告: %s" % out_path)

    if args.enforce and p0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
