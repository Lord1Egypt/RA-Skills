#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识产权一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from collections import Counter
from .base import call_api, debug_print


# ============ API 调用 ============

def _call_patent_api(entname: str) -> Dict[str, Any]:
    """调用专利信息 API"""
    params = {
        'entId': entname,
        'operationType': 1,
        'enableAggregate': True,
        'size': 100
    }
    response = call_api('/patent', params, method='GET')
    return response


def _call_trademark_api(entname: str) -> Dict[str, Any]:
    """调用商标信息 API"""
    params = {
        'entname': entname,
        'enableAggregate': 'true',
        'size': 100
    }
    response = call_api('/trademark/list', params, method='GET')
    return response


def _call_copyright_api(entname: str) -> Dict[str, Any]:
    """调用作品著作权 API"""
    params = {
        'entname': entname,
        'mask': '001',
        'size': 100
    }
    response = call_api('/copyright/query', params, method='GET')
    return response


def _call_software_copyright_api(entname: str) -> Dict[str, Any]:
    """调用软件著作权 API"""
    params = {
        'entname': entname,
        'mask': '010',
        'size': 100
    }
    response = call_api('/copyright/query', params, method='GET')
    return response


# ============ 数据处理 ============

def _process_patent_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理专利数据"""
    if response.get('CODE') != 200:
        return {}

    result = {}
    result['专利数据总量'] = response.get('TOTALCOUNT', 0)

    # 专利有效性统计
    validity_stats = {}
    validity_data = response.get('COUNTOFVALIDITY', [])
    for item in validity_data:
        validity = item.get('VALIDITY', '')
        count = item.get('COUNT', 0)
        if validity == '审中':
            validity_stats['审中专利数量'] = count
        elif validity == '有效':
            validity_stats['有效专利数量'] = count
        elif validity == '失效':
            validity_stats['失效专利数量'] = count
    result['专利有效性统计'] = validity_stats

    # 专利类型统计
    type_stats = {}
    type_data = response.get('COUNTOFTYPENO', [])
    for item in type_data:
        typeno = item.get('TYPENO', '')
        count = item.get('COUNT', 0)
        if typeno == '发明专利':
            type_stats['发明专利数量'] = count
        elif typeno == '发明授权':
            type_stats['发明授权数量'] = count
        elif typeno == '实用新型':
            type_stats['实用新型数量'] = count
        elif typeno == '外观专利':
            type_stats['外观专利数量'] = count
    result['专利类型统计数量'] = type_stats

    # 专利申请年份统计
    year_stats = []
    year_data = response.get('COUNTOFREGYEAR', [])
    for item in year_data:
        year_stats.append({
            '专利申请年份': str(item.get('REGYEAR', '')),
            '数量': item.get('COUNT', 0)
        })
    result['专利申请年份统计'] = year_stats

    # 专利许可总次数
    total_licenses = 0
    basic_info = []
    patent_data_list = response.get('DATA', [])

    for patent_item in patent_data_list:
        patent_basic = patent_item.get('BASIC', {})
        licenses = patent_basic.get('LICENSES', 0)
        if isinstance(licenses, (int, float)):
            total_licenses += licenses
        elif isinstance(licenses, str) and licenses.isdigit():
            total_licenses += int(licenses)

        basic_info.append({
            '专利申请号': patent_basic.get('REG_NO', ''),
            '专利申请日期': patent_basic.get('REGDATE', ''),
            '专利类型': patent_basic.get('TYPENO', ''),
            '专利名称': patent_basic.get('PTNAME', ''),
            '当前专利权人': patent_basic.get('REGPER', ''),
            '发明(设计)人': patent_basic.get('INVENTOR', ''),
            '专利有效性': patent_basic.get('VALIDITY', ''),
            '当前法律状态': patent_basic.get('CURSTATUS', ''),
            '专利转让次数': str(patent_basic.get('TRANSFERS', '')),
            '专利许可次数': str(patent_basic.get('LICENSES', ''))
        })

    result['专利许可总次数'] = total_licenses
    result['专利基本信息'] = basic_info

    return result


def _process_trademark_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理商标数据"""
    if response.get('CODE') != 200:
        return {}

    total_count = response.get('TOTALCOUNT', 0)
    if total_count == 0:
        return {}

    result = {'商标数据总量': total_count}

    # 涉及的国际分类
    uniontype_count = response.get('UNIONTYPECOUNT', [])
    uniontypes = [item.get('UNIONTYPE', '') for item in uniontype_count if item.get('UNIONTYPE')]
    result['涉及的国际分类'] = ','.join(uniontypes)

    # 商标申请年份统计
    app_year_count = response.get('APPYEARCOUNT', [])
    result['商标申请年份统计数量'] = [
        {'商标申请年份': str(item.get('APPYEAR', '')), '数量': item.get('COUNT', 0)}
        for item in app_year_count
    ]

    # 商标有效性统计
    validity_stats = {'有效商标数量': 0, '无效商标数量': 0}
    for item in response.get('ISINVALIDCOUNT', []):
        if item.get('ISINVALID') == '有效':
            validity_stats['有效商标数量'] = item.get('COUNT', 0)
        elif item.get('ISINVALID') == '无效':
            validity_stats['无效商标数量'] = item.get('COUNT', 0)
    result['商标有效性统计数量'] = validity_stats

    # 商标状态统计
    status_stats = {'申请中商标数量': 0, '已注册商标数量': 0, '无效商标数量': 0}
    for item in response.get('SIMSTATUSCOUNT', []):
        status = item.get('SIMSTATUS', '')
        count = item.get('COUNT', 0)
        if status == '申请中':
            status_stats['申请中商标数量'] = count
        elif status == '已注册':
            status_stats['已注册商标数量'] = count
        elif status == '无效':
            status_stats['无效商标数量'] = count
    result['商标状态统计数量'] = status_stats

    # 商标基本信息
    trademark_list = response.get('TRADEMARKLIST', [])
    result['商标基本信息'] = [
        {
            '商标注册号': item.get('MARKCODEKEY', ''),
            '商标国际分类': item.get('UNIONTYPE', ''),
            '商标名称': item.get('MARKNAME', ''),
            '商标申请日期': item.get('APPDATE', ''),
            '商标有效性': item.get('ISINVALID', ''),
            '当前商标状态': item.get('SIMSTATUS', '')
        }
        for item in trademark_list
    ]

    return result


def _process_copyright_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理作品著作权数据"""
    if response.get('code') != 200:
        return {}

    data = response.get('result', {})
    total_count = data.get('COUNTOFPRODUCTCOPYRIGHT', 0)
    if total_count == 0:
        return {}

    result = {'作品著作权数据总量': total_count}

    # 涉及的作品类别
    categories = []
    for item in data.get('FZD_ZPLBCOUNT', []):
        if item.get('FZD_ZPLB'):
            categories.append(item['FZD_ZPLB'])
    result['涉及的作品类别'] = ','.join(categories)

    # 作品登记年份统计
    year_stats = []
    for item in data.get('FZD_DJYEARCOUNT', []):
        year_stats.append({
            '作品登记年份': str(item.get('FZD_DJYEAR', '')),
            '数量': item.get('COUNT', 0)
        })
    result['作品登记年份统计'] = year_stats

    # 作品著作权信息
    copyright_info = []
    for item in data.get('PRODUCTCOPYRIGHT', []):
        copyright_info.append({
            '作品名称': item.get('FZD_ZPMC', ''),
            '作品类别': item.get('FZD_ZPLB', ''),
            '作者姓名': item.get('FZD_ZZNAME', ''),
            '著作权人': item.get('FZD_ZZQRNAME', ''),
            '创作完成日期': item.get('FZD_CZWCDATE', ''),
            '首次发表日期': item.get('FZD_SCFBDATE', '')
        })
    result['作品著作权信息'] = copyright_info

    return result


def _process_software_copyright_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理软件著作权数据"""
    if response.get('code') != 200:
        return {}

    data = response.get('result', {})
    copyright_list = data.get('COPYRIGHTINFO', [])
    if not copyright_list:
        return {}

    total_count = data.get('COUNTOFCOPYRIGHTINFO', len(copyright_list))
    result = {'软件著作权数据总量': total_count}

    # 软件分类
    software_categories = []
    for item in data.get('FRJ_RJFLHCOUNT', []):
        if item.get('FRJ_RJFLHNAME'):
            software_categories.append(item['FRJ_RJFLHNAME'])
    result['涉及的软件分类名称'] = ','.join(software_categories)

    # 行业分类
    industry_categories = []
    for item in data.get('FRJ_HYFLHCOUNT', []):
        if item.get('FRJ_HYFLHNAME'):
            industry_categories.append(item['FRJ_HYFLHNAME'])
    result['涉及的行业分类名称'] = ','.join(industry_categories)

    # 软件登记年份统计
    api_year_stats = data.get('FRJ_DJYEARCOUNT', [])
    year_stats = [
        {'软件登记年份': item.get('FRJ_DJYEAR', ''), '数量': item.get('COUNT', 0)}
        for item in api_year_stats
    ]
    result['软件登记年份统计'] = year_stats

    # 软件著作权详细信息
    software_info = []
    for item in copyright_list:
        software_info.append({
            '软件分类名称': item.get('FRJ_RJFLHNAME', ''),
            '行业分类名称': item.get('FRJ_HYFLHNAME', ''),
            '软件全称': item.get('FRJ_RJQC', ''),
            '软件简称': item.get('FRJ_RJJC', ''),
            '登记日期': item.get('FRJ_DJDATE', ''),
            '开发完成日期': item.get('FRJ_CZWCDATE', '')
        })
    result['软件著作权详细信息'] = software_info

    return result


def _fetch_all_ip_data(entname: str) -> Dict[str, Any]:
    """获取所有知识产权数据"""
    # 并行调用所有 API
    patent_response = _call_patent_api(entname)
    trademark_response = _call_trademark_api(entname)
    copyright_response = _call_copyright_api(entname)
    software_response = _call_software_copyright_api(entname)

    # 处理各类数据
    patents = _process_patent_data(patent_response)
    trademarks = _process_trademark_data(trademark_response)
    copyrights = _process_copyright_data(copyright_response)
    software_copyrights = _process_software_copyright_data(software_response)

    return {
        'patents': patents,
        'trademarks': trademarks,
        'copyrights': copyrights,
        'software_copyrights': software_copyrights
    }


# ============ Markdown 格式化 ============

def _extract_ip_overview(patents: Dict, trademarks: Dict, copyrights: Dict, software_copyrights: Dict) -> str:
    """提取知识产权总览"""
    lines = ["### 知识产权总览"]

    patent_total = patents.get('专利数据总量', 0)
    trademark_total = trademarks.get('商标数据总量', 0)
    copyright_total = copyrights.get('作品著作权数据总量', 0)
    software_total = software_copyrights.get('软件著作权数据总量', 0)

    lines.append(f"专利总量: {patent_total}")
    lines.append(f"商标总量: {trademark_total}")
    lines.append(f"作品著作权总量: {copyright_total}")
    lines.append(f"软件著作权总量: {software_total}")

    return '\n'.join(lines)


def _extract_patent_analysis(patents: Dict) -> str:
    """提取专利深度分析"""
    if not patents or patents.get('专利数据总量', 0) == 0:
        return ""

    lines = ["### 专利深度分析"]

    # 专利有效性
    validity_stats = patents.get('专利有效性统计', {})
    if validity_stats:
        reviewing = validity_stats.get('审中专利数量', 0)
        valid = validity_stats.get('有效专利数量', 0)
        invalid = validity_stats.get('失效专利数量', 0)
        lines.append(f"专利有效性: 审中{reviewing}件, 有效{valid}件, 失效{invalid}件")

    # 专利类型分布
    type_stats = patents.get('专利类型统计数量', {})
    if type_stats:
        invention = type_stats.get('发明专利数量', 0)
        invention_granted = type_stats.get('发明授权数量', 0)
        utility = type_stats.get('实用新型数量', 0)
        design = type_stats.get('外观专利数量', 0)
        lines.append(f"专利类型分布: 发明申请{invention}件, 发明授权{invention_granted}件, 实用新型{utility}件, 外观设计{design}件")

    # 专利申请趋势
    year_stats = patents.get('专利申请年份统计', [])
    if year_stats:
        year_strs = [f"{item.get('专利申请年份', '')}年{item.get('数量', 0)}件" for item in year_stats[:5]]
        lines.append(f"专利申请趋势: {', '.join(year_strs)}")

    # 专利运营
    license_count = patents.get('专利许可总次数', 0)
    lines.append(f"专利运营: 对外许可总次数{license_count}次")

    return '\n'.join(lines)


def _extract_trademark_analysis(trademarks: Dict) -> str:
    """提取商标深度分析"""
    if not trademarks or trademarks.get('商标数据总量', 0) == 0:
        return ""

    lines = ["### 商标深度分析"]

    # 商标国际分类
    classifications = trademarks.get('涉及的国际分类', '')
    if classifications:
        lines.append(f"商标国际分类: {classifications}")

    # 商标申请趋势
    year_stats = trademarks.get('商标申请年份统计数量', [])
    if year_stats:
        year_strs = [f"{item.get('商标申请年份', '')}年{item.get('数量', 0)}件" for item in year_stats[:5]]
        lines.append(f"商标申请趋势: {', '.join(year_strs)}")

    # 商标有效性
    validity_stats = trademarks.get('商标有效性统计数量', {})
    if validity_stats:
        valid = validity_stats.get('有效商标数量', 0)
        invalid = validity_stats.get('无效商标数量', 0)
        lines.append(f"商标有效性: 有效{valid}件, 无效{invalid}件")

    # 商标状态分布
    status_stats = trademarks.get('商标状态统计数量', {})
    if status_stats:
        applying = status_stats.get('申请中商标数量', 0)
        registered = status_stats.get('已注册商标数量', 0)
        lines.append(f"商标状态分布: 申请中{applying}件, 已注册{registered}件")

    return '\n'.join(lines)


def _extract_copyright_analysis(copyrights: Dict, software_copyrights: Dict) -> str:
    """提取著作权深度分析"""
    copyright_total = copyrights.get('作品著作权数据总量', 0)
    software_total = software_copyrights.get('软件著作权数据总量', 0)

    if copyright_total == 0 and software_total == 0:
        return ""

    lines = ["### 著作权深度分析"]

    # 作品著作权
    if copyright_total > 0:
        lines.append("作品著作权:")
        work_types = copyrights.get('涉及的作品类别', '')
        if work_types:
            lines.append(f"  作品类别分布: {work_types}")

        year_stats = copyrights.get('作品登记年份统计', [])
        if year_stats:
            year_strs = [f"{item.get('作品登记年份', '')}年{item.get('数量', 0)}件" for item in year_stats[:5]]
            lines.append(f"  登记年份分布: {', '.join(year_strs)}")

    # 软件著作权
    if software_total > 0:
        lines.append("软件著作权:")
        software_types = software_copyrights.get('涉及的软件分类名称', '')
        if software_types:
            lines.append(f"  软件分类: {software_types}")

        industry_types = software_copyrights.get('涉及的行业分类名称', '')
        if industry_types:
            lines.append(f"  行业分类: {industry_types}")

        year_stats = software_copyrights.get('软件登记年份统计', [])
        if year_stats:
            year_strs = [f"{item.get('软件登记年份', '')}年{item.get('数量', 0)}件" for item in year_stats[:5]]
            lines.append(f"  登记年份分布: {', '.join(year_strs)}")

    return '\n'.join(lines)


def _extract_core_assets(patents: Dict, trademarks: Dict, software_copyrights: Dict) -> str:
    """提取核心资产清单"""
    lines = ["### 核心资产清单"]

    # 代表性专利
    patent_list = patents.get('专利基本信息', [])
    if patent_list:
        valid_patents = [p for p in patent_list if p.get('专利有效性') in ['有效', '审中']][:5]
        if valid_patents:
            lines.append("代表性专利:")
            for p in valid_patents:
                name = p.get('专利名称', '')
                ptype = p.get('专利类型', '')
                status = p.get('当前法律状态', '')
                lines.append(f"  - {name} ({ptype}, 法律状态: {status})")

    # 代表性商标
    trademark_list = trademarks.get('商标基本信息', [])
    if trademark_list:
        registered_trademarks = [t for t in trademark_list if t.get('当前商标状态') == '已注册'][:5]
        if registered_trademarks:
            lines.append("代表性商标:")
            for t in registered_trademarks:
                name = t.get('商标名称', '')
                classification = t.get('商标国际分类', '')
                lines.append(f"  - {name} (国际分类: {classification})")

    # 代表性软件著作权
    software_list = software_copyrights.get('软件著作权详细信息', [])
    if software_list:
        recent_software = software_list[:5]
        if recent_software:
            lines.append("代表性软件著作权:")
            for s in recent_software:
                software_name = s.get('软件全称', '')
                if software_name:
                    lines.append(f"  - {software_name}")

    return '\n'.join(lines)


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    patents = data.get('patents', {})
    trademarks = data.get('trademarks', {})
    copyrights = data.get('copyrights', {})
    software_copyrights = data.get('software_copyrights', {})

    # 检查是否有任何知识产权数据
    has_data = any([
        patents.get('专利数据总量', 0) > 0,
        trademarks.get('商标数据总量', 0) > 0,
        copyrights.get('作品著作权数据总量', 0) > 0,
        software_copyrights.get('软件著作权数据总量', 0) > 0
    ])

    if not has_data:
        return "# 知识产权信息\n\n暂无知识产权数据"

    sections = ["# 知识产权信息提炼"]

    # 知识产权总览
    overview = _extract_ip_overview(patents, trademarks, copyrights, software_copyrights)
    sections.append("")
    sections.append(overview)

    # 专利深度分析
    patent_analysis = _extract_patent_analysis(patents)
    if patent_analysis:
        sections.append("")
        sections.append(patent_analysis)

    # 商标深度分析
    trademark_analysis = _extract_trademark_analysis(trademarks)
    if trademark_analysis:
        sections.append("")
        sections.append(trademark_analysis)

    # 著作权深度分析
    copyright_analysis = _extract_copyright_analysis(copyrights, software_copyrights)
    if copyright_analysis:
        sections.append("")
        sections.append(copyright_analysis)

    # 核心资产清单
    core_assets = _extract_core_assets(patents, trademarks, software_copyrights)
    if core_assets:
        sections.append("")
        sections.append(core_assets)

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业知识产权信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的知识产权信息
    """
    # 1. 获取所有知识产权数据
    data = _fetch_all_ip_data(entname)

    # 2. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s17_ip <企业名称>")
