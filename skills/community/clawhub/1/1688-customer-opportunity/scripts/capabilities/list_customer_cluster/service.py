import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post


def list_customer_cluster():
    body = {"buyer_type": "old"}
    data = api_post("/api/list_customer_cluster/1.0.0", body)
    # BotTool 返回格式有两层 data，取内层（与其他 capability 保持一致）
    return data.get("data") if isinstance(data.get("data"), dict) else data
