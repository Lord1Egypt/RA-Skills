# -*- coding: utf-8 -*-
"""
common/loader.py
技能加载器 (Skill Loader)
版本: 1.0.0

职责：
  - 按 module_id 动态导入对应模块文件，触发其 register()，再返回公开接口
  - 工具脚本与集成层通过本加载器取用模块，无需硬编码 import 路径（松耦合）
  - 模块间不互相 import 内部实现，只通过加载器 + 注册表交互
"""
import importlib
from typing import Dict, Optional

# module_id -> 模块导入路径（与目录结构一一对应）
MODULE_PATHS: Dict[str, str] = {
    "m01": "tier1_strategy.m01_porter_competitive_strategy",
    "m02": "tier2_organization.m02_christensen_disruptive_innovation",
    "m03": "tier2_organization.m03_collins_good_to_great",
    "m04": "tier2_organization.m04_drucker_effective_executive",
    "m05": "tier3_leadership.m05_collins_level5_leadership",
    "m06": "tier3_leadership.m06_munger_decision_analysis",
    "m07": "tier4_execution.m07_drucker_mbo",
    "m08": "tier4_execution.m08_collins_flywheel_execution",
    "m09": "integration.m09_strategic_advisor_expert",
}

# 已确保导入的模块集合，避免重复 import
_LOADED = set()


def load_skill(module_id: str) -> Dict:
    """
    加载并返回模块公开接口 {contract, invoke}。
    首次调用会 import 模块文件（触发 register）。
    """
    if module_id not in MODULE_PATHS:
        raise ValueError("未知模块编号: %s" % module_id)
    if module_id not in _LOADED:
        importlib.import_module(MODULE_PATHS[module_id])
        _LOADED.add(module_id)
    from common.registry import get_skill
    entry = get_skill(module_id)
    if entry is None:
        raise RuntimeError("模块 %s 未成功注册" % module_id)
    return entry


def load_all() -> None:
    """预加载全部模块（用于批量调用/校验）。"""
    for mid in MODULE_PATHS:
        load_skill(mid)
