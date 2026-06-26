#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险大数据一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from .base import call_api, debug_print


# ============ 模块名映射 ============
MODULE_NAME_MAP = {
    'judicial_case': '司法案件',
    'case_filing': '立案信息',
    'delivery': '送达公告',
    'courting': '开庭公告',
    'court_ann': '法院公告',
    'document': '裁判文书',
    'punished': '被执行人',
    'dis_punished': '失信被执行人',
    'final_case': '终本案件',
    'restrict_consume': '限制高消费',
    'auction': '司法拍卖',
    'assistance': '司法协助',
    'bankruptcy': '破产程序',
    'liquidation_group': '清算信息',
    'liquidation_team': '清算组备案',
    'creditor_notice': '债权人公告',
    'simple_logout': '简易注销',
    'product_recall': '产品召回',
    'random_check': '双随机抽查',
    'abnormal': '经营异常名录',
    'subtract_capital': '减资公告',
    'stock_pledge_listed': '股权质押',
    'stock_pledge': '股权出质',
    'bill_overdue': '票据逾期',
    'administrative_penalty': '行政处罚',
    'blacklist': '失信黑名单',
    'misconduct': '不良行为',
    'fund_manager_honesty': '私募基金管理人诚信信息',
    'severity_illegality': '严重违法失信',
    'taxes_illegality': '重大税收违法案件',
    'owing_taxes': '欠税公告',
    'abnormal_company': '非正常户公告',
    'inspection': '抽查检查不合格',
    'product_inspection': '产品抽查不合格',
    'admin_enforce_eminder': '行政强制执行催告信息',
    'violation': '违规处分'
}

# ============ 字段名映射 ============
FIELD_NAME_MAP = {
    # 通用字段
    'case_title': '案件标题',
    'case_reason': '案由',
    'doc_type': '文书类型',
    'case_type': '案件类型',
    'latest_progress': '最新进程',
    'latest_progress_date': '最新进程日期',
    'progress_name': '审判程序',
    'type_name': '当事人类型',
    'name': '当事人名称',
    'litigant': '当事人信息',
    'court_name': '法院名称',
    'regdate': '立案日期',
    'case_progress': '案件状态',
    'publish_date': '公告日期',
    'open_date': '开庭日期',
    'court_room': '法庭',
    'judge': '主审法官',
    'undertaker': '承办人',
    'publish_org': '法院名称',
    'notice_type': '公告类型',
    'case_doc_name': '案件及文书类型',
    'court_level': '法院层级',
    'judgment_date': '裁判日期',
    'judicial_procedure': '审判程序',
    'involved_amount': '涉案金额',
    'judgment_amount': '判决金额',
    'trial_result': '审判结果描述',
    'execute_amount': '执行标的',
    'casecode': '案号',
    'province': '省份',
    'duty': '生效法律文书确定的义务',
    'performedpart': '已履行',
    'unperformpart': '未履行',
    'performance': '被执行人的履行情况',
    'disrupttypename': '失信被执行人行为具体情形',
    'gistunit': '做出执行依据单位',
    'finaldate': '终本日期',
    'unperfmoney': '未履行金额',
    'entname': '企业名称',
    'applicant': '申请人',
    'iname': '关联限消对象',

    # 司法拍卖
    'auction_notice': '拍卖公告标题',
    'mark_type': '标的类型',
    'auction_status': '拍卖状态名称',
    'disposal_unit': '处置单位',
    'sale_price': '起拍价格',
    'starting_price': '起拍价',
    'evaluating_price': '评估价',

    # 司法协助
    'shaream': '被执行人持有股权数额',
    'cur': '币种',
    'assistance_type': '司法协助类型',
    'status': '股权冻结状态',

    # 破产程序
    'leader_of_manager': '管理人主要负责人',
    'manager_org': '管理人机构',

    # 清算信息
    'ligprincipal': '清算负责人',
    'liqmen': '清算组成员',
    'liq_fldate': '清算组备案日期',
    'canreason': '注销原因',

    # 债权人公告
    'stage_date': '公告期',
    'notice_content': '公告内容',

    # 简易注销
    'regorg': '工商登记机关',
    'notice_from_date': '公告开始日期',
    'cancel_result': '简易注销结果',
    'dissent_org': '异议申请人',
    'dissent_des': '异议内容',

    # 产品召回
    'title': '事件标题',
    'prod_name': '召回产品',
    'flaw_type': '缺陷类型',

    # 双随机抽查
    'inspect_plan_name': '抽查计划名称',
    'inspect_task_name': '抽查任务名称',
    'inspect_type': '抽查类型',
    'inspect_org': '抽查机关',
    'inspect_date': '抽查完成日期',
    'inspect_item': '抽查事项',
    'inspect_res': '抽查结果',

    # 经营异常名录
    'indate': '列入日期',
    'outdate': '移出日期',
    'inreason': '列入原因',
    'outreason': '移出原因',

    # 减资公告
    'execute_date': '做出决定日期',
    'execute_content': '公告內容',

    # 股权质押
    'shholder_name': '出质方',
    'pledgeename': '质押方',
    'frozenskamt': '质押股数',
    'frozenrtoh': '占持股比',
    'frozenrtot': '占总股本比',
    'tclose': '质押日收盘价',
    'excompprices': '质押日收盘价前复权价',
    'alertline': '预警线',
    'stopline': '平仓线',
    'pletermdesc': '质押期限描述',
    'unfreezedate': '解押日期',
    'plecause': '质押事由',
    'plenotes': '质押附注',
    'publishdate': '公告日期',

    # 股权出质
    'stk_pawn_czamt': '出质股权数额',
    'stk_pawn_unit': '出质股权单位',
    'stk_pawn_czper': '出质人',
    'stk_pawn_status': '状态',
    'stk_pawn_zqper': '质权人姓名',
    'stk_pawn_date': '公示日期',
    'stk_pawn_res': '注销原因',

    # 票据逾期
    'list_type': '披露名单类型名称',
    'total_execute_amount': '累计承兑发生额',
    'overdue_balance': '逾期余额',
    'total_overdue_amount': '累计逾期发生额',

    # 行政处罚
    'case_name': '案件名称',
    'punish_type': '处罚类别',
    'illegal_type': '违法行为类型',
    'illegal_fact': '违法事实',
    'punish_depend': '处罚依据',
    'punish_content': '处罚内容',
    'punish_date': '处罚日期',
    'end_date': '处罚截止期',
    'punish_amonut': '处罚金额',
    'revover_amount': '没收违法所得金额',
    'forfeiture_amount': '罚没金额',
    'punish_org': '处罚机关',
    'punish_typename': '处罚方式名称',

    # 失信黑名单
    'blacklist_type': '黑名单类型名称',
    'punish_reason': '列入依据',
    'inregorg': '列入机关',
    'org_type': '处理机构类型',
    'punish_result': '处罚结果',

    # 不良行为
    'execute_issues': '处罚事由',
    'organization': '实施机构',

    # 私募基金管理人诚信信息
    'credit_info': '诚信信息',
    'credit_detail': '诚信详情',

    # 重大税收违法案件
    'brk_detail': '主要违法事实',
    'punish_detail': '处罚情况',
    'eval_date': '发布日期',
    'tax_org': '公布机关',

    # 欠税公告
    'tax_category': '欠税税种',
    'balance': '欠税余额',
    'balance_new': '新欠税金额',
    'notice_date': '公告时间',

    # 非正常户公告
    'area_name': '发布地区',

    # 抽查检查不合格
    'isp_type': '数据类型',
    'check_date': '抽查日期',
    'results': '抽查结果',

    # 产品抽查不合格
    'prod_name_details': '产品详细名称',
    'prod_level': '产品等级',
    'check_type': '抽查类型',
    'major_failure': '主要不合格项目',

    # 行政强制执行催告信息
    'detail_type': '分类名称',
    'content': '正文内容',
    'source_name': '官网名称',

    # 违规处分
    'titles': '标题',
    'vioreason': '违规原因',
    'vioparty': '违规当事人',
    'viotype': '违规类型',
    'relatedrules': '相关法规',
    'wholetext': '全文内容',
    'isimportant': '是否重大影响',
    'annttype': '公告类型'
}

# 各模块的主要字段配置
MODULE_FIELD_CONFIG = {
    'judicial_case': [
        'case_title', 'case_reason', 'case_type', 'latest_progress',
        'latest_progress_date', 'litigant'
    ],
    'case_filing': [
        'case_title', 'case_type', 'case_reason', 'court_name',
        'regdate', 'case_progress', 'litigant'
    ],
    'delivery': [
        'case_reason', 'court_name', 'publish_date', 'litigant'
    ],
    'courting': [
        'case_title', 'case_type', 'case_reason', 'open_date',
        'court_room', 'judge', 'undertaker', 'publish_org', 'litigant'
    ],
    'court_ann': [
        'case_reason', 'notice_type', 'publish_date', 'litigant'
    ],
    'document': [
        'case_title', 'case_reason', 'case_type', 'court_name',
        'judgment_date', 'involved_amount', 'judgment_amount',
        'trial_result', 'litigant'
    ],
    'punished': [
        'court_name', 'execute_amount', 'regdate'
    ],
    'dis_punished': [
        'casecode', 'court_name', 'province', 'involved_amount',
        'duty', 'performedpart', 'unperformpart', 'performance',
        'disrupttypename', 'publish_date'
    ],
    'final_case': [
        'casecode', 'court_name', 'finaldate', 'execute_amount', 'unperfmoney'
    ],
    'restrict_consume': [
        'casecode', 'entname', 'applicant', 'court_name', 'publish_date', 'iname'
    ],
    'auction': [
        'auction_notice', 'mark_type', 'auction_status', 'court_name',
        'disposal_unit', 'starting_price', 'evaluating_price', 'publish_date', 'litigant'
    ],
    'assistance': [
        'iname', 'shaream', 'cur', 'assistance_type', 'status',
        'court_name', 'publish_date', 'entname'
    ],
    'bankruptcy': [
        'casecode', 'case_type', 'court_name', 'leader_of_manager',
        'manager_org', 'publish_date', 'litigant'
    ],
    'liquidation_group': [
        'ligprincipal', 'liqmen'
    ],
    'liquidation_team': [
        'liq_fldate', 'canreason'
    ],
    'creditor_notice': [
        'stage_date', 'notice_content'
    ],
    'simple_logout': [
        'regorg', 'notice_from_date', 'cancel_result', 'dissent_org', 'dissent_des'
    ],
    'product_recall': [
        'title', 'prod_name', 'flaw_type', 'publish_date'
    ],
    'random_check': [
        'inspect_plan_name', 'inspect_task_name', 'inspect_type',
        'inspect_org', 'inspect_date', 'inspect_item'
    ],
    'abnormal': [
        'indate', 'outdate', 'inreason', 'outreason'
    ],
    'subtract_capital': [
        'execute_date', 'stage_date', 'execute_content'
    ],
    'stock_pledge_listed': [
        'entname', 'shholder_name', 'pledgeename', 'frozenskamt',
        'frozenrtoh', 'frozenrtot', 'pletermdesc', 'unfreezedate',
        'plecause', 'publishdate'
    ],
    'stock_pledge': [
        'stk_pawn_czamt', 'stk_pawn_unit', 'stk_pawn_czper', 'entname',
        'stk_pawn_status', 'stk_pawn_zqper', 'stk_pawn_date'
    ],
    'bill_overdue': [
        'entname', 'publish_date', 'list_type', 'execute_amount',
        'total_execute_amount', 'overdue_balance', 'total_overdue_amount'
    ],
    'administrative_penalty': [
        'case_name', 'punish_type', 'illegal_type', 'illegal_fact',
        'punish_depend', 'punish_content', 'punish_date', 'end_date',
        'punish_amonut', 'punish_org', 'punish_types'
    ],
    'blacklist': [
        'title', 'blacklist_type', 'inreason', 'punish_reason',
        'inregorg', 'org_type', 'execute_amount', 'punish_result',
        'outreason', 'publish_date'
    ],
    'misconduct': [
        'blacklist_type', 'title', 'execute_content', 'execute_issues',
        'organization', 'indate', 'outdate', 'outreason'
    ],
    'fund_manager_honesty': [
        'credit_info', 'credit_detail'
    ],
    'severity_illegality': [
        'indate', 'outdate', 'inreason', 'outreason'
    ],
    'taxes_illegality': [
        'case_type', 'brk_detail', 'punish_detail', 'eval_date', 'tax_org'
    ],
    'owing_taxes': [
        'tax_category', 'balance', 'balance_new', 'notice_date'
    ],
    'abnormal_company': [
        'eval_date', 'publish_org', 'area_name'
    ],
    'inspection': [
        'isp_type', 'check_date', 'results'
    ],
    'product_inspection': [
        'prod_name', 'prod_name_details', 'prod_level', 'check_type',
        'check_date', 'results', 'major_failure'
    ],
    'admin_enforce_eminder': [
        'case_name', 'publish_date', 'detail_type', 'content', 'source_name'
    ],
    'violation': [
        'titles', 'publish_date', 'vioreason', 'vioparty', 'viotype',
        'relatedrules', 'isimportant', 'annttype'
    ]
}

# 风险模块统计配置
RISK_MODULE_CONFIG = [
    ('judicial_case', '件'),
    ('case_filing', '件'),
    ('delivery', '件'),
    ('courting', '件'),
    ('court_ann', '件'),
    ('document', '件', 'total_execute_amount', '涉案金额'),
    ('punished', '件'),
    ('dis_punished', '件'),
    ('final_case', '件'),
    ('restrict_consume', '件'),
    ('auction', '件'),
    ('assistance', '件', 'total_stock_amount', '股权数额'),
    ('bankruptcy', '件'),
    ('administrative_penalty', '件', 'total_execute_amount', '处罚金额'),
    ('abnormal', '件'),
    ('blacklist', '件', 'total_execute_amount', '涉及金额'),
    ('owing_taxes', '件', 'total_execute_amount', '欠税余额'),
    ('stock_pledge_listed', '件', 'total_stock_amount', '质押股数'),
    ('bill_overdue', '件'),
    ('taxes_illegality', '件'),
    ('severity_illegality', '件'),
    ('fund_manager_honesty', '件'),
    ('misconduct', '件'),
    ('product_recall', '件'),
    ('random_check', '件'),
    ('subtract_capital', '件'),
    ('stock_pledge', '件'),
    ('liquidation_group', '件'),
    ('liquidation_team', '件'),
    ('creditor_notice', '件'),
    ('simple_logout', '件'),
    ('abnormal_company', '件'),
    ('inspection', '件'),
    ('product_inspection', '件'),
    ('admin_enforce_eminder', '件'),
    ('violation', '件')
]


# ============ 辅助函数 ============

def _get_chinese_module_name(module_name: str) -> str:
    """获取模块的中文名称"""
    return MODULE_NAME_MAP.get(module_name, module_name)


def _get_chinese_field_name(field_name: str) -> str:
    """获取字段的中文名称"""
    return FIELD_NAME_MAP.get(field_name, field_name)


def _format_party_array(party_array: List[Dict], case_title: str = '') -> str:
    """格式化当事人数组信息"""
    if not party_array:
        return ""

    party_info = []
    for party in party_array:
        if 'name' in party and 'type_name' in party:
            party_info.append(f"{party.get('name', '')}-{party.get('type_name', '')}")
        elif 'name' in party:
            party_info.append(party.get('name', ''))
        elif 'type_name' in party:
            # 从案件标题提取企业名称
            enterprise_name = _extract_enterprise_from_title(case_title)
            progress_name = party.get('progress_name', '')
            type_name = party.get('type_name', '')
            if enterprise_name and type_name:
                party_info.append(f"{enterprise_name}-{type_name}({progress_name})")
            elif progress_name and type_name:
                party_info.append(f"{progress_name}-{type_name}")

    return "; ".join(party_info)


def _extract_enterprise_from_title(case_title: str) -> str:
    """从案件标题中提取企业名称"""
    if not case_title:
        return ""

    enterprise_name = ""

    if '与' in case_title:
        enterprise_name = case_title.split('与')[0].strip()
    elif '、' in case_title:
        enterprise_name = case_title.split('、')[0].strip()
    elif '被申请执行案件' in case_title:
        enterprise_name = case_title.replace('被申请执行案件', '').strip()
    elif '申请执行' in case_title:
        enterprise_name = case_title.split('申请执行')[0].strip()
    else:
        keywords = ['侵害', '纠纷', '争议', '案件', '申请', '被执行']
        for keyword in keywords:
            if keyword in case_title:
                parts = case_title.split(keyword)
                if len(parts) > 1 and parts[0].strip():
                    enterprise_name = parts[0].strip()
                    break

        if not enterprise_name and len(case_title) > 10:
            company_indicators = ['有限公司', '股份有限公司', '有限责任公司', '集团', '企业']
            for indicator in company_indicators:
                if indicator in case_title:
                    idx = case_title.find(indicator)
                    enterprise_name = case_title[:idx + len(indicator)].strip()
                    break

    return enterprise_name


def _format_punishment_types(punishment_types: List[Dict]) -> str:
    """格式化处罚方式名称"""
    if not punishment_types:
        return ""
    return "; ".join([pt.get('punish_typename', '') for pt in punishment_types if pt.get('punish_typename')])


def _format_inspection_details(inspection_details: List[Dict]) -> str:
    """格式化抽查结果详情"""
    if not inspection_details:
        return ""

    details = []
    for detail in inspection_details:
        item = detail.get('inspect_item', '')
        result = detail.get('inspect_res', '')
        if item and result:
            details.append(f"{item}: {result}")

    return "; ".join(details)


def _format_field_value(field_name: str, value: Any) -> str:
    """格式化字段值，添加单位等"""
    if value is None or value == '':
        return '未知'

    # 金额字段处理
    if 'amount' in field_name and field_name not in ['total_execute_amount', 'total_overdue_amount']:
        if field_name in ['punish_amonut', 'revover_amount', 'forfeiture_amount']:
            return f"{value}万元"
        elif field_name in ['involved_amount', 'judgment_amount', 'execute_amount', 'overdue_balance']:
            return f"{value}元"
        elif field_name in ['balance', 'balance_new']:
            return f"{value}元"

    # 股权相关字段
    elif field_name == 'frozenskamt':
        return f"{value}万股"
    elif field_name in ['frozenrtoh', 'frozenrtot']:
        return f"{value}%"
    elif field_name in ['alertline', 'stopline', 'tclose', 'excompprices']:
        return f"{value}元"

    return str(value)


# ============ API 调用 ============

def _call_risk_api(entname: str) -> Dict[str, Any]:
    """调用风险大数据 API"""
    response = call_api('/entRiskBigData', {'entname': entname, 'size': 100}, method='GET')

    api_code = response.get('code') or response.get('CODE')

    if api_code != 200:
        debug_print(f"风险大数据 API 返回错误: {api_code}")
        return {}

    return response.get('data') or response.get('DATA', {})


# ============ 数据处理 ============

def _process_risk_statistics(page_info: Dict[str, Any]) -> Dict[str, Dict]:
    """处理风险统计信息"""
    if not page_info:
        return {}

    risk_stats = {}

    for module_config in RISK_MODULE_CONFIG:
        module_name = module_config[0]
        unit = module_config[1]

        module_info = page_info.get(module_name, {})
        total_count = module_info.get('totalcount', 0)

        if total_count and int(str(total_count)) > 0:
            chinese_name = _get_chinese_module_name(module_name)

            # 检查是否有金额统计
            if len(module_config) >= 4:
                amount_field = module_config[2]
                amount_desc = module_config[3]
                amount = module_info.get(amount_field, 0)

                if amount and float(str(amount)) > 0:
                    if amount_field == 'total_stock_amount':
                        risk_stats[chinese_name] = {
                            "数量": f"{total_count}{unit}",
                            amount_desc: f"{amount}万股"
                        }
                    else:
                        risk_stats[chinese_name] = {
                            "数量": f"{total_count}{unit}",
                            amount_desc: f"{amount}万元"
                        }
                else:
                    risk_stats[chinese_name] = {"数量": f"{total_count}{unit}"}
            else:
                risk_stats[chinese_name] = {"数量": f"{total_count}{unit}"}

    return risk_stats


def _format_module_data(module_name: str, module_data: List[Dict]) -> List[Dict]:
    """格式化各模块详细数据"""
    if not module_data:
        return []

    result = []
    fields = MODULE_FIELD_CONFIG.get(module_name, [])

    for item in module_data:
        formatted_item = {}

        for field in fields:
            if field == 'litigant':
                party_info = _format_party_array(
                    item.get('litigant', []),
                    item.get('case_title', '')
                )
                if party_info:
                    formatted_item[_get_chinese_field_name(field)] = party_info
            elif field == 'punish_types':
                punish_types = _format_punishment_types(item.get('punish_types', []))
                if punish_types:
                    formatted_item['处罚方式名称'] = punish_types
            elif field == 'inspect_item':
                inspection_details = _format_inspection_details(item.get('inspect_item', []))
                if inspection_details:
                    formatted_item['抽查结果详情'] = inspection_details
            else:
                value = item.get(field)
                if value is not None and value != '':
                    chinese_field = _get_chinese_field_name(field)
                    formatted_value = _format_field_value(field, value)
                    formatted_item[chinese_field] = formatted_value

        # 如果没有配置字段，显示所有可用字段
        if not fields:
            for key, value in item.items():
                if key not in ['litigant', 'punish_types', 'inspect_item'] and value is not None and value != '':
                    chinese_field = _get_chinese_field_name(key)
                    formatted_value = _format_field_value(key, value)
                    formatted_item[chinese_field] = formatted_value

        if formatted_item:
            result.append(formatted_item)

    return result


def _process_risk_details(data: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """处理详细风险信息"""
    if not data:
        return {}

    # 优先显示的重要模块
    priority_modules = [
        'judicial_case', 'case_filing', 'document', 'punished', 'dis_punished',
        'administrative_penalty', 'abnormal', 'blacklist', 'owing_taxes'
    ]

    # 其他模块
    other_modules = [
        'delivery', 'courting', 'court_ann', 'final_case', 'restrict_consume',
        'auction', 'assistance', 'bankruptcy', 'liquidation_group', 'liquidation_team',
        'creditor_notice', 'simple_logout', 'product_recall', 'random_check',
        'subtract_capital', 'stock_pledge_listed', 'stock_pledge', 'bill_overdue',
        'misconduct', 'fund_manager_honesty', 'severity_illegality', 'taxes_illegality',
        'abnormal_company', 'inspection', 'product_inspection', 'admin_enforce_eminder',
        'violation'
    ]

    result = {}

    # 先处理优先模块
    for module_name in priority_modules:
        module_data = data.get(module_name, [])
        if module_data and len(module_data) > 0:
            module_desc = _get_chinese_module_name(module_name)
            formatted_data = _format_module_data(module_name, module_data)
            if formatted_data:
                result[module_desc] = formatted_data

    # 再处理其他模块
    for module_name in other_modules:
        module_data = data.get(module_name, [])
        if module_data and len(module_data) > 0:
            module_desc = _get_chinese_module_name(module_name)
            formatted_data = _format_module_data(module_name, module_data)
            if formatted_data:
                result[module_desc] = formatted_data

    return result


# ============ Markdown 格式化 ============

def _format_risk_summary_markdown(risk_stats: Dict[str, Dict]) -> str:
    """将风险统计转换为 Markdown"""
    if not risk_stats:
        return ""

    lines = ["### 风险统计摘要"]

    for risk_type, info in risk_stats.items():
        if isinstance(info, dict):
            count = info.get('数量', info.get('总数', ''))

            if count:
                lines.append(f"{risk_type}总数: {count}")

            # 处理各种金额字段
            for key, value in info.items():
                if key not in ['数量', '总数'] and value:
                    if key in ['质押股数']:
                        lines.append(f"{key}: {value}")
                    elif key == '涉案金额':
                        lines.append(f"{risk_type}涉案总金额: {value}")
                    elif key == '处罚金额':
                        lines.append(f"{risk_type}总金额: {value}")
                    else:
                        lines.append(f"{risk_type}{key}: {value}")
        else:
            lines.append(f"{risk_type}: {info}")

    return '\n'.join(lines)


def _format_risk_details_markdown(details: Dict[str, List[Dict]]) -> str:
    """将详细风险事件转换为 Markdown"""
    if not details:
        return ""

    lines = ["### 详细风险事件"]

    # 定义需要展示的风险类型及其字段
    risk_field_map = {
        '司法案件': ['案件标题', '案由', '最新进程日期', '当事人信息'],
        '行政处罚': ['处罚类别', '违法事实', '处罚日期', '处罚金额'],
        '裁判文书': ['案件标题', '案由', '裁判日期', '涉案金额']
    }

    for risk_type, field_names in risk_field_map.items():
        if risk_type not in details or not details[risk_type]:
            continue

        events = details[risk_type]
        if not isinstance(events, list):
            continue

        lines.append("")
        lines.append(f"#### {risk_type}")

        for event in events[:3]:  # 最多3个事件
            if not isinstance(event, dict):
                continue

            if risk_type == '司法案件':
                title = event.get('案件标题', '')
                reason = event.get('案由', '')
                date = event.get('最新进程日期', '')
                parties = event.get('当事人信息', '')
                lines.append(f"案件: {title}, 案由: {reason}, 日期: {date}, 当事人: {parties}")

            elif risk_type == '行政处罚':
                penalty_type = event.get('处罚类别', '罚款')
                violation = event.get('违法事实', '')
                if len(violation) > 30:
                    violation = violation[:30] + '等'
                if not violation:
                    violation = event.get('违法行为类型', '')
                date = event.get('处罚日期', '')
                amount = event.get('处罚金额', '')
                lines.append(f"处罚: {penalty_type}, 违法类型: {violation}, 日期: {date}, 金额: {amount}")

            elif risk_type == '裁判文书':
                title = event.get('案件标题', '')
                reason = event.get('案由', '')
                date = event.get('裁判日期', '')
                amount = event.get('涉案金额', '')
                lines.append(f"案件: {title}, 案由: {reason}, 日期: {date}, 涉案金额: {amount}")

    return '\n'.join(lines)


def _format_risk_classification_markdown(risk_stats: Dict[str, Dict], details: Dict[str, List[Dict]]) -> str:
    """生成风险类型分类 Markdown"""
    if not risk_stats:
        return ""

    lines = ["### 风险类型分类"]

    # 司法与合规风险
    judicial_types = ['司法案件', '裁判文书', '行政处罚', '限制高消费']
    judicial_items = []

    for risk_type in judicial_types:
        if risk_type in risk_stats:
            info = risk_stats[risk_type]
            if isinstance(info, dict):
                count = info.get('数量', '')
                if count:
                    if risk_type == '裁判文书':
                        amount = info.get('涉案金额', '')
                        if amount:
                            judicial_items.append(f"{risk_type}总数: {count}，涉案总金额: {amount}")
                        else:
                            judicial_items.append(f"{risk_type}总数: {count}")
                    elif risk_type == '行政处罚':
                        amount = info.get('处罚金额', '')
                        if amount:
                            judicial_items.append(f"{risk_type}总数: {count}，处罚总金额: {amount}")
                        else:
                            judicial_items.append(f"{risk_type}总数: {count}")
                    else:
                        judicial_items.append(f"{risk_type}总数: {count}")

    if judicial_items:
        lines.append("")
        lines.append("#### 司法与合规风险")
        lines.append('；'.join(judicial_items))

    # 经营与财务风险
    business_types = ['股权质押', '股权出质', '司法拍卖']
    business_items = []

    for risk_type in business_types:
        if risk_type in risk_stats:
            info = risk_stats[risk_type]
            if isinstance(info, dict):
                count = info.get('数量', '')
                if risk_type == '股权质押':
                    stock = info.get('质押股数', '')
                    if count and stock:
                        business_items.append(f"{risk_type}总数: {count}，质押股数: {stock}")
                    elif count:
                        business_items.append(f"{risk_type}总数: {count}")
                elif count:
                    business_items.append(f"{risk_type}总数: {count}")

    if business_items:
        lines.append("")
        lines.append("#### 经营与财务风险")
        lines.append('；'.join(business_items))

    return '\n'.join(lines)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业风险大数据

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的风险大数据
    """
    # 1. 调用 API
    data = _call_risk_api(entname)

    if not data:
        return "# 风险大数据\n\n未查询到风险信息"

    # 2. 处理风险统计
    page_info = data.get('page_info', {})
    risk_stats = _process_risk_statistics(page_info)

    # 3. 处理详细风险信息
    risk_details = _process_risk_details(data)

    # 4. 生成 Markdown
    sections = ["# 风险大数据提炼"]

    # 风险统计摘要
    summary_md = _format_risk_summary_markdown(risk_stats)
    if summary_md:
        sections.append("")
        sections.append(summary_md)

    # 详细风险事件
    details_md = _format_risk_details_markdown(risk_details)
    if details_md:
        sections.append("")
        sections.append(details_md)

    # 风险类型分类
    classification_md = _format_risk_classification_markdown(risk_stats, risk_details)
    if classification_md:
        sections.append("")
        sections.append(classification_md)

    # 如果没有任何数据
    if len(sections) == 1:
        sections.append("")
        sections.append("暂无风险数据")

    return '\n'.join(sections)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s05_risk_data <企业名称>")
