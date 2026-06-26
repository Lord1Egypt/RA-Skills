#!/usr/bin/env python3
"""
查询失信/被执行信息辅助脚本

由于执行信息公开网有验证码，此脚本提供查询指引和辅助功能

使用方法:
    python scripts/query_executions.py "公司名称"
    python scripts/query_executions.py "公司名称" --output execution_guide.json
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def generate_query_urls(company_name: str) -> Dict:
    """生成各类查询 URL"""
    base_url = "http://zxgk.court.gov.cn"

    return {
        "失信被执行人": {
            "url": f"{base_url}/shixin/",
            "description": "被执行人未履行生效法律文书确定的义务，并具有失信情形",
            "severity": "高",
            "impact": "严重影响信用，可能被限制高消费、限制出行"
        },
        "被执行人": {
            "url": f"{base_url}/zhixing/",
            "description": "法院立案执行但未履行完毕的被执行人",
            "severity": "中",
            "impact": "存在未履行的债务，需关注执行进度"
        },
        "限制消费人员": {
            "url": f"{base_url}/xiaofei/",
            "description": "被采取限制消费措施的人员或企业法定代表人",
            "severity": "高",
            "impact": "法定代表人被限制高消费"
        },
        "终结本次执行": {
            "url": f"{base_url}/zhongben/",
            "description": "法院裁定终结本次执行程序的案件",
            "severity": "中",
            "impact": "债权未完全实现，但暂时无法执行"
        },
        "财产处置": {
            "url": f"{base_url}/caichan/",
            "description": "司法拍卖、变卖财产信息",
            "severity": "中",
            "impact": "企业资产被司法处置"
        }
    }


def generate_query_guide(company_name: str) -> Dict:
    """生成失信查询指引"""
    return {
        "company_name": company_name,
        "generated_at": datetime.now().isoformat(),

        "query_urls": generate_query_urls(company_name),

        "query_steps": [
            {
                "step": 1,
                "action": "访问中国执行信息公开网",
                "url": "http://zxgk.court.gov.cn/",
                "note": "使用电脑浏览器访问"
            },
            {
                "step": 2,
                "action": "选择查询类型",
                "options": [
                    "失信被执行人 - 最重要，优先查询",
                    "被执行人 - 查看当前执行案件",
                    "限制消费 - 查看是否被限制高消费"
                ]
            },
            {
                "step": 3,
                "action": "输入查询条件",
                "fields": {
                    "名称": company_name,
                    "身份证号/统一社会信用代码": "可选，提高精确度"
                },
                "note": "输入验证码后点击查询"
            },
            {
                "step": 4,
                "action": "分析查询结果",
                "check_items": [
                    "是否有记录",
                    "执行标的金额",
                    "执行法院",
                    "立案时间",
                    "被执行人履行情况"
                ]
            }
        ],

        "risk_assessment": {
            "无记录": {
                "level": "低风险",
                "color": "green",
                "description": "未发现失信/被执行记录",
                "recommendation": "信用状况良好"
            },
            "仅被执行人记录": {
                "level": "中风险",
                "color": "yellow",
                "description": "存在执行案件但未被列入失信",
                "recommendation": "关注案件进展和履行情况"
            },
            "失信被执行人": {
                "level": "高风险",
                "color": "red",
                "description": "被列入失信被执行人名单",
                "recommendation": "信用严重受损，建议谨慎合作"
            },
            "限制消费": {
                "level": "高风险",
                "color": "red",
                "description": "法定代表人被限制高消费",
                "recommendation": "反映企业经营困难或信用问题"
            }
        },

        "key_indicators": [
            {
                "name": "执行标的",
                "description": "被执行人应当履行的金钱债务金额",
                "threshold": {
                    "low": "< 100万",
                    "medium": "100万-1000万",
                    "high": "> 1000万"
                }
            },
            {
                "name": "案件数量",
                "description": "执行案件总数",
                "threshold": {
                    "low": "1-2件",
                    "medium": "3-5件",
                    "high": "> 5件"
                }
            },
            {
                "name": "立案时间",
                "description": "最近一次执行立案时间",
                "threshold": {
                    "low": "> 2年前",
                    "medium": "1-2年内",
                    "high": "< 1年"
                }
            }
        ],

        "output_template": {
            "dishonest_debtor": {
                "has_record": False,
                "count": 0,
                "total_amount": 0,
                "details": []
            },
            "executor": {
                "has_record": False,
                "count": 0,
                "total_amount": 0,
                "details": []
            },
            "consumption_restriction": {
                "has_record": False,
                "count": 0,
                "details": []
            },
            "risk_level": "待评估",
            "notes": []
        }
    }


def print_guide(guide: Dict):
    """打印查询指引"""
    print("=" * 60)
    print(f"失信/被执行信息查询指引: {guide['company_name']}")
    print("=" * 60)
    print()

    # 查询 URL
    print("【查询入口】")
    for name, info in guide["query_urls"].items():
        severity = {"高": "⚠️ ", "中": "📋", "低": "✓"}
        print(f"\n  {severity.get(info['severity'], '')} {name}")
        print(f"    网址: {info['url']}")
        print(f"    说明: {info['description']}")
        print(f"    严重程度: {info['severity']}")
    print()

    # 查询步骤
    print("【查询步骤】")
    for step in guide["query_steps"]:
        print(f"\n  步骤 {step['step']}: {step['action']}")
        if "url" in step:
            print(f"    网址: {step['url']}")
        if "options" in step:
            print("    选项:")
            for opt in step["options"]:
                print(f"      - {opt}")
        if "fields" in step:
            print("    填写:")
            for field, value in step["fields"].items():
                print(f"      - {field}: {value}")
        if "note" in step:
            print(f"    提示: {step['note']}")
        if "check_items" in step:
            print("    检查项目:")
            for item in step["check_items"]:
                print(f"      □ {item}")
    print()

    # 风险评估
    print("【风险评估标准】")
    for condition, info in guide["risk_assessment"].items():
        color = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
        print(f"\n  {color.get(info['color'], '')} {info['level']}")
        print(f"    条件: {condition}")
        print(f"    说明: {info['description']}")
        print(f"    建议: {info['recommendation']}")
    print()

    # 关键指标
    print("【关键指标解读】")
    for indicator in guide["key_indicators"]:
        print(f"\n  {indicator['name']}")
        print(f"    说明: {indicator['description']}")
        print("    阈值:")
        for level, value in indicator["threshold"].items():
            level_name = {"low": "低", "medium": "中", "high": "高"}
            print(f"      - {level_name[level]}: {value}")
    print()

    print("=" * 60)
    print("提示: 查询完成后，请将结果记录到 output_template 格式中")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="失信/被执行信息查询辅助")
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
