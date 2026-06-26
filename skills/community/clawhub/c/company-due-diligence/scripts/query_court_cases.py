#!/usr/bin/env python3
"""
查询诉讼记录辅助脚本

由于裁判文书网有验证码，此脚本提供查询指引和辅助功能

使用方法:
    python scripts/query_court_cases.py "公司名称"
    python scripts/query_court_cases.py "公司名称" --output litigation_guide.json
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def generate_search_keywords(company_name: str) -> List[str]:
    """生成搜索关键词组合"""
    keywords = [
        # 基本搜索
        company_name,

        # 精确匹配
        f'"{company_name}"',

        # 作为当事人
        f'被告:{company_name}',
        f'原告:{company_name}',
        f'被执行人:{company_name}',

        # 案由组合
        f'{company_name} 借款合同',
        f'{company_name} 买卖合同',
        f'{company_name} 劳动争议',
        f'{company_name} 建设工程',

        # 风险关键词
        f'{company_name} 破产',
        f'{company_name} 清算',
    ]

    return keywords


def generate_query_guide(company_name: str) -> Dict:
    """生成诉讼查询指引"""
    return {
        "company_name": company_name,
        "generated_at": datetime.now().isoformat(),

        "query_channels": [
            {
                "name": "中国裁判文书网",
                "url": "http://wenshu.court.gov.cn/",
                "description": "官方裁判文书公开平台",
                "coverage": "全国各级法院裁判文书",
                "features": [
                    "支持当事人搜索",
                    "支持案由筛选",
                    "支持时间范围",
                    "支持法院层级筛选"
                ],
                "limitations": [
                    "需要验证码",
                    "部分案件不公开",
                    "数据有延迟"
                ]
            },
            {
                "name": "人民法院公告网",
                "url": "https://rmfygg.court.gov.cn/",
                "description": "法院公告查询",
                "coverage": "全国法院公告",
                "features": [
                    "开庭公告",
                    "送达公告",
                    "执行公告"
                ]
            },
            {
                "name": "天眼查/企查查",
                "url": "https://www.tianyancha.com/",
                "description": "商业查询平台（需付费）",
                "coverage": "聚合多个数据源",
                "features": [
                    "自动聚合诉讼信息",
                    "无需验证码",
                    "数据结构化"
                ],
                "limitations": [
                    "需要付费会员",
                    "数据可能有延迟"
                ]
            }
        ],

        "search_keywords": generate_search_keywords(company_name),

        "search_strategy": [
            {
                "step": 1,
                "action": "访问裁判文书网",
                "url": "http://wenshu.court.gov.cn/",
                "note": "使用电脑访问，手机端功能有限"
            },
            {
                "step": 2,
                "action": "输入验证码",
                "note": "验证码区分大小写"
            },
            {
                "step": 3,
                "action": "高级检索",
                "fields": {
                    "当事人": company_name,
                    "案件类型": "选择全部或特定类型",
                    "法院层级": "建议选择'全部'",
                    "裁判日期": "建议选择近3年"
                }
            },
            {
                "step": 4,
                "action": "分析搜索结果",
                "focus": [
                    "案件数量趋势",
                    "主要案由分布",
                    "作为原告/被告比例",
                    "涉案金额",
                    "最新案件时间"
                ]
            },
            {
                "step": 5,
                "action": "重点关注",
                "items": [
                    "作为被告的案件",
                    "大额诉讼（>100万）",
                    "金融借款纠纷",
                    "劳动争议（反映用工风险）",
                    "近1年的案件"
                ]
            }
        ],

        "risk_assessment_guide": {
            "low_risk": {
                "condition": "无诉讼或仅有少量小额诉讼（作为原告）",
                "impact": "信用状况良好"
            },
            "medium_risk": {
                "condition": "存在诉讼但数量较少，或案件已结案",
                "impact": "需要关注案件具体情况"
            },
            "high_risk": {
                "condition": "大量诉讼、大额诉讼、作为被告败诉、被申请执行",
                "impact": "信用风险较高，建议谨慎"
            }
        },

        "output_template": {
            "total_cases": 0,
            "as_plaintiff": 0,
            "as_defendant": 0,
            "major_cases": [],
            "total_amount": 0,
            "latest_case_date": None,
            "risk_level": "待评估",
            "notes": []
        }
    }


def print_guide(guide: Dict):
    """打印查询指引"""
    print("=" * 60)
    print(f"诉讼记录查询指引: {guide['company_name']}")
    print("=" * 60)
    print()

    # 查询渠道
    print("【查询渠道】")
    for channel in guide["query_channels"]:
        print(f"\n  {channel['name']}")
        print(f"  网址: {channel['url']}")
        print(f"  说明: {channel['description']}")
    print()

    # 搜索关键词
    print("【推荐搜索关键词】")
    for i, keyword in enumerate(guide["search_keywords"][:5], 1):
        print(f"  {i}. {keyword}")
    print()

    # 查询步骤
    print("【查询步骤】")
    for step in guide["search_strategy"]:
        print(f"\n  步骤 {step['step']}: {step['action']}")
        if "url" in step:
            print(f"    网址: {step['url']}")
        if "note" in step:
            print(f"    提示: {step['note']}")
        if "fields" in step:
            print("    填写:")
            for field, value in step["fields"].items():
                print(f"      - {field}: {value}")
    print()

    # 风险评估
    print("【风险评估标准】")
    for level, info in guide["risk_assessment_guide"].items():
        level_name = {"low_risk": "低风险", "medium_risk": "中风险", "high_risk": "高风险"}
        print(f"\n  {level_name[level]}:")
        print(f"    条件: {info['condition']}")
        print(f"    影响: {info['impact']}")
    print()

    print("=" * 60)
    print("提示: 查询完成后，请将结果记录到 output_template 格式中")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="诉讼记录查询辅助")
    parser.add_argument("company", help="公司名称")
    parser.add_argument("--output", "-o", help="输出 JSON 文件")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式到控制台")

    args = parser.parse_args()

    # 生成查询指引
    guide = generate_query_guide(args.company)

    # 输出
    if args.json:
        print(json.dumps(guide, ensure_ascii=False, indent=2))
    else:
        print_guide(guide)

    # 保存到文件
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(guide, f, ensure_ascii=False, indent=2)
        print(f"\n指引已保存到: {args.output}")


if __name__ == "__main__":
    main()
