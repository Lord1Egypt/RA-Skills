#!/usr/bin/env python3
"""
获取有效的 access_token。
用法: chanjing_get_token
输出: 成功时打印 access_token 到 stdout；失败时打印错误到 stderr 并 exit 1
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import resolve_chanjing_access_token  # noqa: E402


def main():
    token, err = resolve_chanjing_access_token()
    if err:
        print(err, file=sys.stderr)
        return 1
    print(token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
