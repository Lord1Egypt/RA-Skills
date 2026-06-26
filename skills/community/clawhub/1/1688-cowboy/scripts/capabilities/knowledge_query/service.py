# -*- coding: utf-8 -*-
"""转人工 query 记录查询服务

接口：queryTransferRecords
入参：{pageNum, pageSize}　出参：AiSellerCcPageResult<TransferQueryRecordDTO>

项目内部统一叫 question / question_id，仅在向网关请求时映射为 query / id。
"""

from typing import Any, Dict

from _errors import ServiceError
from _http import api_post
from settings import settings


def query_pending_knowledge(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """
    查询转人工 query 记录列表。

    Returns:
        {"markdown": str, "data": dict}
    """
    # 网关接口字段名为 pageNum，仅在这里做一次映射
    body = {"pageNum": page, "pageSize": page_size}

    resp = api_post(
        path=settings.KNOWLEDGE_QUERY_PATH,
        body=body,
        timeout=settings.API_TIMEOUT,
    )

    if not resp.get("success"):
        err = resp.get("errorMsg") or resp.get("message") or resp
        raise ServiceError("查询待完善知识失败：{}".format(err))

    # 网关双层包装：resp.data 实际是 AiSellerCcPageResult 全家桶
    # （其中 data/total/pageNum/totalPages 都藏在内层），需再剥一层。
    # 同时兼容单层：万一哪天网关拆了外壳也不会倒送
    inner = resp.get("data") or {}
    if isinstance(inner, dict):
        raw_items = inner.get("data") or []
        total = inner.get("total", resp.get("total", 0))
        total_pages = inner.get("totalPages", resp.get("totalPages", 1))
        page_num = inner.get("pageNum", resp.get("pageNum", page))
    else:
        raw_items = inner if isinstance(inner, list) else []
        total = resp.get("total", 0)
        total_pages = resp.get("totalPages", 1)
        page_num = resp.get("pageNum", page)

    # 字段映射：网关 → 项目内部命名
    items = [
        {
            "question_id": it.get("id"),
            "question": it.get("query", ""),
            "create_time": it.get("createTime", ""),
            "products": [
                {
                    "id": p.get("productId"),
                    "name": p.get("productName", ""),
                    "image": p.get("productImage", ""),
                }
                for p in (it.get("relatedProducts") or [])
            ],
        }
        for it in raw_items
    ]

    # 渲染 markdown
    lines = ["## 待完善知识（共 {} 条，第 {}/{} 页）\n".format(total, page_num, total_pages)]

    if not items:
        lines.append("当前没有待完善的知识，牛仔表现很好！")
    else:
        for i, item in enumerate(items, 1):
            lines.append("{}. **{}**".format(i, item["question"]))
            lines.append("   - 问题ID：`{}` ｜ 时间：{}".format(
                item["question_id"], item["create_time"]))
            names = "、".join(p["name"] for p in item["products"] if p["name"])
            if names:
                lines.append("   - 关联商品：{}".format(names))
            lines.append("")

    if page_num < total_pages:
        lines.append("\n> 还有更多，可用 `--page {}` 查看下一页".format(page_num + 1))

    return {
        "markdown": "\n".join(lines),
        "data": {
            "items": items,
            "total": total,
            "page": page_num,
            "total_pages": total_pages,
        },
    }
