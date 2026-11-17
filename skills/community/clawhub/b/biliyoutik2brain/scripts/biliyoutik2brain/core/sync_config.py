"""
BiliYouTik2Brain — 分层同步配置 (v4.0)

核心数据（转录/知识）自动同步，辅助数据（截图/缓存）默认本地可选同步。
支持多种同步目标，用户配置一次自动执行。
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════
#  配置模型
# ═══════════════════════════════════════════════════════════

_CONFIG_PATH = os.path.expanduser("~/.biliyoutik2brain/sync_config.json")


@dataclass
class SyncTarget:
    """一个同步目标"""
    name: str               # github / gitlab / nas / notion / obsidian
    enabled: bool = False
    config: Dict = field(default_factory=dict)
    auto_sync: bool = True  # 是否自动同步
    frequency: str = "on_save"  # on_save / hourly / daily
    filters: Dict = field(default_factory=dict)  # 过滤规则


@dataclass
class SyncConfig:
    """完整同步配置"""
    # 核心数据同步（自动开启）
    core_sync: SyncTarget = field(default_factory=lambda: SyncTarget(name="core", enabled=True))

    # 辅助数据同步（默认关闭）
    auxiliary_sync: List[SyncTarget] = field(default_factory=list)

    # 分层同步规则
    layers: Dict = field(default_factory=lambda: {
        "transcripts": {"sync": True, "targets": ["core"]},    # 转录 → 核心
        "knowledge": {"sync": True, "targets": ["core"]},      # 知识 → 核心
        "comments": {"sync": True, "targets": ["core"]},       # 评论 → 核心
        "screenshots": {"sync": False, "targets": []},         # 截图 → 默认不同步
        "cache": {"sync": False, "targets": []},               # 缓存 → 默认不同步
    })


# ═══════════════════════════════════════════════════════════
#  加载/保存
# ═══════════════════════════════════════════════════════════

def load_config() -> SyncConfig:
    """加载同步配置"""
    if not os.path.exists(_CONFIG_PATH):
        return SyncConfig()

    with open(_CONFIG_PATH, encoding="utf-8") as f:
        data = json.load(f)

    return SyncConfig(**data)


def save_config(config: SyncConfig):
    """保存同步配置"""
    os.makedirs(os.path.dirname(_CONFIG_PATH), exist_ok=True)
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "core_sync": config.core_sync.__dict__ if hasattr(config.core_sync, '__dict__') else config.core_sync,
            "auxiliary_sync": [s.__dict__ if hasattr(s, '__dict__') else s for s in config.auxiliary_sync],
            "layers": config.layers,
        }, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
#  同步管理
# ═══════════════════════════════════════════════════════════

def should_sync(data_type: str, config: Optional[SyncConfig] = None) -> bool:
    """判断某类数据是否需要同步"""
    if config is None:
        config = load_config()

    layer = config.layers.get(data_type, {})
    return layer.get("sync", False)


def get_sync_targets(data_type: str, config: Optional[SyncConfig] = None) -> List[str]:
    """获取某类数据的同步目标"""
    if config is None:
        config = load_config()

    layer = config.layers.get(data_type, {})
    return layer.get("targets", [])


def configure_target(
    target_name: str,
    enabled: bool = True,
    auto_sync: bool = True,
    config: Dict = None,
    frequency: str = "on_save",
):
    """配置一个同步目标"""
    sync_config = load_config()

    # 查找现有目标
    existing = [s for s in sync_config.auxiliary_sync if s.name == target_name]
    if existing:
        existing[0].enabled = enabled
        existing[0].auto_sync = auto_sync
        existing[0].frequency = frequency
        if config:
            existing[0].config.update(config)
    else:
        sync_config.auxiliary_sync.append(SyncTarget(
            name=target_name,
            enabled=enabled,
            auto_sync=auto_sync,
            config=config or {},
            frequency=frequency,
        ))

    save_config(sync_config)


# ═══════════════════════════════════════════════════════════
#  执行同步
# ═══════════════════════════════════════════════════════════

def execute_sync(data_type: str, files: List[Dict]) -> Dict:
    """执行同步

    Args:
        data_type: 数据类型（transcripts / knowledge / comments / screenshots）
        files: [{path, content}]

    Returns:
        {success: bool, targets: [{name, synced, failed}]}
    """
    config = load_config()
    if not should_sync(data_type, config):
        return {"success": True, "targets": [], "skipped": True}

    targets = get_sync_targets(data_type, config)
    results = []

    for target_name in targets:
        try:
            adapter = _get_adapter(target_name)
            if not adapter or not adapter.is_configured():
                results.append({"name": target_name, "synced": 0, "failed": len(files), "error": "未配置"})
                continue

            target_config = _get_target_config(target_name, config)
            result = adapter.sync(files, target_config)
            results.append({"name": target_name, **result})
        except Exception as e:
            results.append({"name": target_name, "synced": 0, "failed": len(files), "error": str(e)})

    return {
        "success": all(r.get("synced", 0) > r.get("failed", 0) for r in results),
        "targets": results,
    }


def _get_adapter(name: str):
    """获取同步适配器"""
    try:
        if name == "github":
            from sync_adapters.github_sync import GitHubSync
            return GitHubSync()
        # TODO: 其他适配器
        return None
    except ImportError:
        return None


def _get_target_config(name: str, config: SyncConfig) -> Dict:
    """获取目标配置"""
    for target in config.auxiliary_sync:
        if target.name == name:
            return target.config
    return {}
