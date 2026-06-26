#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科创能力评估一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, Optional
from .base import call_api, debug_print


# ============ 映射表 ============

KECHUANG_DICT = {
    "value_level": "科创综合能力评价等级",
    "dimension_a_level": "科创资质维度评价等级",
    "J0268": "当前是否为有效瞪羚企业",
    "J0269": "当前是否为独角兽企业",
    "J0270": "当前是否为种子独角兽企业",
    "J0271": "当前是否为潜在独角兽企业",
    "J0272": "当前是否为培育瞪羚企业",
    "J0301": "当前是否为有效高新技术企业",
    "J0307": "当前是否为中关村高新技术企业",
    "J0316": "当前是否为有效科技型中小企业",
    "J0318": "上一年度是否为有效科技型中小企业",
    "J0322": "当前是否为有效省级专精特新中小企业",
    "J0327": "当前是否为有效国家级专精特新'小巨人'企业",
    "J0339": "当前是否为有效省级制造业单项冠军示范企业",
    "J0342": "当前是否拥有有效省级制造业单项冠军产品",
    "J0348": "当前是否为有效省级制造业单项冠军培育企业",
    "J0351": "当前是否为有效国家技术创新示范企业",
    "J0354": "当前是否为有效国家众创空间企业",
    "J0360": "当前是否为有效国家级科技企业孵化器",
    "J0364": "当前是否为有效创新型中小企业",
    "J0367": "当前是否为有效雏鹰企业",
    "J0369": "当前是否为有效隐形冠军企业",
    "J0393": "当前是否为有效技术先进型服务企业",
    "J0501": "当前是否为有效国家级制造业单项冠军企业",
    "J0503": "当前是否为有效省级科技小巨人企业",
    "J0504": "当前是否为有效省级专业化小巨人企业",
    "J0505": "当前是否为有效民营科技企业",
    "J0506": "当前是否为有效科技领军企业",
    "J0507": "当前是否为国家级服务型制造示范企业",
    "J0508": "当前是否为省级服务型制造示范企业",
    "J0509": "当前是否为市级服务型制造示范企业",
    "J0510": "当前是否为国家级服务型制造示范培育企业",
    "J0511": "当前是否为省级服务型制造示范培育企业",
    "J0513": "当前是否为牛羚企业",
    "J0516": "当前是否为科改示范企业",
    "J0517": "当前是否为国家级创新型企业",
    "J0518": "当前是否为省级创新型企业",
    "J0519": "当前是否为市级创新型企业",
    "J0520": "当前是否为国家级创新型试点企业",
    "J0521": "当前是否为省级创新型试点企业",
    "J0522": "当前是否为市级创新型试点企业",
    "J0529": "是否获得科技企业孵化器",
    "L0102": "上市板块",
    "L0153": "拟IPO板块",
    "dimension_b_level": "科研能力维度评价等级",
    "J0357": "当前是否为有效国家企业技术中心企业",
    "J0358": "当前是否为有效省级企业技术中心企业",
    "J0375": "当前是否具有效国家级工业设计中心企业",
    "J0377": "当前是否具有效国家重点实验室",
    "J0379": "当前是否具有省部共建国家重点实验室",
    "J0381": "当前是否具有效国家工程技术研究中心",
    "J0383": "当前是否具有效国家工程研究中心",
    "J0385": "当前是否具有效国家工程实验室",
    "J0387": "当前是否具有有效院士专家工作站",
    "J0389": "当前是否具有有效院士工作站",
    "J0391": "当前是否具有效国家地方联合工程研究中心",
    "J0395": "当前是否为有效新型研发机构",
    "J0397": "当前是否为有效制造业创新中心",
    "J0526": "是否获得省市级工业设计中心",
    "J0527": "是否获得省市级工程技术研究中心",
    "J0528": "是否获得科技创新中心",
    "J0610": "专利申请年份数量（单位年）",
    "J0611": "专利申请连续性",
    "J0612": "年均获得有效非外观专利数量",
    "J0613": "累计已授权过专利数量",
    "J0614": "专利授权率",
    "J0615": "有效发明专利平均预期寿命（年）",
    "J0625": "有效发明专利在非外观专利内占比",
    "J0629": "专利核心发明人数量",
    "dimension_c_level": "科研成果维度评价等级",
    "G1028": "获得国家技术发明奖最高级别",
    "G1029": "获得国家科学技术进步奖最高级别",
    "G1030": "累计获得国家科技成果数量",
    "G1031": "近五年内获得国家科技成果数量",
    "J0150": "累计已授权且未终止专利数量",
    "J0153": "累计登记软件著作权数量",
    "J0371": "当前是否为有效国家知识产权优势企业",
    "J0373": "当前是否为有效国家知识产权示范企业",
    "J0523": "累计获得知识产权奖次数",
    "J0524": "累计获得科学技术奖次数",
    "J0601": "累计PCT专利申请数量",
    "J0602": "累计PCT专利进入国家阶段数量",
    "J0603": "累计申请非外观专利涉及主IPC大类数量",
    "J0604": "累计已授权且未终止非外观专利涉及主IPC大类数量",
    "J0605": "累计申请非外观专利涉及主IPC小类数量",
    "J0606": "累计已授权且未终止非外观专利涉及主IPC小类数量",
    "J0616": "当前法律状态处于审中环节专利数量（不包含已授权）",
    "J0617": "当前处于对外许可环节专利数量",
    "J0618": "当前处于对外质押环节专利数量",
    "J0619": "累计申请专利类型为实用新型专利数量",
    "J0620": "累计拥有专利类型为实用新型专利且已授权未终止数量",
    "J0621": "累计申请专利类型为外观专利数量",
    "J0622": "累计拥有专利类型为外观专利且已授权未终止数量",
    "J0623": "累计申请专利类型为发明专利数量",
    "J0624": "累计拥有专利类型为发明且已授权未终止专利数量",
    "J0626": "剩余有效期超过 10 年的发明专利数量",
    "J0627": "剩余有效期在五年以内的发明专利数量",
    "J0628": "剩余有效期在五年至10年的发明专利数量",
    "J0630": "累计集成电路布图设计有效数量",
    "L0128": "累计参与有效国家标准制定次数",
    "L0129": "累计参与有效行业标准制定次数",
    "L0130": "累计参与有效地方标准制定次数",
    "L0131": "累计参与有效团体标准制定次数",
    "dimension_d_level": "成长特性维度评价等级",
    "C0202": "近一年内分支机构数量",
    "C0204": "统计时点分支机构数量",
    "D0255": "融资事件数量",
    "D0265": "近一年内融资次数",
    "E0202": "累计对外投资公司在营企业数量",
    "E0215": "近一年内对外投资公司数量",
    "J0114": "近一年内申请专利数量",
    "J0143": "近五年内申请专利数量",
    "J0127": "近一年内登记软件著作权数量",
    "J0152": "近五年内新登记软著数量",
    "H0407": "近一年内注册资本增资次数",
    "H0412": "近两年内注册资本增资次数",
    "dimension_e_level": "行业潜力维度评价等级",
    "B0203": "所属战略新兴产业类别",
    "B0221": "所属高技术产业(制造业)大类",
    "B0222": "所属高技术产业(服务业)大类",
    "B0223": "所属知识产权(专利)密集型产业大类",
    "B0224": "所属国家重点支持的高新技术领域"
}


# ============ 辅助函数 ============

def _get_dimension_level(score: Any, dimension_type: str) -> str:
    """根据分数和维度类型返回对应的等级"""
    try:
        score = float(score) if score else 0
    except (ValueError, TypeError):
        score = 0

    if dimension_type == 'a':  # 科创资质维度
        if 17 <= score <= 20:
            return "卓越"
        elif 13 <= score < 17:
            return "优秀"
        elif 9 <= score < 13:
            return "良好"
        elif 6 <= score < 9:
            return "一般"
        elif 0 <= score < 6:
            return "入门"
    elif dimension_type in ['b', 'c']:  # 科研能力维度、科研成果维度
        if 25 <= score <= 30:
            return "卓越"
        elif 20 <= score < 25:
            return "优秀"
        elif 12 <= score < 20:
            return "良好"
        elif 6 <= score < 12:
            return "一般"
        elif 0 <= score < 6:
            return "入门"
    elif dimension_type == 'd':  # 成长特性维度
        if 13 <= score <= 15:
            return "卓越"
        elif 10 <= score < 13:
            return "优秀"
        elif 7 <= score < 10:
            return "良好"
        elif 4 <= score < 7:
            return "一般"
        elif 0 <= score < 4:
            return "入门"
    elif dimension_type == 'e':  # 行业潜力维度
        if 4 <= score <= 5:
            return "优秀"
        elif 2 <= score < 4:
            return "良好"
        elif 0 <= score < 2:
            return "一般"

    return "未知"


def _process_label_value(label_code: str, label_value: Any) -> str:
    """根据 label_code 对 label_value 进行特殊处理"""
    if not label_value:
        return str(label_value) if label_value is not None else ''

    # 需要转化为"是"的标签
    year_to_yes_labels = [
        'J0268', 'J0269', 'J0270', 'J0271', 'J0272', 'J0513', 'J0516',
        'J0517', 'J0518', 'J0519', 'J0520', 'J0521', 'J0522'
    ]

    # 需要转化为百分比的标签
    percent_labels = ['J0614', 'J0625']

    # 需要添加年份单位的标签
    year_unit_labels = ['J0610']

    if label_code in year_to_yes_labels:
        if str(label_value).strip() and str(label_value) != '0':
            return "是"
        else:
            return "否"
    elif label_code in percent_labels:
        try:
            percent_val = float(label_value) * 100
            return f"{percent_val:.2f}%"
        except:
            return str(label_value)
    elif label_code in year_unit_labels:
        return f"{label_value}年"

    return str(label_value)


# ============ API 调用 ============

def _call_innovation_api(entname: str) -> Dict[str, Any]:
    """调用科创能力评估 API"""
    response = call_api('/enterprise/scienceTechnologyEvaluation', {'entname': entname}, method='GET')
    return response


def _fetch_innovation_data(entname: str) -> Optional[Dict[str, Any]]:
    """获取并处理科创数据"""
    response = _call_innovation_api(entname)

    if response.get('code') != 200:
        return None

    data = response.get('data', {})
    if not data:
        return None

    processed_data = {}

    # 处理科创能力等级信息
    kc_value_level = data.get('kc_value_level', {})
    if isinstance(kc_value_level, str):
        processed_data['科创能力等级信息'] = {'科创综合能力评价等级': kc_value_level}
    elif isinstance(kc_value_level, dict):
        processed_data['科创能力等级信息'] = {'科创综合能力评价等级': kc_value_level.get('value_level', '')}
    else:
        processed_data['科创能力等级信息'] = {'科创综合能力评价等级': str(kc_value_level) if kc_value_level else ''}

    # 处理命中的特征标签
    hit_feature = data.get('hit_feature', [])
    hit_labels_by_dimension = {'a': {}, 'b': {}, 'c': {}, 'd': {}, 'e': {}}

    for label in hit_feature:
        if isinstance(label, dict):
            label_dimension = label.get('label_dimension', '').lower()
            label_code = label.get('label_code', '')

            if label_code in KECHUANG_DICT:
                label_name = KECHUANG_DICT[label_code]
                label_value = label.get('label_value', '')

                if label_value and label_dimension in hit_labels_by_dimension:
                    processed_value = _process_label_value(label_code, label_value)
                    hit_labels_by_dimension[label_dimension][label_name] = processed_value

    # 处理各个维度
    dimensions = ['a', 'b', 'c', 'd', 'e']
    dimension_names = {
        'a': '科创资质评价维度信息',
        'b': '科研能力评价维度信息',
        'c': '科研成果评价维度信息',
        'd': '成长特性评价维度信息',
        'e': '行业潜力评价维度信息'
    }

    dimension_level_names = {
        'a': '科创资质维度评价等级',
        'b': '科研能力维度评价等级',
        'c': '科研成果维度评价等级',
        'd': '成长特性维度评价等级',
        'e': '行业潜力维度评价等级'
    }

    for dim in dimensions:
        score_key = f'kc_dimension_{dim}_score'
        dimension_score = data.get(score_key, 0)
        dimension_level = _get_dimension_level(dimension_score, dim)

        dimension_labels = hit_labels_by_dimension.get(dim, {})
        dimension_data = {dimension_level_names[dim]: dimension_level}
        dimension_data.update(dimension_labels)

        processed_data[dimension_names[dim]] = dimension_data

    return processed_data


# ============ Markdown 格式化 ============

def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    if not data:
        return "# 科创能力评估\n\n暂无科创能力评估数据"

    sections = ["# 科创能力提炼"]

    # 企业概要
    overview_lines = ["", "### 企业概要"]

    level_info = data.get('科创能力等级信息', {})
    qual_info = data.get('科创资质评价维度信息', {})
    rd_capacity = data.get('科研能力评价维度信息', {})
    rd_results = data.get('科研成果评价维度信息', {})
    growth_info = data.get('成长特性评价维度信息', {})
    industry_info = data.get('行业潜力评价维度信息', {})

    if level_info.get('科创综合能力评价等级'):
        overview_lines.append(f"科创综合能力等级：{level_info.get('科创综合能力评价等级', '')}")
    if qual_info.get('科创资质维度评价等级'):
        overview_lines.append(f"科创资质等级：{qual_info.get('科创资质维度评价等级', '')}")
    if rd_capacity.get('科研能力维度评价等级'):
        overview_lines.append(f"科研能力等级：{rd_capacity.get('科研能力维度评价等级', '')}")
    if rd_results.get('科研成果维度评价等级'):
        overview_lines.append(f"科研成果等级：{rd_results.get('科研成果维度评价等级', '')}")
    if growth_info.get('成长特性维度评价等级'):
        overview_lines.append(f"成长特性等级：{growth_info.get('成长特性维度评价等级', '')}")
    if industry_info.get('行业潜力维度评价等级'):
        overview_lines.append(f"行业潜力等级：{industry_info.get('行业潜力维度评价等级', '')}")

    sections.append('\n'.join(overview_lines))

    # 科创资质
    qual_items = []
    high_tech_items = []
    if qual_info.get('当前是否为有效高新技术企业') == '是':
        high_tech_items.append("高新技术企业")
    if qual_info.get('当前是否为中关村高新技术企业') == '是':
        high_tech_items.append("中关村高新")
    if high_tech_items:
        qual_items.append(f"高新技术类：{', '.join(high_tech_items)}")

    special_items = []
    if qual_info.get('当前是否为有效国家级专精特新"小巨人"企业') == '是':
        special_items.append("国家级小巨人")
    if qual_info.get('当前是否为有效省级专精特新中小企业') == '是':
        special_items.append("省级专精特新")
    if special_items:
        qual_items.append(f"专精特新类：{', '.join(special_items)}")

    gazelle_items = []
    if qual_info.get('当前是否为有效瞪羚企业') == '是':
        gazelle_items.append("瞪羚")
    if qual_info.get('当前是否为独角兽企业') == '是':
        gazelle_items.append("独角兽")
    if gazelle_items:
        qual_items.append(f"瞪羚/独角兽类：{', '.join(gazelle_items)}")

    listing_board = qual_info.get('上市板块')
    ipo_board = qual_info.get('拟IPO板块')
    if listing_board:
        qual_items.append(f"上市/IPO状态：上市板块:{listing_board}")
    elif ipo_board:
        qual_items.append(f"上市/IPO状态：拟IPO板块:{ipo_board}")

    if qual_items:
        sections.append("")
        sections.append("### 科创资质")
        sections.extend(qual_items)

    # 科研能力
    rd_items = []
    patent_indicators = []
    if rd_capacity.get('专利申请年份数量（单位年）'):
        patent_indicators.append(f"专利申请年份数:{rd_capacity.get('专利申请年份数量（单位年）', '')}")
    if rd_capacity.get('专利申请连续性'):
        patent_indicators.append(f"申请连续性:{rd_capacity.get('专利申请连续性', '')}")
    if rd_capacity.get('年均获得有效非外观专利数量'):
        patent_indicators.append(f"年均有效非外观专利:{rd_capacity.get('年均获得有效非外观专利数量', '')}")
    if patent_indicators:
        rd_items.append(f"专利能力指标：{', '.join(patent_indicators)}")

    other_indicators = []
    if rd_capacity.get('累计已授权过专利数量'):
        other_indicators.append(f"累计授权专利:{rd_capacity.get('累计已授权过专利数量', '')}")
    if rd_capacity.get('专利授权率'):
        other_indicators.append(f"专利授权率:{rd_capacity.get('专利授权率', '')}")
    if other_indicators:
        rd_items.append(f"其他专利指标：{', '.join(other_indicators)}")

    if rd_capacity.get('专利核心发明人数量'):
        rd_items.append(f"核心发明人数量：{rd_capacity.get('专利核心发明人数量', '')}")

    if rd_items:
        sections.append("")
        sections.append("### 科研能力")
        sections.extend(rd_items)

    # 科研成果
    result_items = []

    # 奖项与荣誉
    if rd_results.get('累计获得国家科技成果数量'):
        result_items.append(f"累计国家科技成果：{rd_results.get('累计获得国家科技成果数量', '')}")
    if rd_results.get('累计获得知识产权奖次数'):
        result_items.append(f"累计知识产权奖：{rd_results.get('累计获得知识产权奖次数', '')}次")

    # 专利成果
    if rd_results.get('累计已授权且未终止专利数量'):
        result_items.append(f"累计有效专利：{rd_results.get('累计已授权且未终止专利数量', '')}")
    if rd_results.get('累计登记软件著作权数量'):
        result_items.append(f"软著数量：{rd_results.get('累计登记软件著作权数量', '')}")

    # 标准制定
    standard_parts = []
    if rd_results.get('累计参与有效国家标准制定次数'):
        standard_parts.append(f"国家标准:{rd_results.get('累计参与有效国家标准制定次数', '')}")
    if rd_results.get('累计参与有效行业标准制定次数'):
        standard_parts.append(f"行业标准:{rd_results.get('累计参与有效行业标准制定次数', '')}")
    if standard_parts:
        result_items.append(f"标准制定：{', '.join(standard_parts)}")

    if result_items:
        sections.append("")
        sections.append("### 科研成果")
        sections.extend(result_items)

    # 成长特性
    growth_items = []

    # 分支机构
    branch_parts = []
    if growth_info.get('近一年内分支机构数量'):
        branch_parts.append(f"近一年:{growth_info.get('近一年内分支机构数量', '')}")
    if growth_info.get('统计时点分支机构数量'):
        branch_parts.append(f"统计时点:{growth_info.get('统计时点分支机构数量', '')}")
    if branch_parts:
        growth_items.append(f"分支机构：{', '.join(branch_parts)}")

    # 融资与投资
    if growth_info.get('融资事件数量'):
        growth_items.append(f"累计融资事件：{growth_info.get('融资事件数量', '')}")
    if growth_info.get('累计对外投资公司在营企业数量'):
        growth_items.append(f"累计对外投资在营：{growth_info.get('累计对外投资公司在营企业数量', '')}")

    # 知识产权动态
    ip_parts = []
    if growth_info.get('近一年内申请专利数量'):
        ip_parts.append(f"近一年申请专利:{growth_info.get('近一年内申请专利数量', '')}")
    if growth_info.get('近五年内申请专利数量'):
        ip_parts.append(f"近五年申请专利:{growth_info.get('近五年内申请专利数量', '')}")
    if ip_parts:
        growth_items.append(f"知识产权动态：{', '.join(ip_parts)}")

    if growth_items:
        sections.append("")
        sections.append("### 成长特性")
        sections.extend(growth_items)

    # 行业潜力
    industry_items = []
    if industry_info.get('所属战略新兴产业类别'):
        industry_items.append(f"战略新兴产业：{industry_info.get('所属战略新兴产业类别', '')}")
    if industry_info.get('所属高技术产业(制造业)大类'):
        industry_items.append(f"高技术产业(制造)：{industry_info.get('所属高技术产业(制造业)大类', '')}")
    if industry_info.get('所属高技术产业(服务业)大类'):
        industry_items.append(f"高技术产业(服务)：{industry_info.get('所属高技术产业(服务业)大类', '')}")
    if industry_info.get('所属知识产权(专利)密集型产业大类'):
        industry_items.append(f"知识产权密集型产业：{industry_info.get('所属知识产权(专利)密集型产业大类', '')}")
    if industry_info.get('所属国家重点支持的高新技术领域'):
        industry_items.append(f"国家重点支持高新领域：{industry_info.get('所属国家重点支持的高新技术领域', '')}")

    if industry_items:
        sections.append("")
        sections.append("### 行业潜力")
        sections.extend(industry_items)

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业科创能力评估信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的科创能力评估信息
    """
    # 1. 获取科创数据
    data = _fetch_innovation_data(entname)

    if not data:
        return "# 科创能力评估\n\n该企业无法进行科创能力评价"

    # 2. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s18_innovation <企业名称>")
