import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post


def get_cluster_marketing_plan(plan_id):
    if not plan_id:
        raise ValueError("plan_id 不能为空")
    data = api_post("/api/get_cluster_marketing_plan/1.0.0", {"plan_id": plan_id})
    return data.get("data") if isinstance(data.get("data"), dict) else data
