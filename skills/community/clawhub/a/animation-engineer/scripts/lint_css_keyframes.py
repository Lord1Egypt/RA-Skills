#!/usr/bin/env python3
"""CSS 关键帧 lint —— 固化动效 CSS 纪律：查重名、查起止是否用 transform/opacity、
查是否动了 layout 属性、查 animation 引用是否未定义。

纯标准库（argparse / json / re），不联网、不修改被检文件，产出确定可复现。
配合 references/css-keyframes-playbook.md 使用。配置（assets/motion-rules.json）
含 _ 注释键，脚本自动跳过。

检测项：
  E1  @keyframes 同名重复定义（后者覆盖前者，行为诡异）
  E2  关键帧起止（from/0% 与 to/100%）未用 transform 或 opacity（易卡顿/无动画）
  W1  关键帧中使用了 layout 属性（top/left/width/height 等），触发重排
  W2  animation 引用了未定义的 @keyframes 名（断裂的动画）

用法:
  python3 scripts/lint_css_keyframes.py --css styles.css
  python3 scripts/lint_css_keyframes.py --css src/ --config assets/motion-rules.json
  python3 scripts/lint_css_keyframes.py --css a.css b.css --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# 默认规则（可被 config 覆盖/追加）
DEFAULT = {
    "start_end_props": ["transform", "opacity"],
    "layout_thrash_props": [
        "top", "left", "right", "bottom", "width", "height",
        "margin", "padding", "box-shadow", "font-size",
    ],
    "ignore_name_keywords": {
        "none", "normal", "ease", "ease-in", "ease-out", "ease-in-out",
        "linear", "step-start", "step-end", "infinite", "alternate",
        "alternate-reverse", "reverse", "forwards", "backwards", "both",
        "running", "paused", "initial", "inherit", "unset", "auto",
    },
}

KW_RE = re.compile(r"^[a-z-]+(?:-in|-out)?$")
DUR_RE = re.compile(r"^\d+(?:\.\d+)?(?:ms|s)$")


def load_config(path):
    if not path:
        return dict(DEFAULT)
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    cfg = dict(DEFAULT)
    for k in ("start_end_props", "layout_thrash_props", "ignore_name_keywords"):
        if k in data and not str(k).startswith("_"):
            cfg[k] = data[k]
    return cfg


def read_css(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def find_keyframes(css):
    """返回 [(name, body), ...]，用括号深度匹配，正确处理 @media 嵌套。"""
    out = []
    i = 0
    while True:
        m = re.search(r"@keyframes\s+([\w-]+)\s*\{", css[i:])
        if not m:
            break
        name = m.group(1)
        start = i + m.end() - 1  # '{' 位置
        depth = 1
        j = start + 1
        while j < len(css) and depth > 0:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        out.append((name, css[start + 1:j - 1]))
        i = j
    return out


def parse_selectors(body):
    """返回 [(selector_text, [prop_names]), ...]。"""
    groups = []
    for part in body.split("}"):
        if "{" not in part:
            continue
        sel, decls = part.split("{", 1)
        props = re.findall(r"([a-zA-Z-]+)\s*:", decls)
        groups.append((sel.strip(), props))
    return groups


def find_animation_names(css):
    """提取 animation / animation-name 声明里可能的 keyframes 名。"""
    names = []
    for decl in re.findall(r"animation(?:-name)?\s*:\s*([^;{}]+);", css):
        for tok in decl.split():
            if "(" in tok or tok.startswith("--") or tok.startswith("var"):
                continue  # var(--x) / 自定义属性不是关键帧名
            if DUR_RE.match(tok) or tok in DEFAULT["ignore_name_keywords"]:
                continue
            names.append(tok)
    return names


def lint_css(css, cfg, label):
    findings = []
    kfs = find_keyframes(css)
    seen = set()
    for name, body in kfs:
        if name in seen:
            findings.append({"severity": "error", "check": "@keyframes 重名",
                             "detail": f"{label}: @{name} 重复定义"})
        seen.add(name)

        groups = parse_selectors(body)
        if not groups:
            continue
        first_props = groups[0][1]
        last_props = groups[-1][1]
        gpu = cfg["start_end_props"]
        start_ok = any(p in first_props for p in gpu)
        end_ok = any(p in last_props for p in gpu)
        if not (start_ok and end_ok):
            findings.append({"severity": "error", "check": "起止无 transform/opacity",
                             "detail": f"{label}: @{name} 起止未用 {gpu}（易卡顿或无动画）"})

        all_props = [p for _, ps in groups for p in ps]
        bad = [p for p in all_props if p in cfg["layout_thrash_props"]]
        if bad:
            findings.append({"severity": "warn", "check": "layout 属性",
                             "detail": f"{label}: @{name} 使用了 layout 属性 {sorted(set(bad))}（触发重排）"})

    defined = {n for n, _ in kfs}
    for ref in find_animation_names(css):
        if ref not in defined and ref not in cfg["ignore_name_keywords"]:
            findings.append({"severity": "warn", "check": "未定义引用",
                             "detail": f"{label}: animation 引用了未定义的 @{ref}"})
    return findings


def main():
    ap = argparse.ArgumentParser(description="CSS 关键帧 lint（纯标准库）")
    ap.add_argument("--css", nargs="+", required=True, help="CSS 文件或目录")
    ap.add_argument("--config", help="规则 JSON（含 _ 注释键，自动跳过）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    cfg = load_config(args.config)
    findings = []
    for path in args.css:
        import os
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for fn in files:
                    if fn.endswith(".css"):
                        findings += lint_css(read_css(os.path.join(root, fn)), cfg, fn)
        else:
            findings += lint_css(read_css(path), cfg, path)

    errors = [f for f in findings if f["severity"] == "error"]
    if args.json:
        print(json.dumps({"errors": len(errors), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        for f in findings:
            mark = "✗" if f["severity"] == "error" else "!"
            print(f"  [{mark}] {f['check']}: {f['detail']}")
        print(f"\n结果：{len(errors)} error, {len(findings) - len(errors)} warning")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
