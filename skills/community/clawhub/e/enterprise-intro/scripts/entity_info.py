#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主体信息一体化脚本
合并 API 调用和后处理逻辑
"""

from typing import Dict, Any
from .base import call_api, get_headers, encrypt, format_number, BASE_URL, UID, KEY

import requests
import time
import random

uid = UID
key = KEY
url_o = BASE_URL


# ============ 字段映射 ============

MODULE_NAME_MAPPING = {
    'BASIC': '企业照面信息',
    'SHAREHOLDER': '股东及出资信息',
    'LISTEDSHAREHOLDER': '十大股东名单',
    'PERSON': '主要管理人员',
    'LISTEDMANAGER': '上市公司高管',
    'FILIATION': '分支机构',
    'ALTERINFO': '历史沿革信息',
    'YEARREPORTBASIC': '年报-企业基本信息',
    'ENTINV': '企业对外投资',
    'HEADQUARTERS': '总公司信息',
    'GTTYPING': '个体分型信息',
    'GTCLASSTYPE': '个体分类信息',
}

MODULE_FIELD_MAPPING = {
    'SHAREHOLDER': {
        'SUBCONAM': '认缴出资额(万元)',
        'FUNDEDRATIO': '出资比例',
    },
    'ENTINV': {
        'SUBCONAM': '投资数额(万元/股数)',
        'ENTSTATUS': '企业状态',
        'ESDATE': '开业日期',
        'FUNDEDRATIO': '投资比例',
        'REGCAP': '注册资本（万元）',
    },
    'BASIC': {
        'REGCAP': '注册资本（万元）',
        'ENTSTATUS': '经营状态',
        'ESDATE': '成立日期',
    },
    'FILIATION': {
        'BRN_ENTSTATUS': '经营状态',
        'BRN_ESDATE': '成立日期',
    },
}

FIELD_NAME_MAPPING = {
    'ENTNAME': '企业名称',
    'CREDITCODE': '统一社会信用代码',
    'FRNAME': '法定代表人/负责人/执行事务合伙人',
    'REGCAP': '注册资本（万元）',
    'REGCAPCUR': '注册资本币种',
    'PAIDINCAP': '实缴资本(万元)',
    'ENTSTATUS': '经营状态',
    'ESDATE': '成立日期',
    'OPTO': '经营期限至',
    'CANREASON': '注销原因',
    'REVREASON': '吊销原因',
    'CANDATE': '注销日期',
    'REVDATE': '吊销日期',
    'APPRDATE': '最后变更日期',
    'ENTTYPE': '企业(机构)类型',
    'ZSOPSCOPE': '经营业务范围',
    'REGORG': '登记机关',
    'INDUSTRYCONAME': '国民经济行业名称',
    'DOM': '注册地址',
    'REGORGPROVINCE': '所在省份',
    'REGORGCITY': '所在城市',
    'REGORGDISTRICT': '所在区/县',
    'SHORTNAME': '企业简称',
    'COORDINATE': '高德坐标(经纬度)',
    'SHANAME': '股东名称',
    'SUBCONAM': '认缴出资额(万元)',
    'ACCONAM': '实缴出资额(万元)',
    'CONDATE': '出资日期',
    'FUNDEDRATIO': '出资比例',
    'SHHOLDERNAME': '股东名称',
    'SHHOLDERTYPE': '股东机构类型',
    'SHHOLDERNATURE': '股东股权性质',
    'HOLDERRTO': '持股比例',
    'SHARESTYPE': '股份类型',
    'HOLDERAMT': '持股数量',
    'ENTRYDATE': '更新日期',
    'PERNAME': '高管姓名',
    'POSITION': '职务',
    'CNAME': '姓名',
    'ACTDUTYNAME': '职位',
    'BRNAME': '分支机构名称',
    'BRN_ESDATE': '成立日期',
    'BRN_ENTSTATUS': '经营状态',
    'BRN_PROVINCE_NAME': '省份名称',
    'CHANGEDATE': '变更日期',
    'ALTERTYPE': '历史动态事项',
    'OLDVALUE': '变更前内容',
    'NEWVALUE': '变更后内容',
    'ENTJGNAME': '企业(机构)名称',
    'CONFORM': '投资方式',
    'ISLISTED': '是否上市',
}

ALLOWED_FIELDS = {
    'ENTNAME', 'CREDITCODE', 'FRNAME', 'REGCAP', 'REGCAPCUR', 'PAIDINCAP',
    'ENTSTATUS', 'ESDATE', 'OPTO', 'CANREASON', 'REVREASON', 'CANDATE',
    'REVDATE', 'APPRDATE', 'ENTTYPE', 'ZSOPSCOPE', 'REGORG', 'INDUSTRYCONAME',
    'DOM', 'REGORGPROVINCE', 'REGORGCITY', 'REGORGDISTRICT', 'SHORTNAME',
    'COORDINATE', 'SHANAME', 'SUBCONAM', 'ACCONAM', 'CONDATE', 'FUNDEDRATIO',
    'SHHOLDERNAME', 'SHHOLDERTYPE', 'SHHOLDERNATURE', 'HOLDERRTO', 'SHARESTYPE',
    'HOLDERAMT', 'ENTRYDATE', 'PERNAME', 'POSITION', 'CNAME', 'ACTDUTYNAME',
    'BRNAME', 'BRN_ESDATE', 'BRN_ENTSTATUS', 'BRN_PROVINCE_NAME',
    'CHANGEDATE', 'ALTERTYPE', 'OLDVALUE', 'NEWVALUE', 'ENTJGNAME', 'CONFORM', 'ISLISTED'
}


# ============ API 调用函数 ============

def convert_to_chinese(data, parent_module=None):
    """将英文模块名和字段名转换为中文"""
    if isinstance(data, dict):
        chinese_data = {}
        for key, value in data.items():
            if key in MODULE_NAME_MAPPING:
                chinese_key = MODULE_NAME_MAPPING[key]
                if isinstance(value, list):
                    chinese_data[chinese_key] = [convert_to_chinese(item, key) for item in value]
                elif isinstance(value, dict):
                    chinese_data[chinese_key] = convert_to_chinese(value, key)
                else:
                    chinese_data[chinese_key] = value
            else:
                chinese_key = key
                if parent_module and parent_module in MODULE_FIELD_MAPPING:
                    chinese_key = MODULE_FIELD_MAPPING[parent_module].get(key, FIELD_NAME_MAPPING.get(key, key))
                else:
                    chinese_key = FIELD_NAME_MAPPING.get(key, key)

                if isinstance(value, list):
                    chinese_data[chinese_key] = [convert_to_chinese(item, parent_module) for item in value]
                elif isinstance(value, dict):
                    chinese_data[chinese_key] = convert_to_chinese(value, parent_module)
                else:
                    if key == 'ISLISTED':
                        if value == '0' or value == 0:
                            chinese_data[chinese_key] = '否'
                        elif value == '1' or value == 1:
                            chinese_data[chinese_key] = '是'
                        else:
                            chinese_data[chinese_key] = value
                    else:
                        chinese_data[chinese_key] = value
        return chinese_data
    elif isinstance(data, list):
        return [convert_to_chinese(item, parent_module) for item in data]
    else:
        return data


def filter_allowed_fields(data):
    """只保留指定的字段"""
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k in ALLOWED_FIELDS}
    return data


def filter_empty_values(data):
    """过滤掉空值的字段"""
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if v is not None and v != '' and v != []}
    return data


def _call_entinfo_api(entname: str) -> dict:
    """调用企业详情查询 API"""
    url = url_o + '/entinfo'

    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))

    headers = {
        'Accept': 'application/json',
        'X-Uid': uid,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': encrypt(nonce + ";" + key + ";" + timestamp + ";" + uid + ";")
    }

    params = {'name': entname}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response_json = response.json()

        if response_json.get('CODE') != 200:
            return "未查询到企业工商信息"

        data = response_json.get('ENT_INFO', {})
        if not data:
            return "未查询到企业工商信息"

        result = {}
        basic_info = data.get('BASIC', {})
        if basic_info:
            result['BASIC'] = filter_empty_values(filter_allowed_fields(basic_info))

        headquarters_info = data.get('HEADQUARTERS', {})
        is_branch = False
        if headquarters_info and any(v for v in headquarters_info.values() if v):
            is_branch = True
            result['HEADQUARTERS'] = filter_empty_values(filter_allowed_fields(headquarters_info))

        is_individual = False
        if basic_info.get('ENTTYPE') and '个体' in basic_info.get('ENTTYPE', ''):
            is_individual = True

        if is_branch:
            alter_info = data.get('ALTERINFO', [])
            if alter_info:
                filtered_alter = [filter_empty_values(filter_allowed_fields(item)) for item in alter_info if filter_empty_values(filter_allowed_fields(item))]
                if filtered_alter:
                    result['ALTERINFO'] = filtered_alter

            year_report_basic = data.get('YEARREPORTBASIC', [])
            if year_report_basic:
                filtered_year_report = [filter_empty_values(filter_allowed_fields(item)) for item in year_report_basic if filter_empty_values(filter_allowed_fields(item))]
                if filtered_year_report:
                    result['YEARREPORTBASIC'] = filtered_year_report

        elif is_individual:
            alter_info = data.get('ALTERINFO', [])
            if alter_info:
                filtered_alter = [filter_empty_values(filter_allowed_fields(item)) for item in alter_info if filter_empty_values(filter_allowed_fields(item))]
                if filtered_alter:
                    result['ALTERINFO'] = filtered_alter

            year_report_basic = data.get('YEARREPORTBASIC', [])
            if year_report_basic:
                filtered_year_report = [filter_empty_values(filter_allowed_fields(item)) for item in year_report_basic if filter_empty_values(filter_allowed_fields(item))]
                if filtered_year_report:
                    result['YEARREPORTBASIC'] = filtered_year_report

        else:
            listedshareholder_data = data.get('LISTEDSHAREHOLDER', [])
            if listedshareholder_data:
                filtered_data = [filter_empty_values(filter_allowed_fields(item)) for item in listedshareholder_data if filter_empty_values(filter_allowed_fields(item))]
                if filtered_data:
                    result['LISTEDSHAREHOLDER'] = filtered_data
            else:
                shareholder_data = data.get('SHAREHOLDER', [])
                if shareholder_data:
                    filtered_data = [filter_empty_values(filter_allowed_fields(item)) for item in shareholder_data if filter_empty_values(filter_allowed_fields(item))]
                    if filtered_data:
                        result['SHAREHOLDER'] = filtered_data

            listedmanager_data = data.get('LISTEDMANAGER', [])
            if listedmanager_data:
                filtered_data = [filter_empty_values(filter_allowed_fields(item)) for item in listedmanager_data if filter_empty_values(filter_allowed_fields(item))]
                if filtered_data:
                    result['LISTEDMANAGER'] = filtered_data
            else:
                person_data = data.get('PERSON', [])
                if person_data:
                    filtered_data = [filter_empty_values(filter_allowed_fields(item)) for item in person_data if filter_empty_values(filter_allowed_fields(item))]
                    if filtered_data:
                        result['PERSON'] = [{k: v for k, v in item.items() if k != 'ENTNAME'} for item in filtered_data]

            filiation_data = data.get('FILIATION', [])
            if filiation_data:
                filtered_data = [filter_empty_values(filter_allowed_fields(item)) for item in filiation_data]
                if filtered_data:
                    result['FILIATION'] = filtered_data

            entinv_data = data.get('ENTINV', [])
            if entinv_data:
                entinv_fields = {'ENTJGNAME', 'ENTTYPE', 'REGCAP', 'REGCAPCUR', 'ENTSTATUS', 'SUBCONAM', 'FUNDEDRATIO', 'ESDATE', 'CONFORM', 'ISLISTED'}
                filtered_data = []
                for item in entinv_data:
                    filtered_item = filter_empty_values(filter_allowed_fields(item))
                    if filtered_item.get('ENTSTATUS') == '在营（开业）':
                        entinv_item = {field: filtered_item[field] for field in entinv_fields if field in filtered_item}
                        if 'ISLISTED' in entinv_item:
                            islisted_value = entinv_item.get('ISLISTED')
                            if islisted_value == '0' or islisted_value == 0:
                                entinv_item['ISLISTED'] = '否'
                            elif islisted_value == '1' or islisted_value == 1:
                                entinv_item['ISLISTED'] = '是'
                        if entinv_item:
                            filtered_data.append(entinv_item)
                if filtered_data:
                    result['ENTINV'] = filtered_data

            alter_info = data.get('ALTERINFO', [])
            if alter_info:
                filtered_alter = [filter_empty_values(filter_allowed_fields(item)) for item in alter_info if filter_empty_values(filter_allowed_fields(item))]
                if filtered_alter:
                    result['ALTERINFO'] = filtered_alter

            year_report_basic = data.get('YEARREPORTBASIC', [])
            if year_report_basic:
                filtered_year_report = [filter_empty_values(filter_allowed_fields(item)) for item in year_report_basic if filter_empty_values(filter_allowed_fields(item))]
                if filtered_year_report:
                    result['YEARREPORTBASIC'] = filtered_year_report

        chinese_result = convert_to_chinese(result)

        if '注册资本（万元）' in chinese_result.get('企业照面信息', {}) and is_individual:
            chinese_result['企业照面信息']['资金数额（元）'] = chinese_result['企业照面信息'].pop('注册资本（万元）')

        return chinese_result

    except Exception as e:
        return "未查询到企业工商信息"


# ============ 后处理函数 ============

def extract_entity_identity(data: Dict[str, Any]) -> str:
    """提取企业身份信息"""
    info = data.get('企业照面信息', {})

    name = info.get('企业名称', '')
    legal_rep = info.get('法定代表人/负责人/执行事务合伙人', '')
    reg_capital = format_number(info.get('注册资本（万元）', ''))
    paid_capital = format_number(info.get('实缴资本(万元)', ''))
    status = info.get('经营状态', '')
    establish_date = info.get('成立日期', '')
    company_type = info.get('企业(机构)类型', '')
    industry = info.get('国民经济行业名称', '')
    province = info.get('所在省份', '')
    city = info.get('所在城市', '')

    return (f"### 企业身份\n"
            f"名称：{name}；法人：{legal_rep}；"
            f"注册资本：{reg_capital}万元（实缴{paid_capital}万元）；"
            f"状态：{status}；成立：{establish_date}；"
            f"类型：{company_type}；行业：{industry}；"
            f"区位：{province}{city}")


def extract_shareholder_structure(data: Dict[str, Any]) -> str:
    """提取股权结构"""
    shareholders = data.get('股东及出资信息', []) or data.get('十大股东名单', [])

    if not shareholders:
        return "### 股权结构\n股东构成：暂无股东信息数据"

    main_shareholders = shareholders[:10] if len(shareholders) > 10 else shareholders

    shareholder_list = []
    for sh in main_shareholders:
        name = sh.get('股东名称', '')
        amount = format_number(sh.get('认缴出资额(万元)', ''))
        ratio = format_number(sh.get('出资比例', '') or sh.get('持股比例', ''))

        if amount:
            shareholder_list.append(f"{name}（出资{amount}万元，占比{ratio}）")
        else:
            shareholder_list.append(f"{name}（占比{ratio}%）")

    shareholder_text = '、'.join(shareholder_list)

    return f"### 股权结构\n股东构成：{shareholder_text}"


def extract_management_team(data: Dict[str, Any]) -> str:
    """提取治理团队"""
    managers = data.get('主要管理人员', []) or data.get('上市公司高管', [])

    positions = {'董事长': '', '总经理': '', '财务负责人': '', '董秘': ''}

    position_mapping = {
        '董事长': '董事长', '副董事长': '董事长',
        '总经理': '总经理', '经理': '总经理', '行长': '总经理', '副行长': '总经理',
        '财务负责人': '财务负责人', '首席财务官': '财务负责人',
        '董秘': '董秘', '董事会秘书': '董秘'
    }

    for mgr in managers:
        position = mgr.get('职务', '') or mgr.get('职位', '')
        name = mgr.get('高管姓名', '') or mgr.get('姓名', '')

        mapped_position = position_mapping.get(position, '')

        if mapped_position and not positions[mapped_position]:
            positions[mapped_position] = name

    result_parts = []
    if positions['董事长']:
        result_parts.append(f"董事长-{positions['董事长']}")
    if positions['总经理']:
        result_parts.append(f"总经理-{positions['总经理']}")
    if positions['财务负责人']:
        result_parts.append(f"财务负责人-{positions['财务负责人']}")
    if positions['董秘']:
        result_parts.append(f"董秘-{positions['董秘']}")

    if not result_parts:
        return "### 治理团队\n核心职务：暂无管理人员数据"

    return f"### 治理团队\n核心职务：{('；'.join(result_parts))}"


def extract_business_scope(data: Dict[str, Any]) -> str:
    """提取经营资质"""
    info = data.get('企业照面信息', {})
    annual_reports = data.get('年报-企业基本信息', [])

    business_scope = info.get('经营业务范围', '')
    company_type = info.get('企业(机构)类型', '')

    main_business = ''
    for report in annual_reports:
        main_business = report.get('企业主营业务活动', '')
        if main_business:
            break

    if len(business_scope) > 200:
        business_scope = business_scope[:200] + '...'

    return (f"### 经营资质\n"
            f"经营范围：{business_scope}；"
            f"主营业务：{main_business}；"
            f"企业类型：{company_type}")


def extract_branch_layout(data: Dict[str, Any]) -> str:
    """提取分支布局"""
    branches = data.get('分支机构', [])

    if not branches:
        return "### 分支布局\n分支机构：暂无分支机构数据"

    main_branches = branches[:10] if len(branches) > 10 else branches

    branch_list = []
    for branch in main_branches:
        name = branch.get('分支机构名称', '')
        province = branch.get('省份名称', '')
        branch_list.append(f"{name}（{province}）")

    return f"### 分支布局\n分支机构：{'、'.join(branch_list)}"


def extract_investment(data: Dict[str, Any]) -> str:
    """提取对外投资"""
    investments = data.get('企业对外投资', [])

    if not investments:
        return "### 对外投资\n投资企业：暂无对外投资数据"

    investment_list = []
    for inv in investments:
        name = inv.get('企业(机构)名称', '')
        amount = format_number(inv.get('投资数额（万元）', ''))
        ratio = format_number(inv.get('投资比例', ''))

        if amount and ratio:
            investment_list.append(f"{name}（投资{amount}万元，占比{ratio}）")
        elif ratio:
            investment_list.append(f"{name}（占比{ratio}）")
        elif amount:
            investment_list.append(f"{name}（投资{amount}万元）")
        else:
            investment_list.append(name)

    return f"### 对外投资\n投资企业：{'、'.join(investment_list)}"


def extract_timeline(data: Dict[str, Any]) -> str:
    """提取时间节点"""
    info = data.get('企业照面信息', {})
    establish_date = info.get('成立日期', '')

    return f"### 时间节点\n成立时间：{establish_date}"


def extract_history_changes(data: Dict[str, Any]) -> str:
    """提取历史变更"""
    changes = data.get('历史沿革信息', [])

    if not changes:
        return "### 历史变更\n暂无历史变更数据"

    important_changes = changes[:5]

    change_list = []
    for change in important_changes:
        date = change.get('变更日期', '')
        item = change.get('历史动态事项', '')
        before = change.get('变更前内容', '')
        after = change.get('变更后内容', '')

        if len(before) > 100:
            before = before[:100] + '...'
        if len(after) > 100:
            after = after[:100] + '...'

        change_list.append(f"· {date}：{item}（{before}→{after}）")

    return "### 历史变更\n" + '；\n'.join(change_list)


def extract_scale_data(data: Dict[str, Any]) -> str:
    """提取规模数据"""
    info = data.get('企业照面信息', {})

    reg_capital = format_number(info.get('注册资本（万元）', ''))
    paid_capital = format_number(info.get('实缴资本(万元)', ''))

    return (f"### 规模数据\n"
            f"注册资本：{reg_capital}万元（实缴{paid_capital}万元）；"
            f"从业人员：未提供数据")


def _process_entity_info(data: Dict[str, Any]) -> str:
    """处理主体信息数据"""
    if isinstance(data, str):
        return data

    sections = [
        "# 主体信息提炼",
        "",
        extract_entity_identity(data),
        "",
        extract_shareholder_structure(data),
        "",
        extract_management_team(data),
        "",
        extract_business_scope(data),
        "",
        extract_branch_layout(data),
        "",
        extract_investment(data),
        "",
        extract_timeline(data),
        "",
        extract_history_changes(data),
        "",
        extract_scale_data(data)
    ]

    return '\n'.join(sections)


# ============ 统一接口 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业主体信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的处理结果
    """
    raw_data = _call_entinfo_api(entname)

    if isinstance(raw_data, str):
        return raw_data

    return _process_entity_info(raw_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python s01_entity_info.py <企业名称>")
