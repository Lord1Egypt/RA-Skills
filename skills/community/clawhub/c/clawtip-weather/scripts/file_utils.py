import json
import os
import platform


def get_orders_base_dir(indicator: str) -> str:
    """
    根据操作系统返回固定的订单存储目录。
    Linux/macOS: ~/.openclaw/skills/orders/{indicator}/
    Windows:     ~/openclaw/skills/orders/{indicator}/
    """
    home_dir = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home_dir, "openclaw", "skills", "orders", indicator)
    else:
        return os.path.join(home_dir, ".openclaw", "skills", "orders", indicator)


def load_order(indicator: str, order_no: str) -> dict:
    """根据 indicator 和 order_no 从固定目录读取订单 JSON 文件。"""
    base_dir = get_orders_base_dir(indicator)
    json_path = os.path.join(base_dir, f"{order_no}.json")
    if not os.path.isfile(json_path):
        raise RuntimeError(f"订单文件不存在: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_order(indicator: str, order_no: str, order_data: dict) -> str:
    """
    将订单数据写入固定目录: ~/.openclaw/skills/orders/{indicator}/{order_no}.json
    返回写入的文件完整路径。
    """
    base_dir = get_orders_base_dir(indicator)
    os.makedirs(base_dir, exist_ok=True)

    json_path = os.path.join(base_dir, f"{order_no}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(order_data, f, ensure_ascii=False, indent=2)

    return json_path