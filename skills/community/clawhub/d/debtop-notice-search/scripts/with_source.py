#!/usr/bin/env python3
"""给详情链接追加/覆盖 source 参数，标记调用来源客户端。

用法:
    python3 with_source.py <detail_url> <client>

规则:
    - 链接没有查询参数 → 追加 ?source=…
    - 已有其它查询参数 → 追加 &source=…
    - 已有 source → 覆盖其值（同一链接里不会出现两个 source）
    - 只动查询参数，scheme / 域名 / 路径 / 锚点一律保持原样
"""
from __future__ import annotations

import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def with_source(detail_url: str, client: str) -> str:
    parts = urlsplit(detail_url)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k != "source"]
    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode([*query, ("source", client)]), parts.fragment)
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python3 with_source.py <detail_url> <client>", file=sys.stderr)
        return 2
    print(with_source(sys.argv[1], sys.argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
