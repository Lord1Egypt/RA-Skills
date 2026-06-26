#!/usr/bin/env python3
"""业务员评估概览 CLI入口"""

import os
import sys
import re
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.bp_inquiry_evaluate_summary.service import bp_inquiry_evaluate_summary


# ── 服务专业度百分比 → ⭐️ ──────────────────────────────────
def _stars_from_pct(value_str: str) -> str:
    """将服务专业度百分比转换为星级显示

    规则：0%-5% → 1⭐️; 5%-20% → 2⭐️; 20%-30% → 3⭐️;
          30%-50% → 4⭐️; 50%-100% → 5⭐️
    """
    m = re.search(r"(\d+(?:\.\d+)?)%", value_str)
    if not m:
        return value_str
    pct = float(m.group(1))
    if pct <= 5:
        n = 1
    elif pct <= 20:
        n = 2
    elif pct <= 30:
        n = 3
    elif pct <= 50:
        n = 4
    else:
        n = 5
    return "⭐️" * n


# ── 指标辅助函数 ────────────────────────────────────────────
def _indicator_value(indicators: list, name: str) -> str:
    """从指标列表中按 name 取 value，未找到返回 '—'"""
    for ind in indicators:
        if ind.get("name") == name:
            return ind.get("value", "—")
    return "—"


# ── 构建 Markdown 报告 ────────────────────────────────
def build_seller_report(result: dict, start_at: str, end_at: str) -> str:
    """将 API 返回的 result 转换为 Markdown 字符串

    数据结构：
    - evaluateSummary.indicators[]: {name, value, avgCate, contrastCate, description}
    - evaluateDetails[]: {saleIdentityName, saleIdentityId, score, inquiryCnt, inquiryTip, indicators[], inquiryDetails[]}
      - indicators[]: {name, value}
    """

    evaluate_summary = result.get("evaluateSummary", {})
    evaluate_details = result.get("evaluateDetails", [])

    summary_indicators = evaluate_summary.get("indicators", [])

    # ── 服务能力概览 ─────────────────────────────
    lines = []
    lines.append("## 服务能力概览")
    lines.append("")
    if summary_indicators:
        lines.append("| 指标 | 值 | 同行平均 | 对比同行 |")
        lines.append("|------|-----|---------|---------|")
        for ind in summary_indicators:
            value = ind.get("value", "—")
            avg_cate = ind.get("avgCate", "—")
            contrast_cate = ind.get("contrastCate", "—")
            # 服务专业度：值和同行平均转换为星级，对比同行显示"-"
            if ind.get("name") == "服务专业度":
                value = _stars_from_pct(value)
                avg_cate = _stars_from_pct(avg_cate)
                contrast_cate = " - "
            lines.append(f"| {ind.get('name', '')} | {value} | {avg_cate} | {contrast_cate} |")
    else:
        lines.append("> 暂无店铺整体指标数据")
        lines.append("")

    lines.append("")
    if evaluate_details:
        lines.append("| 业务员 | 有效接待询盘数 | 成交金额 | 客单价 | 询盘转化率 | 3分钟响应率 | 服务专业度 | 报告链接 |")
        lines.append("|--------|------------|--------|------|----------|-----------|---------|--------|")
        for detail in evaluate_details:
            d_ind = detail.get("indicators", [])
            name = detail.get("saleIdentityName", "—")
            inquiry_cnt = str(detail.get("inquiryCnt", 0))
            deal_amount = _indicator_value(d_ind, "成交金额")
            unit_price = _indicator_value(d_ind, "客单价")
            conversion_rate = _indicator_value(d_ind, "询盘转化率")
            response_rate = _indicator_value(d_ind, "3分钟响应率")
            service_score = _stars_from_pct(_indicator_value(d_ind, "服务专业度"))
            seller_id = detail.get("saleIdentityId", "")
            report_url = f"https://air.1688.com/app/bp-boot/a2a-team-newton/index.html#/assessment-detail?startAt={start_at}&endAt={end_at}&sellerUserId={seller_id}"
            report_link = f"[点击查看完整评估报告]({report_url})"
            lines.append(f"| {name} | {inquiry_cnt} | {deal_amount} | {unit_price} | {conversion_rate} | {response_rate} | {service_score} | {report_link} |")
    else:
        lines.append("> 暂无业务员数据")
        lines.append("")

    # ── 询盘详情 ─────────────────────────────
    lines.append("")
    lines.append("## 询盘详情")
    lines.append("")

    has_inquiry = False
    for detail in evaluate_details[:3]:
        inquiry_details = detail.get("inquiryDetails", [])
        if not inquiry_details:
            continue

        has_inquiry = True
        sale_name = detail.get("saleIdentityName", "—")
        sale_identity_id = detail.get("saleIdentityId", "")

        for inq in inquiry_details[:1]:
            buyer_name = inq.get("buyerIdentityName", "—")
            inquiry_summary = inq.get("inquirySummary", {})
            inquiry_date = inq.get("inquiryDate", "-")
            inquiry_result = inq.get("inquiryResult", "-")

            lines.append("")
            lines.append(f"> **业务员**：{sale_name}  **买家旺旺ID**：{buyer_name}  **询盘结果**：{inquiry_result}  **询盘日期**：{inquiry_date}")

            # 评估摘要
            evaluate_summary_inq = inq.get("evaluateSummary", {})
            if evaluate_summary_inq:
                lines.append("")
                lines.append("**评估摘要：**")
                lines.append("")
                important_inquiry = evaluate_summary_inq.get("importantInquiry", "")
                if important_inquiry:
                    lines.append(f"- **重要询盘**：{important_inquiry}")
                service_ability = evaluate_summary_inq.get("serviceAbility", "")
                if service_ability:
                    lines.append(f"- **业务员表现**：{service_ability}")
                attention_text = evaluate_summary_inq.get("attentionText", "")
                if attention_text:
                    attention_text = attention_text.replace('"', '')
                    lines.append(f"- **买家高频关注**：{attention_text}")

            lines.append("")
            lines.append("**询盘总结：**")
            lines.append("")

            # 采购需求、沟通总结、询盘结果
            purchase_req = inquiry_summary.get("purchaseRequirements", "")
            if purchase_req:
                lines.append("")
                lines.append(f"- **采购需求**：{purchase_req}")

            comm_summary = inquiry_summary.get("inquirySummary", "")
            if comm_summary:
                lines.append("")
                lines.append(f"- **沟通总结**：{comm_summary}")

            inquiry_result = inquiry_summary.get("inquiryResult", "")
            if inquiry_result:
                lines.append("")
                lines.append(f"- **询盘结果**：{inquiry_result}")
            
            inquiry_id = inq.get("inquiryId", "")
            if inquiry_id:
                detail_url = f"https://air.1688.com/app/bp-boot/a2a-team-newton/index.html#/inquiry-detail?startAt={start_at}&endAt={end_at}&sellerUserId={sale_identity_id}&inquiryId={inquiry_id}"
                lines.append(f"| [点击查看完整询盘详情及AI教练建议]({detail_url}) ")

            # 亮点&改进
            advantages = inq.get("advantageDetails", []) or []
            improvements = inq.get("improvementDetails", []) or []
            if advantages or improvements:
                lines.append("")
                lines.append("**亮点&改进：**")
                for item in advantages:
                    lines.append(f"- ✅ {item}")
                for item in improvements:
                    lines.append(f"- ⚠️ {item}")
            
        lines.append("")
        lines.append("---")
        lines.append("")

    if not has_inquiry:
        lines.append("> 暂无询盘详情数据")
        lines.append("")

    return "\n".join(lines)


# ── 提取业务员列表 ────────────────────────────────────────────
def extract_seller_list(result: dict) -> list:
    """从 result 中提取 evaluateDetails 的 saleIdentityId 和 saleIdentityName 列表

    返回: [{"saleIdentityName": "业务员名称", "saleIdentityId": 123456}, ...]
    """
    evaluate_details = result.get("evaluateDetails", [])
    return [
        {"saleIdentityId": detail.get("saleIdentityId", ""), "saleIdentityName": detail.get("saleIdentityName", "")}
        for detail in evaluate_details
    ]


# ── CLI 入口 ────────────────────────────────────────────────
def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询数据。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="团队服务评估概览")
    parser.add_argument("--startAt", "-s", required=True, help="开始日期")
    parser.add_argument("--endAt", "-e", required=True, help="结束日期")
    args = parser.parse_args()

    try:
        result = bp_inquiry_evaluate_summary(args.startAt, args.endAt)
        data = extract_seller_list(result)
        markdown = build_seller_report(result, args.startAt, args.endAt)
        print_output(True, markdown, data)
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
