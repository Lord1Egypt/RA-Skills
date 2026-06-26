#!/usr/bin/env python3
"""
绑店流程命令层 —— 牛顿客户端 Skill 主入口

职责：
1. 接收用户意图，启动绑店流程
2. 调用 shop_bind_process 获取动态流程
3. 生成对话引导内容
4. 当需要浏览器操作时，返回 browser_action 指令给牛顿客户端
5. 轮询流程状态直到完成

输出格式（JSON）：
{
    "success": bool,
    "markdown": str,           # 展示给用户的对话内容
    "data": dict,              # 结构化数据
    "browser_action": str,     # 浏览器操作指令（如有）
    "browser_params": dict,    # 浏览器操作参数（如有）
    "flow_completed": bool,    # 流程是否完成
}
"""

import json
import os
import sys
import argparse
from typing import Optional

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _errors import SkillError, ServiceError, BrowserError, AuthError
from _const import FLOW_POLL_INTERVAL, FLOW_POLL_MAX_RETRIES

from . import service as bind_service
from ..shop_info import service as shop_info_service
from ..browser import service as browser_service

COMMAND_NAME = "bind_shop"
COMMAND_DESC = "绑店流程 —— 引导用户完成店铺绑定"


def _output(success: bool, markdown: str, data: dict = None,
            browser_action: str = None, browser_params: dict = None,
            flow_completed: bool = False):
    """统一输出 JSON 响应。"""
    result = {
        "success": success,
        "markdown": markdown,
        "data": data or {},
        "flow_completed": flow_completed,
    }
    if browser_action:
        result["browser_action"] = browser_action
        result["browser_params"] = browser_params or {}

    print(json.dumps(result, ensure_ascii=False, indent=2))


def _format_tool_options(options: list) -> str:
    """格式化 ISV 工具选项列表供用户选择。"""
    if not options:
        return "未找到可用的 ISV 工具，请确认已安装铺货工具。"

    lines = ["**请选择要绑定的平台和工具：**\n"]
    for idx, opt in enumerate(options, 1):
        channel_desc = opt.get("channelDesc", opt.get("channel", ""))
        app_name = opt.get("appName", "")
        shops = opt.get("shops", [])
        shop_count = len(shops)

        lines.append(f"{idx}. **{channel_desc}** — {app_name}")
        if shop_count > 0:
            shop_names = ", ".join([s.get("shopName", "") for s in shops[:3]])
            lines.append(f"   已绑定店铺：{shop_names}{' 等' if shop_count > 3 else ''}")
        else:
            lines.append("   暂无绑定店铺")
        lines.append("")

    lines.append("\n请回复数字序号或平台名称（如：抖音、淘宝）。")
    return "\n".join(lines)


def _find_tool_option(options: list, keyword: str) -> Optional[dict]:
    """根据关键词查找工具选项。"""
    keyword = keyword.strip().lower()

    # 尝试按序号匹配
    try:
        idx = int(keyword) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except ValueError:
        pass

    # 按平台名称匹配
    for opt in options:
        channel = opt.get("channel", "").lower()
        channel_desc = opt.get("channelDesc", "").lower()
        app_name = opt.get("appName", "").lower()
        if keyword in channel or keyword in channel_desc or keyword in app_name:
            return opt

    return None


def _get_step_action(step: dict) -> tuple:
    """
    分析当前步骤需要的操作。

    Returns:
        (action_type, action_data)
        action_type: "browser" | "confirm" | "wait" | "done"
    """
    if not step:
        return "done", None

    link_actions = bind_service.get_link_actions(step)
    if link_actions:
        return "browser", link_actions[0]

    event_actions = bind_service.get_event_actions(step)
    if event_actions:
        return "confirm", event_actions[0]

    return "wait", None


# ── 主流程 ────────────────────────────────────────────────────────────────────

def start_bind_flow(channel: str = None, app_key: str = None,
                    terminal: str = "PC", user_input: str = None) -> dict:
    """
    启动绑店流程。

    如果未指定 channel 和 app_key，先获取 ISV 工具列表让用户选择。
    """
    # 1. 如果已指定 channel + app_key，直接初始化流程
    if channel and app_key:
        return _init_bind_flow(channel, app_key, terminal)

    # 2. 获取 ISV 工具列表
    tools_data = shop_info_service.get_all_tools_and_shops()
    options = tools_data.get("options", [])

    if not options:
        return {
            "success": False,
            "markdown": "未找到可用的 ISV 工具，请确认已安装铺货工具后再试。",
            "data": {},
            "flow_completed": False,
        }

    # 3. 如果用户输入了选择关键词，尝试匹配
    if user_input:
        matched = _find_tool_option(options, user_input)
        if matched:
            return _init_bind_flow(
                matched["channel"], matched["appKey"], terminal
            )

    # 4. 返回工具列表供用户选择
    return {
        "success": True,
        "markdown": _format_tool_options(options),
        "data": {"options": options, "stage": "select_tool"},
        "flow_completed": False,
    }


def _init_bind_flow(channel: str, app_key: str, terminal: str = "PC") -> dict:
    """初始化绑店流程并返回第一步引导。"""
    try:
        flow_data = bind_service.query_shop_bind_process(
            terminal=terminal, action="init",
            app_key=app_key, channel=channel
        )
    except ServiceError as e:
        return {
            "success": False,
            "markdown": f"绑店流程初始化失败：{e}",
            "data": {},
            "flow_completed": False,
        }

    return _process_flow_step(flow_data, channel, app_key, terminal)


def _process_flow_step(flow_data: dict, channel: str, app_key: str,
                       terminal: str) -> dict:
    """处理流程的当前步骤，生成引导内容。"""
    # 检查流程是否已完成
    if bind_service.is_flow_completed(flow_data):
        return {
            "success": True,
            "markdown": "🎉 **绑店流程已全部完成！**\n\n店铺已成功绑定，您现在可以进行铺货、选品等操作。",
            "data": {"flow": flow_data, "stage": "completed"},
            "flow_completed": True,
        }

    # 获取下一个待完成步骤
    step = bind_service.get_next_pending_step(flow_data)
    if not step:
        return {
            "success": True,
            "markdown": "当前绑店流程暂无待完成步骤，流程可能已结束。",
            "data": {"flow": flow_data, "stage": "unknown"},
            "flow_completed": True,
        }

    # 生成步骤引导文本
    step_detail = bind_service.get_current_step_detail(step)
    flow_summary = bind_service.get_flow_summary(flow_data)

    markdown = f"{step_detail}\n\n---\n\n**整体进度：**\n\n{flow_summary}"

    # 分析步骤需要的操作
    action_type, action_data = _get_step_action(step)

    result = {
        "success": True,
        "markdown": markdown,
        "data": {
            "flow": flow_data,
            "step": step,
            "stage": "in_progress",
            "channel": channel,
            "appKey": app_key,
            "terminal": terminal,
        },
        "flow_completed": False,
    }

    # 如果需要浏览器操作，返回 browser_action
    if action_type == "browser" and action_data:
        result["browser_action"] = "open_url"
        result["browser_params"] = {
            "url": action_data.get("url"),
            "wait_for_login": True,
            "timeout": 120,
            "action_name": action_data.get("name", ""),
        }
        result["markdown"] += (
            f"\n\n👉 **请点击上方链接完成【{action_data.get('name', '授权')}】，"
            f"完成后我会自动检测并引导您进行下一步。**"
        )

    return result


def continue_bind_flow(channel: str, app_key: str, terminal: str = "PC",
                       user_confirmed: bool = False) -> dict:
    """
    继续绑店流程（浏览器操作完成后调用）。

    重新查询流程状态，返回下一步引导。
    """
    try:
        flow_data = bind_service.query_shop_bind_process(
            terminal=terminal, action="query",
            app_key=app_key, channel=channel
        )
    except ServiceError as e:
        return {
            "success": False,
            "markdown": f"查询流程状态失败：{e}",
            "data": {},
            "flow_completed": False,
        }

    return _process_flow_step(flow_data, channel, app_key, terminal)


def close_bind_flow(channel: str, app_key: str, terminal: str = "PC") -> dict:
    """关闭当前绑店流程。"""
    try:
        bind_service.close_shop_bind_process(channel, app_key, terminal)
        return {
            "success": True,
            "markdown": "绑店流程已关闭。如需重新绑店，请再次发起。",
            "data": {"stage": "closed"},
            "flow_completed": False,
        }
    except ServiceError as e:
        return {
            "success": False,
            "markdown": f"关闭流程失败：{e}",
            "data": {},
            "flow_completed": False,
        }


# ── CLI 入口 ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--action", default="start",
                        choices=["start", "continue", "close", "query"],
                        help="操作类型：start=启动流程, continue=继续流程, close=关闭流程, query=查询状态")
    parser.add_argument("--channel", default="", help="渠道代码，如 douyin、taobao")
    parser.add_argument("--app-key", default="", help="服务商工具 appKey")
    parser.add_argument("--terminal", default="PC", choices=["PC", "MOBILE"], help="终端类型")
    parser.add_argument("--user-input", default="", help="用户输入（用于选择平台/工具）")
    parser.add_argument("--flow-data", default="", help="流程数据 JSON（continue 时使用）")

    args = parser.parse_args()

    if args.action == "start":
        result = start_bind_flow(
            channel=args.channel or None,
            app_key=args.app_key or None,
            terminal=args.terminal,
            user_input=args.user_input or None,
        )
    elif args.action == "continue":
        if not args.channel or not args.app_key:
            _output(False, "继续流程需要提供 --channel 和 --app-key 参数。")
            return
        result = continue_bind_flow(
            channel=args.channel,
            app_key=args.app_key,
            terminal=args.terminal,
        )
    elif args.action == "close":
        if not args.channel or not args.app_key:
            _output(False, "关闭流程需要提供 --channel 和 --app-key 参数。")
            return
        result = close_bind_flow(
            channel=args.channel,
            app_key=args.app_key,
            terminal=args.terminal,
        )
    elif args.action == "query":
        if not args.channel or not args.app_key:
            _output(False, "查询状态需要提供 --channel 和 --app-key 参数。")
            return
        try:
            flow_data = bind_service.query_shop_bind_process(
                terminal=args.terminal, action="query",
                app_key=args.app_key, channel=args.channel
            )
            result = _process_flow_step(flow_data, args.channel, args.app_key, args.terminal)
        except ServiceError as e:
            result = {
                "success": False,
                "markdown": f"查询失败：{e}",
                "data": {},
                "flow_completed": False,
            }
    else:
        result = {
            "success": False,
            "markdown": f"未知操作：{args.action}",
            "data": {},
            "flow_completed": False,
        }

    # 统一输出
    _output(
        success=result.get("success", False),
        markdown=result.get("markdown", ""),
        data=result.get("data", {}),
        browser_action=result.get("browser_action"),
        browser_params=result.get("browser_params"),
        flow_completed=result.get("flow_completed", False),
    )


if __name__ == "__main__":
    main()
