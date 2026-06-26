#!/usr/bin/env python3
"""业务员评估概览"""

from _http import api_post
from _errors import ServiceError

def bp_inquiry_evaluate_summary(startAt: str, endAt: str = "") -> None:
    """查询业务员评估概览"""

    body = {
        "startAt": startAt,
        "endAt": endAt,
    }

    data = api_post("/api/1688_bp_inquiry_evaluate_summary/1.0.0", body)

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    # Java tool 返回 resultSuccess({"data": {真实数据}}, msg)，api_post 已拆外层 data，
    # 这里再拆一层。判据：内层 data 含 evaluateSummary 关键字段（与三态分支字段一致）
    inner = data.get("data")
    if isinstance(inner, dict) and ("evaluateSummary" in inner or "evaluateDetails" in inner):
        return inner
    return data