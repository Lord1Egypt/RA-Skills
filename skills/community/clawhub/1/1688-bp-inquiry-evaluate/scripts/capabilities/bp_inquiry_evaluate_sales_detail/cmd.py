#!/usr/bin/env python3
"""业务员评估销售明细 CLI入口"""

import os
import sys
import re
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.bp_inquiry_evaluate_sales_detail.service import bp_inquiry_evaluate_sales_detail


COMMAND_NAME = "bp_inquiry_evaluate_sales_detail"
COMMAND_DESC = "--startAt <开始日期> --endAt <结束日期>   查询业务员评估销售明细"


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
def build_seller_report(result: dict, sale_identity_id: str, start_at: str, end_at: str) -> str:
    """将 API 返回的 result 转换为 Markdown 字符串

    数据结构：
    - saleIdentityId: String
    - saleIdentityName: String
    - score: Number
    - indicators[]: {name, value}
    - evaluateSummary: {importantInquiry, serviceAbility, attentionText}
    - inquiryDetails[]: {buyerIdentityStr, userType, inquiryResult, purchaseLevel, ...,
        inquirySummary: {purchaseRequirements, inquirySummary, inquiryResult},
        advantageDetails[], improvementDetails[], communicates[]}
    """

    inquiry_details = result.get("inquiryDetails", [])
    sale_identity_name = result.get("saleIdentityName", "—")

    lines = []

    # ── 业务员评估概要 ─────────────────────────────
    indicators = result.get("indicators", [])
    lines.append(f"## {sale_identity_name} 评估概要")
    lines.append("")
    lines.append("### 指标概览")
    lines.append("")
    if indicators:
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        for ind in indicators:
            value = ind.get("value", "—")
            if ind.get("name") == "服务专业度":
                value = _stars_from_pct(value)
            lines.append(f"| {ind.get('name', '')} | {value} |")
    elif result.get('score') is not None:
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        lines.append(f"| 综合评分 | {result.get('score', '—')} |")
        lines.append(f"| 有效询盘数 | {result.get('inquiryCnt', 0)} |")
    else:
        lines.append("> 暂无指标数据")
        lines.append("")

    # ── 业务员评估详情（若存在 evaluateSummary）──────
    evaluate_summary = result.get("evaluateSummary", {})
    if evaluate_summary:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("### 评估摘要")
        lines.append("")
        important_inquiry = evaluate_summary.get("importantInquiry", "")
        if important_inquiry:
            lines.append(f"- **重要询盘**：{important_inquiry}")

        service_ability = evaluate_summary.get("serviceAbility", "")
        if service_ability:
            lines.append(f"- **业务员表现**：{service_ability}")

        attention_text = evaluate_summary.get("attentionText", "")
        if attention_text:
            attention_text = attention_text.replace('"', '')
            lines.append(f"- **买家高频关注**：{attention_text}")

        report_url = f"https://air.1688.com/app/bp-boot/a2a-team-newton/index.html#/assessment-detail?startAt={start_at}&endAt={end_at}&sellerUserId={sale_identity_id}"
        lines.append("")
        lines.append(f"**报告链接**：[点击查看完整评估报告]({report_url})")

    lines.append("")
    lines.append("### 询盘详情")
    lines.append("")
    if not inquiry_details:
        lines.append("> 暂无询盘详情数据")
        lines.append("")
    # ── 具体买家询盘信息（按 inquiryDetails 条数动态渲染）──
    for idx, detail in enumerate(inquiry_details[:10], start=1):
        buyer_name = detail.get("buyerIdentityName", "—")
        inquiry_summary = detail.get("inquirySummary", {})
        inquiry_date = detail.get("inquiryDate", "-")
        inquiry_result = detail.get("inquiryResult", "-")

        lines.append("")
        lines.append(f"#### 询盘{idx}")
        lines.append("")
        lines.append(f"> **买家旺旺ID**：{buyer_name}  **询盘结果**：{inquiry_result}  **询盘日期**：{inquiry_date}")
       
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

        inquiry_esult = inquiry_summary.get("inquiryResult", "")
        if inquiry_esult:
            lines.append("")
            lines.append(f"- **询盘结果**：{inquiry_esult}")
        
        inquiry_id = detail.get("inquiryId", "")
        if inquiry_id:
            detail_url = f"https://air.1688.com/app/bp-boot/a2a-team-newton/index.html#/inquiry-detail?startAt={start_at}&endAt={end_at}&sellerUserId={sale_identity_id}&inquiryId={inquiry_id}"
            lines.append(f"| [点击查看完整询盘详情及AI教练建议]({detail_url}) ")

        # 亮点&改进
        advantages = detail.get("advantageDetails", []) or []
        improvements = detail.get("improvementDetails", []) or []
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

    return "\n".join(lines)


# ── CLI 入口 ────────────────────────────────────────────────
def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询数据。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="业务员询盘评估详情")
    parser.add_argument("--saleIdentityId", "-sid", required=True, help="业务员身份ID")
    parser.add_argument("--startAt", "-s", required=True, help="开始日期，格式：yyyyMMdd")
    parser.add_argument("--endAt", "-e", required=True, help="结束日期，格式：yyyyMMdd")
    args = parser.parse_args()

    try:
        result = bp_inquiry_evaluate_sales_detail(args.saleIdentityId, args.startAt, args.endAt)
        markdown = build_seller_report(result, args.saleIdentityId, args.startAt, args.endAt)
        print_output(True, markdown, {})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
