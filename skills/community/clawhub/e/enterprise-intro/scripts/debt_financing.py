#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
债权融资一体化脚本
合并 API 调用和后处理逻辑
"""

from typing import Dict, Any, List
from .base import call_api, encrypt, debug_print, UID, KEY, BASE_URL

import requests
import time
import random

uid = UID
key = KEY
url_o = BASE_URL


# ============ 币种映射 ============

CURRENCY_MAPPING = {
    "ATS": "奥地利先令",
    "CNY": "人民币",
    "EUR": "欧元",
    "HKD": "港元",
    "JPY": "日元",
    "USD": "美元",
    "GBP": "英镑",
    "TWD": "新台币",
    "CHF": "瑞士法郎",
    "IDR": "印尼盾",
    "KRW": "韩国元",
    "VND": "越南盾",
    "AUD": "澳大利亚元",
    "BDT": "孟加拉塔卡",
    "CAD": "加拿大元",
    "CDF": "刚果法郎",
    "INR": "印度卢比",
    "LAK": "老挝基普",
    "SGD": "新加坡元",
    "": ""
}


# ============ API 调用函数 ============

def _call_bond_api(entname: str) -> dict:
    """债券列表信息查询"""
    url = url_o + '/issueBond'
    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))

    headers = {
        'Accept': 'application/json',
        'X-Uid': uid,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': encrypt(nonce + ";" + key + ";" + timestamp + ";" + uid + ";")
    }

    params = {'entname': entname}

    try:
        response = requests.get(url, headers=headers, params=params)
        response_json = response.json()
        if response_json.get('code') == 404:
            return None
        return response_json
    except Exception:
        return None


def _call_financing_api(entname: str) -> dict:
    """企业融资信息查询"""
    url = url_o + '/financingInformation'
    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))

    headers = {
        'Accept': 'application/json',
        'X-Uid': uid,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': encrypt(nonce + ";" + key + ";" + timestamp + ";" + uid + ";")
    }

    params = {'entname': entname}

    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except Exception:
        return None


# ============ 数据处理函数 ============

def _process_participant_info(participants: List[dict]) -> str:
    """处理当事人信息"""
    if not participants or not isinstance(participants, list):
        return ""

    participant_strings = []
    for participant in participants:
        if isinstance(participant, dict) and 'type_name' in participant and 'name' in participant:
            participant_string = f"{participant['type_name']}-{participant['name']}"
            participant_strings.append(participant_string)

    return ";".join(participant_strings)


def _calculate_statistics(financing_data: dict) -> dict:
    """计算债权融资统计信息"""
    statistics = {
        '债券融资总数据量': 0,
        '应收账款融资总数据量': 0,
        '融资租赁总数据量': 0,
        '信托融资总数据量': 0,
        '银行借款总数据量': 0,
        '授信额度总数据量': 0,
        '其他融资总数据量': 0,
        '有息债务总数据量': 0
    }

    if not financing_data or 'data' not in financing_data:
        return statistics

    data = financing_data['data']

    mapping = {
        'ar_acreceive': '应收账款融资总数据量',
        'fl_finlease': '融资租赁总数据量',
        'tf_finlease': '信托融资总数据量',
        'bl_bankloan': '银行借款总数据量',
        'bd_creditline': '授信额度总数据量',
        'of_othfina': '其他融资总数据量',
        'fin_inbeardebt': '有息债务总数据量'
    }

    for eng_key, chn_key in mapping.items():
        if eng_key in data and data[eng_key]:
            try:
                statistics[chn_key] = data['page_info'][eng_key]['totalcount']
            except (KeyError, TypeError):
                statistics[chn_key] = len(data[eng_key])

    return statistics


def _calculate_bond_statistics(bond_data: dict) -> tuple:
    """计算债券类型和发行年份统计"""
    bondtype_stats = {}
    bondyear_stats = {}

    if not bond_data or 'data' not in bond_data or 'bondinfo' not in bond_data['data']:
        return [], []

    bonds = bond_data['data']['bondinfo']

    # 债券类型统计
    for bond in bonds:
        bondtype = bond.get('bondtype_name', '未知')
        issuescale = float(bond.get('totalissuescale', 0) or 0)

        if bondtype not in bondtype_stats:
            bondtype_stats[bondtype] = {
                '债券类型名称': bondtype,
                '发行规模合计（万元）': 0,
                '债券类型数量': 0
            }

        bondtype_stats[bondtype]['发行规模合计（万元）'] += issuescale
        bondtype_stats[bondtype]['债券类型数量'] += 1

    # 发行年份统计
    for bond in bonds:
        issue_date = bond.get('issbegdate', '')
        if issue_date:
            try:
                year = issue_date[:4]
                issuescale = float(bond.get('totalissuescale', 0) or 0)

                if year not in bondyear_stats:
                    bondyear_stats[year] = {
                        '发行年份': year,
                        '发行规模合计（万元）': 0,
                        '发行年份数量': 0
                    }

                bondyear_stats[year]['发行规模合计（万元）'] += issuescale
                bondyear_stats[year]['发行年份数量'] += 1
            except:
                pass

    return list(bondtype_stats.values()), list(bondyear_stats.values())


def _map_bond_fields(bonds: List[dict]) -> List[dict]:
    """映射债券字段为中文"""
    mapped_bonds = []
    for bond in bonds:
        mapped_bond = {
            '债券全称': bond.get('bondname', ''),
            '债券简称': bond.get('bondsname', ''),
            '债券类型名称': bond.get('bondtype_name', ''),
            '发行人名称': bond.get('issuername', ''),
            '交易市场名称': bond.get('exchange', ''),
            '发行日期': bond.get('issbegdate', ''),
            '上市日期': bond.get('listdate', ''),
            '信用评级': bond.get('initialcreditrate', ''),
            '债券年限(年)': bond.get('maturityyear', ''),
            '票面利率(%)': bond.get('couponrate', ''),
            '发行面值(元)': bond.get('issueprice', ''),
            '发行规模（万元）': bond.get('totalissuescale', ''),
            '息票类型': bond.get('varietytype', ''),
            '付息频率': bond.get('paymentmode', ''),
            '起息日期': bond.get('startdate', ''),
            '止息日期': bond.get('enddate', ''),
            '主承销商': bond.get('leaduwer', ''),
            '到期日期': bond.get('maturitydate', '')
        }
        mapped_bonds.append(mapped_bond)
    return mapped_bonds


def _map_financing_fields(financing_items: List[dict], financing_type: str) -> List[dict]:
    """映射融资字段为中文"""
    mapped_items = []

    party_field_mapping = {
        'ar_acreceive': 'rf_party',
        'fl_finlease': 'fl_party',
        'tf_finlease': 'tf_party',
        'bl_bankloan': 'bl_party',
        'bd_creditline': 'bd_party',
        'of_othfina': 'of_party',
        'fin_inbeardebt': 'fd_party'
    }

    for item in financing_items:
        mapped_item = {}

        # 处理当事人信息
        party_field = party_field_mapping.get(financing_type)
        if party_field and party_field in item:
            mapped_item['当事人信息'] = _process_participant_info(item[party_field])

        if financing_type == 'ar_acreceive':
            mapped_item.update({
                '公告日期': item.get('publishdate', ''),
                '登记类型': item.get('recortype', ''),
                '交易业务类型': item.get('tradetype', ''),
                '币种': CURRENCY_MAPPING.get(item.get('cur', '').upper(), ''),
                '期限': item.get('maturity', ''),
                '财产描述': item.get('leasememo', ''),
                '注销登记日期': item.get('cancel_publishdate', '')
            })

            financenum = item.get('financenum', '')
            if financenum:
                try:
                    mapped_item['合同金额'] = str(float(financenum)) + item.get('cunit', '')
                except:
                    mapped_item['合同金额'] = ''
            else:
                mapped_item['合同金额'] = ''

            propertyvalue = item.get('propertyvalue', '')
            if propertyvalue:
                try:
                    mapped_item['财产价值'] = str(float(propertyvalue)) + item.get('cunit', '')
                except:
                    mapped_item['财产价值'] = ''
            else:
                mapped_item['财产价值'] = ''

        elif financing_type == 'fl_finlease':
            mapped_item.update({
                '公告日期': item.get('publishdate', ''),
                '合同金额': item.get('financenum', ''),
                '合同金额币种': item.get('cur', ''),
                '登记类型': item.get('recortype', ''),
                '期限': item.get('maturity', ''),
                '财产描述': item.get('leasememo', ''),
                '方案状态': item.get('projecttype', ''),
                '租赁类型': item.get('leasetype', ''),
                '方案简述': item.get('projectmemo', ''),
                '利率上限(%)': item.get('inrate', ''),
                '借款余额': item.get('loanbalance', ''),
                '财产价值(元)': item.get('propertyvalue', ''),
                '财产价值币种': CURRENCY_MAPPING.get(item.get('propertyvaluecur', '').upper(), ''),
                '是否到期': item.get('ismaturity', ''),
                '注销登记日期': item.get('cancel_publishdate', '')
            })

        elif financing_type == 'tf_finlease':
            mapped_item.update({
                '公告日期': item.get('publishdate', ''),
                '融资额币种': CURRENCY_MAPPING.get(item.get('cur', '').upper(), ''),
                '期限': item.get('maturity', ''),
                '方案状态': item.get('projecttype', ''),
                '方案简述': item.get('projectmemo', ''),
                '投资方向': item.get('investdirection', ''),
                '年利率(%)': item.get('yearrate', ''),
                '信托计划名称': item.get('trustname', ''),
                '借款余额(万)': item.get('loanbalance', ''),
                '余额截止日期': item.get('balenddate', '')
            })

            financenum = item.get('financenum', '')
            if financenum:
                try:
                    mapped_item['融资额数量'] = str(float(financenum)) + item.get('cunit', '')
                except:
                    mapped_item['融资额数量'] = ''
            else:
                mapped_item['融资额数量'] = ''

        elif financing_type == 'bl_bankloan':
            mapped_item.update({
                '公告日期': item.get('publishdate', ''),
                '融资额数量': item.get('financenum', ''),
                '融资额币种': CURRENCY_MAPPING.get(item.get('cur', '').upper(), ''),
                '融资额说明': item.get('tfinancen', ''),
                '期限': item.get('maturity', ''),
                '方案状态': item.get('projecttype', ''),
                '方案简述': item.get('projectmemo', ''),
                '余额(万元)': item.get('balance', ''),
                '余额截止日期': item.get('benddate', ''),
                '利率': item.get('rate', '')
            })

        elif financing_type == 'bd_creditline':
            mapped_item.update({
                '公告日期': item.get('publishdate', ''),
                '签署授信协议银行家数': item.get('signcreditbanknum', ''),
                '币种': CURRENCY_MAPPING.get(item.get('cur', '').upper(), ''),
                '授信额度合计(亿元)': item.get('totcreditline', ''),
                '已使用额度合计(亿元)': item.get('totusedquota', ''),
                '未使用额度合计(亿元)': item.get('totunusedquota', ''),
                '授信方案': item.get('memo', '')
            })

        elif financing_type == 'of_othfina':
            mapped_item.update({
                '融资类型': item.get('ftype', ''),
                '公告日期': item.get('publishdate', ''),
                '融资额数量(万元)': item.get('financenum', ''),
                '融资额币种': CURRENCY_MAPPING.get(item.get('cur', '').upper(), ''),
                '期限': item.get('maturity', ''),
                '是否到期': item.get('isexpire', ''),
                '利率': item.get('intrate', ''),
                '方案状态': item.get('projecttype', ''),
                '融资金额说明': item.get('memo', ''),
                '借款余额(万元)': item.get('loanbalance', ''),
                '方案简述': item.get('projectmemo', '')
            })

        elif financing_type == 'fin_inbeardebt':
            mapped_item.update({
                '公告日期': item.get('publishdate', ''),
                '报表合并范围': item.get('reportrange', ''),
                '报表日期': item.get('reportdate', ''),
                '币种': CURRENCY_MAPPING.get(item.get('cur', '').upper(), ''),
                '有息债务': item.get('inbeardebt', ''),
                '短期债务': item.get('shtdebt', ''),
                '短期借款': item.get('shorttermborr', ''),
                '长期债务': item.get('ltmdebt', ''),
                '长期借款': item.get('longborr', ''),
                '应付长期债券': item.get('longtermbond', ''),
                '租赁负债': item.get('leaseliab', '')
            })

        mapped_items.append(mapped_item)

    return mapped_items


def _call_debt_financing_api(entname: str) -> dict:
    """债权融资综合查询"""
    # 查询债券信息
    bond_result = _call_bond_api(entname)
    bond_data = None
    if bond_result and isinstance(bond_result, dict) and bond_result.get('code') == 200:
        bond_data = bond_result

    # 查询融资信息
    financing_result = _call_financing_api(entname)
    financing_data = None
    if financing_result and isinstance(financing_result, dict) and financing_result.get('code') == 200:
        financing_data = financing_result

    # 如果都查询失败
    if not bond_data and not financing_data:
        return "未查询到债权融资信息"

    # 构建返回数据
    result = {
        '债权融资统计信息': {},
        '债券类型统计': [],
        '债券发行年份统计': [],
        '债券融资': [],
        '应收账款融资': [],
        '融资租赁': [],
        '信托融资': [],
        '银行借款': [],
        '授信额度': [],
        '其他融资': [],
        '有息债务': []
    }

    # 处理债券数据
    if bond_data and 'data' in bond_data:
        if 'bondinfo' in bond_data['data']:
            result['债券融资'] = _map_bond_fields(bond_data['data']['bondinfo'])

        bondtype_stats, bondyear_stats = _calculate_bond_statistics(bond_data)
        result['债券类型统计'] = bondtype_stats
        result['债券发行年份统计'] = bondyear_stats

    # 处理融资数据
    if financing_data and 'data' in financing_data:
        financing_data_items = financing_data['data']

        financing_types = {
            'ar_acreceive': '应收账款融资',
            'fl_finlease': '融资租赁',
            'tf_finlease': '信托融资',
            'bl_bankloan': '银行借款',
            'bd_creditline': '授信额度',
            'of_othfina': '其他融资',
            'fin_inbeardebt': '有息债务'
        }

        for eng_key, chn_key in financing_types.items():
            if eng_key in financing_data_items and financing_data_items[eng_key]:
                result[chn_key] = _map_financing_fields(financing_data_items[eng_key], eng_key)

    # 计算统计信息
    stats = _calculate_statistics(financing_data if financing_data else {})
    if bond_data and 'data' in bond_data and 'totalcount' in bond_data['data']:
        stats['债券融资总数据量'] = bond_data['data']['totalcount']
    elif bond_data and 'data' in bond_data and 'bondinfo' in bond_data['data']:
        stats['债券融资总数据量'] = len(bond_data['data']['bondinfo'])

    result['债权融资统计信息'] = stats

    return result


# ============ 后处理函数 ============

def _format_number(value: Any, decimals: int = 2) -> str:
    """格式化数字"""
    if value is None or value == "":
        return ""
    try:
        return f"{float(value):.{decimals}f}"
    except:
        return str(value)


def _process_debt_financing(debt_info: dict) -> str:
    """后处理：从数据生成债权融资提炼结果"""
    if isinstance(debt_info, str) and ('未查询到' in debt_info or not debt_info):
        return (
            "债权融资提炼\n"
            "### 债权融资总体统计\n"
            "债权融资总笔数：0笔；应收账款融资：0笔；融资租赁：0笔；信托融资：0笔；"
            "银行借款：0笔；授信额度：0笔；其他融资：0笔；有息债务：0笔。\n\n"
            "### 债券融资明细\n"
            "未查询到债券融资相关数据。\n\n"
            "### 融资方式关键指标\n"
            "未查询到各类融资方式关键指标数据。\n\n"
            "### 当事人与时间信息\n"
            "未查询到当事人与时间相关信息。"
        )

    sections = ["债权融资提炼"]

    # 模块一：债权融资总体统计
    stats = debt_info.get('债权融资统计信息', {})
    if stats:
        sections.append("### 债权融资总体统计")

        total = (
            stats.get('债券融资总数据量', 0) +
            stats.get('应收账款融资总数据量', 0) +
            stats.get('融资租赁总数据量', 0) +
            stats.get('信托融资总数据量', 0) +
            stats.get('银行借款总数据量', 0) +
            stats.get('授信额度总数据量', 0) +
            stats.get('其他融资总数据量', 0) +
            stats.get('有息债务总数据量', 0)
        )

        stat_line = (
            f"债权融资总笔数：{total}笔；"
            f"应收账款融资：{stats.get('应收账款融资总数据量', 0)}笔；"
            f"融资租赁：{stats.get('融资租赁总数据量', 0)}笔；"
            f"信托融资：{stats.get('信托融资总数据量', 0)}笔；"
            f"银行借款：{stats.get('银行借款总数据量', 0)}笔；"
            f"授信额度：{stats.get('授信额度总数据量', 0)}笔；"
            f"其他融资：{stats.get('其他融资总数据量', 0)}笔；"
            f"有息债务：{stats.get('有息债务总数据量', 0)}笔。"
        )
        sections.append(stat_line)
        sections.append("")

    # 模块二：债券融资明细
    bond_types = debt_info.get('债券类型统计', [])
    bond_years = debt_info.get('债券发行年份统计', [])
    bonds = debt_info.get('债券融资', [])

    if bond_types or bond_years or bonds:
        sections.append("### 债券融资明细")

        if bond_types:
            type_parts = []
            for bt in bond_types[:5]:
                amount = _format_number(bt.get('发行规模合计（万元）', 0), 2)
                type_parts.append(f"{bt.get('债券类型名称', '')}发行规模{amount}万元")
            sections.append("债券类型：" + "；".join(type_parts) + "。")

        if bond_years:
            year_parts = []
            for by in sorted(bond_years, key=lambda x: x.get('发行年份', ''), reverse=True)[:5]:
                amount = _format_number(by.get('发行规模合计（万元）', 0), 2)
                year_parts.append(f"{by.get('发行年份', '')}年发行{amount}万元")
            sections.append("发行年份分布：" + "；".join(year_parts) + "。")

        if bonds:
            latest_bond = max(bonds, key=lambda x: x.get('发行日期', ''))
            bond_code = latest_bond.get('债券简称', '')
            scale = _format_number(latest_bond.get('发行规模（万元）', 0), 2)
            rate = latest_bond.get('票面利率(%)', '')
            rate_str = f"，利率{rate}%" if rate else ""
            sections.append(f"代表性债券：{latest_bond.get('债券全称', '')}（{bond_code}，规模{scale}万元{rate_str}）。")

        sections.append("")

    # 模块三：融资方式关键指标
    sections.append("### 融资方式关键指标")
    indicator_parts = []

    ar_financing = debt_info.get('应收账款融资', [])
    if ar_financing:
        ar = ar_financing[0]
        amount = ar.get('合同金额', '')
        period = ar.get('期限', '')
        if amount or period:
            indicator_parts.append(f"应收账款融资：合同金额{amount}，期限{period}")

    trust_financing = debt_info.get('信托融资', [])
    if trust_financing:
        trust = trust_financing[0]
        amount = trust.get('融资额数量', '')
        if amount:
            indicator_parts.append(f"信托融资：融资额{amount}")

    bank_loans = debt_info.get('银行借款', [])
    if bank_loans:
        loan = None
        for l in bank_loans:
            if l.get('利率') or l.get('余额(万元)'):
                loan = l
                break
        if not loan:
            loan = bank_loans[0]

        parts = []
        if loan.get('融资额数量'):
            parts.append(f"融资额{_format_number(loan.get('融资额数量'), 2)}万元")
        if loan.get('利率'):
            rate = loan.get('利率')
            rate_str = rate if '%' in str(rate) else f"{_format_number(rate, 2)}%"
            parts.append(f"利率{rate_str}")
        if loan.get('余额(万元)'):
            parts.append(f"余额{_format_number(loan.get('余额(万元)'), 2)}万元")
        if parts:
            indicator_parts.append(f"银行借款：{'，'.join(parts)}")

    interest_debt = debt_info.get('有息债务', [])
    if interest_debt:
        debt = interest_debt[0]
        total_debt = debt.get('有息债务', '')
        if total_debt:
            indicator_parts.append(f"有息债务：总额{_format_number(total_debt, 2)}万元")

    if indicator_parts:
        sections.append("；\n".join(indicator_parts) + "。")
    else:
        sections.append("未查询到各类融资方式关键指标数据。")
    sections.append("")

    # 模块四：当事人与时间信息
    sections.append("### 当事人与时间信息")

    parties_dict = {}
    latest_date = None
    latest_cancel_date = None

    for ar in ar_financing[:10]:
        party_info = ar.get('当事人信息', '')
        if party_info:
            for part in party_info.split(';'):
                if '-' in part:
                    role, name = part.split('-', 1)
                    if '中国工商银行' in name or len(parties_dict) < 2:
                        parties_dict[name.strip()] = role.strip()

        date = ar.get('公告日期', '')
        if date and (not latest_date or date > latest_date):
            latest_date = date
        cancel_date = ar.get('注销登记日期', '')
        if cancel_date and (not latest_cancel_date or cancel_date > latest_cancel_date):
            latest_cancel_date = cancel_date

    for loan in bank_loans[:10]:
        party_info = loan.get('当事人信息', '')
        if party_info and len(parties_dict) < 2:
            for part in party_info.split(';'):
                if '-' in part:
                    role, name = part.split('-', 1)
                    if '中国工商银行' in name or len(parties_dict) < 2:
                        parties_dict[name.strip()] = role.strip()

        date = loan.get('公告日期', '')
        if date and (not latest_date or date > latest_date):
            latest_date = date

    if parties_dict:
        party_list = [f"{name}（{role}）" for name, role in list(parties_dict.items())[:2]]
        sections.append(f"主要当事人：{('、'.join(party_list))}；")
    else:
        sections.append("主要当事人：暂无数据；")

    def format_date(date_str):
        if not date_str or date_str == "无":
            return "无"
        try:
            if '-' in date_str:
                parts = date_str.split('-')
                return f"{parts[0]}年{parts[1]}月{parts[2]}日"
            return date_str
        except:
            return date_str

    date_str = format_date(latest_date) if latest_date else "无"
    cancel_str = format_date(latest_cancel_date) if latest_cancel_date else "无"
    sections.append(f"最近融资公告日期：{date_str}；最近注销日期：{cancel_str}。")

    return '\n'.join(sections)


# ============ 主接口 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业债权融资信息

    Args:
        entname: 企业名称

    Returns:
        Markdown格式的债权融资信息
    """
    raw_data = _call_debt_financing_api(entname)
    return _process_debt_financing(raw_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python s04_debt_financing.py <企业名称>")
