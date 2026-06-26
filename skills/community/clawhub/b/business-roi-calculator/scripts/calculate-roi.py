#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Business ROI Calculator - 商务合作投资回报率实时计算

功能:
- 短期/长期 ROI 计算
- 期望值计算
- 决策建议 (基于阈值>1.5)
- 敏感性分析
- 盈亏平衡点计算

使用示例:
    python calculate-roi.py --revenue 50000 --cost 5000 --success-rate 0.7
    python calculate-roi.py --revenue 32000 --cost 1450 --success-rate 0.9 --templates
"""

import argparse
import json
from typing import Dict, List, Optional


def calculate_roi(
    revenue: float,
    cost: float,
    success_rate: float = 0.5,
    period: str = "short"
) -> Dict:
    """
    计算 ROI
    
    参数:
        revenue: 预期收益
        cost: 投入成本
        success_rate: 成功率 (0-1)
        period: 时间周期 ("short" 或 "long")
    
    返回:
        包含 ROI、期望值、决策建议的字典
    """
    if cost == 0:
        return {
            "error": "投入成本不能为 0",
            "roi": float('inf'),
            "recommendation": "✅ 零成本项目，建议执行"
        }
    
    # 计算 ROI
    short_term_roi = (revenue - cost) / cost
    long_term_roi = (revenue * success_rate - cost) / cost
    expected_value = revenue * success_rate
    
    # 决策建议
    if period == "short":
        roi = short_term_roi
    else:
        roi = long_term_roi
    
    if roi >= 1.5:
        recommendation = "✅ 强烈推荐执行 (ROI ≥ 1.5 阈值)"
    elif roi >= 0.5:
        recommendation = "🟡 谨慎评估 (ROI 0.5-1.5)"
    else:
        recommendation = "❌ 建议放弃 (ROI < 0.5)"
    
    return {
        "revenue": revenue,
        "cost": cost,
        "success_rate": success_rate,
        "period": period,
        "short_term_roi": short_term_roi,
        "long_term_roi": long_term_roi,
        "expected_value": expected_value,
        "roi": roi,
        "recommendation": recommendation
    }


def sensitivity_analysis(
    revenue: float,
    cost: float,
    base_success_rate: float = 0.5
) -> List[Dict]:
    """
    敏感性分析 - 不同成功率下的 ROI
    
    参数:
        revenue: 预期收益
        cost: 投入成本
        base_success_rate: 基准成功率
    
    返回:
        不同成功率下的 ROI 列表
    """
    rates = [0.9, 0.7, 0.5, 0.3, 0.1]
    results = []
    
    for rate in rates:
        result = calculate_roi(revenue, cost, rate, "long")
        results.append({
            "success_rate": rate,
            "roi": result["long_term_roi"],
            "expected_value": result["expected_value"],
            "recommendation": "✅" if result["long_term_roi"] >= 1.5 else ("🟡" if result["long_term_roi"] >= 0.5 else "❌")
        })
    
    return results


def break_even_analysis(
    revenue: float,
    cost: float
) -> Dict:
    """
    盈亏平衡点分析
    
    参数:
        revenue: 预期收益
        cost: 投入成本
    
    返回:
        盈亏平衡点信息
    """
    if revenue == 0:
        return {"error": "预期收益不能为 0"}
    
    # 盈亏平衡成功率
    break_even_rate = cost / revenue
    
    # 盈亏平衡销量 (假设单客价值)
    unit_price = revenue / 100  # 假设 100 个客户
    break_even_units = cost / unit_price
    
    return {
        "break_even_rate": break_even_rate,
        "break_even_rate_percent": f"{break_even_rate * 100:.1f}%",
        "break_even_units": break_even_units,
        "unit_price": unit_price,
        "interpretation": f"成功率需达到 {break_even_rate * 100:.1f}% 才能盈亏平衡"
    }


def get_template(template_name: str) -> Dict:
    """
    获取预设模板
    
    参数:
        template_name: 模板名称
    
    返回:
        模板配置
    """
    templates = {
        "channel_cooperation": {
            "name": "渠道合作 (KOL/Influencer)",
            "description": "YouTube 合作/播客赞助/Newsletter 推广",
            "success_rates": {
                "head": {"min": 0.3, "max": 0.5, "desc": "头部 KOL (10 万 + 粉丝)"},
                "mid": {"min": 0.5, "max": 0.7, "desc": "中部 KOL (1-10 万粉丝)"},
                "micro": {"min": 0.7, "max": 0.9, "desc": "微型 KOL (<1 万粉丝)"}
            },
            "commission": {"first": 0.3, "recurring": 0.15}
        },
        "skill_launch": {
            "name": "技能培训 (ClawHub 上架)",
            "description": "技能包开发/模板销售/课程制作",
            "success_rates": {
                "validated": {"min": 0.8, "max": 0.95, "desc": "已验证方法论"},
                "new": {"min": 0.5, "max": 0.7, "desc": "新开发技能"},
                "trending": {"min": 0.6, "max": 0.8, "desc": "跟随热点"}
            },
            "price_range": {"min": 280, "max": 499, "currency": "CNY"}
        },
        "email_outreach": {
            "name": "邮件外展 (Cold Email)",
            "description": "商务合作/客户开发/渠道拓展",
            "success_rates": {
                "targeted": {"min": 0.6, "max": 0.8, "desc": "精准名单 + 个性化"},
                "generic": {"min": 0.2, "max": 0.4, "desc": "通用名单 + 模板"},
                "cold": {"min": 0.1, "max": 0.2, "desc": "冷启动无优化"}
            },
            "reply_rate": {"min": 0.05, "max": 0.15}
        },
        "community_promotion": {
            "name": "社群推广 (Discord/Slack)",
            "description": "官方社群/付费社群/地区社群",
            "success_rates": {
                "official": {"min": 0.6, "max": 0.8, "desc": "官方社群 (高信任度)"},
                "paid": {"min": 0.7, "max": 0.9, "desc": "付费社群 (高质量用户)"},
                "regional": {"min": 0.4, "max": 0.6, "desc": "地区社群 (地域限制)"}
            }
        },
        "consulting": {
            "name": "商务咨询服务",
            "description": "1 对 1 咨询/企业内训/长期顾问",
            "success_rates": {
                "inbound": {"min": 0.8, "max": 0.95, "desc": "主动咨询 (客户上门)"},
                "outbound": {"min": 0.3, "max": 0.5, "desc": "被动销售 (主动 outreach)"},
                "referral": {"min": 0.6, "max": 0.8, "desc": "转介绍"}
            },
            "price_range": {"min": 500, "max": 2000, "currency": "CNY", "unit": "hour"}
        }
    }
    
    return templates.get(template_name, {"error": "模板不存在"})


def list_templates() -> List[str]:
    """列出所有可用模板"""
    return [
        "channel_cooperation - 渠道合作 (KOL/Influencer)",
        "skill_launch - 技能培训 (ClawHub 上架)",
        "email_outreach - 邮件外展 (Cold Email)",
        "community_promotion - 社群推广 (Discord/Slack)",
        "consulting - 商务咨询服务"
    ]


def print_report(result: Dict, show_sensitivity: bool = False, show_break_even: bool = False):
    """
    打印 ROI 分析报告
    
    参数:
        result: calculate_roi 返回的结果
        show_sensitivity: 是否显示敏感性分析
        show_break_even: 是否显示盈亏平衡分析
    """
    print("\n" + "="*60)
    print("📊 ROI 分析报告")
    print("="*60)
    
    print(f"\n### 输入数据")
    print(f"- 预期收益：¥{result['revenue']:,.0f}")
    print(f"- 投入成本：¥{result['cost']:,.0f}")
    print(f"- 成功率：{result['success_rate']*100:.0f}%")
    print(f"- 时间周期：{'短期 (1-3 月)' if result['period'] == 'short' else '长期 (6-12 月)'}")
    
    print(f"\n### 计算结果")
    print(f"- 短期 ROI: {result['short_term_roi']:.2f}x ({result['short_term_roi']*100:.0f}%)")
    print(f"- 长期 ROI: {result['long_term_roi']:.2f}x ({result['long_term_roi']*100:.0f}%)")
    print(f"- 期望值：¥{result['expected_value']:,.0f}")
    
    print(f"\n### 决策建议")
    print(result['recommendation'])
    
    if show_sensitivity:
        print(f"\n### 敏感性分析")
        print("| 成功率 | ROI | 期望值 | 决策 |")
        print("|--------|-----|--------|------|")
        sensitivity = sensitivity_analysis(result['revenue'], result['cost'], result['success_rate'])
        for item in sensitivity:
            print(f"| {item['success_rate']*100:.0f}% | {item['roi']:.2f}x | ¥{item['expected_value']:,.0f} | {item['recommendation']} |")
    
    if show_break_even:
        print(f"\n### 盈亏平衡分析")
        be = break_even_analysis(result['revenue'], result['cost'])
        if "error" not in be:
            print(f"- 盈亏平衡成功率：{be['break_even_rate_percent']}")
            print(f"- 解读：{be['interpretation']}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Business ROI Calculator - 商务合作投资回报率实时计算",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python calculate-roi.py --revenue 50000 --cost 5000 --success-rate 0.7
  python calculate-roi.py --revenue 32000 --cost 1450 --success-rate 0.9 --sensitivity
  python calculate-roi.py --templates
  python calculate-roi.py --template skill_launch
        """
    )
    
    parser.add_argument("--revenue", type=float, help="预期收益")
    parser.add_argument("--cost", type=float, help="投入成本")
    parser.add_argument("--success-rate", type=float, default=0.5, help="成功率 (0-1, 默认 0.5)")
    parser.add_argument("--period", choices=["short", "long"], default="short", help="时间周期")
    parser.add_argument("--sensitivity", action="store_true", help="显示敏感性分析")
    parser.add_argument("--break-even", action="store_true", help="显示盈亏平衡分析")
    parser.add_argument("--templates", action="store_true", help="列出所有模板")
    parser.add_argument("--template", type=str, help="查看指定模板")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    # 列出模板
    if args.templates:
        print("\n可用模板:\n")
        for t in list_templates():
            print(f"  {t}")
        print()
        return
    
    # 查看指定模板
    if args.template:
        template = get_template(args.template)
        if "error" not in template:
            print(f"\n### {template['name']}")
            print(f"\n{template['description']}\n")
            if "success_rates" in template:
                print("成功率参考:")
                for key, value in template["success_rates"].items():
                    print(f"  {value['desc']}: {value['min']*100:.0f}-{value['max']*100:.0f}%")
            if "commission" in template:
                print(f"\n佣金比例:")
                print(f"  首单：{template['commission']['first']*100:.0f}%")
                print(f"  续费：{template['commission']['recurring']*100:.0f}%")
        else:
            print(f"\n❌ {template['error']}")
            print("\n可用模板:")
            for t in list_templates():
                print(f"  {t}")
        print()
        return
    
    # 计算 ROI
    if args.revenue and args.cost:
        result = calculate_roi(args.revenue, args.cost, args.success_rate, args.period)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_report(result, args.sensitivity, args.break_even)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
