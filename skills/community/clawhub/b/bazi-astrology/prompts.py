#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
命理分析提示词管理模块
"""

# 导入配置文件
from prompt_config import *


def format_complete_dayun(complete_dayun):
    """将完整大运列表格式化为提示词可读文本。"""
    if not complete_dayun:
        return "未提供完整大运信息。"
    lines = []
    for i, yun in enumerate(complete_dayun, start=1):
        gan_zhi = yun.get('gan_zhi', '')
        year = yun.get('year', '')
        age = yun.get('age', '')
        lines.append(f"{i}. {gan_zhi}（起始年份：{year}，对应年龄：{age}岁）")
    return "\n".join(lines)

def build_bazi_analysis_prompt(bazi_info, analysis_type='bazi_analysis', complete_dayun=None):
    """
    构建八字分析的提示词
    
    Args:
        bazi_info (str): 八字信息字符串
        analysis_type (str): 分析类型，可选值：'bazi_analysis', 'detailed_analysis', 'simple_analysis'
        complete_dayun (list): 完整大运列表（10步）
    
    Returns:
        str: 完整的提示词
    """
    complete_dayun_text = format_complete_dayun(complete_dayun)
    if analysis_type in PROMPT_TEMPLATES:
        return PROMPT_TEMPLATES[analysis_type].format(
            bazi_info=bazi_info,
            complete_dayun=complete_dayun_text,
            dayun_list="未提供当前三步大运信息。",
            existing_mingge_analysis="未提供。",
        )
    else:
        # 默认使用基础分析模板
        return PROMPT_TEMPLATES['bazi_analysis'].format(
            bazi_info=bazi_info,
            complete_dayun=complete_dayun_text
        )

def build_bazi_info_string(bazi_data, gender):
    """
    构建八字信息字符串
    
    Args:
        bazi_data (dict): 八字数据
        gender (str): 性别
    
    Returns:
        str: 格式化的八字信息字符串
    """
    bazi_info = f"""
八字信息：
年柱：{bazi_data['nian']['tian_gan']['char']}{bazi_data['nian']['di_zhi']['char']}
月柱：{bazi_data['yue']['tian_gan']['char']}{bazi_data['yue']['di_zhi']['char']}
日柱：{bazi_data['ri']['tian_gan']['char']}{bazi_data['ri']['di_zhi']['char']}
时柱：{bazi_data['shi']['tian_gan']['char']}{bazi_data['shi']['di_zhi']['char']}
性别：{gender}
日主：{bazi_data['ri']['tian_gan']['char']}
"""
    return bazi_info

def get_system_prompt(prompt_type='bazi_analysis'):
    """
    获取系统提示词
    
    Args:
        prompt_type (str): 提示词类型
    
    Returns:
        str: 系统提示词
    """
    return SYSTEM_PROMPTS.get(prompt_type, SYSTEM_PROMPTS['bazi_analysis'])

def get_analysis_prompt_template():
    """
    获取分析提示词模板
    
    Returns:
        str: 提示词模板
    """
    return """
你是一位精通八字命理的专家。请根据以下八字信息，从专业角度分析命格，并给出以下三个方面的详细分析：

{bazi_info}

请分别分析：
1. 生辰解读：拿到这个八字后进行整体分析，包括性格特点、做事风格、优势短板、事业趋势、婚姻趋势与人生发力点，并给出阶段性建议。
2. 十神格局：分析八字中的十神组合，判断命局格局类型。
3. 五行喜忌：根据五行分析，给出具体的喜用五行和忌用五行建议。

请用专业、准确的中文回答，并控制篇幅：生辰解读180-260字；十神格局80-120字；五行喜忌80-120字。
"""

def build_dayun_analysis_prompt(bazi_info, dayun_ganzhi, complete_dayun=None):
    """
    构建大运分析的提示词
    
    Args:
        bazi_info (str): 八字信息字符串
        dayun_ganzhi (str): 大运干支
        complete_dayun (list): 完整大运列表（10步）
    
    Returns:
        str: 完整的提示词
    """
    return PROMPT_TEMPLATES['dayun_analysis'].format(
        bazi_info=bazi_info,
        dayun_ganzhi=dayun_ganzhi,
        complete_dayun=format_complete_dayun(complete_dayun)
    )

def build_multi_dayun_analysis_prompt(bazi_info, dayun_list):
    """
    构建多大大运分析的提示词
    
    Args:
        bazi_info (str): 八字信息字符串
        dayun_list (list): 大运干支列表，最多3个
    
    Returns:
        str: 完整的提示词
    """
    if len(dayun_list) > 3:
        dayun_list = dayun_list[:3]
    
    dayun_text = "\n".join([f"大运{i+1}：{ganzhi}" for i, ganzhi in enumerate(dayun_list)])
    
    return PROMPT_TEMPLATES['multi_dayun_analysis'].format(
        bazi_info=bazi_info,
        dayun_list=dayun_text,
        ganzhi1=dayun_list[0] if len(dayun_list) > 0 else "",
        ganzhi2=dayun_list[1] if len(dayun_list) > 1 else "",
        ganzhi3=dayun_list[2] if len(dayun_list) > 2 else ""
    )

def parse_dayun_analysis(content):
    """
    解析大运分析结果
    
    Args:
        content (str): AI返回的分析内容
    
    Returns:
        dict: 解析后的分析结果
    """
    analysis = {
        'career': '',
        'wealth': '',
        'love': ''
    }
    
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检测分析部分
        if '事业运势' in line or '1.' in line:
            current_section = 'career'
            continue
        elif '财运分析' in line or '2.' in line:
            current_section = 'wealth'
            continue
        elif '感情运势' in line or '3.' in line:
            current_section = 'love'
            continue
            
        # 如果当前有部分，则添加到对应部分
        if current_section and line:
            if analysis[current_section]:
                analysis[current_section] += ' ' + line
            else:
                analysis[current_section] = line
    
    # 如果没有成功解析，返回原始内容按段落分割
    if not any(analysis.values()):
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if len(paragraphs) >= 3:
            analysis['career'] = paragraphs[0]
            analysis['wealth'] = paragraphs[1]
            analysis['love'] = paragraphs[2]
        else:
            # 如果段落不够，将内容平均分配
            content_parts = content.split('\n')
            part_length = len(content_parts) // 3
            for i, key in enumerate(['career', 'wealth', 'love']):
                start = i * part_length
                end = start + part_length if i < 2 else len(content_parts)
                analysis[key] = '\n'.join(content_parts[start:end])
    
    return analysis

def parse_multi_dayun_analysis(content, dayun_list):
    """
    解析多大大运分析结果
    
    Args:
        content (str): AI返回的分析内容
        dayun_list (list): 大运干支列表
    
    Returns:
        list: 解析后的分析结果列表，每个元素包含career、wealth、love
    """
    results = []
    
    # 按"---"分割内容
    sections = content.split('---')
    
    for i, section in enumerate(sections):
        if i >= len(dayun_list):
            break
            
        analysis = {
            'career': '',
            'wealth': '',
            'love': ''
        }
        
        # 处理单行格式：大运1（壬午）： 事业运势：官印相生，贵人提携 财运分析：财星暗藏，稳步积累 感情运势：午火助身，异性缘佳
        if '：' in section and '事业运势' in section and '财运分析' in section and '感情运势' in section:
            # 提取事业运势
            career_start = section.find('事业运势：')
            wealth_start = section.find('财运分析：')
            love_start = section.find('感情运势：')
            
            if career_start != -1 and wealth_start != -1 and love_start != -1:
                # 提取事业运势内容
                career_end = wealth_start
                analysis['career'] = section[career_start + 5:career_end].strip()
                
                # 提取财运分析内容
                wealth_end = love_start
                analysis['wealth'] = section[wealth_start + 5:wealth_end].strip()
                
                # 提取感情运势内容
                analysis['love'] = section[love_start + 5:].strip()
        
        # 处理多行格式
        else:
            lines = section.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # 检测分析部分
                if '事业运势' in line:
                    current_section = 'career'
                    # 提取事业运势内容
                    if '：' in line:
                        analysis['career'] = line.split('：', 1)[1].strip()
                    continue
                elif '财运分析' in line:
                    current_section = 'wealth'
                    # 提取财运分析内容
                    if '：' in line:
                        analysis['wealth'] = line.split('：', 1)[1].strip()
                    continue
                elif '感情运势' in line:
                    current_section = 'love'
                    # 提取感情运势内容
                    if '：' in line:
                        analysis['love'] = line.split('：', 1)[1].strip()
                    continue
                    
                # 如果当前有部分，则添加到对应部分
                if current_section and line:
                    if analysis[current_section]:
                        analysis[current_section] += ' ' + line
                    else:
                        analysis[current_section] = line
        
        # 如果没有成功解析，显示全部内容
        if not any(analysis.values()):
            analysis['career'] = f"{section}"
            analysis['wealth'] = f"{section}"
            analysis['love'] = f"{section}"
        
        results.append(analysis)
    
    # 确保返回结果数量与输入的大运数量一致
    while len(results) < len(dayun_list):
        ganzhi = dayun_list[len(results)]
        results.append({
            'career': f"{ganzhi}大运事业运势平稳",
            'wealth': f"{ganzhi}大运财运平稳",
            'love': f"{ganzhi}大运感情运势平稳"
        })
    
    return results

# 可配置的提示词参数
PROMPT_CONFIG = LLM_CONFIG

# 分析维度配置（从配置文件中的字典提取名称）
ANALYSIS_DIMENSIONS_NAMES = {k: v['name'] for k, v in ANALYSIS_DIMENSIONS.items()}

# 分析维度描述（从配置文件中的字典提取描述）
DIMENSION_DESCRIPTIONS = {k: v['description'] for k, v in ANALYSIS_DIMENSIONS.items()}

# 为了向后兼容，保留原来的变量名
ANALYSIS_DIMENSIONS = ANALYSIS_DIMENSIONS_NAMES 