#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投资任职查询一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional, Tuple
from .base import call_api, debug_print


# ============ API 调用 ============

def _call_entinfo_api(entname: str) -> Dict[str, Any]:
    """调用企业基本信息 API（获取法人名称和企业名称）"""
    response = call_api('/entinfo', {'name': entname}, method='GET')
    return response


def _call_manager_api(entname: str, name: str) -> Dict[str, Any]:
    """调用投资任职查询 API"""
    params = {
        'entmark': entname,
        'name': name,
        'mask': '1110000001000000000'
    }
    response = call_api('/manager/nam', params, method='GET')
    return response


# ============ 数据处理 ============

def _is_active_enterprise(item: Dict) -> bool:
    """判断是否为在营企业"""
    return item.get('ENTSTATUS', '') == '在营（开业）'


def _process_legal_info(raw_data: Dict, entname: str) -> List[Dict]:
    """处理担任法人信息"""
    result = []
    for item in raw_data.get('RYPOSFR', []):
        if not _is_active_enterprise(item):
            continue
        if item.get('ENTNAME', '') == entname:
            continue

        processed_item = {
            '企业名称': item.get('ENTNAME', ''),
            '企业类型': item.get('ENTTYPE', ''),
            '经营状态': item.get('ENTSTATUS', ''),
            '成立日期': item.get('ESDATE', ''),
            '所在城市': item.get('REGORGCITY', ''),
            '行业名称': item.get('INDUSTRYCONAME', ''),
            '经营范围': item.get('ZSOPSCOPE', ''),
            '注册地址': item.get('DOM', '')
        }

        # 个体工商户不返回注册资本
        if item.get('ENTTYPE', '') and '个体' not in item.get('ENTTYPE', ''):
            processed_item['注册资本(万元)'] = item.get('REGCAP', '')
            processed_item['注册资本币种'] = item.get('REGCAPCUR', '')

        result.append(processed_item)
    return result


def _process_investment_info(raw_data: Dict, entname: str) -> List[Dict]:
    """处理投资企业信息"""
    result = []
    for item in raw_data.get('RYPOSSHA', []):
        if not _is_active_enterprise(item):
            continue
        if item.get('ENTNAME', '') == entname:
            continue

        processed_item = {
            '企业名称': item.get('ENTNAME', ''),
            '企业类型': item.get('ENTTYPE', ''),
            '经营状态': item.get('ENTSTATUS', ''),
            '成立日期': item.get('ESDATE', ''),
            '所在城市': item.get('REGORGCITY', ''),
            '行业名称': item.get('INDUSTRYCONAME', ''),
            '经营范围': item.get('ZSOPSCOPE', ''),
            '投资比例': item.get('FUNDEDRATIO', ''),
            '注册地址': item.get('DOM', '')
        }

        # 个体工商户不返回注册资本和上市信息
        if item.get('ENTTYPE', '') and '个体' not in item.get('ENTTYPE', ''):
            processed_item['注册资本(万元)'] = item.get('REGCAP', '')
            processed_item['注册资本币种'] = item.get('REGCAPCUR', '')
            is_listed = item.get('ISLISTED', '0')
            processed_item['是否上市'] = '是' if is_listed == '1' else '否'

        result.append(processed_item)
    return result


def _process_executive_info(raw_data: Dict, entname: str) -> List[Dict]:
    """处理担任高管信息"""
    result = []
    for item in raw_data.get('RYPOSPER', []):
        if not _is_active_enterprise(item):
            continue
        if item.get('ENTNAME', '') == entname:
            continue

        processed_item = {
            '企业名称': item.get('ENTNAME', ''),
            '企业类型': item.get('ENTTYPE', ''),
            '经营状态': item.get('ENTSTATUS', ''),
            '成立日期': item.get('ESDATE', ''),
            '所在城市': item.get('REGORGCITY', ''),
            '行业名称': item.get('INDUSTRYCONAME', ''),
            '经营范围': item.get('ZSOPSCOPE', ''),
            '职务': item.get('POSITION', ''),
            '注册地址': item.get('DOM', '')
        }

        result.append(processed_item)
    return result


def _process_controlled_info(raw_data: Dict, entname: str) -> List[Dict]:
    """处理实际控制企业信息"""
    result = []
    for item in raw_data.get('RYPOSCTE', []):
        if not _is_active_enterprise(item):
            continue
        if item.get('ENTNAME', '') == entname:
            continue

        processed_item = {
            '识别类型': item.get('DISTINGUISH_NAME', ''),
            '企业名称': item.get('ENTNAME', ''),
            '企业类型': item.get('ENTTYPE', ''),
            '经营状态': item.get('ENTSTATUS', ''),
            '成立日期': item.get('ESDATE', ''),
            '所在城市': item.get('REGORGCITY', ''),
            '行业名称': item.get('INDUSTRYCONAME', ''),
            '注册地址': item.get('DOM', '')
        }

        result.append(processed_item)
    return result


def _fetch_investment_data(entname: str) -> Optional[Dict[str, Any]]:
    """获取投资任职数据"""
    # 1. 获取法人名称和企业名称
    entinfo_response = _call_entinfo_api(entname)

    if entinfo_response.get('CODE') != 200:
        return None

    ent_info = entinfo_response.get('ENT_INFO', {})
    basic_info = ent_info.get('BASIC', {})
    fr_name = basic_info.get('FRNAME', '').strip()
    ent_name = basic_info.get('ENTNAME', '').strip()

    if not fr_name:
        return None

    # 2. 查询投资任职信息
    manager_response = _call_manager_api(entname, fr_name)

    if manager_response.get('CODE') != 200:
        return None

    person_info = manager_response.get('PERSON_INFO', {})
    if not person_info:
        return None

    # 3. 处理数据
    result = {
        '企业名称': ent_name,
        '法人名称': fr_name,
        '担任法人信息': _process_legal_info(person_info, entname),
        '投资企业信息': _process_investment_info(person_info, entname),
        '担任高管信息': _process_executive_info(person_info, entname),
        '实际控制企业信息': _process_controlled_info(person_info, entname)
    }

    return result


# ============ Markdown 格式化 ============

def _format_date(date_str: str) -> str:
    """格式化日期"""
    if not date_str:
        return ""
    return date_str[:10] if len(date_str) >= 10 else date_str


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    if not data:
        return "# 投资任职查询\n\n暂无投资任职信息"

    ent_name = data.get('企业名称', '')
    fr_name = data.get('法人名称', '')

    legal_info = data.get('担任法人信息', [])
    invest_info = data.get('投资企业信息', [])
    exec_info = data.get('担任高管信息', [])
    control_info = data.get('实际控制企业信息', [])

    sections = [f"# {ent_name}投资任职信息分析"]

    # 一、法定代表人情况
    sections.append("")
    sections.append("## 一、法定代表人情况")
    sections.append("")
    sections.append(f"- 姓名：{fr_name}")

    # 统计信息
    total_legal = len(legal_info)
    total_invest = len(invest_info)
    total_exec = len(exec_info)
    total_control = len(control_info)

    desc_parts = []
    if total_legal > 0:
        desc_parts.append(f"担任{total_legal}家企业法定代表人")
    if total_invest > 0:
        desc_parts.append(f"对外投资{total_invest}家企业")
    if total_exec > 0:
        desc_parts.append(f"在{total_exec}家企业担任高管")
    if total_control > 0:
        desc_parts.append(f"实际控制{total_control}家企业")

    if desc_parts:
        sections.append(f"- 对外投资与任职：{fr_name}{'、'.join(desc_parts)}")

        # 找出最早投资日期
        all_dates = []
        for item in legal_info:
            date = item.get('成立日期', '')
            if date:
                all_dates.append(date)
        for item in invest_info:
            date = item.get('成立日期', '')
            if date:
                all_dates.append(date)

        if all_dates:
            earliest_date = min(all_dates)
            sections.append(f"- 最早投资日期：{_format_date(earliest_date)}")
    else:
        sections.append(f"- 对外投资与任职：根据现有数据，仅显示其担任{ent_name}的法定代表人，未发现其他对外投资或高管任职信息")

    # 二、担任法人的企业
    if legal_info:
        sections.append("")
        sections.append("## 二、担任法定代表人的企业")
        sections.append("")

        for i, item in enumerate(legal_info[:20], 1):
            name = item.get('企业名称', '')
            ent_type = item.get('企业类型', '')
            city = item.get('所在城市', '')
            industry = item.get('行业名称', '')
            capital = item.get('注册资本(万元)', '')
            currency = item.get('注册资本币种', '')

            desc_parts = [f"**{name}**"]
            if ent_type:
                desc_parts.append(f"类型：{ent_type}")
            if city:
                desc_parts.append(f"城市：{city}")
            if industry:
                desc_parts.append(f"行业：{industry}")
            if capital:
                desc_parts.append(f"注册资本：{capital}万{currency}")

            sections.append(f"{i}. {' | '.join(desc_parts)}")

        if len(legal_info) > 20:
            sections.append(f"\n（共{len(legal_info)}家，仅显示前20家）")

    # 三、投资的企业
    if invest_info:
        sections.append("")
        sections.append("## 三、对外投资企业")
        sections.append("")

        for i, item in enumerate(invest_info[:20], 1):
            name = item.get('企业名称', '')
            ent_type = item.get('企业类型', '')
            ratio = item.get('投资比例', '')
            capital = item.get('注册资本(万元)', '')
            currency = item.get('注册资本币种', '')
            is_listed = item.get('是否上市', '')

            desc_parts = [f"**{name}**"]
            if ratio:
                desc_parts.append(f"投资比例：{ratio}")
            if capital:
                desc_parts.append(f"注册资本：{capital}万{currency}")
            if is_listed == '是':
                desc_parts.append("（上市公司）")

            sections.append(f"{i}. {' | '.join(desc_parts)}")

        if len(invest_info) > 20:
            sections.append(f"\n（共{len(invest_info)}家，仅显示前20家）")

    # 四、担任高管的企业
    if exec_info:
        sections.append("")
        sections.append("## 四、担任高管的企业")
        sections.append("")

        # 按企业分组
        exec_by_company = {}
        for item in exec_info:
            company = item.get('企业名称', '')
            position = item.get('职务', '')
            if company not in exec_by_company:
                exec_by_company[company] = []
            exec_by_company[company].append(position)

        for i, (company, positions) in enumerate(list(exec_by_company.items())[:20], 1):
            positions_str = '、'.join(set(positions))
            sections.append(f"{i}. **{company}**：担任{positions_str}")

        if len(exec_by_company) > 20:
            sections.append(f"\n（共{len(exec_by_company)}家，仅显示前20家）")

    # 五、实际控制企业
    if control_info:
        sections.append("")
        sections.append("## 五、实际控制的企业")
        sections.append("")

        for i, item in enumerate(control_info[:20], 1):
            name = item.get('企业名称', '')
            identify_type = item.get('识别类型', '')
            ent_type = item.get('企业类型', '')
            city = item.get('所在城市', '')

            desc_parts = [f"**{name}**"]
            if identify_type:
                desc_parts.append(f"识别类型：{identify_type}")
            if ent_type:
                desc_parts.append(f"类型：{ent_type}")
            if city:
                desc_parts.append(f"城市：{city}")

            sections.append(f"{i}. {' | '.join(desc_parts)}")

        if len(control_info) > 20:
            sections.append(f"\n（共{len(control_info)}家，仅显示前20家）")

    # 六、总结
    sections.append("")
    sections.append("## 总结")
    sections.append("")

    total_all = total_legal + total_invest + total_exec + total_control

    if total_all == 0:
        sections.append(f"目前公开信息中，法定代表人{fr_name}仅关联{ent_name}，无其他对外投资或高管任职记录。")
    else:
        summary_parts = []
        if total_legal > 0:
            summary_parts.append(f"担任{total_legal}家企业法人")
        if total_invest > 0:
            summary_parts.append(f"投资{total_invest}家企业")
        if total_exec > 0:
            summary_parts.append(f"在{total_exec}家企业任职")
        if total_control > 0:
            summary_parts.append(f"实际控制{total_control}家企业")

        layout = '广泛' if total_all >= 5 else '集中'
        sections.append(f"法定代表人{fr_name}{'、'.join(summary_parts)}，投资布局较为{layout}。")

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业投资任职信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的投资任职信息
    """
    # 1. 获取数据
    data = _fetch_investment_data(entname)

    if not data:
        return "# 投资任职查询\n\n未查询到投资任职信息"

    # 2. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s21_investment_query <企业名称>")
