#!/usr/bin/env python
"""虚拟商品发货结果验证器 - EP-02事后验证

用法:
  python verify_delivery.py --task-id JJC-002 --order-id XY001 --link-url "https://pan.example.com/s/abc" --buyer-id user_123
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from pathlib import Path as _Path
from typing import Any
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("_lazy", source="skills/_lazy/delivery-verifier/scripts/verify_delivery.py")


def _make_verification_id(task_id: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"VR-{now}-EP02-{task_id}"


def verify_link_accessible(link_url: str) -> dict[str, Any]:
    """验证 link accessible

    Args:
        link_url (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    check = {
        "check_id": "C001",
        "dimension": "existence",
        "description": "网盘链接可访问",
        "expected": "HTTP 200",
        "actual": "",
        "status": "warning",
    }

    try:
        import httpx
        with httpx.Client(timeout=15, follow_redirects=True) as client:
            resp = client.head(link_url)
            if resp.status_code == 200:
                content_length = resp.headers.get("content-length", "unknown")
                check["actual"] = f"HTTP 200, Content-Length: {content_length}"
                check["status"] = "pass"
            else:
                check["actual"] = f"HTTP {resp.status_code}"
                check["status"] = "fail"
    except Exception as e:
        logger.error(f"verify delivery异常: {e}", exc_info=True)
        check["actual"] = f"链接访问失败，无法验证: {e}"
        check["status"] = "fail"

    return check


def verify_chat_message(buyer_id: str, link_url: str) -> dict[str, Any]:
    """验证 chat message

    Args:
        buyer_id (str): 参数说明
        link_url (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    check = {
        "check_id": "C002",
        "dimension": "completeness",
        "description": "闲鱼消息已发送",
        "expected": "消息记录中含网盘链接",
        "actual": "",
        "status": "warning",
    }

    try:
        import httpx
        agent_url = os.environ.get("XIANYU_AGENT_MCP_URL", "http://localhost:8401/mcp")

        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "get_chat_history", "arguments": {"chat_id": buyer_id, "limit": 10}},
            "id": 1,
        }

        with httpx.Client(timeout=30) as client:
            resp = client.post(agent_url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                content = data.get("result", {}).get("content", [])
                if content:
                    text = content[0].get("text", "{}")
                    result = json.loads(text) if isinstance(text, str) else text
                    messages = result.get("data", {}).get("messages", [])

                    link_found = False
                    for msg in messages:
                        msg_content = msg.get("content", "")
                        if link_url in msg_content or "提取码" in msg_content:
                            link_found = True
                            break

                    if link_found:
                        check["actual"] = f"找到含链接的消息(共{len(messages)}条)"
                        check["status"] = "pass"
                    else:
                        check["actual"] = f"未找到含链接的消息(共{len(messages)}条)"
                        check["status"] = "fail"
            else:
                check["actual"] = f"xianyu-agent-mcp返回HTTP {resp.status_code}，无法验证"
                check["status"] = "fail"
    except Exception as e:
        logger.error(f"verify delivery异常: {e}", exc_info=True)
        check["actual"] = f"xianyu-agent-mcp不可用，无法验证: {e}"
        check["status"] = "fail"

    return check


def verify_order_status(order_id: str) -> dict[str, Any]:
    """验证 order status

    Args:
        order_id (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    check = {
        "check_id": "C003",
        "dimension": "correctness",
        "description": "订单状态为已发货",
        "expected": "shipped",
        "actual": "",
        "status": "warning",
    }

    try:
        import httpx
        agent_url = os.environ.get("XIANYU_AGENT_MCP_URL", "http://localhost:8401/mcp")

        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "get_order_status", "arguments": {"order_id": order_id}},
            "id": 2,
        }

        with httpx.Client(timeout=30) as client:
            resp = client.post(agent_url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                content = data.get("result", {}).get("content", [])
                if content:
                    text = content[0].get("text", "{}")
                    result = json.loads(text) if isinstance(text, str) else text
                    status_val = result.get("data", {}).get("status", "unknown")

                    check["actual"] = status_val
                    if status_val in ("shipped", "completed"):
                        check["status"] = "pass"
                    elif status_val == "pending_shipment":
                        check["status"] = "fail"
                    else:
                        check["status"] = "fail"
            else:
                check["actual"] = f"xianyu-agent-mcp返回HTTP {resp.status_code}，无法验证"
                check["status"] = "fail"
    except Exception as e:
        logger.error(f"verify delivery异常: {e}", exc_info=True)
        check["actual"] = f"xianyu-agent-mcp不可用，无法验证: {e}"
        check["status"] = "fail"

    return check


def verify_ai_declaration(buyer_id: str, product_type: str) -> dict[str, Any]:
    """验证 ai declaration

    Args:
        buyer_id (str): 参数说明
        product_type (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    check = {
        "check_id": "C004",
        "dimension": "compliance",
        "description": "AI生成声明(算命类商品)",
        "expected": "消息中含AI生成声明",
        "actual": "",
        "status": "warning",
    }
    fortune_types = {"bazi", "ziwei", "tarot", "meihua", "liuyao", "qimen", "astrology", "almanac", "fortune"}
    if product_type not in fortune_types:
        check["actual"] = f"非算命类商品({product_type}),无需AI声明"
        check["status"] = "pass"
        return check
    try:
        import httpx
        agent_url = os.environ.get("XIANYU_AGENT_MCP_URL", "http://localhost:8401/mcp")
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "get_chat_history", "arguments": {"chat_id": buyer_id, "limit": 20}},
            "id": 3,
        }
        with httpx.Client(timeout=30) as client:
            resp = client.post(agent_url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                content = data.get("result", {}).get("content", [])
                if content:
                    text = content[0].get("text", "{}")
                    result = json.loads(text) if isinstance(text, str) else text
                    messages = result.get("data", {}).get("messages", [])
                    all_text = " ".join(m.get("content", "") for m in messages)
                    if "AI辅助生成" in all_text or "AI生成" in all_text:
                        check["actual"] = "消息中包含AI生成声明"
                        check["status"] = "pass"
                    else:
                        check["actual"] = "消息中未找到AI生成声明(算命类商品必须声明)"
                        check["status"] = "fail"
            else:
                check["actual"] = f"xianyu-agent-mcp返回HTTP {resp.status_code}"
                check["status"] = "fail"
    except Exception as e:
        logger.error(f"verify delivery异常: {e}", exc_info=True)
        check["actual"] = f"无法验证AI声明: {e}"
        check["status"] = "warning"
    return check


def main() -> Any:
    """main

    Returns:
        Any: 返回值说明
    """
    parser = argparse.ArgumentParser(description="虚拟商品发货结果验证器")
    parser.add_argument("--task-id", required=True, help="任务ID")
    parser.add_argument("--order-id", required=True, help="订单ID")
    parser.add_argument("--link-url", required=True, help="网盘链接URL")
    parser.add_argument("--buyer-id", default="", help="买家ID")
    parser.add_argument("--product-type", default="", help="商品类型(算命类需检查AI声明)")
    parser.add_argument("--output", default=None, help="输出文件路径")

    args = parser.parse_args()

    checks = []

    checks.append(verify_link_accessible(args.link_url))

    if args.buyer_id:
        checks.append(verify_chat_message(args.buyer_id, args.link_url))
    else:
        checks.append({
            "check_id": "C002",
            "dimension": "completeness",
            "description": "闲鱼消息已发送",
            "expected": "消息记录中含网盘链接",
            "actual": "未提供buyer_id，无法验证",
            "status": "fail",
        })

    checks.append(verify_order_status(args.order_id))

    if args.buyer_id and args.product_type:
        checks.append(verify_ai_declaration(args.buyer_id, args.product_type))

    pass_count = sum(1 for c in checks if c["status"] == "pass")
    fail_count = sum(1 for c in checks if c["status"] == "fail")
    warning_count = sum(1 for c in checks if c["status"] == "warning")

    if fail_count > 0:
        status = "fail"
    elif warning_count > 0:
        status = "warning"
    else:
        status = "pass"

    report = {
        "success": fail_count == 0,
        "data": {
            "verification_id": _make_verification_id(args.task_id),
            "flow_id": "EP-02",
            "verification_type": "post_execution",
            "verifier": "menxia",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": {
                "skill": "auto-delivery",
                "action": "deliver_virtual_goods",
                "input_summary": f"发货订单{args.order_id}",
            },
            "result": {
                "status": status,
                "checks": checks,
                "pass_count": pass_count,
                "fail_count": fail_count,
                "warning_count": warning_count,
            },
            "evidence": {
                "method": "alist-mcp + xianyu-agent-mcp get_chat_history + get_order_status",
                "raw_response": None,
                "screenshot_path": None,
            },
            "recommendation": None,
        },
        "error": None,
        "code": None,
    }

    output = json.dumps(report, ensure_ascii=False, indent=2)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"验证报告已写入: {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0 if report["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
