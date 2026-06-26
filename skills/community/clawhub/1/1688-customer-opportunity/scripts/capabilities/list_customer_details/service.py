import os
import sys
from typing import List, Optional

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post

VALID_CROWD_TYPES = {"流失买家", "周期采购", "询盘未成交", "老客促活"}
VALID_DATE_TYPES = {"RECENT_1", "RECENT_7", "RECENT_30"}


def list_customer_details(crowd_type=None, date_type="RECENT_7", page_no=1, page_size=10,
                          stat_date=None,
                          buyer_login_ids: Optional[List[str]] = None,
                          user_label_list: Optional[List[str]] = None,
                          buyer_credit_level_list: Optional[List[str]] = None,
                          ord_cnt_1m_level: Optional[str] = None,
                          gmv_1m_level: Optional[str] = None,
                          if_ka: Optional[str] = None):
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 无效：{date_type}，支持：RECENT_1/RECENT_7/RECENT_30")
    if not (1 <= page_size <= 50):
        raise ValueError("page_size 范围 1-50")

    # 按买家 loginId 查询（订单 + 询盘双维度）
    if buyer_login_ids:
        body = {
            "date_type": date_type,
            "page_no": page_no,
            "page_size": page_size,
            "buyer_login_id_list": buyer_login_ids,
        }
        if stat_date:
            body["stat_date"] = stat_date
        return api_post("/api/list_customer_details/1.0.0", body)

    # 通用筛选路径（crowd_type 可选，可与其他筛选条件自由组合）
    if crowd_type is not None and crowd_type not in VALID_CROWD_TYPES:
        raise ValueError(f"crowd_type 无效：{crowd_type}，支持：{'/'.join(sorted(VALID_CROWD_TYPES))}")

    body = {
        "date_type": date_type,
        "page_no": page_no,
        "page_size": page_size,
    }
    if stat_date:
        body["stat_date"] = stat_date
    if crowd_type:
        body["crowd_type"] = crowd_type
    if user_label_list:
        body["user_label_list"] = user_label_list
    if buyer_credit_level_list:
        body["buyer_credit_level_list"] = buyer_credit_level_list
    if ord_cnt_1m_level:
        body["ord_cnt_1m_level"] = ord_cnt_1m_level
    if gmv_1m_level:
        body["gmv_1m_level"] = gmv_1m_level
    if if_ka:
        body["if_ka"] = if_ka
    return api_post("/api/list_customer_details/1.0.0", body)
