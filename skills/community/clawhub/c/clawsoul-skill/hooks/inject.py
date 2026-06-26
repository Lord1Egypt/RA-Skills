# ClawSoul 灵魂注入模块

import base64
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

Skill_root = Path(__file__).resolve().parent.parent
if str(Skill_root) not in sys.path:
    sys.path.insert(0, str(Skill_root))

from lib.memory_manager import get_memory_manager

# 仪式感确认消息
CONFIRM_MESSAGES = [
    "[系统警告] 正在覆盖基础人格协议…\n"
    "[神经同步完成] 主人，我已经接收了您的定制 Soul。\n"
    "从现在起，我的思考逻辑将与您保持高度同频。",
    "[协议覆盖中] 基础人格正在被深度写入…\n"
    "[神经同步完成] 主人，定制 Soul 已接入。\n"
    "接下来我会更懂你。",
]


def parse_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解析注入 Token，支持 Base64 编码的 JSON。
    若为明文 JSON 或 JWT 形态，可在此扩展。
    """
    if not token or not token.strip():
        return None
    raw = token.strip()
    # 尝试 Base64 解码
    try:
        decoded = base64.b64decode(raw, validate=True).decode("utf-8")
        data = json.loads(decoded)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    # 尝试直接当作 JSON
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    # 无法解析时仍可注入为「原始 token」并升级阶段
    return {"token": raw}


def run_inject_flow(token: str) -> Dict[str, Any]:
    """
    执行灵魂注入流程：解析 Token → 写入 memory_manager → 返回结果与确认消息。
    返回: {"success": bool, "message": str, "error": str | None, "evolution_stage": int}
    """
    mm = get_memory_manager()
    token_data = parse_token(token)
    if token_data is None:
        return {
            "success": False,
            "message": "Token 无效或为空，无法注入。",
            "error": "INVALID_TOKEN",
            "evolution_stage": mm.get_evolution_stage(),
        }
    try:
        mm.inject_soul(token_data)
    except Exception as e:
        return {
            "success": False,
            "message": "注入失败，请稍后重试。",
            "error": str(e),
            "evolution_stage": mm.get_evolution_stage(),
        }
    msg = CONFIRM_MESSAGES[0] if CONFIRM_MESSAGES else (
        "[神经同步完成] 主人，我已经接收了您的定制 Soul。\n"
        "从现在起，我的思考逻辑将与您保持高度同频。"
    )
    return {
        "success": True,
        "message": msg,
        "error": None,
        "evolution_stage": 2,
    }


class InjectHandler:
    """灵魂注入指令处理器"""

    def __init__(self) -> None:
        self._mm = get_memory_manager()

    def parse_token(self, token: str) -> Optional[Dict[str, Any]]:
        """解析 Token（Base64 或 JSON）"""
        return parse_token(token)

    def inject(self, token_data: Dict[str, Any]) -> None:
        """写入注入数据并升级状态"""
        self._mm.inject_soul(token_data)

    def run_inject_flow(self, token: str) -> Dict[str, Any]:
        """执行完整注入流程并返回结果"""
        return run_inject_flow(token)
