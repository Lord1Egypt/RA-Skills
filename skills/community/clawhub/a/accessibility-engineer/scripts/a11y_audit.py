#!/usr/bin/env python3
"""a11y_audit.py — 静态 HTML 可访问性审计（确定性、可重复执行）。

对 HTML 做无依赖的静态检查，识别最常见的可访问性缺陷：缺少 lang / title、
图片缺 alt、链接/按钮无名、表单控件缺 label、标题层级跳级、多个 <main>、
废弃标签等。输出 findings（JSON 或文本），--strict 模式下存在 error 则退出码 1。

注意：静态检查只能覆盖“能用 AST 判定”的问题。读屏体验、对比度、键盘可达性等
仍需配合 references/screen-reader-testing.md 与 contrast_check.py 做人工/动态验证。

用法:
    python3 a11y_audit.py page.html
    python3 a11y_audit.py page.html --json
    python3 a11y_audit.py page.html --strict
    cat page.html | python3 a11y_audit.py -            # 从 stdin 读取
"""
import argparse
import json
import sys
from html.parser import HTMLParser

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "param", "source", "track", "wbr",
}
LABELLED_INPUT_TYPES = {"hidden", "button", "submit", "reset"}


class A11yAuditor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.findings = []
        self.in_label = 0
        self.label_fors = set()
        self.headings = []          # (level, line, attrs)
        self.main_count = 0
        self.has_title = False
        self.seen_html = False
        self.html_lang = None
        self.a_ctx = None           # (attrs, [text])
        self.button_ctx = None
        self.stack = []

    def _add(self, rule, severity, element, message, line):
        self.findings.append({
            "rule": rule, "severity": severity, "element": element,
            "message": message, "line": line,
        })

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        line = self.getpos()[0]

        if tag == "html":
            self.seen_html = True
            self.html_lang = d.get("lang")
        elif tag == "title":
            self.has_title = True
        elif tag == "label":
            if d.get("for"):
                self.label_fors.add(d["for"])
            self.in_label += 1
        elif tag == "main":
            self.main_count += 1
            if self.main_count == 2:
                self._add("multiple-main", "error", "main",
                          "存在多个 <main>，每个页面应只有一个", line)
        elif tag == "img" and "alt" not in d:
            self._add("img-alt", "error", "img",
                      "图片缺少 alt 属性（装饰图用 alt=\"\"）", line)
        elif tag in ("blink", "marquee"):
            self._add("deprecated-tag", "error", tag,
                      f"<{tag}> 已废弃，会触发光敏/注意力问题", line)
        elif tag == "input":
            t = (d.get("type") or "text").lower()
            if t == "image" and "alt" not in d:
                self._add("input-image-alt", "error", "input",
                          "input[type=image] 缺少 alt", line)
            elif t in LABELLED_INPUT_TYPES:
                pass
            elif self.in_label:
                pass
            elif d.get("aria-label") or d.get("aria-labelledby"):
                pass
            elif d.get("id") and d.get("id") in self.label_fors:
                pass
            else:
                self._add("input-label", "error", "input",
                          f"input[type={t}] 缺少关联 label（无 for/嵌套/aria-label）", line)
        elif tag == "a":
            self.a_ctx = (d, [])
        elif tag == "button":
            self.button_ctx = (d, [])
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append((int(tag[1]), line, d))

        self.stack.append(tag)

    def handle_data(self, data):
        if self.a_ctx is not None:
            self.a_ctx[1].append(data)
        if self.button_ctx is not None:
            self.button_ctx[1].append(data)

    def handle_endtag(self, tag):
        if tag == "label":
            self.in_label = max(0, self.in_label - 1)
        elif tag == "a" and self.a_ctx is not None:
            text = "".join(self.a_ctx[1]).strip()
            d = self.a_ctx[0]
            if (not text and not d.get("aria-label") and not d.get("aria-labelledby")):
                self._add("link-text", "error", "a",
                          "链接缺少可访问名称（无文本/aria-label/aria-labelledby）",
                          self.getpos()[0])
            self.a_ctx = None
        elif tag == "button" and self.button_ctx is not None:
            text = "".join(self.button_ctx[1]).strip()
            d = self.button_ctx[0]
            if (not text and not d.get("aria-label") and not d.get("aria-labelledby")):
                self._add("button-name", "error", "button",
                          "按钮缺少可访问名称（无文本/aria-label/aria-labelledby）",
                          self.getpos()[0])
            self.button_ctx = None
        if self.stack:
            self.stack.pop()

    def finish(self):
        if self.seen_html and not self.html_lang:
            self._add("html-lang", "error", "html",
                      "<html> 缺少 lang 属性（如 lang=\"zh-CN\"）", 1)
        if not self.has_title:
            self._add("title-missing", "error", "title",
                      "页面缺少 <title>", 1)
        # 标题层级跳级检测：h1 之后直接出现 h3 及以上
        prev = 0
        for level, line, _ in self.headings:
            if prev and level > prev + 1:
                self._add("heading-order", "warning", f"h{level}",
                          f"标题层级跳级：h{prev} 之后直接出现 h{level}", line)
            prev = level


def audit(html):
    a = A11yAuditor()
    a.feed(html)
    a.finish()
    return a.findings


def main():
    ap = argparse.ArgumentParser(description="静态 HTML 可访问性审计（无依赖）")
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

    findings = audit(html)
    errors = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] == "warning"]

    if args.json:
        print(json.dumps(
            {"errors": len(errors), "warnings": len(warnings), "findings": findings},
            ensure_ascii=False, indent=2,
        ))
    else:
        if not findings:
            print("未发现静态可访问性问题。")
        for f in findings:
            loc = f"line {f['line']}" if f.get("line") else ""
            print(f"[{f['severity'].upper():7}] {f['rule']:<16} <{f['element']}> "
                  f"{f['message']}  ({loc})".rstrip())
        print(f"\n汇总: {len(errors)} error / {len(warnings)} warning")

    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
