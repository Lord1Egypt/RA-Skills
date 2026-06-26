#!/usr/bin/env python3
"""
cashflow-pilot 现金流预测模块（付费版）

基于历史数据使用移动平均和线性回归进行未来现金流预测，
提供风险预警和趋势判断。
"""

import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    check_subscription,
    create_parser,
    format_currency,
    format_percentage,
    load_input_data,
    load_ledger,
    output_error,
    output_success,
    require_paid,
)


# ============================================================
# 数据准备
# ============================================================

def prepare_monthly_series(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """将账本记录汇总为按月排序的时间序列。

    Args:
        records: 账本记录列表。

    Returns:
        按月排序的汇总数据列表，每项包含 period, income, expense, net。
    """
    monthly = defaultdict(lambda: {"income": 0.0, "expense": 0.0})

    for r in records:
        date_str = r.get("date", "")
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            key = f"{dt.year}-{dt.month:02d}"
        except (ValueError, TypeError):
            continue

        amount = float(r.get("amount", 0))
        txn_type = r.get("type", "unknown")

        if txn_type == "income":
            monthly[key]["income"] += amount
        elif txn_type == "expense":
            monthly[key]["expense"] += amount

    # 按时间排序
    series = []
    for key in sorted(monthly.keys()):
        data = monthly[key]
        series.append({
            "period": key,
            "income": round(data["income"], 2),
            "expense": round(data["expense"], 2),
            "net": round(data["income"] - data["expense"], 2),
        })

    return series


# ============================================================
# 预测算法
# ============================================================

def moving_average(values: List[float], window: int = 3) -> float:
    """计算移动平均值。

    Args:
        values: 历史数值序列。
        window: 窗口大小，默认 3。

    Returns:
        移动平均值。
    """
    if not values:
        return 0.0

    window = min(window, len(values))
    return sum(values[-window:]) / window


def linear_regression(values: List[float]) -> Tuple[float, float]:
    """简单线性回归，返回斜率和截距。

    使用最小二乘法拟合 y = a * x + b。

    Args:
        values: 历史数值序列（y 值，x 值为 0, 1, 2, ...）。

    Returns:
        (斜率 a, 截距 b) 元组。
    """
    n = len(values)
    if n < 2:
        return 0.0, values[0] if values else 0.0

    x_vals = list(range(n))
    x_mean = sum(x_vals) / n
    y_mean = sum(values) / n

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, values))
    denominator = sum((x - x_mean) ** 2 for x in x_vals)

    if denominator == 0:
        return 0.0, y_mean

    a = numerator / denominator
    b = y_mean - a * x_mean

    return a, b


def predict_values(
    values: List[float], months_ahead: int = 3, method: str = "combined"
) -> List[Dict[str, Any]]:
    """预测未来 N 个月的数值。

    Args:
        values: 历史数值序列。
        months_ahead: 预测月数，默认 3。
        method: 预测方法，"ma"（移动平均）、"lr"（线性回归）、"combined"（加权组合）。

    Returns:
        预测结果列表。
    """
    if not values:
        return [{"month_offset": i + 1, "predicted": 0.0, "method": method}
                for i in range(months_ahead)]

    predictions = []
    n = len(values)

    for i in range(months_ahead):
        if method == "ma":
            pred = moving_average(values, window=3)
        elif method == "lr":
            a, b = linear_regression(values)
            pred = a * (n + i) + b
        else:  # combined
            ma_pred = moving_average(values, window=3)
            a, b = linear_regression(values)
            lr_pred = a * (n + i) + b
            # 加权组合：移动平均 40%，线性回归 60%
            pred = ma_pred * 0.4 + lr_pred * 0.6

        pred = max(pred, 0)  # 不允许负值预测
        predictions.append({
            "month_offset": i + 1,
            "predicted": round(pred, 2),
            "method": method,
        })

        # 将预测值加入序列以支持递推预测
        values = values + [pred]

    return predictions


# ============================================================
# 风险预警
# ============================================================

def assess_risk(
    series: List[Dict[str, Any]],
    predictions: Dict[str, List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """评估现金流风险。

    Args:
        series: 历史月度数据序列。
        predictions: 预测结果（包含 income 和 expense 的预测）。

    Returns:
        风险预警列表。
    """
    warnings = []

    # 检查预测净现金流是否为负
    income_preds = predictions.get("income", [])
    expense_preds = predictions.get("expense", [])

    for i in range(min(len(income_preds), len(expense_preds))):
        inc = income_preds[i]["predicted"]
        exp = expense_preds[i]["predicted"]
        net = inc - exp

        if net < 0:
            warnings.append({
                "level": "高",
                "month_offset": i + 1,
                "message": (
                    f"预测第 {i + 1} 个月净现金流为负（{format_currency(net)}），"
                    f"预测收入 {format_currency(inc)}，支出 {format_currency(exp)}。"
                    "建议提前做好资金储备或催收应收款。"
                ),
            })

    # 检查支出增长趋势
    if len(series) >= 3:
        recent_expenses = [s["expense"] for s in series[-3:]]
        if all(recent_expenses[i] < recent_expenses[i + 1] for i in range(len(recent_expenses) - 1)):
            growth_rate = (recent_expenses[-1] - recent_expenses[0]) / recent_expenses[0] if recent_expenses[0] > 0 else 0
            if growth_rate > 0.2:
                warnings.append({
                    "level": "中",
                    "month_offset": 0,
                    "message": (
                        f"支出连续3个月增长，累计增幅 {format_percentage(growth_rate)}。"
                        "建议审视支出结构，控制非必要开支。"
                    ),
                })

    # 检查收入波动
    if len(series) >= 4:
        incomes = [s["income"] for s in series[-4:]]
        avg_income = sum(incomes) / len(incomes)
        if avg_income > 0:
            variance = sum((x - avg_income) ** 2 for x in incomes) / len(incomes)
            std_dev = math.sqrt(variance)
            cv = std_dev / avg_income
            if cv > 0.3:
                warnings.append({
                    "level": "中",
                    "month_offset": 0,
                    "message": (
                        f"收入波动较大（变异系数 {cv:.2f}），"
                        "建议建立至少2个月支出的现金储备。"
                    ),
                })

    return warnings


# ============================================================
# 预测报告生成
# ============================================================

def generate_forecast(
    records: List[Dict[str, Any]], months_ahead: int = 3
) -> Dict[str, Any]:
    """生成完整的现金流预测报告。

    Args:
        records: 账本记录列表。
        months_ahead: 预测月数，默认 3。

    Returns:
        预测报告数据字典。
    """
    series = prepare_monthly_series(records)

    if len(series) < 2:
        return {
            "error": "历史数据不足，至少需要2个月的数据才能进行预测。",
            "months_available": len(series),
        }

    # 分别预测收入和支出
    income_values = [s["income"] for s in series]
    expense_values = [s["expense"] for s in series]
    net_values = [s["net"] for s in series]

    income_forecast = predict_values(income_values, months_ahead)
    expense_forecast = predict_values(expense_values, months_ahead)
    net_forecast = predict_values(net_values, months_ahead)

    # 计算预测期间的标签
    last_period = series[-1]["period"]
    last_year, last_month = map(int, last_period.split("-"))

    for forecasts in [income_forecast, expense_forecast, net_forecast]:
        for f in forecasts:
            m = last_month + f["month_offset"]
            y = last_year
            while m > 12:
                m -= 12
                y += 1
            f["period"] = f"{y}-{m:02d}"

    # 风险评估
    risk_warnings = assess_risk(
        series,
        {"income": income_forecast, "expense": expense_forecast},
    )

    # 生成 Mermaid 图表
    mermaid_chart = _build_forecast_chart(series, income_forecast, expense_forecast)

    # 汇总
    total_pred_income = sum(f["predicted"] for f in income_forecast)
    total_pred_expense = sum(f["predicted"] for f in expense_forecast)
    total_pred_net = total_pred_income - total_pred_expense

    report = {
        "forecast_months": months_ahead,
        "historical_months": len(series),
        "income_forecast": income_forecast,
        "expense_forecast": expense_forecast,
        "net_forecast": net_forecast,
        "total_predicted_income": round(total_pred_income, 2),
        "total_predicted_expense": round(total_pred_expense, 2),
        "total_predicted_net": round(total_pred_net, 2),
        "risk_warnings": risk_warnings,
        "mermaid_chart": mermaid_chart,
        "markdown": _render_forecast_markdown(
            income_forecast, expense_forecast, net_forecast,
            risk_warnings, mermaid_chart, months_ahead,
        ),
    }

    return report


def _build_forecast_chart(
    series: List[Dict[str, Any]],
    income_forecast: List[Dict[str, Any]],
    expense_forecast: List[Dict[str, Any]],
) -> str:
    """生成预测趋势图 Mermaid 代码。"""
    # 取最近3个月历史 + 预测数据
    recent = series[-3:] if len(series) >= 3 else series

    all_periods = [s["period"] for s in recent] + [f["period"] for f in income_forecast]
    income_data = [s["income"] for s in recent] + [f["predicted"] for f in income_forecast]
    expense_data = [s["expense"] for s in recent] + [f["predicted"] for f in expense_forecast]

    lines = [
        "```mermaid",
        "xychart-beta",
        '    title "现金流预测趋势"',
        '    x-axis [' + ", ".join(f'"{p}"' for p in all_periods) + "]",
        '    y-axis "金额（元）"',
        "    line [" + ", ".join(str(round(v, 0)) for v in income_data) + "]",
        "    line [" + ", ".join(str(round(v, 0)) for v in expense_data) + "]",
        "```",
    ]
    return "\n".join(lines)


def _render_forecast_markdown(
    income_forecast: List[Dict[str, Any]],
    expense_forecast: List[Dict[str, Any]],
    net_forecast: List[Dict[str, Any]],
    risk_warnings: List[Dict[str, Any]],
    mermaid_chart: str,
    months: int,
) -> str:
    """渲染预测报告为 Markdown 格式。"""
    lines = [
        f"# 现金流预测报告（未来{months}个月）\n",
        "## 预测概览\n",
        "| 月份 | 预测收入 | 预测支出 | 预测净现金流 |\n",
        "|------|--------:|--------:|-----------:|\n",
    ]

    for i in range(len(income_forecast)):
        period = income_forecast[i]["period"]
        inc = format_currency(income_forecast[i]["predicted"])
        exp = format_currency(expense_forecast[i]["predicted"])
        net = format_currency(net_forecast[i]["predicted"])
        lines.append(f"| {period} | {inc} | {exp} | {net} |\n")

    if mermaid_chart:
        lines.extend(["\n## 趋势预测图\n", mermaid_chart, "\n"])

    if risk_warnings:
        lines.append("\n## 风险预警\n")
        for w in risk_warnings:
            level_icon = {"高": "!!!", "中": "!!", "低": "!"}.get(w["level"], "!")
            lines.append(f"- [{level_icon} {w['level']}风险] {w['message']}\n")
    else:
        lines.append("\n## 风险评估\n\n当前现金流状况良好，未检测到显著风险。\n")

    lines.append("\n---\n*预测由 cashflow-pilot 基于历史数据生成，仅供参考*\n")
    return "".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    """主入口函数。"""
    parser = create_parser("cashflow-pilot 现金流预测工具（付费版）")
    parser.add_argument("--months", type=int, default=3, help="预测月数，默认 3")

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    try:
        if args.action == "predict":
            if not require_paid("现金流预测"):
                return

            # 加载数据
            data = load_input_data(args)
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict) and "records" in data:
                records = data["records"]
            else:
                records = load_ledger()

            if not records:
                output_error("没有可用的账本数据，请先导入账单。", "NO_DATA")
                return

            forecast = generate_forecast(records, args.months)
            output_success(forecast)

        else:
            output_error(
                f"不支持的操作: {args.action}。支持的操作: predict",
                "INVALID_ACTION",
            )

    except ValueError as e:
        output_error(str(e), "FORECAST_ERROR")
    except Exception as e:
        output_error(f"预测执行失败: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    main()
