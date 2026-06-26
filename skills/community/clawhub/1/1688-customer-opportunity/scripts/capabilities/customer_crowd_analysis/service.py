import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post
from _errors import SkillError

VALID_CROWD_TYPES = {"流失买家", "周期采购", "询盘未成交", "老客促活"}
MAX_WORKERS = 5


def customer_crowd_analysis(crowd_type, buyer_login_id, ds=None):
    if crowd_type not in VALID_CROWD_TYPES:
        raise ValueError(f"crowd_type 无效：{crowd_type}，支持：{'/'.join(sorted(VALID_CROWD_TYPES))}")
    if not buyer_login_id:
        raise ValueError("buyer_login_id 不能为空")

    body = {
        "crowd_type": crowd_type,
        "buyer_login_id": buyer_login_id,
    }
    if ds:
        body["ds"] = ds
    return api_post("/api/customer_crowd_analysis/1.0.0", body)


def _process_one(crowd_type, login_id, ds):
    try:
        data = customer_crowd_analysis(crowd_type=crowd_type, buyer_login_id=login_id, ds=ds)
        return {"input": {"login_id": login_id}, "label": login_id, "status": "OK", "data": data}
    except (SkillError, Exception) as e:
        return {"input": {"login_id": login_id}, "label": login_id, "status": "FAILED", "reason": str(e)}


def batch_customer_crowd_analysis(crowd_type, buyer_login_ids: list, ds=None) -> dict:
    if crowd_type not in VALID_CROWD_TYPES:
        raise ValueError(f"crowd_type 无效：{crowd_type}，支持：{'/'.join(sorted(VALID_CROWD_TYPES))}")
    if not buyer_login_ids:
        raise ValueError("buyer_login_ids 列表不能为空")

    results = [None] * len(buyer_login_ids)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(_process_one, crowd_type, lid, ds): i
                   for i, lid in enumerate(buyer_login_ids)}
        for future in as_completed(futures):
            idx = futures[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                results[idx] = {"input": {"login_id": buyer_login_ids[idx]},
                                "label": buyer_login_ids[idx], "status": "FAILED", "reason": str(e)}

    success = sum(1 for r in results if r and r.get("status") == "OK")
    failed = len(results) - success
    return {
        "crowd_type": crowd_type,
        "total": len(buyer_login_ids),
        "success": success,
        "failed": failed,
        "results": results,
    }
