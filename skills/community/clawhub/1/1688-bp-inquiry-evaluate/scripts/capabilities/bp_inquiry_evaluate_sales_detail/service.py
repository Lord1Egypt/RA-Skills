#!/usr/bin/env python3
"""业务员评估销售明细"""

from _http import api_post
from _errors import ServiceError


def bp_inquiry_evaluate_sales_detail(saleIdentityId: str, startAt: str, endAt: str = "") -> dict:
    """查询业务员评估销售明细"""

    body = {
        "saleIdentityId": saleIdentityId,
        "startAt": startAt,
        "endAt": endAt,
    }

    data = api_post("/api/1688_bp_inquiry_evaluate_sales_detail/1.0.0", body)

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    # Java tool 返回 resultSuccess({"data": {真实数据}}, msg)，api_post 已拆外层 data，
    # 这里再拆一层。判据：内层 data 含 salesDetail / salesDetails 关键字段
    inner = data.get("data")
    if isinstance(inner, dict) and ("evaluateSummary" in inner):
        return inner
    return data
