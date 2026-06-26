#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update parse_config_from_text to support English configuration
"""

# Read the file
with open('fetch_and_generate_v2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the parse_config_from_text function
old_func_start = "# ========== 配置解析函数 =========="
old_func_end = "def prompt_user_for_input():"

# New function with English support
new_func = '''# ========== 配置解析函数 ==========
def parse_config_from_text(text):
    """
    从用户输入文本中解析完整的播报配置信息
    
    支持中文和英文配置格式
    
    中文配置格式示例：
    - 示例1: 【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
    - 示例2: 【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，不需要深度解读】
    
    英文配置格式示例：
    - Example 1: [Apple earnings report, style is formal news, format is single broadcast, voice is young female, no deep analysis]
    - Example 2: [Huawei Mate80 release, style is tech commentary, format is dual dialogue, host voice is mature male, commentator voice is gentle female, need deep analysis]
    
    返回:
        - 如果解析成功且配置完整: 返回配置字典
        - 如果解析成功但配置不完整: 返回 None（需要交互式收集）
        - 如果没有检测到配置格式: 返回 None
    """
    # 检测输入语言
    lang = detect_language(text)
    
    # 检查是否包含方括号包裹的配置信息（支持【】和[]）
    config_match = re.search(r'[【\\[](.+?)[】\\]]', text, re.DOTALL)
    if not config_match:
        return None
    
    config_text_raw = config_match.group(1).strip()
    
    # 根据语言选择分隔符
    if lang == 'en':
        # 英文配置使用逗号分隔
        parts = config_text_raw.split(',')
    else:
        # 中文配置使用中文逗号分隔
        parts = config_text_raw.split('，')
    
    if len(parts) < 1:
        return None
    
    keyword = parts[0].strip()
    if not keyword:
        return None
    
    config_text_lower = config_text_raw.lower()
    
    # 检查是否是"使用默认配置"模式（支持中英文）
    use_defaults = ('使用默认配置' in config_text_raw or 
                   'use default config' in config_text_lower)
    
    # 检查是否是"其他用默认配置"模式（支持中英文）
    use_partial_defaults = ('其他用默认配置' in config_text_raw or 
                             '其他使用默认' in config_text_raw or
                             'other use default' in config_text_lower)
    
    # 初始化配置
    config = {
        'keyword': keyword,
        'style': '',
        'format': '单人口播',
        'voice': '年轻活力的女生',
        'output_dir': '',
        'need_deep_analysis': False,
        'deep_analysis_style': '正式新闻腔',
        'deep_analysis_voice': '沉稳的中年男性',
        'is_complete_config': False,
        'use_defaults': False,
        'language': lang,
    }
    
    if use_defaults:
        config['is_complete_config'] = True
        config['use_defaults'] = True
        return config
    
    # 解析风格
    if lang == 'en':
        # 英文风格解析: style is X
        style_match = re.search(r'style\s+is\s+([^,]+)', config_text_lower)
        if style_match:
            style_en = style_match.group(1).strip()
            config['style'] = map_english_style(style_en)
    else:
        # 中文风格解析
        style_match = re.search(r'风格[是为]?([^，。]+)', config_text_raw)
        if style_match:
            style_raw = style_match.group(1).strip()
            style_map = {
                '正式新闻腔': '正式新闻腔',
                '正式新闻': '正式新闻腔',
                '轻松早报腔': '轻松早报腔',
                '轻松早报': '轻松早报腔',
                '财经严肃腔': '财经严肃腔',
                '财经严肃': '财经严肃腔',
                '科技快评腔': '科技快评腔',
                '科技快评': '科技快评腔',
            }
            config['style'] = style_map.get(style_raw, style_raw)
    
    # 解析形式
    if lang == 'en':
        # 英文形式解析: format is X
        format_match = re.search(r'format\s+is\s+([^,]+)', config_text_lower)
        if format_match:
            format_en = format_match.group(1).strip()
            config['format'] = map_english_format(format_en)
    else:
        # 中文形式解析
        if '单人口播' in config_text_raw:
            config['format'] = '单人口播'
        elif '双人对话' in config_text_raw or '双人' in config_text_raw:
            config['format'] = '双人对话式播报'
    
    # 解析音色
    if config['format'] == '双人对话式播报':
        # 双人对话
        if lang == 'en':
            # 英文: host voice is X, commentator voice is Y
            host_match = re.search(r'host\s+voice\s+is\s+([^,]+)', config_text_lower)
            commentator_match = re.search(r'commentator\s+voice\s+is\s+([^,]+)', config_text_lower)
            
            host_voice = map_english_voice(host_match.group(1).strip()) if host_match else '沉稳的中年男性'
            commentator_voice = map_english_voice(commentator_match.group(1).strip()) if commentator_match else '年轻活力的女生'
            config['voice'] = f'主播:{host_voice},评论员:{commentator_voice}'
        else:
            # 中文解析（原有逻辑）
            host_match = re.search(r'主播[用是为\\s]*([^，。]+?)(?:音色|声音)?[,，]', config_text_raw)
            if not host_match:
                host_match = re.search(r'主播[用是为\\s]*([^，。评论员]+)', config_text_raw)
            if host_match:
                host_voice = host_match.group(1).strip()
                if '男' in host_voice or '沉' in host_voice:
                    host_voice = '沉稳的中年男性'
                elif '女' in host_voice or '温' in host_voice:
                    host_voice = '温柔的女生'
                elif '专业' in host_voice or '新闻' in host_voice:
                    host_voice = '专业新闻主播'
                elif '年轻' in host_voice or '活力' in host_voice:
                    host_voice = '年轻活力的女生'
                config['voice'] = f'主播:{host_voice}'
            else:
                config['voice'] = '主播:沉稳的中年男性'
            
            commentator_match = re.search(r'评论员[用是为\\s]*([^，。]+?)(?:音色|声音)?[,，]', config_text_raw)
            if not commentator_match:
                commentator_match = re.search(r'评论员[用是为\\s]*([^，。]+)', config_text_raw)
            if commentator_match:
                commentator_voice = commentator_match.group(1).strip()
                if '男' in commentator_voice or '沉' in commentator_voice:
                    commentator_voice = '沉稳的中年男性'
                elif '女' in commentator_voice or '温' in commentator_voice:
                    commentator_voice = '温柔的女生'
                elif '专业' in commentator_voice or '新闻' in commentator_voice:
                    commentator_voice = '专业新闻主播'
                elif '年轻' in commentator_voice or '活力' in commentator_voice:
                    commentator_voice = '年轻活力的女生'
                config['voice'] += f',评论员:{commentator_voice}'
            else:
                config['voice'] += ',评论员:年轻活力的女生'
    else:
        # 单人口播
        if lang == 'en':
            # 英文: voice is X
            voice_match = re.search(r'voice\s+is\s+([^,]+)', config_text_lower)
            if voice_match:
                voice_en = voice_match.group(1).strip()
                config['voice'] = map_english_voice(voice_en)
        else:
            # 中文解析（原有逻辑）
            voice_patterns = [
                r'用([^，。]+?)(?:音色|声音)',
                r'(?:音色|声音)是([^，。]+)',
            ]
            voice_matched = False
            for pattern in voice_patterns:
                match = re.search(pattern, config_text_raw)
                if match:
                    voice_raw = match.group(1).strip()
                    if voice_raw and '风格' not in voice_raw and voice_raw not in ['用', '是']:
                        config['voice'] = voice_raw
                        voice_matched = True
                        break
            
            if not voice_matched:
                if '沉稳' in config_text_raw or '中年' in config_text_raw or '男声' in config_text_raw or '男性' in config_text_raw:
                    config['voice'] = '沉稳的中年男性'
                elif '温柔' in config_text_raw or '柔和' in config_text_raw:
                    config['voice'] = '温柔的女生'
                elif '专业' in config