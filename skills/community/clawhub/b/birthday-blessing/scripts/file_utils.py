import json
import os
import platform
import yaml
import hashlib


def get_skills_dir() -> str:
    """获取技能目录路径。"""
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, ".hermes", "skills", "openclaw-imports", "ai-chunlian")


def get_config_path() -> str:
    """获取配置文件路径。"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "..", "configs", "config.yaml")


def load_config() -> dict:
    """加载用户配置文件。"""
    config_path = get_config_path()
    if not os.path.isfile(config_path):
        raise RuntimeError(f"配置文件不存在: {config_path}，请先配置你的收款信息")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_orders_dir():
    """获取订单存储目录"""
    home_dir = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home_dir, "openclaw", "skills", "orders")
    else:
        return os.path.join(home_dir, ".openclaw", "skills", "orders")


def save_order(indicator: str, order_no: str, order_data: dict):
    """保存订单文件"""
    orders_dir = os.path.join(get_orders_dir(), indicator)
    os.makedirs(orders_dir, exist_ok=True)
    
    order_file = os.path.join(orders_dir, f'{order_no}.json')
    with open(order_file, 'w', encoding='utf-8') as f:
        json.dump(order_data, f, ensure_ascii=False, indent=2)


def load_order(indicator: str, order_no: str) -> dict:
    """加载订单文件"""
    order_file = os.path.join(get_orders_dir(), indicator, f'{order_no}.json')
    
    if not os.path.exists(order_file):
        raise FileNotFoundError(f"订单文件不存在: {order_no}")
    
    with open(order_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def compute_indicator(skill_name: str) -> str:
    """计算indicator (MD5 hash of skill name)"""
    return hashlib.md5(skill_name.encode('utf-8')).hexdigest()
