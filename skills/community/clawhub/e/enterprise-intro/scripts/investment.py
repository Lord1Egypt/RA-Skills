#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投融资事件一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base import call_api, debug_print


# ============ API 调用 ============

def _call_investment_api(entname: str) -> Dict[str, Any]:
    """调用股权投融资 API"""
    response = call_api('/invevents', {'entname': entname}, method='GET')
    return response


# ============ 数据处理 ============

def _process_api_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理 API 返回的数据"""
    invevents = response.get('INVEVENTS', {})

    financing = invevents.get('FINANCING', [])
    investment = invevents.get('INVESTMENT', [])

    # 当前时间和三年前时间
    today = datetime.today()
    three_years_ago = today - timedelta(days=3*365)

    def is_recent(date_str: str) -> bool:
        """判断披露日期是否在三年内"""
        if not date_str:
            return False
        try:
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            return date_obj >= three_years_ago
        except ValueError:
            return False

    # 处理融资事件（全部保留）
    filtered_financing = [
        {
            "披露日期": item.get("DECLAREDATE", ""),
            "事件全称": item.get("EVENTNAME", ""),
            "投资方名称": item.get("INVNAME", ""),
            "投资方名称全称": item.get("INVNAME_ALL", ""),
            "投资性质/轮次（中文）": item.get("INVNATURE_NAME", ""),
            "投资股权比例（%）": item.get("INVEQUITYR", ""),
            "投资金额（万元）": item.get("INVAMT", ""),
            "投资金额级别": item.get("INVAMT2", ""),
            "币种中文": item.get("CURNAME", ""),
            "企业阶段": item.get("COMPSTAGE", "")
        }
        for item in financing
    ]

    # 处理投资事件（筛选最近三年）
    filtered_investment = [
        {
            "披露日期": item.get("DECLAREDATE", ""),
            "事件全称": item.get("EVENTNAME", ""),
            "投资方名称": item.get("INVNAME", ""),
            "投资方名称全称": item.get("INVNAME_ALL", ""),
            "融资方名称": item.get("FINNAME", ""),
            "融资方名称全称": item.get("FINNAME_ALL", ""),
            "投资性质/轮次（中文）": item.get("INVNATURE_NAME", ""),
            "投资股权比例（%）": item.get("INVEQUITYR", ""),
            "投资金额（万元）": item.get("INVAMT", ""),
            "投资金额级别": item.get("INVAMT2", ""),
            "币种中文": item.get("CURNAME", ""),
            "企业阶段": item.get("COMPSTAGE", "")
        }
        for item in investment
        if is_recent(item.get("DECLAREDATE"))
    ]

    return {
        "融资事件": filtered_financing,
        "投资事件": filtered_investment
    }


# ============ Markdown 格式化 ============

def _extract_enterprise_summary(events: List[Dict]) -> str:
    """企业概要"""
    lines = ["### 企业概要"]

    for event in events:
        stage = event.get('企业阶段', '')
        date = event.get('披露日期', '')
        if stage:
            lines.append(f"企业发展阶段判定依据：{stage}（披露日期：{date}）")
            return '\n'.join(lines)

    lines.append("企业发展阶段判定依据：无相关数据")
    return '\n'.join(lines)


def _extract_enterprise_history(events: List[Dict]) -> str:
    """企业历程"""
    if not events:
        return "### 企业历程\n无相关数据"

    lines = ["### 企业历程"]

    # 按时间正序排列
    sorted_events = sorted(events, key=lambda x: x.get('披露日期', ''))

    # 投融资时间线
    dates = [e.get('披露日期', '') for e in sorted_events if e.get('披露日期')]
    if dates:
        lines.append(f"投融资时间线：{'、'.join(dates)}")

    # 事件类型与规模
    event_details = []
    for e in sorted_events:
        event_name = e.get('事件全称', '')
        amount = e.get('投资金额（万元）', '')
        if event_name and amount:
            event_details.append(f"{event_name}（{amount}万元）")

    if event_details:
        lines.append(f"事件类型与规模：{'、'.join(event_details)}")

    # 融资轮次演进
    rounds = [e.get('投资性质/轮次（中文）', '') for e in sorted_events if e.get('投资性质/轮次（中文）')]
    if rounds:
        lines.append(f"融资轮次演进：{'、'.join(rounds)}")

    return '\n'.join(lines)


def _extract_equity_governance(events: List[Dict]) -> str:
    """股权与治理"""
    if not events:
        return "### 股权与治理\n无相关数据"

    lines = ["### 股权与治理"]

    # 投资方背景分析 - 按时间正序
    sorted_events = sorted(events, key=lambda x: x.get('披露日期', ''))
    investors = []
    for e in sorted_events:
        investor_full = e.get('投资方名称全称', '')
        if investor_full and investor_full not in investors:
            investors.append(investor_full)

    if investors:
        lines.append(f"投资方背景分析：{'、'.join(investors)}")

    # 股权变动情况（只取有股权比例的）
    equity_changes = []
    for e in events:
        investor_full = e.get('投资方名称全称', '')
        ratio = e.get('投资股权比例（%）', '')
        date = e.get('披露日期', '')
        if investor_full and ratio:
            equity_changes.append(f"{investor_full}投资股权比例{ratio}（披露日期：{date}）")

    if equity_changes:
        lines.append(f"股权变动情况：{'、'.join(equity_changes)}")

    # 投资比例统计（只取有股权比例的）
    ratio_stats = []
    for e in events:
        investor_full = e.get('投资方名称全称', '')
        ratio = e.get('投资股权比例（%）', '')
        if investor_full and ratio:
            ratio_stats.append(f"{investor_full}{ratio}")

    if ratio_stats:
        lines.append(f"投资比例统计：{'、'.join(ratio_stats)}")

    return '\n'.join(lines)


def _extract_market_competitiveness(events: List[Dict]) -> str:
    """市场竞争力"""
    if not events:
        return "### 市场竞争力\n无相关数据"

    lines = ["### 市场竞争力"]

    # 融资能力指标 - 按时间正序
    sorted_events = sorted(events, key=lambda x: x.get('披露日期', ''))
    amounts = [e.get('投资金额（万元）', '') for e in sorted_events if e.get('投资金额（万元）')]
    if amounts:
        lines.append(f"融资能力指标：{'、'.join([f'{a}万元' for a in amounts])}")

    # 投资规模等级
    levels = [e.get('投资金额级别', '') for e in events if e.get('投资金额级别')]
    if levels:
        lines.append(f"投资规模等级：{'、'.join(levels)}")
    else:
        lines.append("投资规模等级：无相关数据")

    # 资本市场认可度
    rounds = [e.get('投资性质/轮次（中文）', '') for e in sorted(events, key=lambda x: x.get('披露日期', '')) if e.get('投资性质/轮次（中文）')]
    if rounds:
        lines.append(f"资本市场认可度：{'、'.join(rounds)}")

    return '\n'.join(lines)


def _extract_operation_capital(events: List[Dict]) -> str:
    """经营与资本"""
    if not events:
        return "### 经营与资本\n无相关数据"

    lines = ["### 经营与资本"]

    # 融资金额统计 - 按时间正序
    sorted_events = sorted(events, key=lambda x: x.get('披露日期', ''))
    amounts = [e.get('投资金额（万元）', '') for e in sorted_events if e.get('投资金额（万元）')]
    if amounts:
        lines.append(f"融资金额统计：{'、'.join([f'{a}万元' for a in amounts])}")

    # 币种分布
    currencies = []
    for e in events:
        currency = e.get('币种中文', '')
        date = e.get('披露日期', '')
        if currency:
            currencies.append(f"{currency}（披露日期：{date}）")

    if currencies:
        lines.append(f"币种分布：{'、'.join(currencies)}")

    # 发展阶段资金需求
    stage_demands = []
    for e in events:
        stage = e.get('企业阶段', '')
        amount = e.get('投资金额（万元）', '')
        date = e.get('披露日期', '')
        if stage and amount:
            stage_demands.append(f"{stage}（{amount}万元，披露日期：{date}）")

    if stage_demands:
        lines.append(f"发展阶段资金需求：{'、'.join(stage_demands)}")

    # 融资轮次特征
    rounds = [e.get('投资性质/轮次（中文）', '') for e in sorted(events, key=lambda x: x.get('披露日期', '')) if e.get('投资性质/轮次（中文）')]
    if rounds:
        lines.append(f"融资轮次特征：{'、'.join(rounds)}")

    return '\n'.join(lines)


def _extract_value_growth(events: List[Dict]) -> str:
    """价值与成长"""
    if not events:
        return "### 价值与成长\n无相关数据"

    lines = ["### 价值与成长"]

    # 成长阶段标识
    for e in events:
        stage = e.get('企业阶段', '')
        date = e.get('披露日期', '')
        if stage:
            lines.append(f"成长阶段标识：{stage}（披露日期：{date}）")
            break

    # 融资进度分析
    sorted_events = sorted(events, key=lambda x: x.get('披露日期', ''))
    progress = []
    for e in sorted_events:
        round_type = e.get('投资性质/轮次（中文）', '')
        amount = e.get('投资金额（万元）', '')
        if round_type and amount:
            progress.append(f"{round_type}（{amount}万元）")

    if progress:
        lines.append(f"融资进度分析：{'、'.join(progress)}")

    # 价值评估依据 - 按时间正序
    amounts = [e.get('投资金额（万元）', '') for e in sorted_events if e.get('投资金额（万元）')]
    if amounts:
        lines.append(f"价值评估依据：{'、'.join([f'{a}万元' for a in amounts])}")

    return '\n'.join(lines)


def _extract_enterprise_association(events: List[Dict]) -> str:
    """企业关联分析"""
    if not events:
        return "### 企业关联分析\n无相关数据"

    lines = ["### 企业关联分析"]

    # 投资关系网络 - 按时间正序
    sorted_events = sorted(events, key=lambda x: x.get('披露日期', ''))
    investors = []
    for e in sorted_events:
        investor_full = e.get('投资方名称全称', '')
        if investor_full and investor_full not in investors:
            investors.append(investor_full)

    if investors:
        lines.append(f"投资关系网络：{'、'.join(investors)}")

    # 股权投资结构
    structures = []
    for e in events:
        investor_full = e.get('投资方名称全称', '')
        ratio = e.get('投资股权比例（%）', '')
        date = e.get('披露日期', '')
        if investor_full and ratio:
            structures.append(f"{investor_full}投资{ratio}（披露日期：{date}）")

    if structures:
        lines.append(f"股权投资结构：{'、'.join(structures)}")

    return '\n'.join(lines)


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    financing_events = data.get('融资事件', [])
    investment_events = data.get('投资事件', [])

    if not financing_events and not investment_events:
        return "# 投融资事件\n\n暂无投融资事件数据"

    sections = ["# 投融资事件提炼"]

    # 主要使用融资事件数据
    if financing_events:
        sections.append("")
        sections.append(_extract_enterprise_summary(financing_events))
        sections.append("")
        sections.append(_extract_enterprise_history(financing_events))
        sections.append("")
        sections.append(_extract_equity_governance(financing_events))
        sections.append("")
        sections.append(_extract_market_competitiveness(financing_events))
        sections.append("")
        sections.append(_extract_operation_capital(financing_events))
        sections.append("")
        sections.append(_extract_value_growth(financing_events))
        sections.append("")
        sections.append(_extract_enterprise_association(financing_events))

    # 如果有投资事件，单独列出
    if investment_events:
        sections.append("")
        sections.append("### 对外投资事件")
        sorted_inv = sorted(investment_events, key=lambda x: x.get('披露日期', ''), reverse=True)
        for event in sorted_inv[:10]:
            date = event.get('披露日期', '')
            name = event.get('事件全称', '')
            target = event.get('融资方名称全称', '') or event.get('融资方名称', '')
            amount = event.get('投资金额（万元）', '')
            round_type = event.get('投资性质/轮次（中文）', '')

            parts = []
            if date:
                parts.append(f"披露日期：{date}")
            if name:
                parts.append(f"事件：{name}")
            if target:
                parts.append(f"融资方：{target}")
            if amount:
                parts.append(f"金额：{amount}万元")
            if round_type:
                parts.append(f"轮次：{round_type}")

            if parts:
                sections.append(f"- {', '.join(parts)}")

    sections.append("")
    sections.append("注：查询结果仅反映企业外部公开的投融资事件信息，不代表企业投融资历程全貌。")

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业投融资事件信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的投融资事件信息
    """
    # 1. 调用 API
    response = _call_investment_api(entname)

    # 检查响应
    if not response or not response.get('INVEVENTS'):
        return "# 投融资事件\n\n未查询到企业股权投融资信息"

    # 2. 处理数据
    processed_data = _process_api_data(response)

    if not processed_data.get('融资事件') and not processed_data.get('投资事件'):
        return "# 投融资事件\n\n暂无投融资事件数据"

    # 3. 生成 Markdown
    return _format_markdown(processed_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s12_investment <企业名称>")
