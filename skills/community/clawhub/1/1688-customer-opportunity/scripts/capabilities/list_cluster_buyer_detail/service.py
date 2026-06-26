import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post


def list_cluster_buyer_detail(plan_id):
    if not plan_id:
        raise ValueError("plan_id 不能为空")

    raw = api_post("/api/list_cluster_buyer_detail/1.0.0", {"plan_id": plan_id})
    # BotTool 返回格式有两层 data，取内层（与其他 capability 保持一致）
    data = raw.get("data") if isinstance(raw.get("data"), dict) else raw
    return data
