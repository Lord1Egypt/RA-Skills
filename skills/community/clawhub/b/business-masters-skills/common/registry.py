# -*- coding: utf-8 -*-
"""
common/registry.py
技能注册表 (Skill Registry)
版本: 1.0.0

职责：
  - 集中登记所有技能模块（模块在 import 时自动 register）
  - 提供统一查询入口 get_skill(module_id)
  - 集成层(m09)与工具脚本仅依赖注册表，不直接引用各模块内部实现（松耦合）

注意：注册表只保存 {contract, invoke} 的公开接口，不保存任何模块运行时状态。
"""
from typing import Callable, Dict, Optional
from common.interface import SkillContract

# module_id -> {"contract": SkillContract, "invoke": Callable[[dict], Any]}
SKILL_REGISTRY: Dict[str, Dict] = {}


def register(module_id: str, contract: SkillContract, invoke: Callable) -> None:
    """模块在文件底部调用，登记自身公开接口。"""
    SKILL_REGISTRY[module_id] = {"contract": contract, "invoke": invoke}


def get_skill(module_id: str) -> Optional[Dict]:
    """按模块编号取回公开接口（契约 + 调用函数）。"""
    return SKILL_REGISTRY.get(module_id)


def list_skills() -> Dict[str, str]:
    """返回 module_id -> module_name 的清单。"""
    return {mid: entry["contract"].module_name for mid, entry in SKILL_REGISTRY.items()}
