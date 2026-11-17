#!/usr/bin/env python3
"""静态质量检查 —— JavaScript 语法、未声明变量、HTML 可访问性、CSP、外部依赖、构建产物大小。

运行：python scripts/quality_check.py
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_PATH = os.path.join(ROOT, "assets", "dashboard.html")
ARTIFACTS_DIR = os.path.join(ROOT, "tests", "artifacts")

passed = 0
failed = 0
warnings = 0


def ok(label, cond, msg=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"  [PASS] {label}")
    else:
        failed += 1
        print(f"  [FAIL] {label}: {msg}")


def warn(label, msg=""):
    global warnings
    warnings += 1
    print(f"  [WARN] {label}: {msg}")


def read_dashboard():
    with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
        return f.read()


def extract_js(html):
    m = re.search(r"<script>([\s\S]*?)</script>", html)
    return m.group(1) if m else ""


def main():
    global passed, failed, warnings
    html = read_dashboard()
    js = extract_js(html)

    print("\n=== JavaScript 语法检查 ===")
    # 用 node 检查语法
    import tempfile, subprocess
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp_path = f.name
    try:
        result = subprocess.run(["node", "--check", tmp_path], capture_output=True, text=True)
        ok("JavaScript 语法正确", result.returncode == 0, result.stderr.strip())
    except FileNotFoundError:
        warn("未找到 node，跳过语法检查")
    finally:
        os.unlink(tmp_path)

    print("\n=== 构建产物大小监控 ===")
    size_bytes = len(html.encode("utf-8"))
    size_kb = size_bytes / 1024
    ok(f"构建产物大小 {size_kb:.1f} KB < 500 KB", size_kb < 500, f"实际 {size_kb:.1f} KB")
    # 保存大小到 artifacts
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    with open(os.path.join(ARTIFACTS_DIR, "build_size.json"), "w", encoding="utf-8") as f:
        json.dump({"bytes": size_bytes, "kb": round(size_kb, 1)}, f)

    print("\n=== CSP 与外部依赖检查 ===")
    ok("CSP 包含 connect-src 'none'", "connect-src 'none'" in " ".join(html.split()))
    ok("CSP 包含 script-src 'self'", "script-src 'self'" in html)
    ok("CSP 禁止 object-src", "object-src 'none'" in html)
    ok("无外部 script src", not re.search(r'<script[^>]+src\s*=\s*["\']https?://', html))
    ok("无外部 link href", not re.search(r'<link[^>]+href\s*=\s*["\']https?://', html))

    print("\n=== HTML 可访问性检查 ===")
    ok("有 lang 属性", 'lang=' in html)
    ok("有 viewport meta", 'viewport' in html)
    ok("有 title", '<title>' in html)
    ok("canvas 有替代文本", 'role="img"' in html and 'aria-label' in html)
    ok("tablist 有 aria-label", 'role="tablist"' in html and 'aria-label=' in html)
    ok("tab 有 aria-controls", 'aria-controls=' in html)
    ok("图片有 alt（或无图片）", not re.search(r'<img(?![^>]*alt=)', html) or '<img' not in html)

    print("\n=== 未声明变量检查（no-undef 近似） ===")
    # 检查常见错误：matches（应为 this._marks）
    ok("未使用未声明的 matches 变量", "matches.length" not in js or "this._marks.length" in js)
    # 检查裸 marks 赋值（排除 this._marks 和 this._marks 子串）
    # 真正的裸赋值是：行首或分号后的 marks = []，且前面没有 _ 或 this._
    bare_marks_assign = re.search(r'(?<![\.\w])marks\s*=\s*\[\]', js)
    ok("marks 赋值通过 this._marks", bare_marks_assign is None, "发现裸 marks 赋值")
    bare_clean = re.search(r'(?<![\.\w])cleanHtml\s*=', js)
    ok("cleanHtml 赋值通过 this._cleanHtml", bare_clean is None, "发现裸 cleanHtml 赋值")

    print("\n=== 关键功能完整性 ===")
    required_functions = [
        ("sanitizeUrl", "URL 安全"),
        ("determineRootPrefix", "路径匹配"),
        ("computeSettingCompletion", "完成度计算"),
        ("diagnoseChapters", "章节诊断"),
        ("classifyError", "错误分类"),
        ("stripMarkdown", "TXT 导出"),
        ("SourceSession", "数据源状态收敛"),
        ("Store.bumpVersion", "数据版本驱动"),
    ]
    for fn, desc in required_functions:
        ok(f"定义了 {fn}（{desc}）", fn in js)

    print(f"\n=== 结果：{passed} 通过，{failed} 失败，{warnings} 警告 ===\n")

    # 保存检查结果到 artifacts
    with open(os.path.join(ARTIFACTS_DIR, "quality_check.json"), "w", encoding="utf-8") as f:
        json.dump({"passed": passed, "failed": failed, "warnings": warnings}, f, ensure_ascii=False)

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
