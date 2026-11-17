#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抖音数据采集统一入口：评论采集 + 账号主页作品抓取。

薄路由层：只负责按子命令分发到各自脚本，参数定义/帮助仍归各自脚本维护，
避免重复实现。延迟导入子模块，保证「没装 playwright」不影响评论功能。

用法:
    python douyin.py comments <视频链接> [选项]       # 评论采集（= fetch_comments.py）
    python douyin.py posts    <主页链接/sec_uid> [选项]  # 主页作品抓取（= fetch_posts.py）

子命令别名：comments / comment / c；posts / post / p。
子命令后接 ``-h`` 查看各自完整参数。
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

_USAGE = """\
抖音数据采集统一入口（评论 + 主页作品）

用法:
  douyin <子命令> [选项]

子命令:
  comments, comment, c   评论采集（= fetch_comments.py）
      例: douyin comments "<视频链接>" --browser --output c.json
  posts, post, p         账号主页作品抓取（= fetch_posts.py）
      例: douyin posts "<主页链接或sec_uid>" --since 2026-09-01 --until 2026-09-18 --analyze

子命令后加 -h 查看完整参数:
  douyin comments -h
  douyin posts -h
"""


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(_USAGE, end="", file=sys.stderr)
        return 2
    if argv[0] in ("-h", "--help", "help"):
        print(_USAGE, end="")
        return 0

    cmd = argv[0]
    rest = argv[1:]

    if cmd in ("comments", "comment", "c"):
        from fetch_comments import main as comments_main  # noqa: E402
        return comments_main(rest)

    if cmd in ("posts", "post", "p"):
        try:
            from fetch_posts import main as posts_main  # noqa: E402
        except SystemExit as exc:
            # fetch_posts 顶层 import playwright 失败会 sys.exit(2)，友好提示已打印到 stderr
            return int(exc.code) if exc.code is not None else 2
        return posts_main(rest)

    print(f"未知子命令：{cmd!r}\n", file=sys.stderr)
    print(_USAGE, end="", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
