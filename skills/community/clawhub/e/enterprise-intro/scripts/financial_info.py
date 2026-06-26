#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务信息一体化脚本
合并 API 调用和后处理逻辑
"""

from typing import Dict, Any, List
from .base import call_api, encrypt, debug_print, UID, KEY, BASE_URL

import requests
import time
import random
from datetime import datetime

uid = UID
key = KEY
url_o = BASE_URL


# ============ 字段映射 ============

REPORT_TYPE_MAPPING = {
    1: "合并期末",
    2: "母公司期末",
    3: "合并期末_调整",
    4: "母公司期末_调整"
}

REPORT_DATE_TYPE_MAPPING = {
    1: "一季报",
    2: "中报（累计）",
    3: "三季报（累计）",
    4: "年报(累计)"
}

# 资产负债表字段映射
BALANCE_SHEET_FIELD_MAPPING = {
    "reporttype": "报表类型",
    "reportyear": "会计年度",
    "reportdatetype": "报告期类型",
    "curfds": "货币资金",
    "tradfinasset": "交易性金融资产",
    "notesaccorece": "应收票据及应收账款",
    "recfinanc": "应收款项融资",
    "prep": "预付款项",
    "otherrecetot": "其他应收款合计",
    "inve": "存货",
    "contractasset": "合同资产",
    "totcurrasset": "流动资产合计",
    "longrece": "长期应收款",
    "equiinve": "长期股权投资",
    "fixedassecleatot": "固定资产及清理合计",
    "intaasset": "无形资产",
    "goodwill": "商誉",
    "defetaxasset": "递延所得税资产",
    "totalnoncassets": "非流动资产合计",
    "totasset": "资产总计",
    "shorttermborr": "短期借款",
    "notesaccopaya": "应付票据及应付账款",
    "advapaym": "预收款项",
    "leaseliab": "租赁负债",
    "otherpaytot": "其他应付款合计",
    "contractliab": "合同负债",
    "totalcurrliab": "流动负债合计",
    "longpayatot": "长期应付款合计",
    "totalnoncliab": "非流动负债合计",
    "totliab": "负债合计",
    "paidincapi": "实收资本(或股本)",
    "capisurp": "资本公积",
    "rese": "盈余公积",
    "undiprof": "未分配利润",
    "paresharrigh": "归属于母公司股东权益合计",
    "righaggr": "所有者权益(或股东权益)合计"
}

BALANCE_SHEET_ALLOWED_FIELDS = {
    'reporttype', 'reportyear', 'reportdatetype', "curfds", "tradfinasset",
    "notesaccorece", "recfinanc", "prep", "otherrecetot", "inve", "contractasset",
    "totcurrasset", "longrece", "equiinve", "fixedassecleatot", "intaasset",
    "goodwill", "defetaxasset", "totalnoncassets", "totasset", "shorttermborr",
    "notesaccopaya", "advapaym", "leaseliab", "otherpaytot", "contractliab",
    "totalcurrliab", "longpayatot", "totalnoncliab", "totliab", "paidincapi",
    "capisurp", "rese", "undiprof", "paresharrigh", "righaggr"
}

# 利润表字段映射
PROFIT_FIELD_MAPPING = {
    "reporttype": "报表类型",
    "reportyear": "会计年度",
    "reportdatetype": "报告期类型",
    "biztotinco": "营业总收入",
    "deveexpe": "研发费用",
    "finexpe": "财务费用",
    "perprofit": "营业利润",
    "netprofit": "净利润",
    "parenetp": "归属于母公司所有者的净利润",
    "basiceps": "基本每股收益",
    "mainbizinco": "主营业务收入"
}

PROFIT_ALLOWED_FIELDS = {
    'reporttype', 'reportyear', 'reportdatetype', 'biztotinco', 'deveexpe',
    'finexpe', 'perprofit', 'netprofit', 'parenetp', 'basiceps', 'mainbizinco'
}

# 现金流量表字段映射
CASH_FLOW_FIELD_MAPPING = {
    "reporttype": "报表类型",
    "reportyear": "会计年度",
    "reportdatetype": "报告期类型",
    "laborgetcash": "销售商品、提供劳务收到的现金",
    "bizcashinfl": "经营活动现金流入小计",
    "mananetr": "一、经营活动产生的现金流量净额",
    "invnetcashflow": "二、投资活动产生的现金流量净额",
    "finnetcflow": "三、筹资活动产生的现金流量净额",
    "cashnetr": "五、现金及现金等价物净增加额"
}

CASH_FLOW_ALLOWED_FIELDS = {
    'reporttype', 'reportyear', 'reportdatetype', 'laborgetcash', 'bizcashinfl',
    'mananetr', 'invnetcashflow', 'finnetcflow', 'cashnetr'
}

# 企业基本信息字段映射
BASIC_INFO_FIELD_MAPPING = {
    'COMPSNAME': '公司简称',
    'ENGNAME': '英文名称',
    'ENGSNAME': '英文简称',
    'WORKFORCE': '员工人数',
    'MAJORBIZ': '主营业务',
    'COMPINTRO': '公司简介',
    'REGADDR': '注册地址',
    'OFFICEADDR': '办公地址',
    'CHAIRMAN': '董事长',
    'BSECRETARY': '董秘',
    'MANAGER': '总经理',
    'SEAFFREPR': '证券代表',
    'LECONSTANT': '律师事务所',
    'ACCFIRM': '会计师事务所',
    'CSRCLEVEL1NAME': '证监会一级行业',
    'CSRCLEVEL2NAME': '证监会二级行业'
}


# ============ API 调用函数 ============

def _call_balance_sheet_api(entname: str) -> List[dict]:
    """企业资产负债表查询"""
    url = url_o + '/financialstatements/generalCompanyAssetsLiabilities'
    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))

    headers = {
        'Accept': 'application/json',
        'X-Uid': uid,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': encrypt(nonce + ";" + key + ";" + timestamp + ";" + uid + ";")
    }

    params = {'entname': entname, 'size': 1000}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return []
        response_data = response.json()
        if response_data.get('code') == 200:
            return response_data.get('data', [])
        return []
    except Exception:
        return []


def _call_profit_api(entname: str) -> List[dict]:
    """企业利润表查询"""
    url = url_o + '/financialstatements/generalCorporateProfit'
    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))

    headers = {
        'Accept': 'application/json',
        'X-Uid': uid,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': encrypt(nonce + ";" + key + ";" + timestamp + ";" + uid + ";")
    }

    params = {'entname': entname, 'size': 1000}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return []
        response_data = response.json()
        if response_data.get('code') == 200:
            return response_data.get('data', [])
        return []
    except Exception:
        return []


def _call_cashflow_api(entname: str) -> List[dict]:
    """企业现金流量表查询"""
    url = url_o + '/financialstatements/generalCompanyCashFlow'
    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))

    headers = {
        'Accept': 'application/json',
        'X-Uid': uid,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': encrypt(nonce + ";" + key + ";" + timestamp + ";" + uid + ";")
    }

    params = {'entname': entname, 'size': 1000}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return []
        response_data = response.json()
        if response_data.get('code') == 200:
            return response_data.get('data', [])
        return []
    except Exception:
        return []


def _call_basic_info_api(entname: str) -> dict:
    """上市公司基本信息查询"""
    url = url_o + '/listed/inv'
    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))

    headers = {
        'Accept': 'application/json',
        'X-Uid': uid,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': encrypt(nonce + ";" + key + ";" + timestamp + ";" + uid + ";")
    }

    params = {'entname': entname, 'mask': "111001100001011010100011"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response_json = response.json()

        api_code = response_json.get('CODE') or response_json.get('code')
        if api_code != 200:
            return {}

        listedinv_data = response_json.get('LISTEDINV') or response_json.get('listedinv')
        if listedinv_data and 'BASICINFO' in listedinv_data:
            basic_info_raw = listedinv_data['BASICINFO']
            # 转换为中文字段名
            return {
                BASIC_INFO_FIELD_MAPPING.get(k, k): v
                for k, v in basic_info_raw.items()
                if k in BASIC_INFO_FIELD_MAPPING and v
            }
        return {}
    except Exception:
        return {}


# ============ 数据处理函数 ============

def _process_financial_data(all_data: List[dict]) -> List[dict]:
    """
    处理财务数据，实现近三年一期的数据获取和去重逻辑
    """
    if not all_data:
        return []

    processed_data = []
    for item in all_data:
        try:
            report_year = item.get('reportyear')
            reportdate_type = item.get('reportdatetype')
            end_date = item.get('enddate')
            report_type = item.get('reporttype')

            if not all([report_year, reportdate_type, end_date, report_type]):
                continue

            item_copy = item.copy()
            item_copy['_report_year'] = int(report_year) if report_year else 0
            item_copy['_reportdate_type'] = int(reportdate_type) if reportdate_type else 0
            item_copy['_end_date'] = str(end_date) if end_date else ''
            item_copy['_report_type'] = int(report_type) if report_type else 0
            processed_data.append(item_copy)
        except (ValueError, TypeError):
            continue

    if not processed_data:
        return []

    # 按会计年度倒序取最近3年的年报数据
    annual_data = [item for item in processed_data if item['_reportdate_type'] == 4]
    annual_data.sort(key=lambda x: x['_report_year'], reverse=True)

    current_year = datetime.now().year
    base_year = current_year - 1
    recent_years = [base_year - i for i in range(3)]
    data_1 = [item for item in annual_data if item['_report_year'] in recent_years]

    # 按截止日期取最近1个
    processed_data.sort(key=lambda x: x['_end_date'], reverse=True)
    processed_data.sort(key=lambda x: (0 if x['_report_type'] == 3 else 1 if x['_report_type'] == 4 else 2, x['_report_type']))

    data_2 = [processed_data[0]] if processed_data else []

    # 合并去重
    combined_data = data_1.copy()
    for item_2 in data_2:
        is_contained = False
        for item_1 in data_1:
            if (item_1['_report_year'] == item_2['_report_year'] and
                item_1['_reportdate_type'] == item_2['_reportdate_type'] and
                item_1['_end_date'] == item_2['_end_date']):
                is_contained = True
                break
        if not is_contained:
            combined_data.append(item_2)

    # 相同键去重
    final_data = []
    processed_keys = set()

    for item in combined_data:
        key = (item['_report_year'], item['_reportdate_type'], item['_end_date'])
        if key in processed_keys:
            continue

        same_key_items = [x for x in combined_data if
                         (x['_report_year'], x['_reportdate_type'], x['_end_date']) == key]
        same_key_items.sort(key=lambda x: (0 if x['_report_type'] == 3 else 1 if x['_report_type'] == 4 else 2, x['_report_type']))

        if same_key_items:
            final_data.append(same_key_items[0])
            processed_keys.add(key)

    # 清理临时字段
    for item in final_data:
        for temp_key in ['_report_year', '_reportdate_type', '_end_date', '_report_type']:
            item.pop(temp_key, None)

    return final_data


def _format_financial_data(data_list: List[dict], data_type: str) -> List[dict]:
    """格式化财务数据"""
    if not data_list:
        return []

    if data_type == 'cashflow':
        field_mapping = CASH_FLOW_FIELD_MAPPING
        allowed_fields = CASH_FLOW_ALLOWED_FIELDS
    elif data_type == 'balance':
        field_mapping = BALANCE_SHEET_FIELD_MAPPING
        allowed_fields = BALANCE_SHEET_ALLOWED_FIELDS
    elif data_type == 'profit':
        field_mapping = PROFIT_FIELD_MAPPING
        allowed_fields = PROFIT_ALLOWED_FIELDS
    else:
        return data_list

    formatted_results = []
    for item in data_list:
        formatted_item = {}
        for key, value in item.items():
            if key in allowed_fields:
                chinese_name = field_mapping.get(key, key)

                # 报表类型转换
                if key == 'reporttype' and value is not None:
                    try:
                        value = REPORT_TYPE_MAPPING.get(int(value), str(value))
                    except (ValueError, TypeError):
                        pass

                # 报告期类型转换
                elif key == 'reportdatetype' and value is not None:
                    try:
                        value = REPORT_DATE_TYPE_MAPPING.get(int(value), str(value))
                    except (ValueError, TypeError):
                        pass

                formatted_item[chinese_name] = value

        formatted_results.append(formatted_item)

    return formatted_results


def _call_financial_api(entname: str) -> dict:
    """综合财务报表查询"""
    # 调用三大报表接口
    assets_data = _call_balance_sheet_api(entname)
    profit_data = _call_profit_api(entname)
    cashflow_data = _call_cashflow_api(entname)

    # 调用企业基本信息接口
    basic_info = _call_basic_info_api(entname)

    # 处理各报表数据
    processed_assets = _process_financial_data(assets_data)
    processed_profit = _process_financial_data(profit_data)
    processed_cashflow = _process_financial_data(cashflow_data)

    # 格式化数据
    formatted_assets = _format_financial_data(processed_assets, 'balance')
    formatted_profit = _format_financial_data(processed_profit, 'profit')
    formatted_cashflow = _format_financial_data(processed_cashflow, 'cashflow')

    # 按会计年度倒序排列
    def sort_by_year(data_list):
        return sorted(data_list, key=lambda x: int(x.get('会计年度', 0)), reverse=True)

    formatted_assets = sort_by_year(formatted_assets)
    formatted_profit = sort_by_year(formatted_profit)
    formatted_cashflow = sort_by_year(formatted_cashflow)

    # 检查数据有效性
    if formatted_assets:
        current_year = datetime.now().year
        last_year = current_year - 1
        first_asset_year = formatted_assets[0].get('会计年度')
        if first_asset_year:
            try:
                report_year = int(first_asset_year)
                if report_year != current_year and report_year != last_year:
                    return "未查询到上市公司财务信息"
            except (ValueError, TypeError):
                return "未查询到上市公司财务信息"

    # 检查是否有数据
    if len(formatted_assets) + len(formatted_profit) + len(formatted_cashflow) == 0:
        return "未查询到上市公司财务信息"

    return {
        '企业基本信息': basic_info,
        '资产负债表': formatted_assets,
        '利润表': formatted_profit,
        '现金流量表': formatted_cashflow
    }


# ============ 后处理函数 ============

def _format_value(value: Any) -> str:
    """格式化字段值"""
    if value is None or value == "":
        return "暂无数据"
    return str(value)


def _process_financial_info(financial: dict) -> str:
    """后处理：从数据生成财务信息提炼结果"""
    if isinstance(financial, str):
        return f"# 财务信息提炼\n\n{financial}"

    sections = ["财务信息提炼"]

    # 1. 提取企业基本信息
    basic_info = financial.get('企业基本信息', {})
    if basic_info:
        sections.append("1. 企业基本信息")
        fields = [
            '公司简称', '英文名称', '英文简称', '员工人数', '主营业务', '公司简介',
            '注册地址', '办公地址', '董事长', '董秘', '总经理', '证券代表',
            '律师事务所', '会计师事务所', '证监会一级行业', '证监会二级行业'
        ]
        for field_name in fields:
            value = basic_info.get(field_name)
            sections.append(f"{field_name}：{_format_value(value)}")
        sections.append("")

    # 2. 提取现金流量表（取最新一期）
    cash_flow = financial.get('现金流量表', [])
    if cash_flow and len(cash_flow) > 0:
        latest_cash_flow = cash_flow[0]
        sections.append("2. 现金流量表")
        sections.append(f"报表类型：{_format_value(latest_cash_flow.get('报表类型'))}")
        sections.append(f"会计年度：{_format_value(latest_cash_flow.get('会计年度'))}")
        sections.append(f"报告期类型：{_format_value(latest_cash_flow.get('报告期类型'))}")
        sections.append(f"销售商品、提供劳务收到的现金：{_format_value(latest_cash_flow.get('销售商品、提供劳务收到的现金'))}")
        sections.append(f"经营活动现金流入小计：{_format_value(latest_cash_flow.get('经营活动现金流入小计'))}")
        sections.append(f"经营活动产生的现金流量净额：{_format_value(latest_cash_flow.get('一、经营活动产生的现金流量净额'))}")
        sections.append(f"投资活动产生的现金流量净额：{_format_value(latest_cash_flow.get('二、投资活动产生的现金流量净额'))}")
        sections.append(f"筹资活动产生的现金流量净额：{_format_value(latest_cash_flow.get('三、筹资活动产生的现金流量净额'))}")
        sections.append(f"现金及现金等价物净增加额：{_format_value(latest_cash_flow.get('五、现金及现金等价物净增加额'))}")
        sections.append("")

    # 3. 提取资产负债表（取最新一期）
    balance_sheet = financial.get('资产负债表', [])
    if balance_sheet and len(balance_sheet) > 0:
        latest_balance = balance_sheet[0]
        sections.append("3. 资产负债表")
        sections.append(f"报表类型：{_format_value(latest_balance.get('报表类型'))}")
        sections.append(f"会计年度：{_format_value(latest_balance.get('会计年度'))}")
        sections.append(f"报告期类型：{_format_value(latest_balance.get('报告期类型'))}")
        sections.append(f"货币资金：{_format_value(latest_balance.get('货币资金'))}")
        sections.append(f"交易性金融资产：{_format_value(latest_balance.get('交易性金融资产'))}")
        sections.append(f"应收票据及应收账款：{_format_value(latest_balance.get('应收票据及应收账款'))}")
        sections.append(f"应收款项融资：{_format_value(latest_balance.get('应收款项融资'))}")
        sections.append(f"预付款项：{_format_value(latest_balance.get('预付款项'))}")
        sections.append(f"其他应收款合计：{_format_value(latest_balance.get('其他应收款合计'))}")
        sections.append(f"存货：{_format_value(latest_balance.get('存货'))}")
        sections.append(f"合同资产：{_format_value(latest_balance.get('合同资产'))}")
        sections.append(f"流动资产合计：{_format_value(latest_balance.get('流动资产合计'))}")
        sections.append(f"长期应收款：{_format_value(latest_balance.get('长期应收款'))}")
        sections.append(f"长期股权投资：{_format_value(latest_balance.get('长期股权投资'))}")
        sections.append(f"固定资产及清理合计：{_format_value(latest_balance.get('固定资产及清理合计'))}")
        sections.append(f"无形资产：{_format_value(latest_balance.get('无形资产'))}")
        sections.append(f"商誉：{_format_value(latest_balance.get('商誉'))}")
        sections.append(f"递延所得税资产：{_format_value(latest_balance.get('递延所得税资产'))}")
        sections.append(f"非流动资产合计：{_format_value(latest_balance.get('非流动资产合计'))}")
        sections.append(f"资产总计：{_format_value(latest_balance.get('资产总计'))}")
        sections.append(f"短期借款：{_format_value(latest_balance.get('短期借款'))}")
        sections.append(f"应付票据及应付账款：{_format_value(latest_balance.get('应付票据及应付账款'))}")
        sections.append(f"预收款项：{_format_value(latest_balance.get('预收款项'))}")
        sections.append(f"租赁负债：{_format_value(latest_balance.get('租赁负债'))}")
        sections.append(f"其他应付款合计：{_format_value(latest_balance.get('其他应付款合计'))}")
        sections.append(f"合同负债：{_format_value(latest_balance.get('合同负债'))}")
        sections.append(f"流动负债合计：{_format_value(latest_balance.get('流动负债合计'))}")
        sections.append(f"长期应付款合计：{_format_value(latest_balance.get('长期应付款合计'))}")
        sections.append(f"非流动负债合计：{_format_value(latest_balance.get('非流动负债合计'))}")
        sections.append(f"负债合计：{_format_value(latest_balance.get('负债合计'))}")
        sections.append(f"实收资本(或股本)：{_format_value(latest_balance.get('实收资本(或股本)'))}")
        sections.append(f"资本公积：{_format_value(latest_balance.get('资本公积'))}")
        sections.append(f"盈余公积：{_format_value(latest_balance.get('盈余公积'))}")
        sections.append(f"未分配利润：{_format_value(latest_balance.get('未分配利润'))}")
        sections.append(f"归属于母公司股东权益合计：{_format_value(latest_balance.get('归属于母公司股东权益合计'))}")
        sections.append(f"所有者权益(或股东权益)合计：{_format_value(latest_balance.get('所有者权益(或股东权益)合计'))}")
        sections.append("")

    # 4. 提取利润表（取最新一期）
    income_statement = financial.get('利润表', [])
    if income_statement and len(income_statement) > 0:
        latest_income = income_statement[0]
        sections.append("4. 利润表")
        sections.append(f"报表类型：{_format_value(latest_income.get('报表类型'))}")
        sections.append(f"会计年度：{_format_value(latest_income.get('会计年度'))}")
        sections.append(f"报告期类型：{_format_value(latest_income.get('报告期类型'))}")
        sections.append(f"营业总收入：{_format_value(latest_income.get('营业总收入'))}")
        sections.append(f"研发费用：{_format_value(latest_income.get('研发费用'))}")
        sections.append(f"财务费用：{_format_value(latest_income.get('财务费用'))}")
        sections.append(f"营业利润：{_format_value(latest_income.get('营业利润'))}")
        sections.append(f"净利润：{_format_value(latest_income.get('净利润'))}")
        sections.append(f"归属于母公司所有者的净利润：{_format_value(latest_income.get('归属于母公司所有者的净利润'))}")
        sections.append(f"基本每股收益：{_format_value(latest_income.get('基本每股收益'))}")
        sections.append(f"主营业务收入：{_format_value(latest_income.get('主营业务收入'))}")

    return '\n'.join(sections)


# ============ 主接口 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业财务信息

    Args:
        entname: 企业名称

    Returns:
        Markdown格式的财务信息
    """
    raw_data = _call_financial_api(entname)
    return _process_financial_info(raw_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python s03_financial_info.py <企业名称>")
