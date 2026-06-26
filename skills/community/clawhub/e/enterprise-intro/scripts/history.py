#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史大数据一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import call_api, debug_print


# ============ 辅助函数 ============

def _format_ratio(value: Any) -> str:
    """格式化投资比例（添加%）"""
    if value and float(value) > 0:
        return f"{value}%"
    return ""


def _format_amount(value: Any) -> str:
    """格式化投资数额（添加万）"""
    if value and float(value) > 0:
        return f"{value}万"
    return ""


def _format_listed_status(value: Any) -> str:
    """将是否上市状态码转换为中文"""
    if str(value) == "0":
        return "未上市"
    elif str(value) == "1":
        return "上市"
    return str(value) if value else ""


# ============ API 调用 ============

def _call_entinfo_api(entname: str) -> Dict[str, Any]:
    """调用企业基本信息 API（用于获取成立日期）"""
    response = call_api('/entinfo', {'name': entname}, method='GET')
    return response


def _call_history_api(entname: str) -> Dict[str, Any]:
    """调用历史大数据 API"""
    response = call_api('/historical/historicalBigData', {'entname': entname, 'size': 100}, method='GET')
    return response


def _get_establishment_date(entname: str) -> str:
    """获取企业成立日期"""
    try:
        entinfo_result = _call_entinfo_api(entname)
        if isinstance(entinfo_result, dict) and 'ENT_INFO' in entinfo_result:
            ent_info = entinfo_result['ENT_INFO']
            if 'BASIC' in ent_info and isinstance(ent_info['BASIC'], dict):
                basic_data = ent_info['BASIC']
                return basic_data.get('ESDATE', '')
    except Exception:
        pass
    return ""


# ============ 数据处理 ============

def _process_api_data(response: Dict[str, Any], establishment_date: str) -> Dict[str, Any]:
    """处理 API 返回的数据"""
    content = response.get('data', {})
    page_info = content.get('page_info', {})

    result = {
        "历史数据统计": {
            "曾用名数量": page_info.get('his_entname', {}).get('totalcount', 0),
            "企业地址变更记录次数": page_info.get('his_address', {}).get('totalcount', 0),
            "注册资本变更记录次数": page_info.get('his_regcap', {}).get('totalcount', 0),
            "企业类型变更记录次数": page_info.get('his_enttype', {}).get('totalcount', 0),
            "法定代表人变更记录次数": page_info.get('his_legal_person', {}).get('totalcount', 0),
            "历史管理人员数量": page_info.get('his_ent_person', {}).get('totalcount', 0),
            "历史股东数量": page_info.get('his_ent_stockholder', {}).get('totalcount', 0),
            "历史对外投资过的企业数量": page_info.get('his_ent_investor', {}).get('totalcount', 0),
            "历史对外投资过的合计投资数额": _format_amount(page_info.get('his_ent_investor', {}).get('total_subconam_amount', ''))
        },
        "企业成立日期": establishment_date,
        "曾用名": [],
        "历史企业地址": [],
        "历史注册资本": [],
        "历史企业类型": [],
        "历史法定代表人": [],
        "历史管理人员": [],
        "历史股东信息": [],
        "历史对外投资": []
    }

    # 处理曾用名
    if 'his_entname' in content:
        for item in content['his_entname']:
            result["曾用名"].append({
                "曾用名": item.get('entname', ''),
                "曾用名变更开始日期": item.get('start_date', ''),
                "曾用名变更结束日期": item.get('end_date', '')
            })

    # 处理历史企业地址
    if 'his_address' in content:
        for item in content['his_address']:
            result["历史企业地址"].append({
                "历史企业地址": item.get('address', ''),
                "历史企业地址变更开始日期": item.get('start_date', ''),
                "历史企业地址变更结束日期": item.get('end_date', '')
            })

    # 处理历史注册资本
    if 'his_regcap' in content:
        for item in content['his_regcap']:
            regcap = item.get('regcap', '')
            if regcap and not str(regcap).endswith('万元'):
                regcap = f"{regcap}万元"
            result["历史注册资本"].append({
                "历史注册资本(企业:万元)": regcap,
                "历史注册资本币种": item.get('regcapcur', ''),
                "历史注册资本变更开始日期": item.get('start_date', ''),
                "历史注册资本变更结束日期": item.get('end_date', '')
            })

    # 处理历史企业类型
    if 'his_enttype' in content:
        for item in content['his_enttype']:
            result["历史企业类型"].append({
                "历史企业类型": item.get('enttype', ''),
                "历史企业类型变更开始日期": item.get('start_date', ''),
                "历史企业类型变更结束日期": item.get('end_date', '')
            })

    # 处理历史法定代表人
    if 'his_legal_person' in content:
        for item in content['his_legal_person']:
            result["历史法定代表人"].append({
                "历史法定代表人姓名": item.get('name', ''),
                "历史法定代表人任职日期": item.get('start_date', ''),
                "历史法定代表人卸任日期": item.get('end_date', '')
            })

    # 处理历史管理人员
    if 'his_ent_person' in content:
        for item in content['his_ent_person']:
            result["历史管理人员"].append({
                "历史管理人员姓名": item.get('name', ''),
                "历史管理人员职位": item.get('position', ''),
                "历史管理人员最早任职日期": item.get('start_date', ''),
                "历史管理人员最终卸任日期": item.get('end_date', '')
            })

    # 处理历史股东信息
    if 'his_ent_stockholder' in content:
        for item in content['his_ent_stockholder']:
            result["历史股东信息"].append({
                "历史股东名称": item.get('shaname', ''),
                "历史股东投资比例": _format_ratio(item.get('fundedratio', '')),
                "历史股东投资数额(万)": _format_amount(item.get('subconam', '')),
                "历史股东最早投资日期": item.get('start_date', ''),
                "历史股东最终退出日期": item.get('end_date', '')
            })

    # 处理历史企业对外投资
    if 'his_ent_investor' in content:
        for item in content['his_ent_investor']:
            result["历史对外投资"].append({
                "历史对外投资的企业名": item.get('entname', ''),
                "历史对外投资的企业成立日期": item.get('esdate', ''),
                "历史对外投资的企业经营状态": item.get('entstatus', ''),
                "历史对外投资的企业注册资本(万元)": item.get('regcap', ''),
                "历史对外投资的投资比例": _format_ratio(item.get('fundedratio', '')),
                "历史对外投资的投资数额(万)": _format_amount(item.get('subconam', '')),
                "历史对外投资的企业是否上市": _format_listed_status(item.get('islisted', '')),
                "历史对外投资该企业的最早投资日期": item.get('start_date', ''),
                "历史对外投资该企业的最终退出日期": item.get('end_date', '')
            })

    return result


# ============ Markdown 格式化 ============

def _extract_enterprise_history(data: Dict[str, Any]) -> str:
    """提取企业历程"""
    lines = ["### 企业历程"]

    # 曾用名记录
    former_names = data.get('曾用名', [])
    if former_names:
        name_strs = []
        for name in former_names:
            name_text = name.get('曾用名', '')
            start_date = name.get('曾用名变更开始日期', '')
            end_date = name.get('曾用名变更结束日期', '')
            name_strs.append(f"曾用名: {name_text} ({start_date} 至 {end_date})")
        if name_strs:
            lines.append(f"曾用名记录：{', '.join(name_strs)}")

    # 地址变更记录
    addresses = data.get('历史企业地址', [])
    if addresses:
        addr_strs = []
        for addr in addresses:
            address = addr.get('历史企业地址', '')
            start_date = addr.get('历史企业地址变更开始日期', '')
            end_date = addr.get('历史企业地址变更结束日期', '')
            addr_strs.append(f"地址变更: {address} ({start_date} 至 {end_date})")
        if addr_strs:
            lines.append(f"地址变更记录：{', '.join(addr_strs)}")

    # 注册资本变更记录
    capitals = data.get('历史注册资本', [])
    establish_date = data.get('企业成立日期', '')

    years_since_establishment = 0
    if establish_date:
        try:
            est_date = datetime.strptime(establish_date, '%Y-%m-%d')
            years_since_establishment = (datetime.now() - est_date).days / 365.25
        except Exception:
            pass

    if capitals:
        cap_strs = []
        for cap in capitals:
            capital = cap.get('历史注册资本(企业:万元)', '')
            currency = cap.get('历史注册资本币种', '')
            start_date = cap.get('历史注册资本变更开始日期', '')
            end_date = cap.get('历史注册资本变更结束日期', '')

            # 如果公司成立超过10年，且该变更开始日期等于成立日期，则跳过
            if years_since_establishment > 10 and start_date == establish_date:
                continue

            cap_strs.append(f"注册资本变更: {capital} ({currency}) ({start_date} 至 {end_date})")
        if cap_strs:
            lines.append(f"注册资本变更记录：{', '.join(cap_strs)}")

    # 企业类型变更记录
    types = data.get('历史企业类型', [])
    if types:
        type_strs = []
        for typ in types:
            type_name = typ.get('历史企业类型', '')
            start_date = typ.get('历史企业类型变更开始日期', '')
            end_date = typ.get('历史企业类型变更结束日期', '')
            type_strs.append(f"企业类型变更: {type_name} ({start_date} 至 {end_date})")
        if type_strs:
            lines.append(f"企业类型变更记录：{', '.join(type_strs)}")

    # 法定代表人变更记录
    legal_reps = data.get('历史法定代表人', [])
    if legal_reps:
        rep_strs = []
        for rep in legal_reps:
            name = rep.get('历史法定代表人姓名', '')
            start_date = rep.get('历史法定代表人任职日期', '')
            end_date = rep.get('历史法定代表人卸任日期', '')
            rep_strs.append(f"法定代表人变更: {name} ({start_date} 至 {end_date})")
        if rep_strs:
            lines.append(f"法定代表人变更记录：{', '.join(rep_strs)}")

    # 关键事件统计
    stats = data.get('历史数据统计', {})
    if stats:
        stat_parts = []
        for key, label in [
            ('曾用名数量', '曾用名数量'),
            ('企业地址变更记录次数', '地址变更次数'),
            ('注册资本变更记录次数', '注册资本变更次数'),
            ('企业类型变更记录次数', '企业类型变更次数'),
            ('法定代表人变更记录次数', '法定代表人变更次数')
        ]:
            value = stats.get(key, 0)
            stat_parts.append(f"{label}: {value}")

        if stat_parts:
            lines.append(f"关键事件统计：{', '.join(stat_parts)}")

    return '\n'.join(lines)


def _extract_equity_governance(data: Dict[str, Any]) -> str:
    """提取股权与治理"""
    lines = ["### 股权与治理"]

    # 历史股东信息
    shareholders = data.get('历史股东信息', [])
    if shareholders:
        shareholder_strs = []
        for sh in shareholders:
            name = sh.get('历史股东名称', '')
            ratio = sh.get('历史股东投资比例', '')
            amount = sh.get('历史股东投资数额(万)', '')
            start_date = sh.get('历史股东最早投资日期', '')
            end_date = sh.get('历史股东最终退出日期', '')
            if amount and amount.endswith('万'):
                amount = amount[:-1]
            shareholder_strs.append(f"股东: {name}, 比例: {ratio}, 数额: {amount} 万元 ({start_date} 至 {end_date})")

        if shareholder_strs:
            lines.append(f"历史股东信息：{', '.join(shareholder_strs)}")

    # 历史管理人员
    managers = data.get('历史管理人员', [])
    if managers:
        manager_strs = []
        for mgr in managers:
            name = mgr.get('历史管理人员姓名', '')
            position = mgr.get('历史管理人员职位', '')
            start_date = mgr.get('历史管理人员最早任职日期', '')
            end_date = mgr.get('历史管理人员最终卸任日期', '')
            manager_strs.append(f"管理人员: {name}, 职位: {position} ({start_date} 至 {end_date})")

        if manager_strs:
            lines.append(f"历史管理人员：{', '.join(manager_strs)}")

    # 股东与管理人员统计
    stats = data.get('历史数据统计', {})
    if stats:
        sh_count = stats.get('历史股东数量', 0)
        mgr_count = stats.get('历史管理人员数量', 0)
        lines.append(f"股东与管理人员统计：历史股东数量: {sh_count}, 历史管理人员数量: {mgr_count}")

    return '\n'.join(lines)


def _extract_operation_capital(data: Dict[str, Any]) -> str:
    """提取经营与资本"""
    lines = ["### 经营与资本"]

    # 注册资本变更历史
    stats = data.get('历史数据统计', {})
    capital_changes = stats.get('注册资本变更记录次数', 0)
    lines.append(f"注册资本变更历史：注册资本变更次数: {capital_changes}")

    # 对外投资历史
    investments = data.get('历史对外投资', [])
    if investments:
        investment_strs = []
        for inv in investments:
            name = inv.get('历史对外投资的企业名', '')
            ratio = inv.get('历史对外投资的投资比例', '')
            amount = inv.get('历史对外投资的投资数额(万)', '')
            is_listed = inv.get('历史对外投资的企业是否上市', '')
            start_date = inv.get('历史对外投资该企业的最早投资日期', '')
            end_date = inv.get('历史对外投资该企业的最终退出日期', '')
            investment_strs.append(f"对外投资: {name}, 比例: {ratio}, 数额: {amount} 万元, 上市: {is_listed} ({start_date} 至 {end_date})")

        if investment_strs:
            lines.append(f"对外投资历史：{', '.join(investment_strs)}")

    # 投资总额统计
    if stats:
        inv_count = stats.get('历史对外投资过的企业数量', 0)
        total_amount = stats.get('历史对外投资过的合计投资数额', '')
        if inv_count > 0 or total_amount:
            lines.append(f"投资总额统计：历史对外投资企业数量: {inv_count}, 合计投资数额: {total_amount}")

    return '\n'.join(lines)


def _extract_enterprise_association(data: Dict[str, Any]) -> str:
    """提取企业关联分析"""
    lines = []

    investments = data.get('历史对外投资', [])
    if investments:
        lines.append("### 企业关联分析")

        investment_strs = []
        for inv in investments:
            name = inv.get('历史对外投资的企业名', '')
            status = inv.get('历史对外投资的企业经营状态', '')
            capital = inv.get('历史对外投资的企业注册资本(万元)', '')
            ratio = inv.get('历史对外投资的投资比例', '')
            amount = inv.get('历史对外投资的投资数额(万)', '')
            is_listed = inv.get('历史对外投资的企业是否上市', '')
            start_date = inv.get('历史对外投资该企业的最早投资日期', '')
            end_date = inv.get('历史对外投资该企业的最终退出日期', '')
            investment_strs.append(f"被投资企业: {name}, 状态: {status}, 注册资本: {capital} 万元, 投资比例: {ratio}, 投资数额: {amount} 万元, 上市: {is_listed} ({start_date} 至 {end_date})")

        if investment_strs:
            lines.append(f"历史对外投资企业：{', '.join(investment_strs)}")

        # 关联企业摘要
        stats = data.get('历史数据统计', {})
        inv_count = stats.get('历史对外投资过的企业数量', 0)
        if inv_count > 0:
            lines.append(f"关联企业摘要：关联企业数量: {inv_count}")

    return '\n'.join(lines) if lines else ""


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    sections = ["# 历史大数据提炼"]

    # 企业历程
    sections.append("")
    sections.append(_extract_enterprise_history(data))

    # 股权与治理
    sections.append("")
    sections.append(_extract_equity_governance(data))

    # 经营与资本
    sections.append("")
    sections.append(_extract_operation_capital(data))

    # 企业关联分析（仅在有对外投资时才添加）
    association = _extract_enterprise_association(data)
    if association:
        sections.append("")
        sections.append(association)

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业历史大数据

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的历史大数据信息
    """
    # 1. 调用历史大数据 API
    response = _call_history_api(entname)

    # 检查响应状态
    if response.get('code') != 200:
        return "# 历史大数据\n\n该企业未查得工商历史信息"

    # 2. 获取企业成立日期
    establishment_date = _get_establishment_date(entname)

    # 3. 处理数据
    processed_data = _process_api_data(response, establishment_date)

    if not processed_data:
        return "# 历史大数据\n\n暂无历史数据"

    # 4. 生成 Markdown
    return _format_markdown(processed_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s13_history <企业名称>")
