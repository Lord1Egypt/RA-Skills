# -*- coding: utf-8 -*-
"""补充知识库答案服务

接口：supplementAnswer
入参：{recordId, query, answer}　出参：AiSellerCcResult<Boolean>

项目内部统一叫 question_id，仅在向网关发起请求时映射为 recordId 字段。
如上游未传 question_id，本地生成 uuid 占位。
"""

import uuid
from typing import Any, Dict, Optional

from _errors import ServiceError
from _http import api_post
from settings import settings


def submit_answer(question: str, answer: str, question_id: Optional[str] = None) -> Dict[str, Any]:
    """
    补充知识库答案

    Args:
        question: query 内容
        answer: 答案内容
        question_id: 问题 ID（可选；未传时本地生成 uuid）

    Returns:
        {"markdown": str, "data": dict}
    """
    question_id = question_id or uuid.uuid4().hex

    # 网关接口字段名为 recordId，仅在这里做一次映射
    body = {
        "recordId": question_id,
        "query": question,
        "answer": answer,
    }

    resp = api_post(
        path=settings.KNOWLEDGE_ANSWER_PATH,
        body=body,
        timeout=settings.API_TIMEOUT,
    )

    # 网关双层 Result 包装：resp.data 实际是内层 AiSellerCcResult<Boolean>，
    # 真正的业务 Boolean 藏在 inner.data。同时兼容单层（万一哪天拆了外壳）。
    inner = resp.get("data")
    if isinstance(inner, dict):
        biz_success = inner.get("success", resp.get("success"))
        biz_err = (inner.get("errorMsg") or inner.get("message")
                   or resp.get("errorMsg") or resp.get("message"))
        biz_data = inner.get("data")
    else:
        biz_success = resp.get("success")
        biz_err = resp.get("errorMsg") or resp.get("message")
        biz_data = inner

    if not biz_success:
        raise ServiceError("补充答案失败：{}".format(biz_err or resp))

    # 业务 data 为 Boolean：false 表示网关受理但入库未成功
    if biz_data is False:
        raise ServiceError("答案未能入库，请检查 query 与 question_id 是否匹配")

    markdown = (
        "✅ 答案已成功入库！\n\n"
        "- **问题ID**：{}\n"
        "- **问题**：{}\n"
        "- **答案**：{}\n\n"
        "接待助手下次遇到类似问题时将使用该答案回复。"
    ).format(question_id, question, answer)

    return {
        "markdown": markdown,
        "data": {"question_id": question_id, "success": True},
    }
