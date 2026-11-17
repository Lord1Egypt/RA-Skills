"""
BiliYouTik2Brain — 集成配置管理 (v4.0)

默认不集成任何外部系统，用户通过配置开启想要的集成。
不开的不干扰，保持技能独立性。
"""

import os
import json
from typing import Dict, List, Optional

_CONFIG_PATH = os.path.expanduser("~/.biliyoutik2brain/integration_config.json")


# ═══════════════════════════════════════════════════════════
#  数据模型
# ═══════════════════════════════════════════════════════════

SUPPORTED_INTEGRATIONS = {
    "memory_system": {"name": "记忆系统", "desc": "转录知识推送到 MEMORY.md / memory/"},
    "obsidian": {"name": "Obsidian", "desc": "同步到 Obsidian Vault"},
    "notion": {"name": "Notion", "desc": "同步到 Notion 数据库"},
}


def load_integration_config() -> Dict:
    """加载集成配置"""
    if not os.path.exists(_CONFIG_PATH):
        return {"integrations": {}}

    with open(_CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_integration_config(config: Dict):
    """保存集成配置"""
    os.makedirs(os.path.dirname(_CONFIG_PATH), exist_ok=True)
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def is_integration_enabled(name: str) -> bool:
    """检查某集成是否启用"""
    config = load_integration_config()
    integrations = config.get("integrations", {})
    return integrations.get(name, {}).get("enabled", False)


def enable_integration(name: str, config: Dict = None):
    """启用某集成"""
    if name not in SUPPORTED_INTEGRATIONS:
        raise ValueError(f"不支持的集成: {name}，可选: {list(SUPPORTED_INTEGRATIONS.keys())}")

    full_config = load_integration_config()
    integrations = full_config.setdefault("integrations", {})
    integrations[name] = {
        "enabled": True,
        "config": config or {},
    }
    save_integration_config(full_config)


def disable_integration(name: str):
    """禁用某集成"""
    full_config = load_integration_config()
    integrations = full_config.get("integrations", {})
    if name in integrations:
        integrations[name]["enabled"] = False
        save_integration_config(full_config)


def get_enabled_integrations() -> List[Dict]:
    """获取所有已启用的集成"""
    config = load_integration_config()
    integrations = config.get("integrations", {})

    result = []
    for name, data in integrations.items():
        if data.get("enabled"):
            result.append({
                "name": name,
                "info": SUPPORTED_INTEGRATIONS.get(name, {}),
                "config": data.get("config", {}),
            })

    return result


def get_integration_config(name: str) -> Optional[Dict]:
    """获取某集成的配置"""
    config = load_integration_config()
    integrations = config.get("integrations", {})
    if name in integrations and integrations[name].get("enabled"):
        return integrations[name].get("config", {})
    return None
