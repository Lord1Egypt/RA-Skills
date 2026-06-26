"""报表模板配置模块"""

from typing import Dict, Any, List

# 模板配置字典
TEMPLATES: Dict[str, Dict[str, Any]] = {
    'monthly_operation': {
        'name': '月度运营报告',
        'description': '适用于月度业务运营数据分析',
        'sheets': ['封面', '数据概览', '图表分析', 'AI分析', '原始数据'],
        'chart_types': ['line', 'bar', 'pie'],
        'recommended_columns': ['日期', '月份', '销售额', '订单量', '用户数', '转化率'],
    },
    'financial': {
        'name': '财务报表',
        'description': '适用于财务收支、预算执行等分析',
        'sheets': ['封面', '数据概览', '图表分析', 'AI分析', '原始数据'],
        'chart_types': ['bar', 'line', 'pie'],
        'recommended_columns': ['日期', '收入', '支出', '利润', '预算', '实际'],
    },
    'sales': {
        'name': '销售报告',
        'description': '适用于销售业绩、区域对比等分析',
        'sheets': ['封面', '数据概览', '图表分析', 'AI分析', '原始数据'],
        'chart_types': ['bar', 'line', 'scatter'],
        'recommended_columns': ['日期', '销售额', '客户数', '产品数', '区域', '渠道'],
    },
    'data_comparison': {
        'name': '数据对比报告',
        'description': '适用于多周期、多维度数据对比',
        'sheets': ['封面', '数据概览', '图表分析', 'AI分析', '原始数据'],
        'chart_types': ['bar', 'line'],
        'recommended_columns': ['期间', '指标A', '指标B', '变化率'],
    },
    'custom': {
        'name': '自定义模板',
        'description': '通用模板，可根据实际数据灵活配置',
        'sheets': ['封面', '数据概览', '图表分析', 'AI分析', '原始数据'],
        'chart_types': ['line', 'bar', 'pie', 'scatter'],
        'recommended_columns': [],
    },
}


def get_template(template_name: str) -> Dict[str, Any]:
    """获取指定模板配置

    Args:
        template_name: 模板名称

    Returns:
        dict: 模板配置字典

    Raises:
        KeyError: 模板不存在时抛出
    """
    if template_name not in TEMPLATES:
        raise KeyError(f"模板 '{template_name}' 不存在。可用模板: {list(TEMPLATES.keys())}")
    return TEMPLATES[template_name]


def list_templates() -> List[str]:
    """列出所有可用模板名称

    Returns:
        list: 模板名称列表
    """
    return list(TEMPLATES.keys())


def get_template_info(template_name: str) -> str:
    """获取模板的简要信息

    Args:
        template_name: 模板名称

    Returns:
        str: 模板信息描述
    """
    template = get_template(template_name)
    return f"[{template['name']}] {template['description']}"
