"""
qdrant_utils.py — Qdrant 统一操作模块
所有脚本从此处获取 Qdrant 连接和操作方法。
"""

import json
from pathlib import Path

# === 连接配置（集中管理） ===
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
KB_COLLECTION = "knowledge_base"

# === 通用函数 ===


def get_collection_info(name: str = None) -> dict | None:
    """获取集合信息"""
    import requests
    name = name or KB_COLLECTION
    resp = requests.get(f"{QDRANT_URL}/collections/{name}", timeout=5)
    if resp.status_code == 200:
        return resp.json()["result"]
    return None


def search(query_vector: list, limit: int = 5, filter_dict: dict = None,
           with_payload: bool = True) -> list:
    """向量搜索"""
    import requests
    payload = {
        "vector": query_vector,
        "limit": limit,
        "with_payload": with_payload,
    }
    if filter_dict:
        payload["filter"] = filter_dict

    resp = requests.post(
        f"{QDRANT_URL}/collections/{KB_COLLECTION}/points/search",
        json=payload,
        timeout=10,
    )
    if resp.status_code == 200:
        return resp.json().get("result", [])
    return []


def scroll(filter_dict: dict = None, limit: int = 500,
           with_payload: bool = True) -> tuple:
    """滚动获取点，返回 (points, next_offset)"""
    import requests
    payload = {
        "limit": limit,
        "with_payload": with_payload,
        "with_vector": False,
    }
    if filter_dict:
        payload["filter"] = filter_dict

    resp = requests.post(
        f"{QDRANT_URL}/collections/{KB_COLLECTION}/points/scroll",
        json=payload,
        timeout=30,
    )
    if resp.status_code == 200:
        data = resp.json().get("result", {})
        return data.get("points", []), data.get("next_page_offset")
    return [], None


def scroll_all(filter_dict: dict = None, max_points: int = 3000) -> list:
    """滚动获取所有点（自动翻页）"""
    points = []
    offset = None
    while len(points) < max_points:
        payload = {
            "limit": min(500, max_points - len(points)),
            "with_payload": True,
            "with_vector": False,
        }
        if filter_dict:
            payload["filter"] = filter_dict
        if offset:
            payload["offset"] = offset

        resp = __import__("requests").post(
            f"{QDRANT_URL}/collections/{KB_COLLECTION}/points/scroll",
            json=payload, timeout=30,
        )
        if resp.status_code != 200:
            break
        data = resp.json().get("result", {})
        batch = data.get("points", [])
        points.extend(batch)
        offset = data.get("next_page_offset")
        if not batch or offset is None:
            break
    return points


def upsert_points(points: list) -> bool:
    """写入/更新点"""
    import requests
    for i in range(0, len(points), 100):
        batch = points[i:i + 100]
        resp = requests.put(
            f"{QDRANT_URL}/collections/{KB_COLLECTION}/points",
            json={"points": batch},
            timeout=30,
        )
        if resp.status_code != 200:
            return False
    return True


def update_payload(point_ids: list, payload: dict) -> bool:
    """更新点的 payload"""
    import requests
    resp = requests.post(
        f"{QDRANT_URL}/collections/{KB_COLLECTION}/points/payload",
        json={"points": point_ids, "payload": payload},
        timeout=10,
    )
    return resp.status_code == 200


def delete_points(point_ids: list) -> bool:
    """删除点"""
    import requests
    if not point_ids:
        return True
    resp = requests.post(
        f"{QDRANT_URL}/collections/{KB_COLLECTION}/points/delete",
        json={"points": point_ids},
        timeout=10,
    )
    return resp.status_code == 200


def is_available() -> bool:
    """检查 Qdrant 是否可用"""
    import requests
    try:
        resp = requests.get(f"{QDRANT_URL}/collections/{KB_COLLECTION}", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def get_point(point_id: str) -> dict | None:
    """通过 ID 获取点"""
    import requests
    resp = requests.post(
        f"{QDRANT_URL}/collections/{KB_COLLECTION}/points",
        json={"ids": [point_id], "with_payload": True, "with_vector": False},
        timeout=10,
    )
    if resp.status_code == 200:
        result = resp.json().get("result", [])
        return result[0] if result else None
    return None


def count() -> int:
    """获取集合中的点数"""
    info = get_collection_info()
    if info:
        return info.get("points_count", 0)
    return 0
