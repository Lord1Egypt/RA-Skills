"""Code Review Gate 测试用例。"""

from __future__ import annotations

import sys
from pathlib import Path

# 确保 src 可导入
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.checks.security import SecurityChecker
from src.checks.functional import FunctionalChecker
from src.checks.performance import PerformanceChecker
from src.checks.readability import ReadabilityChecker
from src.checks.maintainability import MaintainabilityChecker
from src.checks.testing import TestingChecker
from src.checks.documentation import DocumentationChecker


# --- Fixtures ---

SAFE_DIFF = """diff --git a/utils.py b/utils.py
new file mode 100644
--- /dev/null
+++ b/utils.py
@@ -0,0 +1,10 @@
+def add(a: int, b: int) -> int:
+    \"\"\"Add two numbers.\"\"\"
+    if not isinstance(a, int) or not isinstance(b, int):
+        raise TypeError("Both arguments must be integers")
+    return a + b
+
+def multiply(a: int, b: int) -> int:
+    \"\"\"Multiply two numbers.\"\"\"
+    return a * b
"""

SQL_INJECTION_DIFF = """diff --git a/api/users.py b/api/users.py
--- a/api/users.py
+++ b/api/users.py
@@ -10,6 +10,8 @@
+def get_user(user_id):
+    query = f"SELECT * FROM users WHERE id = {user_id}"
+    return db.execute(query)
"""

SECRET_IN_CODE_DIFF = """diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -0,0 +1,3 @@
+API_KEY = "sk-abcdef1234567890"
+DATABASE_URL = "postgresql://localhost/mydb"
+PASSWORD = "my_secret_password_123"
"""

BARE_EXCEPT_DIFF = """diff --git a/service.py b/service.py
--- a/service.py
+++ b/service.py
@@ -5,0 +5,5 @@
+def process():
+    try:
+        do_something()
+    except:
+        pass
"""

PRINT_LOGGING_DIFF = """diff --git a/handler.py b/handler.py
--- a/handler.py
+++ b/handler.py
@@ -1,0 +1,5 @@
+def handle_request(data):
+    print("Processing request...")
+    result = process(data)
+    print(f"Result: {result}")
+    return result
"""

NO_TESTS_DIFF = """diff --git a/service.py b/service.py
--- a/service.py
+++ b/service.py
@@ -0,0 +1,5 @@
+def calculate_total(items):
+    return sum(item.price for item in items)
+
+def validate_order(order):
+    return order.status != "cancelled"
"""

LONG_FUNCTION_DIFF = (
    "diff --git a/big.py b/big.py\n"
    "--- a/big.py\n"
    "+++ b/big.py\n"
    "@@ -0,0 +1,110 @@\n"
    "+def long_function():\n"
    "+    \"\"\"A very long function.\"\"\"\n"
    + "\n".join(f"+    line_{i} = {i}" for i in range(110))
)


# --- Security Tests ---

def test_detect_sql_injection():
    """检测 f-string SQL 注入。"""
    checker = SecurityChecker(SQL_INJECTION_DIFF, "", None)
    results = checker.run()
    assert len(results) > 0
    findings = results[0].findings
    sql_findings = [f for f in findings if "SQL" in (f.detail or "") and f.status == "fail"]
    assert len(sql_findings) >= 1, f"Expected SQL injection findings, got {[(f.detail, f.status) for f in findings]}"


def test_detect_hardcoded_secrets():
    """检测硬编码密钥。"""
    checker = SecurityChecker(SECRET_IN_CODE_DIFF, "", None)
    results = checker.run()
    findings = results[0].findings
    secret_findings = [f for f in findings if f.check_id == "sec-secret" and f.status == "fail"]
    assert len(secret_findings) >= 1


def test_safe_code_passes_security():
    """正常代码应通过安全检查。"""
    checker = SecurityChecker(SAFE_DIFF, "", None)
    results = checker.run()
    assert results[0].status == "pass"


# --- Functional Tests ---

def test_detect_bare_except():
    """检测裸 except。"""
    checker = FunctionalChecker(BARE_EXCEPT_DIFF, "", None)
    results = checker.run()
    findings = results[0].findings
    bare_excepts = [f for f in findings if "裸 except" in (f.detail or "")]
    assert len(bare_excepts) >= 1


def test_safe_code_passes_functional():
    """正常代码应通过功能检查。"""
    checker = FunctionalChecker(SAFE_DIFF, "", None)
    results = checker.run()
    assert results[0].status == "pass"


# --- Performance Tests ---

def test_detect_simple_diff():
    """简单 diff 的性能检查应通过。"""
    checker = PerformanceChecker(SAFE_DIFF, "", None)
    results = checker.run()
    assert results[0].status == "pass"


# --- Readability Tests ---

def test_detect_long_function():
    """检测过长函数。"""
    checker = ReadabilityChecker(LONG_FUNCTION_DIFF, "", None)
    results = checker.run()
    # 100+ 行的函数应该被检测到
    findings = results[0].findings
    long_funcs = [f for f in findings if "函数长度超过" in (f.detail or "")]
    assert len(long_funcs) >= 1, f"Expected long function finding, got {[(f.detail) for f in findings]}"


def test_safe_code_passes_readability():
    """正常代码应通过可读性检查。"""
    checker = ReadabilityChecker(SAFE_DIFF, "", None)
    results = checker.run()
    assert results[0].status == "pass"


# --- Maintainability Tests ---

def test_detect_print_logging():
    """检测 print 代替 logging。"""
    checker = MaintainabilityChecker(PRINT_LOGGING_DIFF, "", None)
    results = checker.run()
    findings = results[0].findings
    print_findings = [f for f in findings if "print()" in (f.detail or "")]
    assert len(print_findings) >= 1


def test_safe_code_passes_maintainability():
    """正常代码应通过可维护性检查。"""
    checker = MaintainabilityChecker(SAFE_DIFF, "", None)
    results = checker.run()
    assert results[0].status == "pass"


# --- Testing Tests ---

def test_detect_missing_tests():
    """检测缺少测试。"""
    checker = TestingChecker(NO_TESTS_DIFF, "", None)
    results = checker.run()
    findings = results[0].findings
    test_findings = [f for f in findings if f.status == "fail"]
    assert len(test_findings) >= 1


# --- Documentation Tests ---

def test_detect_missing_docstrings():
    """检测缺少文档字符串。"""
    diff = """diff --git a/lib.py b/lib.py
--- a/lib.py
+++ b/lib.py
@@ -0,0 +1,3 @@
+def public_function():
+    return 42
"""
    checker = DocumentationChecker(diff, "", None)
    results = checker.run()
    findings = results[0].findings
    doc_findings = [f for f in findings if "缺少文档字符串" in (f.detail or "")]
    assert len(doc_findings) >= 1


def test_detect_todo():
    """检测 TODO。"""
    diff = """diff --git a/main.py b/main.py
--- a/main.py
+++ b/main.py
@@ -0,0 +1,2 @@
+# TODO: implement error handling
"""
    checker = DocumentationChecker(diff, "", None)
    results = checker.run()
    findings = results[0].findings
    todo_findings = [f for f in findings if "TODO" in (f.detail or "")]
    assert len(todo_findings) >= 1


# --- Non-code file skip ---

def test_skip_non_code_files():
    """Markdown 等非代码文件应跳过检查。"""
    md_diff = """diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1 +1,2 @@
 # Title
+Some text
"""
    checker = SecurityChecker(md_diff, "", None)
    results = checker.run()
    assert results[0].status == "pass"
    assert any("skip" in (f.check_id or "") for f in results[0].findings)
