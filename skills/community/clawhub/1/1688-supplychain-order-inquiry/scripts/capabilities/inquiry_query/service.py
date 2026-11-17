# -*- coding: utf-8 -*-
"""
询盘结果查询能力实现

调用 alibaba.1688.ai.inquiry.query 接口，根据 taskId 查询询盘任务状态及商家回复。

接口入参：
  - taskId：询盘任务 ID（发起询盘时返回，必填）

原始 API 返回结构（内部解析用，不直接暴露给调用方）：
  - data.status：任务状态（SUCCESS / PENDING / FAILED / RUNNING）
  - data.questions：询盘问题列表
  - data.subTasks[]：子任务列表（每个对应一个商家）
    - .topics[].result.summary[].answer：商家回复内容
    - .receiverMainLoginId：商家登录 ID
    - .sellerReplyTime：商家回复时间戳（毫秒）
  - data.image：商品图片 URL

函数实际输出（精简后）：
  - 非终态 → {"status": "RUNNING", "message": "询盘未完成"}
  - 终态   → {"status": "SUCCESS", "summary": [{"question":"...","answer":"..."}]}
"""

import logging
import time
from typing import Dict, Any

from _http import api_post
from _errors import ServiceError, ParamError
from settings import settings

logger = logging.getLogger(__name__)


def inquiry_query(
    task_id: str,
) -> Dict[str, Any]:
    """
    查询询盘结果主函数，根据 taskId 查询询盘任务状态及商家回复。

    Args:
        task_id: 询盘任务 ID（必填，发起询盘时生成）

    Returns:
        {"result": dict, "elapsed_seconds": float}
    """
    if not task_id or not task_id.strip():
        raise ParamError("taskId 不能为空")

    body: Dict[str, Any] = {
        "taskId": task_id.strip(),
    }

    start_time = time.time()

    resp = api_post(
        path=settings.INQUIRY_QUERY_PATH,
        body=body,
        timeout=settings.TOOL_TIMEOUT,
    )

    elapsed = round(time.time() - start_time, 1)

    # 解析接口返回：实际结构为 {"data": {...}, "class": "..."}
    # _http 层已拦截 {"success": false} 的业务错误，走到这里说明请求成功
    raw_data = resp.get("data")
    if raw_data is None:
        error_msg = resp.get("msgInfo") or resp.get("message") or "未返回询盘数据"
        raise ServiceError("询盘结果查询失败: {}".format(error_msg))

    # 精简返回：展平 data 层，移除无关字段
    result = {}
    if isinstance(raw_data, dict):
        # 接口可能多包一层 data，尝试取 inner data
        inner = raw_data.get("data", raw_data) if isinstance(raw_data.get("data"), dict) else raw_data

        status = inner.get("status", "")
        result["status"] = status

        # 非终态（如 RUNNING / PENDING）只返回 status + 固定 message，不返回完整结构
        if status not in ("SUCCESS", "FAILED"):
            result["message"] = "询盘未完成"
            return {
                "result": result,
                "elapsed_seconds": elapsed,
            }

        # 终态精简：只保留 status + 所有 summary 条目（多 subTask / 多 summary 全部保留）
        summaries = []
        for st in inner.get("subTasks", []):
            for topic in st.get("topics", []):
                topic_result = topic.get("result")
                if topic_result and isinstance(topic_result.get("summary"), list):
                    summaries.extend(topic_result["summary"])
        result["summary"] = summaries

        if not summaries:
            result["message"] = "询盘已发送，商家尚未回复"

    return {
        "result": result,
        "elapsed_seconds": elapsed,
    }
