#!/usr/bin/env python3
"""
统一配置管理
所有配置存放在全局目录 ~/.archery/，跨项目共享

配置文件位置:
- ~/.archery/config.json - 凭证配置（用户名/密码/URL）
- ~/.archery/cache/instances.json - 实例别名配置
- ~/.archery/cache/table_cache.json - 表列表缓存
- ~/.archery/cache/session.json - Session 缓存
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

# 全局配置目录（唯一位置）
GLOBAL_CONFIG_DIR = Path.home() / ".archery" / "cache"
GLOBAL_INSTANCES_FILE = GLOBAL_CONFIG_DIR / "instances.json"
GLOBAL_TABLE_CACHE_FILE = GLOBAL_CONFIG_DIR / "table_cache.json"

# 默认配置
DEFAULT_CONFIG = {}


def ensure_cache_dir():
    """确保缓存目录存在"""
    GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_instances() -> dict:
    """加载实例配置"""
    ensure_cache_dir()

    if GLOBAL_INSTANCES_FILE.exists():
        with open(GLOBAL_INSTANCES_FILE) as f:
            return json.load(f)

    # 第一次使用，创建默认配置
    save_instances(DEFAULT_CONFIG)
    return DEFAULT_CONFIG


def save_instances(config: dict):
    """保存实例配置"""
    ensure_cache_dir()
    with open(GLOBAL_INSTANCES_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_instance(alias: str) -> tuple:
    """根据别名获取实例和数据库"""
    config = load_instances()
    if alias in config:
        instance_data = config[alias]
        # 支持两种格式：[instance, db] 或 {"instance": ..., "db": ...}
        if isinstance(instance_data, list):
            return tuple(instance_data)
        elif isinstance(instance_data, dict):
            return (instance_data.get("instance"), instance_data.get("db"))
    return (alias, "your-database")


def get_aliases() -> list:
    """获取所有别名列表"""
    return list(load_instances().keys())


def add_instance(alias: str, instance_name: str, database: str):
    """添加实例到配置"""
    config = load_instances()
    config[alias] = [instance_name, database]
    save_instances(config)
    print(f"✅ 已添加实例: {alias} → {instance_name} / {database}")
    return config


def remove_instance(alias: str):
    """删除实例配置"""
    config = load_instances()
    if alias in config:
        del config[alias]
        save_instances(config)
        print(f"✅ 已删除实例: {alias}")
    else:
        print(f"⚠️  别名 '{alias}' 不存在")


def list_instances():
    """列出所有实例配置"""
    config = load_instances()
    print("\n缓存的实例别名:\n")
    print(f"{'别名':<15} {'实例名':<30} {'数据库':<20}")
    print("-" * 65)
    for alias, data in config.items():
        if isinstance(data, list):
            instance, db = data[0], data[1]
        else:
            instance, db = data.get("instance"), data.get("db")
        print(f"{alias:<15} {instance:<30} {db:<20}")


def init_cache():
    """初始化缓存（命令行调用）"""
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "list":
            list_instances()
        elif cmd == "add" and len(sys.argv) == 4:
            add_instance(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "your-database")
        elif cmd == "remove" and len(sys.argv) == 3:
            remove_instance(sys.argv[2])
        elif cmd == "init":
            save_instances(DEFAULT_CONFIG)
            print("✅ 已初始化实例缓存")
            list_instances()
        else:
            print("用法:")
            print("  python3 cache_config.py init")
            print("  python3 cache_config.py list")
            print("  python3 cache_config.py add <别名> <实例名> [数据库]")
            print("  python3 cache_config.py remove <别名>")
    else:
        # 默认：初始化并显示
        config = load_instances()
        print("✅ 已加载实例缓存")
        list_instances()


# 导出常用实例（供其他脚本直接使用）
INSTANCES = load_instances()


# ========================================
# 表缓存操作
# ========================================

def load_table_cache() -> Dict[str, Any]:
    """加载表缓存"""
    ensure_cache_dir()

    if GLOBAL_TABLE_CACHE_FILE.exists():
        with open(GLOBAL_TABLE_CACHE_FILE) as f:
            return json.load(f)

    return {}


def save_table_cache(cache: Dict[str, Any]):
    """保存表缓存"""
    ensure_cache_dir()
    with open(GLOBAL_TABLE_CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def get_tables_from_cache(instance: str, database: str) -> Optional[List[str]]:
    """从缓存获取表列表"""
    cache = load_table_cache()
    cache_key = f"{instance}:{database}"
    return cache.get(cache_key)


def save_tables_to_cache(instance: str, database: str, tables: List[str]):
    """保存表列表到缓存"""
    cache = load_table_cache()
    cache_key = f"{instance}:{database}"
    cache[cache_key] = tables
    save_table_cache(cache)


def clear_table_cache(instance: str = None, database: str = None):
    """清除表缓存

    Args:
        instance: 实例名，为空则清除所有
        database: 数据库名
    """
    if instance and database:
        cache = load_table_cache()
        cache_key = f"{instance}:{database}"
        if cache_key in cache:
            del cache[cache_key]
            save_table_cache(cache)
            print(f"✅ 已清除缓存: {cache_key}")
    elif instance:
        cache = load_table_cache()
        keys_to_delete = [k for k in cache if k.startswith(f"{instance}:")]
        for key in keys_to_delete:
            del cache[key]
        save_table_cache(cache)
        print(f"✅ 已清除 {len(keys_to_delete)} 个缓存项")
    else:
        if GLOBAL_TABLE_CACHE_FILE.exists():
            GLOBAL_TABLE_CACHE_FILE.unlink()
            print("✅ 已清除所有表缓存")


if __name__ == "__main__":
    init_cache()
