#!/usr/bin/env python3
"""preview_url — 浏览器预览 URL"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def main():
    params = parse_input()
    url = get_param(params, "url", required=True)

    if not url.startswith(("http://", "https://", "file://")):
        url = "https://" + url

    import webbrowser
    try:
        opened = webbrowser.open(url, new=2)  # new=2: 新标签页
    except Exception as e:
        output_error(f"无法打开浏览器: {e}", EXIT_EXEC_ERROR)

    if opened:
        output_ok({"url": url, "opened": True, "message": "已在新标签页打开"})
    else:
        output_error(f"无法打开: {url}", EXIT_EXEC_ERROR)


if __name__ == "__main__":
    main()
