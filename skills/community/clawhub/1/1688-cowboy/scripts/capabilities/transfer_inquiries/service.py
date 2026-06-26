# -*- coding: utf-8 -*-
"""
转人工询盘查询能力实现

接口：queryTransferInquiries（path: api/query_transfer_inquiries/1.0.0）
入参：{date, pageNum, pageSize}
出参：AiSellerCcPageResult<TransferInquiryDTO>，与 daily_report 相同的双层 data 包装：
  外层 resp.data = AiSellerCcPageResult {
      success, errorMsg, errorCode, code, traceId, message,
      data: [...TransferInquiryDTO],
      total, pageNum, pageSize, totalPages,
  }
每项 DTO 字段：
  id / inquiryTime / inquirySummary / transferReason /
  buyerAvatar / buyerNickname / buyerCompanyName / buyerTags /
  buyerLoginId / buyerLoginIdEncode

sellerUserId 不需要传递，网关会根据 AK 自动注入实际调用方 userId。
buyerLoginIdEncode 属于系统内部编码值，不向商家展示。
"""

import time
from datetime import date as _date
from typing import Any, Dict, List

from _errors import ParamError, ServiceError
from _http import api_post
from settings import settings


def _normalize_date(date: str) -> str:
    """把 'today' 转成 'YYYY-MM-DD'；其余原样返回（上游 cmd 已做过格式校验）"""
    if date == "today":
        return _date.today().isoformat()
    return date


def query_transfer_inquiries(date: str, page_num: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """
    分页查询指定日期的转人工询盘记录

    Args:
        date:      查询日期，"today" 或 "YYYY-MM-DD"
        page_num:  页码（>=1）
        page_size: 每页大小（1~100）

    Returns:
        {
          "date": "2026-05-14",
          "elapsed_seconds": 0.4,
          "page_num": 1,
          "page_size": 10,
          "total": 5,
          "total_pages": 1,
          "inquiries": [
              {
                "id": "INQ001",
                "inquiry_time": "2026-05-14 10:30:00",
                "inquiry_summary": "...",
                "transfer_reason": "...",
                "buyer_nickname": "张三",
                "buyer_login_id": "zhangsan",
                "buyer_company_name": "上海科技有限公司",
                "buyer_tags": "VIP客户, 老客户",
                "buyer_avatar": "https://...",
              },
              ...
          ]
        }
    """
    if page_num < 1:
        raise ParamError("pageNum 必须 >= 1")
    if page_size < 1 or page_size > 100:
        raise ParamError("pageSize 必须在 1~100 之间")

    start_time = time.time()

    query_date = _normalize_date(date)
    body = {
        "date": query_date,
        "pageNum": page_num,
        "pageSize": page_size,
    }

    resp = api_post(
        path=settings.QUERY_INQUIRY_PATH,
        body=body,
        timeout=settings.API_TIMEOUT,
    )

    if not resp.get("success"):
        err = resp.get("errorMsg") or resp.get("message") or resp
        raise ServiceError("查询转人工询盘失败：{}".format(err))

    # 网关双层包装：resp.data = AiSellerCcPageResult，列表在内层 data 字段
    page_result = resp.get("data") or {}
    if not isinstance(page_result, dict):
        raise ServiceError("响应结构异常：data 字段不是对象（实际类型 {}）".format(type(page_result).__name__))

    # 内层 PageResult 本身也带 success 字段；若 false 直接抛出
    if page_result.get("success") is False:
        err = page_result.get("errorMsg") or page_result.get("message") or page_result
        raise ServiceError("查询转人工询盘失败：{}".format(err))

    raw_items = page_result.get("data") or []
    if not isinstance(raw_items, list):
        raise ServiceError(
            "响应结构异常：PageResult.data 不是列表（实际类型 {}）".format(type(raw_items).__name__)
        )

    inquiries: List[Dict[str, Any]] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        inquiries.append({
            "id": item.get("id") or "",
            "inquiry_time": item.get("inquiryTime") or "",
            "inquiry_summary": item.get("inquirySummary") or "",
            "transfer_reason": item.get("transferReason") or "",
            "buyer_nickname": item.get("buyerNickname") or "",
            "buyer_login_id": item.get("buyerLoginId") or "",
            "buyer_company_name": item.get("buyerCompanyName") or "",
            "buyer_tags": item.get("buyerTags") or "",
            "buyer_avatar": item.get("buyerAvatar") or "",
            # buyerLoginIdEncode 为系统内部编码，不暴露给商家
        })

    return {
        "date": query_date,
        "elapsed_seconds": round(time.time() - start_time, 1),
        "page_num": page_result.get("pageNum") or page_num,
        "page_size": page_result.get("pageSize") or page_size,
        "total": page_result.get("total") or 0,
        "total_pages": page_result.get("totalPages") or 0,
        "inquiries": inquiries,
    }


def format_inquiries_markdown(result: Dict[str, Any]) -> str:
    """将转人工询盘列表格式化为 Markdown 表格"""
    date_str = result.get("date", "")
    inquiries = result.get("inquiries", [])
    total = result.get("total", 0)
    page_num = result.get("page_num", 1)
    page_size = result.get("page_size", 10)
    total_pages = result.get("total_pages", 0)

    lines = ["## 转人工询盘（{}）\n".format(date_str)]

    if not inquiries:
        lines.append("该日期暂无转人工询盘。")
        return "\n".join(lines)

    lines.append(
        "> 共 **{}** 条 · 第 {} / {} 页（每页 {} 条）\n".format(
            total, page_num, total_pages or 1, page_size
        )
    )

    lines.append("| 时间 | 买家 | 公司 | 询盘总结 | 转人工原因 |")
    lines.append("|------|------|------|----------|------------|")
    for it in inquiries:
        buyer = it["buyer_nickname"] or it["buyer_login_id"] or "—"
        if it["buyer_tags"]:
            buyer = "{}（{}）".format(buyer, it["buyer_tags"])
        company = it["buyer_company_name"] or "—"
        summary = (it["inquiry_summary"] or "—").replace("|", "\\|").replace("\n", " ")
        reason = (it["transfer_reason"] or "—").replace("|", "\\|").replace("\n", " ")
        lines.append("| {} | {} | {} | {} | {} |".format(
            it["inquiry_time"] or "—", buyer, company, summary, reason
        ))

    return "\n".join(lines)
