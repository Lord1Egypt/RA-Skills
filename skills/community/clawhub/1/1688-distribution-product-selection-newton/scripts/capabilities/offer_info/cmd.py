#!/usr/bin/env python3
"""商品分销参谋数据查询命令 — CLI 入口"""

COMMAND_NAME = "offer_info"
COMMAND_DESC = "查询商品分销参谋数据"

import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from scripts._sys._output import print_output, print_error
from scripts.capabilities.offer_info.service import get_offer_info, extract_decision_factors


def main():
    import argparse
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--offer-id", required=True, help="商品 ID")
    parser.add_argument("--decision", action="store_true", help="是否提取决策因素")
    args = parser.parse_args()

    try:
        raw_data = get_offer_info(args.offer_id)

        if args.decision:
            factors = extract_decision_factors(raw_data)
            markdown = _format_decision_factors(args.offer_id, factors)
            print_output(True, markdown, {"raw": raw_data, "decision_factors": factors})
        else:
            markdown = f"✅ 商品 {args.offer_id} 的分销参谋数据查询成功"
            print_output(True, markdown, raw_data)
    except Exception as e:
        print_error(e)


def _format_decision_factors(offer_id: str, factors: dict) -> str:
    """将决策因素格式化为可读的 Markdown。"""
    lines = [f"### 商品 {offer_id} 分销参谋分析\n"]

    if factors.get("onePiecePrice"):
        lines.append(f"- **一件包邮价**：¥{factors['onePiecePrice']}")
    if factors.get("multiPiecePrice"):
        lines.append(f"- **分销专属价**：¥{factors['multiPiecePrice']}（起批量 {factors.get('startNum', '-')}）")

    if factors.get("onePieceFreePostage"):
        lines.append("- **包邮**：✅ 支持一件包邮")
    elif factors.get("freePostage"):
        lines.append("- **包邮**：✅ 多件包邮")
    elif factors.get("freeDeliverFee"):
        lines.append("- **包邮**：✅ 包邮")
    else:
        cost = factors.get("freightCost")
        lines.append(f"- **运费**：¥{cost}" if cost else "- **运费**：需自付")

    if factors.get("officialLogistics"):
        lines.append("- **物流**：✅ 官方物流")

    if factors.get("isBrandOffer"):
        auth_status = "✅ 已授权" if factors.get("isBrandAuth") else "❌ 未授权"
        lines.append(f"- **品牌**：{factors.get('brandName', '品牌商品')}（{auth_status}）")

    if factors.get("alreadyUpgrade"):
        lines.append("- **分销品**：✅ 已升级为分销品")

    channels = factors.get("supportedChannels", [])
    if channels:
        lines.append(f"- **支持渠道**：{', '.join(channels)}")

    high_exp = factors.get("highExperienceScoreChannels", [])
    if high_exp:
        lines.append(f"- **高体验分渠道**：{', '.join(high_exp)}")

    high_lgt = factors.get("highPerfectLgtRateChannels", [])
    if high_lgt:
        lines.append(f"- **高履约率渠道**：{', '.join(high_lgt)}")

    protections = factors.get("protections", [])
    if protections:
        lines.append(f"- **服务保障**：{', '.join(protections)}")

    return "\n".join(lines)


if __name__ == "__main__":
    main()