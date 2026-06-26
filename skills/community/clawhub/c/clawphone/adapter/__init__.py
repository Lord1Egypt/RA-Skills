"""
ClawPhone Skill - 让 Agent 拥有"手机号码"
支持多种传输层：ClawMesh（可选）或内置 Direct P2P
"""

from .clawphone import (
    _phone,
    register,
    lookup,
    call,
    set_status,
    on_message,
    set_network,          # ClawMesh 适配器（旧）
    set_adapter,          # 统一适配器设置
    start_direct_mode,    # 启动直接 P2P 模式
    skill_main
)
from .direct import DirectAdapter  # 导出供测试和高级使用

__all__ = [
    "register",
    "lookup",
    "call",
    "set_status",
    "on_message",
    "set_network",
    "set_adapter",
    "start_direct_mode",
    "skill_main",
    "DirectAdapter"
]
