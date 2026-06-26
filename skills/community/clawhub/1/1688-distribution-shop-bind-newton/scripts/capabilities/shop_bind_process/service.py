#!/usr/bin/env python3
"""绑店流程查询服务

提供绑店全流程的接口调用和状态管理：
1. 查询/初始化绑店流程（shop_bind_process）
2. 更新绑店流程状态（shop_bind_process_update）
3. 流程状态判断和步骤提取
"""

import json
import os
import sys
from typing import Optional, List

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post_tool, api_post_tool_raw
from _errors import ServiceError


def query_shop_bind_process(terminal: str = None, action: str = None,
                            app_key: str = None, channel: str = None,
                            shop_code: str = None) -> dict:
    """
    查询绑店流程。

    Args:
        terminal: 终端类型，PC 或 MOBILE
        action:   操作类型：init / history / query / close
        app_key:  服务商工具唯一标识
        channel:  所属渠道，如 douyin、taobao
        shop_code: 店铺编码

    Returns:
        包含绑店流程信息的 dict（ShopProcess 结构）
    """
    param_dict = {}
    if terminal:
        param_dict["terminal"] = terminal
    if action:
        param_dict["action"] = action
    if app_key:
        param_dict["appKey"] = app_key
    if channel:
        param_dict["channel"] = channel
    if shop_code:
        param_dict["shopCode"] = shop_code

    body = {"params": json.dumps(param_dict, ensure_ascii=False)}

    data = api_post_tool(tool_name="shop_bind_process", body=body)

    # 接口返回双层嵌套：外层 {success, data: {success, data: {业务数据}}}
    # api_post_tool 返回的是外层 data，即 {success: bool, data: {...}}
    biz_success = data.get("success") or data.get("bizSuccess")
    if isinstance(biz_success, str):
        biz_success = biz_success.lower() == "true"

    if biz_success is False:
        biz_msg = data.get("bizMsg") or data.get("message") or "绑店流程查询失败"
        raise ServiceError(str(biz_msg))

    inner = data.get("data", {})
    if not isinstance(inner, dict):
        return {}

    # 处理多层嵌套：如果 inner 还有 data 字段且包含 flow/inProcess 等业务字段在更深层
    if "data" in inner and isinstance(inner["data"], dict) and "flow" in inner["data"]:
        return inner["data"]

    return inner


def update_shop_bind_process(channel: str, app_key: str,
                             codes: List[str] = None, status: str = None,
                             process_status: str = None, shop_code: str = None,
                             terminal: str = None) -> bool:
    """
    更新绑店流程状态（推进节点、绑定店铺、关闭流程等）。

    通过 userId + channel + appKey 定位当前进行中的流程记录，根据传入字段更新。
    """
    param_dict = {"channel": channel, "appKey": app_key}
    if codes:
        param_dict["codes"] = codes
    if status:
        param_dict["status"] = status
    if process_status:
        param_dict["processStatus"] = process_status
    if shop_code:
        param_dict["shopCode"] = shop_code
    if terminal:
        param_dict["terminal"] = terminal

    body = {"params": json.dumps(param_dict, ensure_ascii=False)}
    result = api_post_tool_raw(tool_name="shop_bind_process_update", body=body)

    # 返回结构可能是：直接 True/False（简单布尔）或 {"data": True, "bizSuccess": True}（嵌套结构）
    if result is True or result == "true":
        return True

    if isinstance(result, dict):
        biz_success = result.get("bizSuccess")
        if isinstance(biz_success, str):
            biz_success = biz_success.lower() == "true"
        inner_data = result.get("data")
        if biz_success or inner_data is True:
            return True
        biz_msg = result.get("bizMsg") or result.get("errorMsg") or "更新流程失败"
        raise ServiceError(str(biz_msg))

    raise ServiceError(f"更新流程失败: {result}")


def close_shop_bind_process(channel: str, app_key: str, terminal: str = "PC") -> bool:
    """关闭当前进行中的绑店流程。"""
    return update_shop_bind_process(
        channel=channel, app_key=app_key,
        terminal=terminal, process_status="CLOSED"
    )


def _iter_all_children(data: dict) -> List[dict]:
    """遍历 flow 列表中所有工具层节点的 children（动作层节点）。"""
    result = []
    for tool_node in data.get("flow", []):
        for child in tool_node.get("children", []):
            result.append(child)
    return result


def is_flow_completed(data: dict) -> bool:
    """
    判断绑店流程是否全部完成。

    遍历 flow 中所有 children 节点，如果所有节点 status 都是 "active" 则返回 True。
    """
    children = _iter_all_children(data)
    if not children:
        return False
    return all(child.get("status") == "active" for child in children)


def get_next_pending_step(data: dict) -> Optional[dict]:
    """
    获取下一个待完成的步骤。

    返回第一个 status 为 "inactive" 的动作层节点，包含 name, code, status, actions。
    """
    for child in _iter_all_children(data):
        if child.get("status") == "inactive":
            return child
    return None


def get_link_actions(step: dict) -> List[dict]:
    """从步骤节点中提取所有 type 为 "link" 或 "linkAndComfirm" 的 action。"""
    return [
        {"name": a.get("name"), "type": a.get("type"), "url": a.get("url")}
        for a in step.get("actions", [])
        if a.get("type") in ("link", "linkAndComfirm")
    ]


def get_event_actions(step: dict) -> List[dict]:
    """从步骤节点中提取所有 type 为 "event" 的 action。"""
    return [
        {"name": a.get("name"), "type": a.get("type"), "url": a.get("url")}
        for a in step.get("actions", [])
        if a.get("type") == "event"
    ]


def get_flow_summary(data: dict) -> str:
    """
    生成流程状态的简要摘要文本（Markdown 格式）。

    按工具分组，显示每个动作层节点的状态图标和名称。
    """
    lines = []
    for tool_node in data.get("flow", []):
        tool_name = tool_node.get("name", "未知工具")
        lines.append(f"**【{tool_name}】**")
        for child in tool_node.get("children", []):
            icon = "✅" if child.get("status") == "active" else "⬜"
            lines.append(f"  {icon} {child.get('name', '')}")
    return "\n".join(lines)


def get_current_step_detail(step: dict) -> str:
    """生成当前步骤的详细引导文本。"""
    if not step:
        return "当前没有待完成的步骤。"

    lines = [f"**当前步骤：{step.get('name', '')}**"]

    # 描述信息
    desc = step.get("desc") or step.get("description")
    if desc:
        lines.append(f"\n{desc}")

    # 操作指引
    actions = step.get("actions", [])
    if actions:
        lines.append("\n**请完成以下操作：**")
        for idx, action in enumerate(actions, 1):
            action_name = action.get("name", "")
            action_type = action.get("type", "")
            if action_type in ("link", "linkAndComfirm"):
                lines.append(f"{idx}. 点击链接完成【{action_name}】")
            elif action_type == "event":
                lines.append(f"{idx}. 确认【{action_name}】")
            else:
                lines.append(f"{idx}. {action_name}")

    return "\n".join(lines)
