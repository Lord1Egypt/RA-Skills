"""快手 / B 站 / 抖音 视频发布统一 CLI（CDP + Chrome）。

依赖: pip install requests websockets

用法示例:

  python cli.py publish-kuaishou --config ./test_data/描述.txt
  python cli.py publish-bilibili --config ./test_data/描述.txt --no-publish
  python cli.py publish-douyin --config ./test_data/描述.txt --wait-timeout 300
  python cli.py publish-all --config ./test_data/描述.txt

退出码: 0 成功, 2 错误或未全部成功（publish-all 时若任一失败）。
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

# 保证可从 scripts 目录运行：python cli.py 或 python -m 时能找到 kbs / chrome_launcher
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("kbs-cli")


def _output(data: dict, exit_code: int = 0) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


def _connect_browser(args: argparse.Namespace):
    from chrome_launcher import ensure_chrome, has_display
    from kbs.cdp import Browser

    headless = bool(getattr(args, "headless", False))
    if not headless and not has_display():
        headless = True

    if not ensure_chrome(port=args.port, headless=headless, user_data_dir=args.user_data_dir):
        _output({"success": False, "error": "无法启动或连接 Chrome，请检查是否已安装并允许远程调试端口"}, 2)

    browser = Browser(host=args.host, port=args.port)
    browser.connect()
    page = browser.get_or_create_page()
    return browser, page


def cmd_publish_kuaishou(args: argparse.Namespace) -> None:
    from kbs.publish_kuaishou import publish_kuaishou
    from kbs.types import load_publish_config

    cfg = load_publish_config(args.config)
    browser, page = _connect_browser(args)
    try:
        r = publish_kuaishou(
            page,
            cfg,
            wait_timeout=args.wait_timeout,
            do_publish=not args.no_publish,
        )
        _output({"success": r.success, **r.to_dict()}, 0 if r.success else 2)
    finally:
        browser.close()


def cmd_publish_bilibili(args: argparse.Namespace) -> None:
    from kbs.publish_bilibili import publish_bilibili
    from kbs.types import load_publish_config

    cfg = load_publish_config(args.config)
    browser, page = _connect_browser(args)
    try:
        r = publish_bilibili(
            page,
            cfg,
            wait_timeout=args.wait_timeout,
            do_publish=not args.no_publish,
        )
        _output({"success": r.success, **r.to_dict()}, 0 if r.success else 2)
    finally:
        browser.close()


def cmd_publish_douyin(args: argparse.Namespace) -> None:
    from kbs.publish_douyin import publish_douyin
    from kbs.types import load_publish_config

    cfg = load_publish_config(args.config)
    browser, page = _connect_browser(args)
    try:
        r = publish_douyin(
            page,
            cfg,
            wait_timeout=args.wait_timeout,
            do_publish=not args.no_publish,
        )
        _output({"success": r.success, **r.to_dict()}, 0 if r.success else 2)
    finally:
        browser.close()


def cmd_publish_all(args: argparse.Namespace) -> None:
    from kbs.publish_bilibili import publish_bilibili
    from kbs.publish_douyin import publish_douyin
    from kbs.publish_kuaishou import publish_kuaishou
    from kbs.types import load_publish_config

    cfg = load_publish_config(args.config)
    browser, page = _connect_browser(args)
    results = []
    exit_code = 0
    try:
        for name, fn in (
            ("kuaishou", publish_kuaishou),
            ("bilibili", publish_bilibili),
            ("douyin", publish_douyin),
        ):
            r = fn(
                page,
                cfg,
                wait_timeout=args.wait_timeout,
                do_publish=not args.no_publish,
            )
            results.append(r.to_dict())
            if not r.success:
                exit_code = 2
                logger.warning("平台 %s 未完成: %s", name, r.message)
    finally:
        browser.close()

    _output({"success": exit_code == 0, "results": results}, exit_code)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kbs-publish-cli", description="快手/B站/抖音 视频发布 CDP CLI")
    p.add_argument("--host", default="127.0.0.1", help="Chrome 调试地址 (default: 127.0.0.1)")
    p.add_argument("--port", type=int, default=9222, help="Chrome 调试端口 (default: 9222)")
    p.add_argument(
        "--user-data-dir",
        default="",
        help="Chrome 用户数据目录（默认 ~/.kbs/chrome-profile，与 chrome_launcher 一致）",
    )
    p.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="无头模式启动 Chrome（需本机已登录对应站点）",
    )
    sub = p.add_subparsers(dest="command", required=True)

    def _add_common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--config", required=True, help="TXT 配置文件路径")
        sp.add_argument(
            "--wait-timeout",
            type=float,
            default=300.0,
            help="等待上传/处理的最长时间（秒），默认 300（5 分钟）",
        )
        sp.add_argument(
            "--no-publish",
            action="store_true",
            help="只填写表单与上传，不点击发布/投稿",
        )

    s1 = sub.add_parser("publish-kuaishou", help="快手 cp.kuaishou.com")
    _add_common(s1)
    s1.set_defaults(func=cmd_publish_kuaishou)

    s2 = sub.add_parser("publish-bilibili", help="B 站创作中心上传页")
    _add_common(s2)
    s2.set_defaults(func=cmd_publish_bilibili)

    s3 = sub.add_parser("publish-douyin", help="抖音创作者中心上传页")
    _add_common(s3)
    s3.set_defaults(func=cmd_publish_douyin)

    s4 = sub.add_parser("publish-all", help="依次执行快手、B 站、抖音（同一浏览器会话）")
    _add_common(s4)
    s4.set_defaults(func=cmd_publish_all)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if getattr(args, "user_data_dir", "") == "":
        args.user_data_dir = None

    try:
        args.func(args)
    except Exception as e:
        logger.exception("执行失败")
        _output({"success": False, "error": str(e)}, 2)


if __name__ == "__main__":
    main()
