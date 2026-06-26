#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上市信息一体化脚本
合并 API 调用和后处理逻辑
"""

from typing import Dict, Any, List
from .base import call_api, encrypt, get_headers, BASE_URL, debug_print, UID, KEY

import requests
import time
import random
from datetime import datetime

uid = UID
key = KEY
url_o = BASE_URL


# ============ 字段映射 ============

MODULE_NAME_MAPPING = {
    'BASICINFO': '企业基本信息',
    'CONTACTINFO': '企业联系信息',
    'IPODECLAREINFO': '申报情况',
    'SKBASICINFO': '股票基本信息',
    'STKFREEZING': '股东持股冻结信息',
    'GUARANTEE': '对外担保信息',
    'SKPROIPO': '发行信息',
    'IMPORTANTINDIC': '重要指标',
    'OTSHOLDER': '十大流通股东',
    'DIVIDENTS': '分红情况',
    'FINANCIALINDEX': '财务指标',
    'basicinfo': '港股企业基本信息',
    'contactinfo': '港股企业联系信息',
    'hkbasicinfo': '港股股票基本信息',
    'hk_basicinfo': '港股企业基本信息',
    'hk_contactinfo': '港股企业联系信息',
    'hk_hkbasicinfo': '港股股票基本信息'
}

FIELD_NAME_MAPPING = {
    # 企业基本信息字段
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
    'CSRCLEVEL2NAME': '证监会二级行业',
    'BIZSCOPE': '经营范围',

    # 企业联系信息字段
    'COMPURL': '公司网址',
    'COMPEMAIL': '公司电子邮箱',
    'COMPTEL': '公司电话',
    'COMPFAX': '公司传真',
    'SERVICETEL': '客服电话',

    # 申报情况字段
    'ENTNAME': '公司全称',
    'FINANCINGAMOUNT': '融资金额',
    'AUDITSTATUS': '审核状态',
    'UPDATEDATE': '更新日期',
    'ACCEPTDATE': '已受理日期',
    'ENQUIRYDATE': '已问询日期',
    'COMMITTEEMEETINGDATE': '上市委会议日期',
    'REGISTRYDATE': '提交注册日期',
    'REGISTRYRESULTDATE': '注册结果日期',
    'SPONSOR': '保荐机构',
    'SPONSORREP': '保荐代表人',
    'SIGNACCOUNTANT': '签字会计师',
    'SIGNLAWYER': '签字律师',
    'APPRAISEFIRM': '评估机构',
    'SIGNAPPRAISER': '签字评估师',
    'LASTAUDITTIME': '最近一期审计基准日',
    'BOARD': '申报上市板块',
    'STOCKCODE': '北交所代码',
    'SUSPENDDATE': '中止日期',
    'TERMDATE': '终止日期',

    # 股票基本信息字段
    'SYMBOL': '股票代码',
    'SESNAME': '证券简称',
    'SETYPENAME': '证券类型',
    'SEENGNAME': '英文简称',
    'CURNAME': '交易币种',
    'TOTALSHARE': '总股本',
    'LISTDATE': '上市日期',
    'LISTSTATUS': '上市状态',
    'EXCHANGE': '上市交易市场',
    'DELISTDATE': '退市日期',
    'AUTHCAPSK': '法定股本(股)',
    'HSILEVEL1NAME': '恒生一级行业名称',
    'HSILEVEL2NAME': '恒生二级行业名称',
    'LETYPE': '主体类型',
    'letype': '主体类型',

    # 股东持股冻结信息字段
    'SHHOLDERNAME': '股东名称',
    'FROZENSKAMT': '冻结股数（万股）',
    'HOLDINGSK': '所持股数（万股）',
    'FROZENRTOH': '冻结占所持股比例',
    'FROZENRTOT': '冻结占总股本比例',
    'FROZENRSN': '冻结事由',
    'FROZENBEGDATE': '冻结起始日',
    'UNFREEZEDATE': '解冻日期',
    'FROZENRSNTYPE': '冻结事由类型中文',
    'FREEZINGPERIOD': '冻结期限描述',
    'FIRSTPUBLISHDATE': '首次公布日期',
    'LATESTPUBLISHDATE': '最新更新日期',

    # 对外担保信息字段
    'GUARNAME': '担保方名称',
    'SECUREDPARTYNAME': '被担保方名称',
    'GUARTYPE': '担保形式',
    'GUARSTATUS': '担保状态',
    'GUARCONTENT': '担保内容',
    'GUARMETHOD': '担保方式',
    'ACTURALGUARAMT': '实际担保金额（万元）',
    'GUARTERM': '担保期限',
    'GUARBEGDATE': '担保起始日',
    'GUARENDDATE': '担保终止日',
    'REPORTENDDATE': '报告截止日期',

    # 发行信息字段
    'SETYPE': '证券类型',
    'ONLSUBBEGDATE': '网上发行日期',
    'ISSUEMODE': '发行方式',
    'PERVALUE': '每股面值(元)',
    'ACTISSQTY': '发行规模（万股）',
    'TOTISSEXP': '发行费用（万元）',
    'ACTNETRAISEAMT': '募资净额（万元）',
    'ACTTOTRAISEAMT': '发行总市值（万元）',
    'ISSPRICE': '发行价格（元/股）',
    'PEAFT': '发行市盈率（倍）',
    'ONLLOTWINRT': '定价中签率（%）',
    'OFFLLOTWINRT': '网下配售中签率（%）',
    'LEADUWER': '主承销商',
    'LISTRECOMER': '上市保荐机构',
    'TURNRATE': '首日换手率（%）',
    'TOPEN': '首日开盘价（元）',
    'TCLOSE': '首日收盘价（元）',

    # 重要指标字段
    'SENAME': '证券简称',
    'TRADEDATE': '交易日期',
    'TOTMKTCAP': '总市值（万元）',
    'NEGOTIABLEMV': '流通市值（万元）',
    'AMOUNT': '成交额（元）',
    'VOL': '成交量（股）',
    'LCLOSE': '前收盘价',
    'THIGH': '最高价',
    'TLOW': '最低价',
    'PCHG': '涨跌幅',
    'PB': '市净率',
    'PELFY': '静态市盈率',
    'PETTM': '滚动市盈率市盈率',
    'PEMRQ': '动态市盈率',

    # 十大流通股东字段
    'SHARESTYPE': '股份类型',
    'ENDDATE': '截止日期',
    'SHHOLDERTYPE': '股东机构类型',
    'SHHOLDERNATURE': '股东股权性质',
    'RANK': '股东排名',
    'HOLDERAMT': '持股数(股)',
    'PCTOFFLOATSHARES': '占流通A股比例(%)',
    'HOLDERRTO': '持股数量占总股本比例(%)',
    'HOLDERSUMCHG': '持股数量增减(股)',
    'HOLDERSUMCHGRATE': '持股数量增减幅度(%)',
    'PCTOFFLOTSHARES': '占流通股比例(%)',
    'ISHIS': '是否上一报告期存在股东',
    'ISREPORTDATE': '是否报告期披露',

    # 分红情况字段
    'DIVIYEAR': '年度',
    'DATETYPE': '权益日期类型',
    'DIVITYPE': '权益类型',
    'GRAOBJTYPE': '发放对象类型',
    'GRAOBJ': '发放对象',
    'EQURECORDDATE': '股权登记日',
    'XDRDATE': '除权除息日',
    'TOTCASHDV': '分红金额合计（人民币万元）',
    'ISNEWEST': '是否最新方案',
    'DIVIEXPMEMO': '权息说明',
    'PUBLISHDATE': '发布日期',

    # 财务指标字段
    'ENDPUBLISHDATE': '末次公告日期',
    'REPORTYEAR': '报告期年度',
    'REPORTDATETYPE': '报告期类型',
    'REPORTTYPE': '报表类型',
    'CUR': '币种',
    'ROEDILUTED': '净资产收益率ROE(摊薄)',
    'EPSDILUTED': '摊薄每股收益(元)',
    'NAPS': '每股净资产(元)',
    'OPNCFPS': '每股经营现金流(元)',
    'UPPS': '每股未分配利润(元)',
    'CRPS': '每股资本公积金(元)',
    'OPREVPS': '每股销售收入(元)',
    'TOPREVPS': '每股营业总收入(元)',
    'NCFPS': '每股现金流量净额(元)',
    'SCOSTRT': '销售成本率(%)',
    'ROEAVG': '净资产收益率_平均(%)',
    'SGPMARGIN': '销售毛利率(%)',
    'SNPMARGINCONMS': '销售净利率(含少数股权权益%)',
    'CURRENTRT': '流动比率(倍)',
    'QUICKRT': '速动比率(倍)',
    'ASSLIABRT': '资产负债率(%)',
    'EM': '权益乘数(倍)',
    'EQURT': '产权比率(%)',
    'CASHRT': '现金比率(倍)',
    'OPNCFTOCURLIAB': '现金流量比率(倍)',
    'ACCRECGTURNRT': '应收账款周转率(次)',
    'ACCRECGTURNDAYS': '应收账款周转天数(天)',
    'INVTURNRT': '存货周转率(次)',
    'INVTURNDAYS': '存货周转天数(天)',
    'TATURNRT': '总资产周转率(次)',
    'TATURNDAYS': '总资产周转天数(天)',
    'NPCUT': '扣非净利润(元)',
    'OPGPMARGIN': '营业毛利润(元)',
    'NPTOAVGTA': '总资产净利率_平均(%)',
    'NPTOTP': '归属母公司的净利润/利润总额(%)',
    'TAAVG': '平均资产总额(元)',
    'TAGRT': '营业总收入同比增长(%)',
    'NPGRT': '归母净利润同比增长率(%)',

    # 港股字段 (小写)
    'compsname': '公司简称',
    'engname': '英文名称',
    'engsname': '英文简称',
    'workforce': '员工人数',
    'bizscope': '经营范围',
    'majorbiz': '主营业务',
    'compintro': '公司简介',
    'chairman': '董事长',
    'bsecretary': '董秘',
    'manager': '总经理',
    'seaffrepr': '证券代表',
    'leconstant': '律师事务所',
    'accfirm': '会计师事务所',
    'compurl': '公司网址',
    'compemail': '公司电子邮箱',
    'comptel': '公司电话',
    'compfax': '公司传真',
    'servicetel': '客服电话',
    'symbol': '股票代码',
    'sesname': '证券简称',
    'seengname': '英文简称',
    'setypename': '证券类型名称',
    'curname': '交易币种',
    'listdate': '上市日期',
    'authcapsk': '法定股本(股)',
    'liststatus': '上市状态',
    'exchange': '上市交易市场',
    'board': '上市板块',
    'delistdate': '退市日期',
    'hsilevel1name': '恒生一级行业名称',
    'hsilevel2name': '恒生二级行业名称',
    'publishdate': '公告日期',
    'begindate': '变动起始日',
    'enddate': '变动截止日',
    'totalshare': '总股本(股)',
    'mktshare': '流通股本(股)',
    'hkshare': 'H股股本(股)',
    'changersn': '变动原因',
    'sharetype': '股份类型',
    'shareamt': '股本数量',
    'changedire': '变动方向',
    'changeamt': '变动数量',
    'vaule': '面值',
}

# 报表类型中文映射
REPORT_TYPE_MAPPING = {
    1: "合并期末",
    2: "母公司期末",
    3: "合并期末_调整",
    4: "母公司期末_调整"
}

# 报告期类型中文映射
REPORT_DATE_TYPE_MAPPING = {
    1: "一季报",
    2: "中报（累计）",
    3: "三季报（累计）",
    4: "年报(累计)"
}


# ============ API 调用函数 ============

def _call_mainland_listed_api(entname: str) -> dict:
    """内地上市公司基本信息查询"""
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

    params = {
        'entname': entname,
        'mask': "111001100001011010100011"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response_json = response.json()

        api_code = response_json.get('CODE') or response_json.get('code')
        api_message = response_json.get('MSG') or response_json.get('message', '未知错误')

        if api_code != 200:
            return {'code': api_code, 'message': '未查询到内地上市信息', 'data': ""}

        listedinv_data = response_json.get('LISTEDINV') or response_json.get('listedinv')

        processed_data = None
        if listedinv_data:
            processed_data = listedinv_data.copy()

            if 'BASICINFO' in processed_data:
                basic_info_raw = processed_data['BASICINFO']
                required_fields = [
                    'COMPSNAME', 'ENGNAME', 'ENGSNAME', 'WORKFORCE', 'MAJORBIZ',
                    'COMPINTRO', 'REGADDR', 'OFFICEADDR', 'CHAIRMAN', 'BSECRETARY',
                    'MANAGER', 'SEAFFREPR', 'LECONSTANT', 'ACCFIRM', 'CSRCLEVEL1NAME',
                    'CSRCLEVEL2NAME'
                ]
                filtered_basic_info = {
                    field: basic_info_raw[field]
                    for field in required_fields if field in basic_info_raw
                }
                if filtered_basic_info:
                    processed_data['BASICINFO'] = filtered_basic_info
                else:
                    del processed_data['BASICINFO']

        has_data = bool(processed_data and any(value for value in processed_data.values() if value))

        return {
            'code': api_code,
            'message': api_message,
            'data': processed_data if has_data else ""
        }

    except Exception as e:
        return {'code': -1, 'message': '未查询到内地上市信息', 'data': ""}


def _call_hk_listed_api(entname: str, mask: str = "11100000000") -> dict:
    """港股上市公司信息查询"""
    url = url_o + '/hkListed/inv'
    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))

    headers = {
        'Accept': 'application/json',
        'X-Uid': uid,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': encrypt(nonce + ";" + key + ";" + timestamp + ";" + uid + ";")
    }

    params = {'entname': entname, 'mask': mask}

    try:
        response = requests.get(url, headers=headers, params=params)
        response_json = response.json()

        api_code = response_json.get('CODE') or response_json.get('code')
        api_message = response_json.get('MSG') or response_json.get('message', '未知错误')

        if api_code != 200:
            return {'code': api_code, 'message': '未查询到港股上市信息', 'data': ""}

        processed_data = None
        data_field = response_json.get('data')
        if data_field:
            processed_data = data_field.copy()

            if 'basicinfo' in processed_data:
                basic_info_raw = processed_data['basicinfo']
                required_fields = [
                    'compsname', 'engname', 'engsname', 'workforce', 'majorbiz',
                    'compintro', 'regaddr', 'officeaddr', 'chairman', 'bsecretary',
                    'manager', 'seaffrepr', 'leconstant', 'accfirm'
                ]
                filtered_basic_info = {
                    field: basic_info_raw[field]
                    for field in required_fields if field in basic_info_raw
                }
                if filtered_basic_info:
                    processed_data['basicinfo'] = filtered_basic_info
                else:
                    del processed_data['basicinfo']

        has_data = bool(processed_data and any(value for value in processed_data.values() if value))

        return {
            'code': api_code,
            'message': api_message,
            'data': processed_data if has_data else ""
        }

    except Exception as e:
        return {'code': -1, 'message': '未查询到港股上市信息', 'data': ""}


def _merge_listed_info(mainland_data: dict, hk_data: dict) -> dict:
    """合并内地和港股上市信息"""
    merged = {}

    if isinstance(mainland_data, dict):
        merged.update(mainland_data)

    if isinstance(hk_data, dict):
        for key, value in hk_data.items():
            if key == 'basicinfo':
                if 'BASICINFO' in merged:
                    continue
                else:
                    merged['BASICINFO'] = value
                    continue
            hk_key = f"hk_{key}" if key not in merged else f"hk_{key}"
            merged[hk_key] = value

    return merged


def _process_financial_index_data(all_data: List[dict]) -> List[dict]:
    """处理财务指标数据，实现近三年一期的数据获取和去重逻辑"""
    if not all_data:
        return []

    processed_data = []
    for item in all_data:
        try:
            report_year = item.get('REPORTYEAR') or item.get('reportyear')
            reportdate_type = item.get('REPORTDATETYPE') or item.get('reportdatetype')
            end_date = item.get('ENDDATE') or item.get('enddate')
            report_type = item.get('REPORTTYPE') or item.get('reporttype')

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


def _format_financial_index_data(data_list: List[dict]) -> List[dict]:
    """格式化财务指标数据"""
    if not data_list:
        return []

    formatted_results = []
    for item in data_list:
        formatted_item = item.copy()

        report_type = formatted_item.get('REPORTTYPE') or formatted_item.get('reporttype')
        if report_type is not None:
            try:
                formatted_item['REPORTTYPE'] = REPORT_TYPE_MAPPING.get(int(report_type), str(report_type))
            except (ValueError, TypeError):
                pass

        reportdate_type = formatted_item.get('REPORTDATETYPE') or formatted_item.get('reportdatetype')
        if reportdate_type is not None:
            try:
                formatted_item['REPORTDATETYPE'] = REPORT_DATE_TYPE_MAPPING.get(int(reportdate_type), str(reportdate_type))
            except (ValueError, TypeError):
                pass

        formatted_results.append(formatted_item)

    return formatted_results


def _process_financial_index_in_listed_info(merged_info: dict) -> dict:
    """处理合并后的上市信息中的财务指标数据"""
    if not merged_info or not isinstance(merged_info, dict):
        return merged_info

    financial_index_data = merged_info.get('FINANCIALINDEX')
    if not financial_index_data or not isinstance(financial_index_data, list):
        return merged_info

    processed_financial_index = _process_financial_index_data(financial_index_data)
    formatted_financial_index = _format_financial_index_data(processed_financial_index)

    merged_info_copy = merged_info.copy()
    if formatted_financial_index:
        merged_info_copy['FINANCIALINDEX'] = formatted_financial_index
    else:
        merged_info_copy.pop('FINANCIALINDEX', None)

    return merged_info_copy


def _convert_to_chinese(data: dict) -> dict:
    """将API返回的英文字段名转换为中文"""
    if not isinstance(data, dict):
        return data

    chinese_data = {}

    for english_module, chinese_module in MODULE_NAME_MAPPING.items():
        chinese_data[chinese_module] = ""

    for key, value in data.items():
        if key not in MODULE_NAME_MAPPING:
            continue

        chinese_key = MODULE_NAME_MAPPING[key]

        if isinstance(value, dict):
            chinese_value = {}
            for field_key, field_value in value.items():
                if field_key in FIELD_NAME_MAPPING:
                    chinese_field_key = FIELD_NAME_MAPPING[field_key]
                    chinese_value[chinese_field_key] = field_value
            if chinese_value:
                chinese_data[chinese_key] = chinese_value
        elif isinstance(value, list):
            chinese_list = []
            for item in value:
                if isinstance(item, dict):
                    chinese_item = {}
                    for field_key, field_value in item.items():
                        if field_key in FIELD_NAME_MAPPING:
                            chinese_field_key = FIELD_NAME_MAPPING[field_key]
                            chinese_item[chinese_field_key] = field_value
                    if chinese_item:
                        chinese_list.append(chinese_item)
                else:
                    chinese_list.append(item)
            if chinese_list:
                chinese_data[chinese_key] = chinese_list
        else:
            chinese_data[chinese_key] = value if value else ""

    return chinese_data


def _call_listed_api(entname: str) -> dict:
    """企业上市信息综合查询"""
    mainland_result = _call_mainland_listed_api(entname)
    hk_result = _call_hk_listed_api(entname)

    has_mainland = mainland_result.get('code') == 200 and mainland_result.get('data')
    has_hk = hk_result.get('code') == 200 and hk_result.get('data')

    if has_mainland and has_hk:
        merged_data = _merge_listed_info(mainland_result['data'], hk_result['data'])
        merged_info = _process_financial_index_in_listed_info(merged_data)
    elif has_mainland:
        merged_info = _process_financial_index_in_listed_info(mainland_result['data'])
    elif has_hk:
        merged_info = _process_financial_index_in_listed_info(hk_result['data'])
    else:
        return "未查询到任何上市信息"

    result = {
        'mainland_info': mainland_result,
        'hk_info': hk_result,
        'merged_info': merged_info
    }

    # 转换为中文
    if not result.get('merged_info'):
        return "未查询到上市信息"

    chinese_merged_info = _convert_to_chinese(result['merged_info'])

    # 处理十大流通股东数据格式
    try:
        chinese_merged_info['十大流通股东'] = chinese_merged_info['十大流通股东'][1]
    except:
        pass

    # 优先级处理：如果有内地上市信息，删除港股的基本信息和联系信息
    if has_mainland:
        for key in ['港股企业基本信息', '港股企业联系信息']:
            chinese_merged_info.pop(key, None)

    return chinese_merged_info


# ============ 后处理函数 ============

def _extract_basic_info(data: Dict[str, Any]) -> str:
    """提取企业基本信息"""
    info = data.get('企业基本信息', {})
    if not info:
        return ""

    lines = ["### 企业基本信息"]
    field_mapping = {
        '公司简称': '公司简称', '英文名称': '英文名称', '员工人数': '员工人数',
        '主营业务': '主营业务', '公司简介': '公司简介', '注册地址': '注册地址',
        '办公地址': '办公地址', '董事长': '董事长', '董秘': '董秘',
        '总经理': '总经理', '证券代表': '证券代表', '律师事务所': '律师事务所',
        '会计师事务所': '会计师事务所', '证监会一级行业': '证监会一级行业',
        '证监会二级行业': '证监会二级行业'
    }

    for key, label in field_mapping.items():
        value = info.get(key, '')
        if value:
            lines.append(f"{label}：{value}")

    return '\n'.join(lines)


def _extract_contact_info(data: Dict[str, Any]) -> str:
    """提取企业联系信息"""
    info = data.get('企业联系信息', {})
    if not info:
        return ""

    lines = ["### 企业联系信息"]
    field_mapping = {
        '公司网址': '公司网址', '公司电子邮箱': '公司电子邮箱',
        '公司电话': '公司电话', '公司传真': '公司传真', '客服电话': '客服电话'
    }

    for key, label in field_mapping.items():
        value = info.get(key, '')
        if value:
            lines.append(f"{label}：{value}")

    return '\n'.join(lines)


def _extract_application_info(data: Dict[str, Any]) -> str:
    """提取申报与上市信息"""
    applications = data.get('申报情况', [])
    lines = ["### 申报与上市信息"]

    if not applications:
        lines.append("暂无数据")
        return '\n'.join(lines)

    app = applications[0] if applications else {}

    for key in ['公司全称', '公司简称', '融资金额', '审核状态']:
        if app.get(key):
            lines.append(f"{key}：{app.get(key)}")

    dates = []
    date_fields = {
        '已受理日期': '受理', '已问询日期': '问询', '上市委会议日期': '上市委会议',
        '提交注册日期': '提交注册', '注册结果日期': '注册结果',
        '中止日期': '中止', '终止日期': '终止', '更新日期': '更新日期'
    }

    for key, label in date_fields.items():
        date = app.get(key, '')
        if date:
            dates.append(f"{label}:{date}")

    if dates:
        lines.append(f"关键日期：{','.join(dates)}")

    for key in ['保荐机构', '保荐代表人', '会计师事务所', '签字会计师',
                '律师事务所', '签字律师', '评估机构', '签字评估师', '申报上市板块']:
        if app.get(key):
            lines.append(f"{key}：{app.get(key)}")

    return '\n'.join(lines)


def _extract_stock_basic_info(data: Dict[str, Any]) -> str:
    """提取股票基本信息"""
    stocks = data.get('股票基本信息', [])
    lines = ["### 股票基本信息"]

    if not stocks:
        lines.append("暂无数据")
        return '\n'.join(lines)

    for stock in stocks:
        parts = []
        for key, label in [('股票代码', '股票代码'), ('证券简称', '证券简称'),
                          ('证券类型', '证券类型'), ('上市日期', '上市日期'),
                          ('上市状态', '上市状态'), ('上市交易市场', '交易市场'),
                          ('申报上市板块', '上市板块')]:
            if stock.get(key):
                parts.append(f"{label}:{stock[key]}")
        if parts:
            lines.append(','.join(parts))

    return '\n'.join(lines)


def _extract_issue_info(data: Dict[str, Any]) -> str:
    """提取发行信息"""
    issues = data.get('发行信息', [])
    lines = ["### 发行信息"]

    if not issues:
        lines.append("暂无数据")
        return '\n'.join(lines)

    issue = issues[0] if issues else {}
    field_mapping = {
        '发行规模（万股）': ('发行规模', '万股'),
        '发行价格（元/股）': ('发行价格', '元'),
        '募资净额（万元）': ('募资净额', '万元'),
        '发行费用（万元）': ('发行费用', '万元'),
        '定价中签率（%）': ('中签率', '%'),
        '主承销商': ('主承销商', ''),
        '上市保荐机构': ('上市保荐机构', ''),
        '首日开盘价（元）': ('首日开盘价', '元'),
        '首日收盘价（元）': ('首日收盘价', '元'),
        '首日换手率（%）': ('首日换手率', '%')
    }

    for key, (label, unit) in field_mapping.items():
        value = issue.get(key, '')
        if value:
            lines.append(f"{label}：{value}{unit}")

    return '\n'.join(lines)


def _extract_market_indicators(data: Dict[str, Any]) -> str:
    """提取重要指标"""
    indicators = data.get('重要指标', [])
    lines = ["### 市场交易与指标"]

    if not indicators:
        lines.append("暂无数据")
        return '\n'.join(lines)

    indicator = indicators[0] if indicators else {}
    field_mapping = {
        '交易日期': ('交易日期', ''),
        '总市值（万元）': ('总市值', '万元'),
        '流通市值（万元）': ('流通市值', '万元'),
        '成交额（元）': ('成交额', '元'),
        '成交量（股）': ('成交量', '股'),
        '最高价': ('最高价', '元'),
        '最低价': ('最低价', '元'),
        '涨跌幅': ('涨跌幅', '%'),
        '静态市盈率': ('市盈率(静态)', ''),
        '滚动市盈率市盈率': ('市盈率(滚动)', ''),
        '动态市盈率': ('市盈率(动态)', ''),
        '市净率': ('市净率', '')
    }

    for key, (label, unit) in field_mapping.items():
        value = indicator.get(key, '')
        if value:
            lines.append(f"{label}：{value}{unit}")

    return '\n'.join(lines)


def _extract_top_shareholders(data: Dict[str, Any]) -> str:
    """提取十大流通股东"""
    shareholder = data.get('十大流通股东', {})
    lines = ["### 十大流通股东"]

    if not shareholder:
        lines.append("暂无数据")
        return '\n'.join(lines)

    parts = []
    for key, (label, unit) in [
        ('股东名称', ('股东名称', '')),
        ('持股数(股)', ('持股数', '股')),
        ('持股数量占总股本比例(%)', ('持股比例', '%')),
        ('股东机构类型', ('股东类型', '')),
        ('股东股权性质', ('股权性质', '')),
        ('股东排名', ('排名', ''))
    ]:
        if shareholder.get(key):
            parts.append(f"{label}:{shareholder[key]}{unit}")

    if parts:
        lines.append(','.join(parts))

    return '\n'.join(lines)


def _extract_dividend_info(data: Dict[str, Any]) -> str:
    """提取分红情况"""
    dividends = data.get('分红情况', [])
    lines = ["### 分红情况"]

    if not dividends:
        lines.append("暂无数据")
        return '\n'.join(lines)

    for dividend in dividends[:3]:
        parts = []
        for key, (label, unit) in [
            ('年度', ('分红年度', '')),
            ('发布日期', ('公告日期', '')),
            ('股权登记日', ('股权登记日', '')),
            ('分红金额合计（人民币万元）', ('分红金额', '万元')),
            ('是否最新方案', ('是否最新方案', ''))
        ]:
            if dividend.get(key):
                parts.append(f"{label}:{dividend[key]}{unit}")
        if parts:
            lines.append(','.join(parts))

    return '\n'.join(lines)


def _extract_financial_indicators(data: Dict[str, Any]) -> str:
    """提取财务指标"""
    financials = data.get('财务指标', [])
    lines = ["### 财务指标"]

    if not financials:
        lines.append("暂无数据")
        return '\n'.join(lines)

    for financial in financials[:4]:
        parts = []
        for key, (label, unit) in [
            ('截止日期', ('报告期', '')),
            ('净资产收益率ROE(摊薄)', ('ROE', '')),
            ('摊薄每股收益(元)', ('每股收益', '元')),
            ('每股净资产(元)', ('每股净资产', '元')),
            ('销售毛利率(%)', ('毛利率', '%')),
            ('销售净利率(含少数股权权益%)', ('净利率', '%')),
            ('资产负债率(%)', ('资产负债率', '%')),
            ('营业总收入同比增长(%)', ('营收增长率', '%')),
            ('归母净利润同比增长率(%)', ('净利润增长率', '%'))
        ]:
            if financial.get(key):
                parts.append(f"{label}:{financial[key]}{unit}")
        if parts:
            lines.append(','.join(parts))

    return '\n'.join(lines)


def _extract_hk_stock_info(data: Dict[str, Any]) -> str:
    """提取港股股票基本信息"""
    hk_stocks = data.get('港股股票基本信息', [])
    lines = ["### 港股企业信息"]

    if not hk_stocks:
        lines.append("暂无数据")
        return '\n'.join(lines)

    has_listed = False
    for stock in hk_stocks:
        if stock.get('上市状态') == '上市':
            parts = []
            if stock.get('证券简称'):
                parts.append(f"公司简称:{stock['证券简称']}")
            if stock.get('英文简称'):
                parts.append(f"英文名称:{stock['英文简称']}")

            basic_info = data.get('企业基本信息', {})
            if isinstance(basic_info, dict):
                for key in ['主营业务', '董事长', '董秘', '总经理']:
                    if basic_info.get(key):
                        parts.append(f"{key}:{basic_info[key]}")

            for key in ['股票代码', '上市日期']:
                if stock.get(key):
                    parts.append(f"{key}:{stock[key]}")

            if stock.get('恒生一级行业名称') and stock.get('恒生二级行业名称'):
                parts.append(f"行业分类:{stock['恒生一级行业名称']}/{stock['恒生二级行业名称']}")
            if stock.get('主体类型'):
                parts.append(f"主体类型:{stock['主体类型']}")

            if parts:
                lines.append(','.join(parts))
                has_listed = True
                break

    if not has_listed:
        lines.append("暂无数据")

    return '\n'.join(lines)


def _process_listed_info(listed_info: dict) -> str:
    """后处理：从数据生成上市信息提炼结果"""
    if isinstance(listed_info, str):
        return listed_info

    # 检查审核状态
    applications = listed_info.get('申报情况', [])
    is_terminated = False

    if applications:
        status = applications[0].get('审核状态', '')
        if '终止' in status:
            is_terminated = True

    sections = ["# 上市信息提炼", ""]

    if is_terminated:
        sections.append(_extract_application_info(listed_info))
    else:
        all_sections = [
            _extract_basic_info(listed_info),
            _extract_contact_info(listed_info),
            _extract_application_info(listed_info),
            _extract_stock_basic_info(listed_info),
            _extract_issue_info(listed_info),
            _extract_market_indicators(listed_info),
            _extract_top_shareholders(listed_info),
            _extract_dividend_info(listed_info),
            _extract_financial_indicators(listed_info),
            _extract_hk_stock_info(listed_info)
        ]

        for section in all_sections:
            if section:
                sections.append(section)
                sections.append("")

    return '\n'.join(sections).rstrip()


# ============ 主接口 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业上市信息

    Args:
        entname: 企业名称

    Returns:
        Markdown格式的上市信息
    """
    raw_data = _call_listed_api(entname)

    if isinstance(raw_data, str):
        return raw_data

    return _process_listed_info(raw_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python s02_listed_info.py <企业名称>")
