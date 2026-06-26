#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
空壳公司识别一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from .base import call_api, debug_print


# ============ 映射表 ============

# 空壳公司类型映射
SHELL_TYPE_MAPPING = {
    'CORPSE1': '僵尸类空壳公司',
    'DIFFMANAGE': '地址存疑类空壳公司',
    'NOACTUALOPT': '无实际经营类空壳公司',
    'SUITE': '套牌类空壳公司',
    'PUPPET': '傀儡类空壳公司',
    'RELATE': '空壳关联方类空壳公司',
    'BACKDOOR': '借壳经营类空壳公司',
    'SHELLGANG': '团伙类空壳公司'
}

# 傀儡类型映射
PUPPET_TYPE_MAPPING = {
    '01': '一人多企',
    '02': '一号多企',
    '04': '经营白户'
}

# 借壳前类型映射
ORIGINAL_TYPE_MAPPING = {
    '01': '僵尸企业',
    '03': '地址存疑',
    '04': '无实际经营',
    '05': '套牌公司',
    '07': '傀儡公司',
    '08': '空壳公司关联方',
    '09': '借壳经营',
    '11': '空壳团伙'
}

# 风险描述
RISK_DESCRIPTIONS = {
    'CORPSE1': '僵尸企业虽已不再经营，但账户可能被用于不法行为，需防范洗钱风险',
    'DIFFMANAGE': '注册地址疑似非真实经营地址，需防范洗钱风险和欺诈风险',
    'NOACTUALOPT': '无实际经营活动迹象，需防范洗钱和欺诈风险',
    'SUITE': '套牌公司常充当犯罪工具，需防范洗钱风险',
    'PUPPET': '傀儡公司风险程度很高，需重点防范洗钱和欺诈风险',
    'RELATE': '关联方存在多家空壳公司，需关注关联风险',
    'BACKDOOR': '借壳经营存在洗钱和欺诈风险',
    'SHELLGANG': '团伙类空壳公司影响恶劣，需重点防范洗钱风险'
}

# 高风险类型
HIGH_RISK_TYPES = ['PUPPET', 'SUITE', 'SHELLGANG', 'BACKDOOR']
MEDIUM_RISK_TYPES = ['CORPSE1', 'DIFFMANAGE', 'NOACTUALOPT']


# ============ API 调用 ============

def _call_entinfo_api(entname: str) -> Dict[str, Any]:
    """调用企业基本信息 API（获取企业名称和经营状态）"""
    response = call_api(
        '/entinfo',
        {'name': entname, 'mask': '100000000000000000000000000000000'},
        method='GET'
    )
    return response


def _call_shell_company_api(entname: str) -> Dict[str, Any]:
    """调用空壳公司识别 API"""
    response = call_api('/shell/company', {'entname': entname}, method='GET')
    return response


# ============ 数据处理 ============

def _format_date(date_str: str) -> str:
    """格式化日期字符串"""
    if date_str and len(date_str) == 8:
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return date_str


def _process_puppet_type(puppet_type: str) -> str:
    """处理傀儡类型"""
    return PUPPET_TYPE_MAPPING.get(puppet_type, puppet_type)


def _process_original_type(original_type: str) -> str:
    """处理借壳前类型"""
    if not original_type:
        return "未知"

    if ',' in str(original_type):
        type_codes = str(original_type).split(',')
        type_names = []
        for code in type_codes:
            code = code.strip()
            if code:
                type_names.append(ORIGINAL_TYPE_MAPPING.get(code, f"未知类型({code})"))
        return ', '.join(type_names) if type_names else "未知"
    else:
        return ORIGINAL_TYPE_MAPPING.get(str(original_type).strip(), f"未知类型({original_type})")


def _process_relate_companies(relat_companies: List[Dict]) -> Dict[str, Any]:
    """处理关联空壳公司信息"""
    if not relat_companies:
        return {}

    result = {
        "关联空壳公司数量": len(relat_companies)
    }

    # 统计关联公司的空壳类型
    shell_type_counts = {}
    for company in relat_companies:
        if 'TYPE' in company:
            for type_code in company['TYPE']:
                type_name = ORIGINAL_TYPE_MAPPING.get(type_code, type_code)
                shell_type_counts[type_name] = shell_type_counts.get(type_name, 0) + 1

    if shell_type_counts:
        type_summary = [f"{k}({v}家)" for k, v in shell_type_counts.items()]
        result["关联空壳类型分布"] = '; '.join(type_summary)

    return result


def _fetch_shell_data(entname: str) -> Optional[Dict[str, Any]]:
    """获取空壳公司数据"""
    # 1. 先获取企业基本信息
    entinfo_response = _call_entinfo_api(entname)

    if entinfo_response.get('CODE') != 200:
        return None

    ent_info = entinfo_response.get('ENT_INFO', {})
    if not ent_info:
        return None

    basic_info = ent_info.get('BASIC', {})
    entname = basic_info.get('ENTNAME', '').strip()
    entstatus = basic_info.get('ENTSTATUS', '').strip()

    if not entname or not entstatus:
        return None

    # 2. 只有在营企业才查询空壳公司
    if entstatus != '在营（开业）':
        return {
            "企业名称": entname,
            "经营状态": entstatus,
            "是否疑似空壳公司": "不适用",
            "说明": "企业非在营状态，不进行空壳公司识别"
        }

    # 3. 调用空壳公司识别 API
    shell_response = _call_shell_company_api(entname)

    if shell_response.get('CODE') != 200:
        return None

    data = shell_response.get('DATA', {})
    if not data:
        return None

    # 4. 处理数据
    result = {
        "企业名称": entname,
        "经营状态": entstatus
    }

    # 获取数据日期
    data_date = ""
    if 'BASEINFO' in data:
        data_date = data['BASEINFO'].get('DATA_DATE', '')
        data_date = _format_date(data_date)

    # 判断是否为空壳公司
    shell_data = data.get('SHELLDATA', {})
    is_shell = shell_data.get('ISSHELL', False)
    result["是否疑似空壳公司"] = "是" if is_shell else "否"

    if not is_shell:
        return result

    # 5. 处理各类空壳公司信息
    detected_types = []
    risk_level = 0
    shell_details = {}

    for shell_type, type_name in SHELL_TYPE_MAPPING.items():
        if shell_type in data and data[shell_type]:
            shell_info = data[shell_type]
            detected_types.append(type_name)

            # 获取判定日期
            judgment_date = ""
            if shell_type == "DIFFMANAGE" and 'INDATE' in shell_info:
                judgment_date = shell_info.get('INDATE', '')
            if not judgment_date:
                judgment_date = data_date

            # 基本信息
            detail = {
                "判定原因": shell_info.get('RISK_TIPS', ''),
                "判定日期": judgment_date,
                "风险描述": RISK_DESCRIPTIONS.get(shell_type, '')
            }

            # 特殊字段处理
            if shell_type == "PUPPET" and 'PUPPET_TYPE' in shell_info:
                detail["傀儡类型"] = _process_puppet_type(shell_info['PUPPET_TYPE'])

            if shell_type == "BACKDOOR" and 'ORIGINAL_TYPE' in shell_info:
                detail["借壳前空壳类型"] = _process_original_type(shell_info['ORIGINAL_TYPE'])

            if shell_type == "RELATE" and 'RELATCOMPANIES' in shell_info:
                relate_info = _process_relate_companies(shell_info['RELATCOMPANIES'])
                detail.update(relate_info)

            shell_details[type_name] = detail

            # 风险等级评估
            if shell_type in HIGH_RISK_TYPES:
                risk_level = max(risk_level, 3)
            elif shell_type in MEDIUM_RISK_TYPES:
                risk_level = max(risk_level, 2)
            else:
                risk_level = max(risk_level, 1)

    result["空壳类型"] = detected_types
    result["详细分析"] = shell_details

    # 风险等级判定
    if risk_level >= 3:
        result["风险等级"] = "高风险"
    elif risk_level >= 2:
        result["风险等级"] = "中风险"
    elif risk_level >= 1:
        result["风险等级"] = "低风险"
    else:
        result["风险等级"] = "无风险"

    return result


# ============ Markdown 格式化 ============

def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    if not data:
        return "# 空壳公司识别\n\n暂无空壳公司识别数据"

    sections = ["# 空壳公司识别提炼"]

    entname = data.get('企业名称', '')
    entstatus = data.get('经营状态', '')
    is_shell = data.get('是否疑似空壳公司', '否')

    # 基本信息
    sections.append("")
    sections.append("## 识别结果")
    sections.append("")
    sections.append(f"- 企业名称：{entname}")
    sections.append(f"- 经营状态：{entstatus}")
    sections.append(f"- 是否疑似空壳公司：{is_shell}")

    # 如果不是空壳公司或不适用
    if is_shell == "不适用":
        sections.append(f"- 说明：{data.get('说明', '')}")
        return '\n'.join(sections)

    if is_shell == "否":
        sections.append("")
        sections.append("该企业未被识别为疑似空壳公司。")
        return '\n'.join(sections)

    # 空壳公司详细信息
    risk_level = data.get('风险等级', '未知')
    shell_types = data.get('空壳类型', [])
    details = data.get('详细分析', {})

    sections.append(f"- 风险等级：{risk_level}")
    sections.append(f"- 命中空壳类型：{len(shell_types)}种")

    # 风险概述
    sections.append("")
    sections.append("## 风险概述")
    sections.append("")

    if shell_types:
        sections.append(f"该企业被识别为疑似空壳公司，命中以下{len(shell_types)}种空壳类型：")
        sections.append("")
        for i, shell_type in enumerate(shell_types, 1):
            sections.append(f"{i}. {shell_type}")

    # 详细分析
    if details:
        sections.append("")
        sections.append("## 详细分析")

        for type_name, type_detail in details.items():
            sections.append("")
            sections.append(f"### {type_name}")
            sections.append("")

            if type_detail.get('判定原因'):
                sections.append(f"- 判定原因：{type_detail['判定原因']}")
            if type_detail.get('判定日期'):
                sections.append(f"- 判定日期：{type_detail['判定日期']}")
            if type_detail.get('风险描述'):
                sections.append(f"- 风险描述：{type_detail['风险描述']}")

            # 特殊字段
            if type_detail.get('傀儡类型'):
                sections.append(f"- 傀儡类型：{type_detail['傀儡类型']}")
            if type_detail.get('借壳前空壳类型'):
                sections.append(f"- 借壳前空壳类型：{type_detail['借壳前空壳类型']}")
            if type_detail.get('关联空壳公司数量'):
                sections.append(f"- 关联空壳公司数量：{type_detail['关联空壳公司数量']}家")
            if type_detail.get('关联空壳类型分布'):
                sections.append(f"- 关联空壳类型分布：{type_detail['关联空壳类型分布']}")

    # 风险提示
    sections.append("")
    sections.append("## 风险提示")
    sections.append("")

    risk_tips = []
    if '傀儡类空壳公司' in shell_types:
        risk_tips.append("傀儡公司风险程度很高，需重点防范洗钱和欺诈风险")
    if '套牌类空壳公司' in shell_types:
        risk_tips.append("套牌公司是专业养壳机构批量设立空壳公司的主要形态，常充当犯罪工具")
    if '团伙类空壳公司' in shell_types:
        risk_tips.append("空壳团伙可以实施更隐蔽、规模更大的违法行为，需重点关注")
    if '借壳经营类空壳公司' in shell_types:
        risk_tips.append("借壳经营可能用于获取对公账户进行洗钱或绕过行业准入限制")
    if '僵尸类空壳公司' in shell_types:
        risk_tips.append("僵尸企业账户可能被用于不法行为，需注意防范洗钱风险")
    if '地址存疑类空壳公司' in shell_types:
        risk_tips.append("地址存疑增加监管难度，容易引发偷税漏税及其他违法行为")
    if '无实际经营类空壳公司' in shell_types:
        risk_tips.append("无实际经营的企业可能被用于洗钱、包装贷等不法活动")
    if '空壳关联方类空壳公司' in shell_types:
        risk_tips.append("企业关联方存在多家空壳公司，需关注关联风险")

    if risk_tips:
        for tip in risk_tips:
            sections.append(f"- {tip}")
    else:
        sections.append("- 请综合评估企业实际经营情况和风险状况")

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业空壳公司识别信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的空壳公司识别信息
    """
    # 1. 获取数据
    data = _fetch_shell_data(entname)

    if not data:
        return "# 空壳公司识别\n\n未查询到企业空壳公司识别信息"

    # 2. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s19_shell_company <企业名称>")
