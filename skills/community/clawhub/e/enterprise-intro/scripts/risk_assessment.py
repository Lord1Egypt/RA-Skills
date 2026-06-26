#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险评测一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from .base import call_api, debug_print


# ============ 映射表 ============

# 风险分类代码映射
RISK_CLASSIFICATION_MAPPING = {
    'B': '基础特征',
    'L': '低风险',
    'A': '决策人异常',
    'Z': '政策禁止',
    'G': '高风险',
    'Q': '主体异常',
    'E': '联系方式异常',
    'T': '住所地址异常',
    'S': '法定代表人异常',
    'H': '股权或治理结构异常',
    'X': '企业沿革异常',
    'K': '关联方异常',
    'M': '空壳公司特征'
}

# 风险分类排序（按重要性）
CLASSIFICATION_ORDER = [
    '政策禁止', '高风险', '主体异常', '决策人异常', '股权或治理结构异常',
    '关联方异常', '联系方式异常', '住所地址异常', '法定代表人异常',
    '企业沿革异常', '空壳公司特征', '低风险'
]


# ============ API 调用 ============

def _call_entinfo_api(entname: str) -> Dict[str, Any]:
    """调用企业基本信息 API（处理分公司）"""
    response = call_api('/entinfo', {'name': entname}, method='GET')
    return response


def _call_risk_classification_api(entname: str) -> Dict[str, Any]:
    """调用风险评级 API"""
    response = call_api('/index/accountRiskClassification', {'entname': entname}, method='GET')
    return response


# ============ 数据处理 ============

def _map_risk_classification(label_code: str) -> str:
    """映射风险分类代码到中文"""
    if not label_code:
        return ""
    first_char = label_code[0].upper()
    return RISK_CLASSIFICATION_MAPPING.get(first_char, label_code)


def _categorize_risk_labels(hit_features: List[Dict]) -> Dict[str, str]:
    """根据权重对风险标签进行分类"""
    high_risk_labels = []  # weight >= 0.5
    med_risk_labels = []   # 0.03 <= weight < 0.5
    low_risk_labels = []   # 0 <= weight < 0.03

    for feature in hit_features:
        label_code = feature.get('labelCode', '')

        # 过滤掉B类标签
        if label_code.startswith('B'):
            continue

        weight = feature.get('weight', 0)
        label_name = feature.get('labelName', '')

        # Z类和G类标签直接归为高风险
        if label_code.startswith('Z') or label_code.startswith('G'):
            high_risk_labels.append(label_name)

        # 处理weight为None的情况
        if weight is None:
            if label_code.startswith('L'):
                low_risk_labels.append(label_name)
            else:
                med_risk_labels.append(label_name)
            continue

        if weight >= 0.5:
            high_risk_labels.append(label_name)
        elif weight >= 0.03:
            med_risk_labels.append(label_name)
        else:
            low_risk_labels.append(label_name)

    return {
        'highrisklabel': ','.join(high_risk_labels),
        'medrisklabel': ','.join(med_risk_labels),
        'lowrisklabel': ','.join(low_risk_labels)
    }


def _fetch_risk_data(entname: str, retry_count: int = 0) -> Optional[Dict[str, Any]]:
    """获取风险评测数据"""
    if retry_count > 1:
        return None

    response = _call_risk_classification_api(entname)
    code = response.get('code')

    # 处理分公司情况
    if code == 202:
        entinfo_response = _call_entinfo_api(entname)

        if entinfo_response.get('CODE') != 200:
            return None

        ent_info = entinfo_response.get('ENT_INFO', {})
        basic_info = ent_info.get('BASIC', {})
        entstatus = basic_info.get('ENTSTATUS', '')

        if entstatus != '在营（开业）':
            return None

        # 检查是否有总公司
        headquarters = ent_info.get('HEADQUARTERS', {})
        if headquarters:
            parent_entname = headquarters.get('ENTNAME', '')
            if parent_entname and parent_entname != entname:
                return _fetch_risk_data(parent_entname, retry_count + 1)

        return None

    # 处理其他非成功状态
    if code in [203, 404] or code != 200:
        return None

    # 处理成功的响应数据
    data = response.get('data', {})
    risk_level = data.get('riskLevel', '')

    # 低风险/中低风险不输出
    if risk_level in ['低风险', '中低风险']:
        return None

    # 处理风险标签信息
    hit_features = data.get('hitFeature', [])

    # 过滤B类标签
    filtered_features = [
        feature for feature in hit_features
        if not feature.get('labelCode', '').startswith('B')
    ]

    # 处理每个标签的风险分类映射
    for feature in filtered_features:
        label_code = feature.get('labelCode', '')
        feature['风险分类'] = _map_risk_classification(label_code)

    # 根据权重分类风险标签
    risk_categorization = _categorize_risk_labels(filtered_features)

    # 收集所有的风险分类
    risk_classifications = list(set([
        feature.get('风险分类', '')
        for feature in filtered_features
        if feature.get('风险分类', '')
    ]))

    # 按顺序排列已存在的分类
    sorted_classifications = [
        item for item in CLASSIFICATION_ORDER
        if item in risk_classifications
    ]

    result = {
        '风险级别': risk_level,
        '风险标签信息': []
    }

    if filtered_features:
        risk_info = {
            '风险分类': '、'.join(sorted_classifications),
            '高权重指标': risk_categorization.get('highrisklabel', ''),
            '中权重指标': risk_categorization.get('medrisklabel', ''),
            '低权重指标': risk_categorization.get('lowrisklabel', '')
        }

        # 移除空的指标
        risk_info = {k: v for k, v in risk_info.items() if v}
        result['风险标签信息'].append(risk_info)

    return result


# ============ Markdown 格式化 ============

def _parse_comma_separated_tags(tag_string: str) -> List[str]:
    """解析逗号分隔的标签字符串，返回标签列表（倒序）"""
    if not tag_string:
        return []

    tags = [tag.strip() for tag in tag_string.split(',')]
    tags = [tag for tag in tags if tag]
    return list(reversed(tags))


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    if not data:
        return ""

    risk_level = data.get('风险级别', '')
    risk_tags_info = data.get('风险标签信息', [])

    sections = ["# 风险评测提炼"]

    # 如果没有风险标签信息，只输出风险等级
    if not risk_tags_info:
        if risk_level:
            sections.append("")
            sections.append("## 风险等级摘要")
            sections.append("")
            sections.append(f"整体风险等级：{risk_level}")
        return '\n'.join(sections)

    # 获取第一个风险标签信息项
    risk_info = risk_tags_info[0] if risk_tags_info else {}

    # 提取各权重指标
    high_weight_tags = _parse_comma_separated_tags(risk_info.get('高权重指标', ''))
    medium_weight_tags = _parse_comma_separated_tags(risk_info.get('中权重指标', ''))
    low_weight_tags = _parse_comma_separated_tags(risk_info.get('低权重指标', ''))

    # 提取风险分类
    risk_classification = risk_info.get('风险分类', '')

    # 1. 风险等级摘要
    if risk_level:
        sections.append("")
        sections.append("## 风险等级摘要")
        sections.append("")
        sections.append(f"整体风险等级：{risk_level}")

    # 2. 风险标签详情
    tag_sections = []

    if high_weight_tags:
        tag_list_str = '、'.join(high_weight_tags)
        tag_sections.append(f"- 高风险标签（高权重）：{tag_list_str}")

    if medium_weight_tags:
        tag_list_str = '、'.join(medium_weight_tags)
        tag_sections.append(f"- 中风险标签（中权重）：{tag_list_str}")

    if low_weight_tags:
        tag_list_str = '、'.join(low_weight_tags)
        tag_sections.append(f"- 低风险标签（低权重）：{tag_list_str}")

    if tag_sections:
        sections.append("")
        sections.append("## 风险标签详情")
        sections.append("")
        sections.extend(tag_sections)

    # 3. 风险分类
    if risk_classification:
        sections.append("")
        sections.append("## 风险分类")
        sections.append("")
        sections.append(f"涉及风险分类：{risk_classification}")

    # 4. 风险说明
    sections.append("")
    sections.append("## 风险说明")
    sections.append("")
    sections.append("- 风险级别从高到低分为六类：政策禁止、高风险、中高风险、中风险、中低风险、低风险")
    sections.append("- 高权重指标：重度风险标签，风险程度较高，需要重点关注")
    sections.append("- 中权重指标：中度风险标签，风险程度一般，需要关注")
    sections.append("- 低权重指标：轻度风险标签，虽存在一定风险，但影响程度较小")

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业风险评测信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的风险评测信息
    """
    # 1. 获取数据
    data = _fetch_risk_data(entname)

    if not data:
        return "# 风险评测\n\n该企业风险评级为低风险或暂无风险评测数据"

    # 2. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s20_risk_assessment <企业名称>")
