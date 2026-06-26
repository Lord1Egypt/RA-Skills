#!/usr/bin/env python3
"""
浏览器操作命令层

提供浏览器状态查询和直接操作的能力。
主要用于测试和调试浏览器交互。
"""

import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from . import service

COMMAND_NAME = "browser"
COMMAND_DESC = "浏览器操作 —— 打开 URL、检测登录状态等"


def _output(success: bool, markdown: str, data: dict = None,
            browser_action: str = None, browser_params: dict = None):
    """统一输出 JSON 响应。"""
    result = {
        "success": success,
        "markdown": markdown,
        "data": data or {},
    }
    if browser_action:
        result["browser_action"] = browser_action
        result["browser_params"] = browser_params or {}
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--action", default="open",
                        choices=["open", "close", "status"],
                        help="操作类型：open=打开URL, close=关闭浏览器, status=获取状态")
    parser.add_argument("--url", default="", help="要打开的 URL")
    parser.add_argument("--wait-login", action="store_true", help="是否等待登录完成")
    parser.add_argument("--timeout", type=int, default=30, help="超时秒数")

    args = parser.parse_args()

    if args.action == "open":
        if not args.url:
            _output(False, "请提供 --url 参数。")
            return

        # 返回浏览器操作指令给牛顿客户端
        _output(
            success=True,
            markdown=f"正在打开授权页面：{args.url}",
            data={"url": args.url},
            browser_action="open_url",
            browser_params={
                "url": args.url,
                "wait_for_login": args.wait_login,
                "timeout": args.timeout,
            },
        )

    elif args.action == "close":
        result = service.close_browser()
        _output(
            success=True,
            markdown="浏览器已关闭。",
            data=result,
        )

    elif args.action == "status":
        result = service.wait_for_browser_result(timeout=args.timeout)
        _output(
            success=result.get("success", False),
            markdown="浏览器状态查询完成。" if result.get("success") else f"查询失败：{result.get('error', '')}",
            data=result,
        )


if __name__ == "__main__":
    main()
