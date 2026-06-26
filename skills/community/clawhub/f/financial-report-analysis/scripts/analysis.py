#!/usr/bin/env python3
"""
财报分析技能包核心脚本
功能：获取上市公司财务数据，进行智能分析，生成专业报告
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Optional

# 模拟数据 - 实际使用时需要接入真实数据源API
SAMPLE_DATA = {
    "贵州茅台": {
        "股票代码": "600519",
        "报告期": "2025年年报",
        "资产负债表": {
            "总资产": 285000000000,
            "总负债": 45000000000,
            "股东权益": 240000000000,
            "流动资产": 180000000000,
            "流动负债": 38000000000,
        },
        "利润表": {
            "营业收入": 145000000000,
            "营业成本": 15000000000,
            "净利润": 78000000000,
            "毛利润": 130000000000,
        },
        "现金流量表": {
            "经营活动现金流": 85000000000,
            "投资活动现金流": -12000000000,
            "筹资活动现金流": -35000000000,
        },
    }
}


def get_company_info(company_name: str) -> Dict:
    """获取公司基本信息"""
    # TODO: 接入真实API（东方财富、同花顺、Wind等）
    return {
        "公司名称": company_name,
        "股票代码": SAMPLE_DATA.get(company_name, {}).get("股票代码", "N/A"),
        "行业": "白酒",
        "上市日期": "2001-08-27",
        "注册资本": "12.56亿",
    }


def get_financial_data(company_name: str, period: str) -> Dict:
    """获取财务数据"""
    # TODO: 接入真实API
    data = SAMPLE_DATA.get(company_name)
    if not data:
        raise ValueError(f"未找到 {company_name} 的财务数据")
    return data


def calculate_financial_ratios(financial_data: Dict) -> Dict:
    """计算财务指标"""
    balance_sheet = financial_data["资产负债表"]
    income_statement = financial_data["利润表"]
    cash_flow = financial_data["现金流量表"]

    # 盈利能力指标
    roe = income_statement["净利润"] / balance_sheet["股东权益"] * 100
    roa = income_statement["净利润"] / balance_sheet["总资产"] * 100
    gross_margin = income_statement["毛利润"] / income_statement["营业收入"] * 100
    net_margin = income_statement["净利润"] / income_statement["营业收入"] * 100

    # 偿债能力指标
    asset_liability_ratio = balance_sheet["总负债"] / balance_sheet["总资产"] * 100
    current_ratio = balance_sheet["流动资产"] / balance_sheet["流动负债"]
    quick_ratio = (balance_sheet["流动资产"] - 0) / balance_sheet["流动负债"]  # 简化计算

    # 运营能力指标（需要更多数据，这里简化）
    asset_turnover = income_statement["营业收入"] / balance_sheet["总资产"]

    # 现金流指标
    operating_cash_to_net_profit = cash_flow["经营活动现金流"] / income_statement["净利润"]

    return {
        "盈利能力": {
            "ROE(净资产收益率)": f"{roe:.2f}%",
            "ROA(总资产收益率)": f"{roa:.2f}%",
            "毛利率": f"{gross_margin:.2f}%",
            "净利率": f"{net_margin:.2f}%",
        },
        "偿债能力": {
            "资产负债率": f"{asset_liability_ratio:.2f}%",
            "流动比率": f"{current_ratio:.2f}",
            "速动比率": f"{quick_ratio:.2f}",
        },
        "运营能力": {
            "总资产周转率": f"{asset_turnover:.2f}",
        },
        "现金流": {
            "经营现金流/净利润": f"{operating_cash_to_net_profit:.2f}",
        },
    }


def analyze_risks(financial_data: Dict, ratios: Dict) -> List[Dict]:
    """风险分析"""
    risks = []

    # 检查资产负债率
    debt_ratio = float(ratios["偿债能力"]["资产负债率"].replace("%", ""))
    if debt_ratio > 70:
        risks.append(
            {
                "类型": "偿债风险",
                "等级": "高",
                "描述": f"资产负债率为{debt_ratio:.2f}%，高于70%警戒线",
                "建议": "关注公司债务结构和偿债能力",
            }
        )
    elif debt_ratio > 50:
        risks.append(
            {
                "类型": "偿债风险",
                "等级": "中",
                "描述": f"资产负债率为{debt_ratio:.2f}%，处于中等水平",
                "建议": "需关注债务变化趋势",
            }
        )

    # 检查现金流
    cash_ratio = float(ratios["现金流"]["经营现金流/净利润"])
    if cash_ratio < 0.8:
        risks.append(
            {
                "类型": "现金流风险",
                "等级": "高",
                "描述": "经营活动现金流/净利润低于0.8，利润质量存疑",
                "建议": "关注应收账款和存货情况",
            }
        )

    return risks


def generate_investment_advice(ratios: Dict, risks: List[Dict]) -> Dict:
    """生成投资建议"""
    # 简单评分模型
    score = 100

    # 扣分项
    for risk in risks:
        if risk["等级"] == "高":
            score -= 20
        elif risk["等级"] == "中":
            score -= 10

    # ROE加分
    roe = float(ratios["盈利能力"]["ROE(净资产收益率)"].replace("%", ""))
    if roe > 20:
        score += 10

    # 评级
    if score >= 90:
        rating = "优秀"
        advice = "公司财务状况优秀，具备投资价值"
    elif score >= 70:
        rating = "良好"
        advice = "公司财务状况良好，可考虑投资"
    elif score >= 60:
        rating = "一般"
        advice = "公司财务状况一般，需谨慎投资"
    else:
        rating = "较差"
        advice = "公司财务状况较差，不建议投资"

    return {
        "综合评分": score,
        "评级": rating,
        "投资建议": advice,
    }


def analyze_report(company_name: str, period: str = "最新年报") -> Dict:
    """主分析函数"""
    try:
        # 1. 获取数据
        company_info = get_company_info(company_name)
        financial_data = get_financial_data(company_name, period)

        # 2. 计算指标
        ratios = calculate_financial_ratios(financial_data)

        # 3. 风险分析
        risks = analyze_risks(financial_data, ratios)

        # 4. 投资建议
        advice = generate_investment_advice(ratios, risks)

        # 5. 生成报告
        report = {
            "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "公司信息": company_info,
            "报告期": financial_data["报告期"],
            "财务指标": ratios,
            "风险提示": risks if risks else [{"类型": "无明显风险", "等级": "低", "描述": "未发现重大财务风险", "建议": "继续保持关注"}],
            "投资建议": advice,
        }

        return report

    except Exception as e:
        return {"错误": str(e)}


def format_report(report: Dict) -> str:
    """格式化报告为文本"""
    lines = []
    lines.append("=" * 50)
    lines.append("财务分析报告")
    lines.append("=" * 50)
    lines.append(f"\n【公司信息】")
    for key, value in report["公司信息"].items():
        lines.append(f"  {key}: {value}")

    lines.append(f"\n【报告期】{report['报告期']}")

    lines.append(f"\n【财务指标】")
    for category, metrics in report["财务指标"].items():
        lines.append(f"\n  {category}:")
        for key, value in metrics.items():
            lines.append(f"    - {key}: {value}")

    lines.append(f"\n【风险提示】")
    for risk in report["风险提示"]:
        lines.append(f"  - [{risk['等级']}] {risk['类型']}: {risk['描述']}")
        lines.append(f"    建议: {risk['建议']}")

    lines.append(f"\n【投资建议】")
    advice = report["投资建议"]
    lines.append(f"  综合评分: {advice['综合评分']}分")
    lines.append(f"  评级: {advice['评级']}")
    lines.append(f"  建议: {advice['投资建议']}")

    lines.append("\n" + "=" * 50)
    lines.append("免责声明: 本报告仅供参考，不构成投资建议")
    lines.append("=" * 50)

    return "\n".join(lines)


if __name__ == "__main__":
    # 命令行调用
    if len(sys.argv) < 2:
        print("用法: python analysis.py <公司名称> [报告期]")
        print("示例: python analysis.py 贵州茅台 2025年年报")
        sys.exit(1)

    company_name = sys.argv[1]
    period = sys.argv[2] if len(sys.argv) > 2 else "最新年报"

    report = analyze_report(company_name, period)
    print(format_report(report))
