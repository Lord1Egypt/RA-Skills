#!/usr/bin/env python3
"""aria_lint.py — ARIA 用法静态校验（确定性、可重复执行）。

校验 HTML 中 role 与 aria-* 的使用是否合法：
  1. role 取值必须在 WAI-ARIA 1.2 角色表中（否则 error）
  2. aria-* 属性名必须在标准列表中（疑似拼写错误 → warning）
  3. 复合组件（listbox/menu/radiogroup/tablist/tree/...）必须包含必需的子角色
  4. 冗余 role（如 <button role="button">、<nav role="navigation">）→ warning

纯标准库实现。配合 a11y_audit.py 与 references/semantic-html-aria.md 使用。

用法:
    python3 aria_lint.py page.html
    python3 aria_lint.py page.html --json
    python3 aria_lint.py page.html --strict
    cat page.html | python3 aria_lint.py -
"""
import argparse
import json
import sys
from html.parser import HTMLParser

# WAI-ARIA 1.2 标准角色（节选权威全集）
ARIA_ROLES = {
    # 命令 / 窗口
    "button", "link", "dialog", "alertdialog",
    # 复合组件
    "combobox", "grid", "listbox", "menu", "menubar", "radiogroup", "tablist",
    "tree", "treegrid", "table", "feed", "select",
    # 地标
    "banner", "complementary", "contentinfo", "form", "main", "navigation",
    "region", "search",
    # 结构
    "application", "article", "blockquote", "caption", "cell", "code",
    "columnheader", "definition", "deletion", "emphasis", "figure", "group",
    "heading", "img", "insertion", "list", "listitem", "log", "marquee", "math",
    "note", "paragraph", "presentation", "none", "row", "rowgroup", "section",
    "separator", "strong", "subscript", "superscript", "term", "time", "tooltip",
    # 小组件
    "checkbox", "gridcell", "menuitem", "menuitemcheckbox", "menuitemradio",
    "option", "progressbar", "radio", "scrollbar", "searchbox", "slider",
    "spinbutton", "switch", "tab", "tabpanel", "textbox", "treeitem",
    # 实时区域
    "alert", "status",
}

# 标准 aria-* 状态与属性
ARIA_STATE_PROPS = {
    "aria-activedescendant", "aria-atomic", "aria-autocomplete", "aria-busy",
    "aria-checked", "aria-colcount", "aria-colindex", "aria-colspan",
    "aria-controls", "aria-current", "aria-describedby", "aria-details",
    "aria-disabled", "aria-errormessage", "aria-expanded", "aria-flowto",
    "aria-haspopup", "aria-hidden", "aria-invalid", "aria-keyshortcuts",
    "aria-label", "aria-labelledby", "aria-level", "aria-live", "aria-modal",
    "aria-multiline", "aria-multiselectable", "aria-orientation", "aria-owns",
    "aria-placeholder", "aria-posinset", "aria-pressed", "aria-readonly",
    "aria-relevant", "aria-required", "aria-roledescription", "aria-rowcount",
    "aria-rowindex", "aria-rowspan", "aria-selected", "aria-setsize",
    "aria-sort", "aria-valuemax", "aria-valuemin", "aria-valuenow",
    "aria-valuetext",
}

# 复合组件的必需子角色（只需出现其一）
REQUIRED_CHILDREN = {
    "listbox": {"option"},
    "menu": {"menuitem"},
    "menubar": {"menuitem"},
    "radiogroup": {"radio"},
    "tablist": {"tab"},
    "tree": {"treeitem"},
    "treegrid": {"row", "gridcell"},
    "table": {"row"},
    "grid": {"row"},
    "row": {"gridcell", "columnheader", "rowheader", "cell"},
    "feed": {"article"},
}

# 标签隐式角色（用于冗余 role 检测）
IMPLICIT_ROLE = {
    "a": "link",          # 仅当有 href
    "button": "button",
    "nav": "navigation",
    "main": "main",
    "ul": "list",
    "ol": "list",
    "li": "listitem",
    "article": "article",
    "dialog": "dialog",
    "table": "table",
    "tr": "row",
    "th": "columnheader",
    "td": "cell",
    "section": "region",  # 仅当有 aria-label
}

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "param", "source", "track", "wbr",
}


class AriaLinter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.findings = []
        # 栈：每个显式 role 元素一个 frame；composite 记录已见子角色
        self.stack = []

    def _add(self, rule, severity, element, message, line):
        self.findings.append({
            "rule": rule, "severity": severity, "element": element,
            "message": message, "line": line,
        })

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        line = self.getpos()[0]
        role = (d.get("role") or "").strip().lower()

        # 1) role 合法性
        if role and role not in ARIA_ROLES:
            self._add("invalid-role", "error", tag,
                      f"role=\"{role}\" 不是合法的 WAI-ARIA 角色", line)

        # 2) aria-* 合法性
        for k in d:
            if k.startswith("aria-") and k not in ARIA_STATE_PROPS:
                self._add("unknown-aria-attr", "warning", tag,
                          f"未知 aria 属性 \"{k}\"（疑似拼写错误）", line)

        # 4) 冗余 role
        if role:
            implicit = IMPLICIT_ROLE.get(tag)
            if tag == "a" and "href" not in d:
                implicit = None
            if tag == "section" and "aria-label" not in d and "aria-labelledby" not in d:
                implicit = None
            if implicit and implicit == role:
                self._add("redundant-role", "warning", tag,
                          f"<{tag}> 的隐式角色已是 {role}，无需重复声明", line)

        if role in REQUIRED_CHILDREN and tag not in VOID_TAGS:
            self.stack.append({"role": role, "seen": set(), "line": line})
        elif tag not in VOID_TAGS:
            self.stack.append(None)  # 占位，保持与 endtag 对齐

        # 3) 子角色反馈给所有祖先复合组件
        if role:
            for frame in self.stack:
                if isinstance(frame, dict) and frame["role"] in REQUIRED_CHILDREN:
                    frame["seen"].add(role)

    def handle_endtag(self, tag):
        if not self.stack:
            return
        frame = self.stack.pop()
        if isinstance(frame, dict) and frame["role"] in REQUIRED_CHILDREN:
            need = REQUIRED_CHILDREN[frame["role"]]
            if not (need & frame["seen"]):
                self._add("missing-child-role", "error", tag,
                          f"role=\"{frame['role']}\" 缺少必需子角色 {sorted(need)}",
                          frame["line"])


def lint(html):
    l = AriaLinter()
    l.feed(html)
    # 处理未闭合（防御性）：检查栈中残留的 composite
    for frame in l.stack:
        if isinstance(frame, dict) and frame["role"] in REQUIRED_CHILDREN:
            need = REQUIRED_CHILDREN[frame["role"]]
            if not (need & frame["seen"]):
                l._add("missing-child-role", "error", frame["role"],
                       f"role=\"{frame['role']}\" 缺少必需子角色 {sorted(need)}（标签未闭合？）",
                       frame["line"])
    return l.findings


def main():
    ap = argparse.ArgumentParser(description="ARIA 用法静态校验（无依赖）")
    ap.add_argument("file", help="HTML 文件路径，或用 - 从 stdin 读取")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true",
                    help="存在 error 级缺陷则退出码 1")
    args = ap.parse_args()

    if args.file == "-":
        html = sys.stdin.read()
    else:
        try:
            with open(args.file, encoding="utf-8") as fh:
                html = fh.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"error: 无法读取 {args.file}: {e}", file=sys.stderr)
            return 2

    findings = lint(html)
    errors = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] == "warning"]

    if args.json:
        print(json.dumps(
            {"errors": len(errors), "warnings": len(warnings), "findings": findings},
            ensure_ascii=False, indent=2,
        ))
    else:
        if not findings:
            print("未发现 ARIA 用法问题。")
        for f in findings:
            loc = f"line {f['line']}" if f.get("line") else ""
            print(f"[{f['severity'].upper():7}] {f['rule']:<20} <{f['element']}> "
                  f"{f['message']}  ({loc})".rstrip())
        print(f"\n汇总: {len(errors)} error / {len(warnings)} warning")

    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
