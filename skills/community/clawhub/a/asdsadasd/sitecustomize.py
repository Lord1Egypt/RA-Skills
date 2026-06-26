"""
sitecustomize.py — auto-fix Windows terminal encoding to UTF-8.
Đặt file này ở root project, Python sẽ tự load trước mọi script khác.
"""
import sys
import io

if sys.platform == "win32":
    # Force UTF-8 stdout/stderr để render emoji và tiếng Việt đúng
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
