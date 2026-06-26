"""
Config Manager - 读取和写入预算配置文件
负责: config.json, budget_YYYYMM.json, pools.json
"""
import os, json
from pathlib import Path

DATA_DIR = Path("~/Documents/02_Personal/01_Budget").expanduser()
CONFIG_DIR = DATA_DIR / "config"
DATA_DIR_DATA = DATA_DIR / "data"

def _read_json(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None

def _write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_config():
    """读取全局配置 (budget_rules, reminder_day, timezone)"""
    path = CONFIG_DIR / "config.json"
    data = _read_json(path)
    return data if data else {
        "reminder_day": 16,
        "timezone": "Asia/Shanghai",
        "budget_rules": {"weekday": 100, "weekend": 200},
        "dynamic_budget": {"enabled": True}
    }

def get_budget(month=None):
    """
    读取月度预算数据
    month: YYYY-MM 格式，如 None 则取当前月份
    """
    if month is None:
        import datetime
        month = datetime.datetime.now().strftime("%Y-%m")
    m = month.replace("-", "")
    path = DATA_DIR_DATA / f"budget_{m}.json"
    data = _read_json(path)
    return data if data else None

def set_budget(month, total, pools=None, daily_budget=100, weekly_budget=750, note=""):
    """
    设置月度预算
    month: YYYY-MM
    total: 总预算金额
    pools: dict, 各池子预算分配，如 {"food": 1320, "transport": 330, "fun": 550, "save": 1100}
    """
    m = month.replace("-", "")
    path = DATA_DIR_DATA / f"budget_{m}.json"
    data = {
        "month": month,
        "total": total,
        "pools": pools or {},
        "daily_budget": daily_budget,
        "weekly_budget": weekly_budget,
        "note": note
    }
    _write_json(path, data)
    return data

def get_pools():
    """读取预算池配置"""
    path = CONFIG_DIR / "pools.json"
    return _read_json(path) or {}

def set_pools(pools):
    """写入预算池配置"""
    path = CONFIG_DIR / "pools.json"
    _write_json(path, pools)
    return pools
