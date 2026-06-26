"""
工具集名称：全国高考志愿填报助手 MCP
工具集简介：提供高考志愿填报相关工具，获取学校和专业以往的录取分数线，提供推荐信息等。注意：往年的数据都是真实数据，当前2026年的数据还未发布，为提前获得完整体验，暂时基于2025年数据虚拟了一份，后面会及时更新。
"""

from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_control_lines(
    province: str,
    year: Optional[int] = None
) -> Dict[str, Any]:
    """
    获取某省某年的高考控制分数线（一本线/二本线）。
    
    Args:
        province: 招生省份
        year: 年份，默认为今年
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "province": province,
        "year": year
    }
    
    return call_api("1820705335657482", "get_control_lines", arguments)

def get_school_scores(
    province: str,
    school: str,
    category: str
) -> Dict[str, Any]:
    """
    获取学校前几年的录取分数线。
    
    Args:
        province: 招生省份
        school: 学校名称，如"清华大学"
        category: 科类：综合/文科/理科/物理类/历史类
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "province": province,
        "school": school,
        "category": category
    }
    
    return call_api("1820705335657482", "get_school_scores", arguments)

def get_plans(
    province: str,
    school: str,
    year: Optional[int] = None
) -> Dict[str, Any]:
    """
    查询某所学校在某省某年的招生计划。
    
    Args:
        province: 招生省份
        school: 学校名称，如"清华大学"
        year: 年份，默认为今年
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "province": province,
        "school": school,
        "year": year
    }
    
    return call_api("1820705335657482", "get_plans", arguments)

def get_major_scores(
    province: str,
    school: str,
    category: str
) -> Dict[str, Any]:
    """
    查询某所学校在某省某科类的各专业历年录取分数线。当用户想了解具体专业的录取分数（如"北大的计算机多少分"、"西安交大各专业录取分数"）时使用。返回每个专业的最低分、位次和录取人数。
    
    Args:
        province: 招生省份
        school: 学校名称，如"清华大学"
        category: 科类：综合/文科/理科/物理类/历史类
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "province": province,
        "school": school,
        "category": category
    }
    
    return call_api("1820705335657482", "get_major_scores", arguments)

def search_schools(
    is985: Optional[bool] = None,
    score: str,
    province: str,
    is211: Optional[bool] = None,
    level: Optional[str] = None,
    target_provinces: Optional[str] = None,
    category: str
) -> Dict[str, Any]:
    """
    根据考生条件筛选有录取数据的候选学校，返回的学校中筛选录取位次接近考生排名（考生排名±3000名）的学校名称。你需要提取学校名称传给 calculate_probability 计算概率。
    
    Args:
        is985: 是否只看985（可选）
        score: 高考分数
        province: 招生省份
        is211: 是否只看211（可选）
        level: 报考等级（本科或者专科）,默认为本科
        target_provinces: 指定选择哪些省份的学校，省份名称以逗号分隔。若不输入此参数，则搜索所有省份的学校。
        category: 科类：综合/文科/理科/物理类/历史类
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "is985": is985,
        "score": score,
        "province": province,
        "is211": is211,
        "level": level,
        "target_provinces": target_provinces,
        "category": category
    }
    
    return call_api("1820705335657482", "search_schools", arguments)

def calculate_probability(
    score: str,
    province: str,
    level: Optional[str] = None,
    target_schools: str,
    category: str
) -> Dict[str, Any]:
    """
    批量计算录取概率。传入学校代码列表，返回每所学校的录取概率、档位（冲刺/稳妥/保底/不建议）和说明。
    
    Args:
        score: 高考分数
        province: 招生省份
        level: 报考等级（本科或者专科）,默认为本科
        target_schools: 目标学校名称列表，逗号分隔
        category: 科类：综合/文科/理科/物理类/历史类
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "score": score,
        "province": province,
        "level": level,
        "target_schools": target_schools,
        "category": category
    }
    
    return call_api("1820705335657482", "calculate_probability", arguments)

def lookup_scores(
    province: str,
    school: str,
    category: str
) -> Dict[str, Any]:
    """
    查询某所学校在某省某科类的历年录取分数线（最近5年），包含最低分、最低排名
    
    Args:
        province: 招生省份
        school: 学校名称，如"清华大学"
        category: 科类：综合/文科/理科/物理类/历史类
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "province": province,
        "school": school,
        "category": category
    }
    
    return call_api("1820705335657482", "lookup_scores", arguments)

def search_school_by_keyword(
    is985: Optional[bool] = None,
    q: str,
    is211: Optional[bool] = None,
    level: Optional[str] = None,
    target_provinces: Optional[str] = None
) -> Dict[str, Any]:
    """
    模糊搜索学校。按学校名称或代码搜索，支持筛选条件。
    
    Args:
        is985: 是否只看985（可选）
        q: 学校名称的搜索关键词
        is211: 是否只看211（可选）
        level: 报考等级（本科或者专科）,默认为本科
        target_provinces: 指定选择哪些省份的学校，省份名称以逗号分隔。若不输入此参数，则搜索所有省份的学校。
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "is985": is985,
        "q": q,
        "is211": is211,
        "level": level,
        "target_provinces": target_provinces
    }
    
    return call_api("1820705335657482", "search_school_by_keyword", arguments)

def score_to_rank(
    score: str,
    province: str,
    year: Optional[int] = None,
    level: Optional[str] = None,
    category: str
) -> Dict[str, Any]:
    """
    将高考分数转换为省排名（基于官方一分一段表）。当用户只有分数不知道位次时使用此工具。
    
    Args:
        score: 高考分数
        province: 招生省份
        year: 年份，默认为今年
        level: 报考等级（本科或者专科）,默认为本科
        category: 科类：综合/文科/理科/物理类/历史类
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "score": score,
        "province": province,
        "year": year,
        "level": level,
        "category": category
    }
    
    return call_api("1820705335657482", "score_to_rank", arguments)

def get_school_info(
    info_type: Optional[str] = None,
    school: str
) -> Dict[str, Any]:
    """
    获取关于指定学校的某方面信息。通过设置参数info_type的值（"基本信息", "学校简介", "学校详情", "大学排名", "学科评估", "特色专业", "院系设置"）获取相应信息。默认返回基本信息。
    
    Args:
        info_type: 信息选项（可选），支持查询的信息选项："基本信息", "学校简介", "学校详情", "大学排名", "学科评估", "特色专业", "院系设置"。
        school: 学校名称，如"清华大学"
    
    Returns:
        返回文本信息或JSON格式数据。
    """
    arguments = {
        "info_type": info_type,
        "school": school
    }
    
    return call_api("1820705335657482", "get_school_info", arguments)

def get_major_info(
    info_type: Optional[str] = None,
    major: str
) -> Dict[str, Any]:
    """
    获取关于指定专业的某方面信息。通过设置参数info_type的值（"基本信息", "专业介绍", "培养目标", "授予学位", "修业年限", "男女比例", "专业与就业", "专业解析", "报考指南","主要就业行业分布", "主要就业地区分布", "近10年平均薪资", "就业方向", "主要职业分布"）获取相应信息。默认返回基本信息。
    
    Args:
        info_type: 信息选项（可选），支持查询的信息选项："基本信息", "专业介绍", "培养目标", "授予学位", "修业年限", "男女比例", "专业与就业", "专业解析", "报考指南","主要就业行业分布", "主要就业地区分布", "近10年平均薪资", "就业方向", "主要职业分布"。
        major: 专业名称
    
    Returns:
        返回文本信息或JSON格式数据。
    """
    arguments = {
        "info_type": info_type,
        "major": major
    }
    
    return call_api("1820705335657482", "get_major_info", arguments)

def get_schools_of_major(
    major: str
) -> Dict[str, Any]:
    """
    获取开设某专业的学校列表（按该专业的排名顺序）。
    
    Args:
        major: 专业名称
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "major": major
    }
    
    return call_api("1820705335657482", "get_schools_of_major", arguments)

def get_majors_of_school(
    school: str
) -> Dict[str, Any]:
    """
    获取某学校开设的专业列表。
    
    Args:
        school: 学校名称，如"清华大学"
    
    Returns:
        返回JSON格式数据。
    """
    arguments = {
        "school": school
    }
    
    return call_api("1820705335657482", "get_majors_of_school", arguments)

