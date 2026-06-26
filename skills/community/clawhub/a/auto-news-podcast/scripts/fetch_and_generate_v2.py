#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto News Podcast v2.0 - 智能新闻播客生成器
功能：多源搜索 → 去重清洗 → 三级摘要 → 风格化播报文案 → 配图 → 播报音频
支持单人口播和双人对话两种形式，5 种音色，4 种播报风格
"""

import json
import os
import sys
import codecs
import re
import time
import hashlib
import requests
from datetime import datetime
from difflib import SequenceMatcher

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

# 导入优化版图片搜索模块（优先 v3）
try:
    from image_search_v3 import search_cover_image_v3
    search_cover_image = search_cover_image_v3
    IMAGE_SEARCH_V3_AVAILABLE = True
    IMAGE_SEARCH_V2_AVAILABLE = False
except ImportError:
    IMAGE_SEARCH_V3_AVAILABLE = False
    try:
        from image_search_v2 import search_cover_image_v2
        search_cover_image = search_cover_image_v2
        IMAGE_SEARCH_V2_AVAILABLE = True
    except ImportError:
        IMAGE_SEARCH_V2_AVAILABLE = False

# 全局缓存（用于图片搜索 fallback）
news_items_cache = []


def _get_unsplash_key():
    """获取 Unsplash API Key
    
    优先级：
    1. OpenClaw 配置文件 (~/.openclaw/openclaw.json)
    2. 环境变量 UNSPLASH_ACCESS_KEY
    
    Returns:
        str: API Key 或 None（未配置）
    """
    # 1. 尝试从 OpenClaw 配置读取
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 尝试从 custom 中读取
                unsplash_key = config.get('custom', {}).get('unsplash', {}).get('accessKey')
                if unsplash_key:
                    return unsplash_key
                # 尝试从 env 中读取
                unsplash_key = config.get('env', {}).get('UNSPLASH_ACCESS_KEY')
                if unsplash_key:
                    return unsplash_key
        except Exception as e:
            print(f'[WARN] 读取 OpenClaw 配置失败: {e}')
    
    # 2. 尝试从环境变量读取
    unsplash_key = os.environ.get('UNSPLASH_ACCESS_KEY')
    if unsplash_key:
        return unsplash_key
    
    # 未配置，返回 None
    return None


# Unsplash access key（动态获取，可能为 None）
UNSPLASH_KEY = _get_unsplash_key()

# ========== 音色映射 ==========

VOICE_MAP = {
    '年轻': 'zh-CN-XiaoxiaoNeural',
    '活力': 'zh-CN-XiaoxiaoNeural',
    '沉稳': 'zh-CN-YunxiNeural',
    '中年': 'zh-CN-YunxiNeural',
    '男声': 'zh-CN-YunxiNeural',
    '男生': 'zh-CN-YunxiNeural',
    '温柔': 'zh-CN-XiaoyiNeural',
    '柔和': 'zh-CN-XiaoyiNeural',
    '专业': 'zh-CN-YunyangNeural',
    '新闻': 'zh-CN-YunyangNeural',
    '主播': 'zh-CN-YunyangNeural',
    '播音': 'zh-CN-YunyangNeural',
    '情感': 'zh-CN-XiaobeiNeural',
    '戏剧': 'zh-CN-XiaobeiNeural',
    '活泼': 'zh-CN-XiaobeiNeural',
}

VOICE_LABELS = {
    'zh-CN-XiaoxiaoNeural': '年轻活力的女生',
    'zh-CN-YunxiNeural': '沉稳的中年男性',
    'zh-CN-XiaoyiNeural': '温柔的女生',
    'zh-CN-YunyangNeural': '专业新闻主播',
    'zh-CN-XiaobeiNeural': '情感丰富的声音',
}

# 双人对话默认音色（主播=沉稳中年男性，评论员=年轻活力女生）
DEFAULT_HOST_VOICE = 'zh-CN-YunxiNeural'           # 主播：沉稳的中年男性
DEFAULT_COMMENTATOR_VOICE = 'zh-CN-XiaoxiaoNeural' # 评论员：年轻活力的女生

# ========== 播报风格 ==========

STYLES = {
    '1': '正式新闻腔',
    '2': '轻松早报腔',
    '3': '财经严肃腔',
    '4': '科技快评腔',
}

STYLE_KEYWORDS = {
    '正式新闻腔': ['政策', '政府', '国务院', '部委', '人大', '政协', '外交部', '联合国'],
    '财经严肃腔': ['股票', '基金', '经济', '房价', 'GDP', '通胀', '利率', '财报', '市值', '涨跌'],
    '科技快评腔': ['AI', '芯片', '互联网', '产品', '发布', '技术', '算法', '模型', 'APP', '智能'],
}

# ========== 播报形式 ==========

FORMATS = {
    '1': '单人口播',
    '2': '双人对话式播报',
}

# ========== 宽泛领域关键词列表 ==========
BROAD_KEYWORDS = [
    '财经', '科技', '教育', '医疗', '体育', '娱乐', '房产', '汽车',
    'AI', '芯片', '互联网', '新能源', '房地产', '金融', '股市',
    '中东', '欧洲', '美国', '中国', '国际', '国内', '社会',
]


# ========== English Configuration Mappings ==========
STYLE_MAP_EN = {
    'formal news': '正式新闻腔',
    'formal': '正式新闻腔',
    'morning brief': '轻松早报腔',
    'casual morning': '轻松早报腔',
    'finance serious': '财经严肃腔',
    'financial serious': '财经严肃腔',
    'finance': '财经严肃腔',
    'tech commentary': '科技快评腔',
    'technology commentary': '科技快评腔',
    'tech': '科技快评腔',
    'technology': '科技快评腔',
}

FORMAT_MAP_EN = {
    'single broadcast': '单人口播',
    'single': '单人口播',
    'solo': '单人口播',
    'dual dialogue': '双人对话式播报',
    'dual': '双人对话式播报',
    'dialogue': '双人对话式播报',
    'double': '双人对话式播报',
    'two person': '双人对话式播报',
    'two host': '双人对话式播报',
}

VOICE_MAP_EN = {
    'young female': '年轻活力的女生',
    'young woman': '年轻活力的女生',
    'young girl': '年轻活力的女生',
    'energetic female': '年轻活力的女生',
    'mature male': '沉稳的中年男性',
    'mature man': '沉稳的中年男性',
    'middle aged male': '沉稳的中年男性',
    'middle aged man': '沉稳的中年男性',
    'calm male': '沉稳的中年男性',
    'gentle female': '温柔的女生',
    'gentle woman': '温柔的女生',
    'soft female': '温柔的女生',
    'soft voice': '温柔的女生',
    'professional anchor': '专业新闻主播',
    'professional broadcaster': '专业新闻主播',
    'news anchor': '专业新闻主播',
    'anchor': '专业新闻主播',
    'emotional': '情感丰富的声音',
    'dramatic': '情感丰富的声音',
    'lively': '情感丰富的声音',
}


def _load_openclaw_config():
    """读取 OpenClaw 配置文件"""
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f'  [WARN] 读取 OpenClaw 配置失败: {e}')
    return {}


def _get_default_model_config():
    """获取 OpenClaw 默认模型配置
    
    优先读取当前 Agent 会话使用的模型配置（agents.list[].model），
    如果没有则回退到全局默认模型（agents.defaults.model.primary）。
    """
    config = _load_openclaw_config()
    
    # 优先获取当前 Agent 的模型配置
    default_model = None
    agent_list = config.get('agents', {}).get('list', [])
    for agent in agent_list:
        if agent.get('id') == 'main':  # 当前会话通常是 main agent
            default_model = agent.get('model')
            break
    
    # 如果当前 Agent 没有配置模型，回退到全局默认
    if not default_model:
        default_model = config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', 'qwen/qwen3.5-plus')
    
    # 解析 provider 和 model
    if '/' in default_model:
        provider_name, model_id = default_model.split('/', 1)
    else:
        provider_name = 'qwen'
        model_id = default_model
    
    # 查找对应的 provider 配置
    providers = config.get('models', {}).get('providers', {})
    provider_config = None
    
    # 尝试匹配 provider
    for name, cfg in providers.items():
        if name.lower() == provider_name.lower() or provider_name.lower() in name.lower():
            provider_config = cfg
            break
    
    if provider_config:
        return {
            'provider': provider_name,
            'model': model_id,
            'api_key': provider_config.get('apiKey'),
            'base_url': provider_config.get('baseUrl'),
            'models_list': provider_config.get('models', [])
        }
    
    # 如果找不到配置，返回 None
    return None


def _get_model_api_key(provider_config):
    """从 provider 配置中获取 API Key
    
    支持从环境变量或配置文件中获取。
    """
    api_key = provider_config.get('apiKey')
    
    # 如果 apiKey 是环境变量引用（如 "DASHSCOPE_API_KEY"），从环境变量读取
    if api_key and not api_key.startswith('sk-'):
        env_key = os.environ.get(api_key)
        if env_key:
            return env_key
    
    return api_key


def is_broad_keyword(keyword):
    keyword_lower = keyword.lower()
    
    # 直接匹配宽泛领域词
    if keyword_lower in [k.lower() for k in BROAD_KEYWORDS]:
        return True
    
    # 如果关键词很短（2字以内），认为是宽泛领域
    if len(keyword_lower) <= 4:  # 2个汉字 = 4字节(UTF-8)
        return True
    
    # 如果包含具体实体（公司名、产品名、人名等），认为是具体新闻
    # 简单判断：包含数字、英文、特定标点等
    if any(c.isdigit() for c in keyword):
        return False
    if re.search(r'[a-zA-Z]', keyword):
        return False
    
    # 默认认为是宽泛领域
    return True


# ========== 事件深度解读播报提示词 ==========
DEEP_ANALYSIS_PROMPT = '''请基于以下新闻内容，撰写一篇专业、客观、深度解读文章，要求逻辑严谨、结构清晰，适合公众号 / 行业分析使用。
请精简冗余语句，强化逻辑链条，使全文更像专业深度评论。

写作结构严格按照以下 5 部分展开：

1. 事件核心梳理：用简洁语言概括新闻关键信息，不冗余。
2. 事件背景与前因：解释为什么会发生，相关政策、行业环境、历史脉络。
3. 多维度影响分析：对行业、市场、相关企业、普通用户 / 公众分别影响。
4. 利益博弈与各方态度：梳理不同主体的立场、动机与潜在冲突。
5. 趋势判断与启示：短期、中长期趋势，风险点，机会点，可落地启示。

语言风格：正式、中立、深度，避免情绪化表达，控制字数在 800–1200 字。

新闻内容如下：
{news_content}

补充背景：该新闻处于当前行业关注焦点，需结合宏观环境进行深度分析。
请加入数据化分析视角，用对比、比例、趋势描述影响，避免空泛。
请保持中立批判视角，既讲利好也讲风险，不吹捧不抹黑。
文风偏财经评论、智库报告风格。'''

# ========== 单人口播文案提示词 ==========
SINGLE_HOST_PROMPT = '''请基于以下新闻内容，撰写一篇单人口播新闻播报文案。

要求：
1. 风格：{style}
2. 开头要有问候语和栏目介绍
3. 每条新闻之间要有自然过渡
4. 要包含新闻来源和可信度说明
5. 结尾要有结束语
6. 语言口语化，适合朗读，避免长句
7. 控制总时长在 3-5 分钟

新闻内容：
{news_content}

请直接输出播报文案，不要添加任何说明。'''

# ========== 双人对话式播报文案提示词 ==========
DUAL_HOST_PROMPT = '''请基于以下新闻内容，撰写一篇双人对话式新闻播报文案。

角色设定：
- 主播（晓晓）：引导话题，提出问题，总结要点
- 评论员（云深）：解读新闻，分析细节，提供观点

要求：
1. 风格：{style}
2. 开头要有问候语和自我介绍
3. 采用对话形式，主播和评论员交替发言
4. 每条新闻的结构：主播引入 → 评论员速报 → 主播追问 → 评论员解读 → 要点总结
5. 要包含新闻来源和可信度说明
6. 结尾要有结束语
7. 语言口语化，自然流畅，像真实对话
8. 控制总时长在 4-6 分钟

输出格式：
主播：...
评论员：...
主播：...
评论员：...
（以此类推）

新闻内容：
{news_content}

请直接输出播报文案，不要添加任何说明。'''


def parse_config_from_text(text):
    """
    从用户输入文本中解析完整的播报配置信息
    
    支持的配置格式示例：
    - 示例1: 【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
    - 示例2: 【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，不需要深度解读】
    - 示例3: 【华为Mate80发布，风格是科技快评腔，形式是单人口播，用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
    - 示例4: 【华为Mate80发布，风格是科技快评腔，形式是单人口播，用温柔女生音色，不需要深度解读】
    - 示例5: 【华为Mate80发布，使用默认配置】
    - 示例6: 【华为Mate80发布，风格是科技快评腔，其他用默认配置】
    
    返回:
        - 如果解析成功且配置完整: 返回配置字典
        - 如果解析成功但配置不完整: 返回 None（需要交互式收集）
        - 如果没有检测到配置格式: 返回 None
    """
    # 检查是否包含方括号包裹的配置信息
    config_match = re.search(r'[【\[](.+?)[】\]]', text)
    if not config_match:
        return None
    
    config_text = config_match.group(1).strip()
    
    # 提取关键词（第一个逗号前的内容，或如果没有其他配置则是全部内容）
    # 先检查是否是"使用默认配置"模式
    if '使用默认配置' in config_text:
        keyword = config_text.split('，')[0].replace('使用默认配置', '').strip()
        if not keyword:
            return None
        return {
            'keyword': keyword,
            'style': '',  # 自动匹配
            'format': '单人口播',
            'voice': '年轻活力的女生',
            'output_dir': '',  # 使用默认
            'need_deep_analysis': False,
            'deep_analysis_style': '正式新闻腔',
            'deep_analysis_voice': '沉稳的中年男性',
            'is_complete_config': True,
            'use_defaults': True,
        }
    
    # 提取关键词（第一个逗号前的内容）
    parts = config_text.split('，')
    if len(parts) < 1:
        return None
    
    keyword = parts[0].strip()
    if not keyword:
        return None
    


def detect_language(text):
    """Detect input language (en/zh)"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    if english_chars > chinese_chars * 2:
        return 'en'
    return 'zh'


def map_english_style(style_en):
    """Map English style to Chinese"""
    return STYLE_MAP_EN.get(style_en.lower().strip(), style_en)


def map_english_format(format_en):
    """Map English format to Chinese"""
    return FORMAT_MAP_EN.get(format_en.lower().strip(), format_en)


def map_english_voice(voice_en):
    """Map English voice to Chinese"""
    return VOICE_MAP_EN.get(voice_en.lower().strip(), voice_en)
    # 检查是否是"其他用默认配置"模式
    use_partial_defaults = '其他用默认配置' in config_text or '其他使用默认' in config_text
    
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
    }
    
    # 解析风格（支持"风格是X"或"风格 X"格式）
    style_match = re.search(r'风格[是为]?([^，。]+)', config_text)
    if style_match:
        style_raw = style_match.group(1).strip()


# English Prompt Templates
DEEP_ANALYSIS_PROMPT_EN = """Based on the following news content, write a professional, objective, and in-depth analysis article.

Structure:
1. Event Core Summary
2. Background and Causes  
3. Multi-dimensional Impact Analysis
4. Stakeholder Game and Attitudes
5. Trend Judgment and Insights

News Content:
{news_content}

Output in English."""

SINGLE_HOST_PROMPT_EN = """Based on the following news content, write a single-host news broadcast script.

Requirements:
1. Style: {style}
2. Include greeting and program introduction
3. Natural transitions between news items
4. Include news sources
5. Include closing statement
6. Colloquial language, suitable for reading aloud
7. Duration: 3-5 minutes

News Content:
{news_content}

Output in English."""

DUAL_HOST_PROMPT_EN = """Based on the following news content, write a dual-host dialogue-style news broadcast script.

Characters:
- Host: Guides topic, asks questions, summarizes
- Commentator: Interprets news, analyzes details

Requirements:
1. Style: {style}
2. Greeting and self-introduction
3. Dialogue format with alternating speeches
4. Include news sources
5. Closing statement
6. Natural conversation style
7. Duration: 4-6 minutes

News Content:
{news_content}

Output in English."""


# ========== 事件深度解读播报提示词 ==========
DEEP_ANALYSIS_PROMPT = '''请基于以下新闻内容，撰写一篇专业、客观、深度解读文章，要求逻辑严谨、结构清晰，适合公众号 / 行业分析使用。
请精简冗余语句，强化逻辑链条，使全文更像专业深度评论。

写作结构严格按照以下 5 部分展开：

1. 事件核心梳理：用简洁语言概括新闻关键信息，不冗余。
2. 事件背景与前因：解释为什么会发生，相关政策、行业环境、历史脉络。
3. 多维度影响分析：对行业、市场、相关企业、普通用户 / 公众分别影响。
4. 利益博弈与各方态度：梳理不同主体的立场、动机与潜在冲突。
5. 趋势判断与启示：短期、中长期趋势，风险点，机会点，可落地启示。

语言风格：正式、中立、深度，避免情绪化表达，控制字数在 800–1200 字。

新闻内容如下：
{news_content}

补充背景：该新闻处于当前行业关注焦点，需结合宏观环境进行深度分析。
请加入数据化分析视角，用对比、比例、趋势描述影响，避免空泛。
请保持中立批判视角，既讲利好也讲风险，不吹捧不抹黑。
文风偏财经评论、智库报告风格。'''

# ========== 单人口播文案提示词 ==========
SINGLE_HOST_PROMPT = '''请基于以下新闻内容，撰写一篇单人口播新闻播报文案。

要求：
1. 风格：{style}
2. 开头要有问候语和栏目介绍
3. 每条新闻之间要有自然过渡
4. 要包含新闻来源和可信度说明
5. 结尾要有结束语
6. 语言口语化，适合朗读，避免长句
7. 控制总时长在 3-5 分钟

新闻内容：
{news_content}

请直接输出播报文案，不要添加任何说明。'''

# ========== 双人对话式播报文案提示词 ==========
DUAL_HOST_PROMPT = '''请基于以下新闻内容，撰写一篇双人对话式新闻播报文案。

角色设定：
- 主播（晓晓）：引导话题，提出问题，总结要点
- 评论员（云深）：解读新闻，分析细节，提供观点

要求：
1. 风格：{style}
2. 开头要有问候语和自我介绍
3. 采用对话形式，主播和评论员交替发言
4. 每条新闻的结构：主播引入 → 评论员速报 → 主播追问 → 评论员解读 → 要点总结
5. 要包含新闻来源和可信度说明
6. 结尾要有结束语
7. 语言口语化，自然流畅，像真实对话
8. 控制总时长在 4-6 分钟

输出格式：
主播：...
评论员：...
主播：...
评论员：...
（以此类推）

新闻内容：
{news_content}

请直接输出播报文案，不要添加任何说明。'''


# ========== 配置解析函数 ==========
def parse_config_from_text(text):
    """
    从用户输入文本中解析完整的播报配置信息
    
    支持中文和英文配置格式
    
    返回:
        - 如果解析成功且配置完整: 返回配置字典
        - 如果解析成功但配置不完整: 返回 None（需要交互式收集）
        - 如果没有检测到配置格式: 返回 None
    """
    # 检测输入语言
    lang = detect_language(text)
    
    # 检查是否包含方括号包裹的配置信息（支持【】和[]）
    config_match = re.search(r'\[([^\]]+)\]', text) or re.search(r'【([^】]+)】', text)
    if not config_match:
        return None
    
    config_text_raw = config_match.group(1).strip()
    
    # 根据语言选择分隔符
    if lang == 'en':
        parts = config_text_raw.split(',')
    else:
        parts = config_text_raw.split('，')
    
    if len(parts) < 1:
        return None
    
    keyword = parts[0].strip()
    if not keyword:
        return None
    
    config_text_lower = config_text_raw.lower()
    
    # 检查是否是"使用默认配置"模式
    use_defaults = ('使用默认配置' in config_text_raw or 
                   'use default config' in config_text_lower)
    
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
        style_match = re.search(r'style\s+is\s+([^,]+)', config_text_lower)
        if style_match:
            style_en = style_match.group(1).strip()
            config['style'] = map_english_style(style_en)
    else:
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
        format_match = re.search(r'format\s+is\s+([^,]+)', config_text_lower)
        if format_match:
            format_en = format_match.group(1).strip()
            config['format'] = map_english_format(format_en)
    else:
        if '单人口播' in config_text_raw:
            config['format'] = '单人口播'
        elif '双人对话' in config_text_raw or '双人' in config_text_raw:
            config['format'] = '双人对话式播报'
    
    # 解析音色
    if config['format'] == '双人对话式播报':
        if lang == 'en':
            host_match = re.search(r'host\s+voice\s+is\s+([^,]+)', config_text_lower)
            commentator_match = re.search(r'commentator\s+voice\s+is\s+([^,]+)', config_text_lower)
            
            host_voice = map_english_voice(host_match.group(1).strip()) if host_match else '沉稳的中年男性'
            commentator_voice = map_english_voice(commentator_match.group(1).strip()) if commentator_match else '年轻活力的女生'
            config['voice'] = f'主播:{host_voice},评论员:{commentator_voice}'
        else:
            host_match = re.search(r'主播[用是为\s]*([^，。]+?)(?:音色|声音)?[,，]', config_text_raw)
            if not host_match:
                host_match = re.search(r'主播[用是为\s]*([^，。评论员]+)', config_text_raw)
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
            
            commentator_match = re.search(r'评论员[用是为\s]*([^，。]+?)(?:音色|声音)?[,，]', config_text_raw)
            if not commentator_match:
                commentator_match = re.search(r'评论员[用是为\s]*([^，。]+)', config_text_raw)
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
        if lang == 'en':
            voice_match = re.search(r'voice\s+is\s+([^,]+)', config_text_lower)
            if voice_match:
                voice_en = voice_match.group(1).strip()
                config['voice'] = map_english_voice(voice_en)
        else:
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
                elif '专业' in config_text_raw or '主播' in config_text_raw or '播音' in config_text_raw:
                    config['voice'] = '专业新闻主播'
                elif '年轻' in config_text_raw or '活力' in config_text_raw:
                    config['voice'] = '年轻活力的女生'
                elif '情感' in config_text_raw or '戏剧' in config_text_raw or '活泼' in config_text_raw:
                    config['voice'] = '情感丰富的声音'
    
    # 解析深度解读
    has_explicit_deep_analysis = False
    if lang == 'en':
        if 'no deep analysis' in config_text_lower or 'without deep analysis' in config_text_lower:
            config['need_deep_analysis'] = False
            has_explicit_deep_analysis = True
        elif 'need deep analysis' in config_text_lower or 'with deep analysis' in config_text_lower:
            config['need_deep_analysis'] = True
            has_explicit_deep_analysis = True
            da_voice_match = re.search(r'deep analysis voice is ([^,]+)', config_text_lower)
            if da_voice_match:
                config['deep_analysis_voice'] = map_english_voice(da_voice_match.group(1).strip())
    else:
        if '不需要深度解读' in config_text_raw or '不生成深度解读' in config_text_raw:
            config['need_deep_analysis'] = False
            has_explicit_deep_analysis = True
        elif '需要深度解读' in config_text_raw or '生成深度解读' in config_text_raw:
            config['need_deep_analysis'] = True
            has_explicit_deep_analysis = True
            da_voice_match = re.search(r'深度解读音色是([^，。]+)', config_text_raw)
            if da_voice_match:
                config['deep_analysis_voice'] = da_voice_match.group(1).strip()
    
    if not has_explicit_deep_analysis:
        config['need_deep_analysis'] = not is_broad_keyword(keyword)
    
    # 解析输出目录
    if lang == 'en':
        output_dir_match = re.search(r'output dir is ([^,\]]+)', config_text_lower)
        if output_dir_match:
            config['output_dir'] = output_dir_match.group(1).strip()
    else:
        output_dir_match = re.search(r'输出目录是(.+?)(?=，|】|\])', config_text_raw)
        if output_dir_match:
            config['output_dir'] = output_dir_match.group(1).strip()
    
    # 判断配置是否完整
    if use_partial_defaults:
        config['is_complete_config'] = True
        config['use_defaults'] = True
        return config
    
    required_for_complete = ['style', 'format']
    is_complete = all(config.get(field) for field in required_for_complete)
    
    if config['format'] == '双人对话式播报':
        if '主播:' not in config['voice'] or '评论员:' not in config['voice']:
            is_complete = False
    else:
        if not config['voice']:
            is_complete = False
    
    if config['need_deep_analysis'] and not config.get('deep_analysis_voice'):
        config['deep_analysis_voice'] = '沉稳的中年男性'
    
    config['is_complete_config'] = is_complete
    return config if is_complete else None


def prompt_user_for_input():
    """交互式收集用户输入"""
    print()
    print('=' * 60)
    print('📰 Auto News Podcast v2.0 - 智能新闻播客')
    print('=' * 60)

    # 1. 关键词/领域
    print()
    print('📰 请输入你感兴趣的新闻关键词或领域：')
    print('  领域类：财经、科技、教育、医疗、体育、娱乐、房产、汽车')
    print('  主题类：AI 芯片、新能源汽车、中东局势、北京房价')
    print('  具体词：华为 Mate80、宝马 X5、伊朗声明')
    print('  💡 可以输入多个，用空格分隔')
    try:
        keyword = input('  > ').strip()
    except (EOFError, KeyboardInterrupt):
        keyword = ''

    if not keyword:
        print('[ERROR] 关键词不能为空')
        sys.exit(1)

    # 判断是否为具体新闻事件（非宽泛领域）
    is_specific_news = not is_broad_keyword(keyword)
    
    # 如果是具体新闻事件，询问是否生成深度解读
    need_deep_analysis = False
    deep_analysis_style = '正式新闻腔'
    deep_analysis_voice = '沉稳的中年男性'
    
    if is_specific_news:
        print()
        print('📊 检测到您输入的是具体新闻事件关键词。')
        print('  是否需要生成【事件深度解读播报】？')
        print('  1. ✅ 是 — 生成深度解读文章 + 单人播报音频')
        print('  2. ❌ 否 — 仅生成常规新闻播报')
        try:
            analysis_choice = input('  > ').strip()
        except (EOFError, KeyboardInterrupt):
            analysis_choice = ''
        
        if analysis_choice == '1':
            need_deep_analysis = True
            print()
            print('🎨 请选择深度解读播报风格（直接回车默认正式新闻腔）：')
            print('  1. 📻 正式新闻腔 — 标准播音，适合时政、财经、官方消息')
            print('  2. ☀️ 轻松早报腔 — 亲切自然，适合日常热点、生活资讯')
            print('  3. 💹 财经严肃腔 — 专业理性，适合股市、产业、数据')
            print('  4. 🚀 科技快评腔 — 简洁有力带点评，适合 AI、互联网、新产品')
            print('  💡 也可以直接输入你想要的风格描述，如"幽默风趣"、"严肃深度"等')
            try:
                da_style_choice = input('  > ').strip()
            except (EOFError, KeyboardInterrupt):
                da_style_choice = ''
            # 如果是数字，使用映射；否则直接使用输入的文本
            if da_style_choice in STYLES:
                deep_analysis_style = STYLES[da_style_choice]
            elif da_style_choice:
                deep_analysis_style = da_style_choice
            else:
                deep_analysis_style = '正式新闻腔'
            
            print()
            print('🎵 请选择深度解读播报音色（直接回车默认沉稳的中年男性）：')
            print('  1. 🌸 年轻活力的女生')
            print('  2. 💼 沉稳的中年男性（默认）')
            print('  3. 🎀 温柔的女生')
            print('  4. 📻 专业新闻主播')
            print('  5. 🎭 情感丰富的声音')
            print('  💡 也可以直接输入你想要的音色描述，如"成熟男声"、"甜美女生"等')
            try:
                da_voice_choice = input('  > ').strip()
            except (EOFError, KeyboardInterrupt):
                da_voice_choice = ''
            voice_map_short = {'1': '年轻活力的女生', '2': '沉稳的中年男性', '3': '温柔的女生',
                               '4': '专业新闻主播', '5': '情感丰富的声音'}
            # 如果是数字，使用映射；否则直接使用输入的文本
            if da_voice_choice in voice_map_short:
                deep_analysis_voice = voice_map_short[da_voice_choice]
            elif da_voice_choice:
                deep_analysis_voice = da_voice_choice
            else:
                deep_analysis_voice = '沉稳的中年男性'
    print()
    print('🎨 请选择播报文案风格（直接回车自动匹配）：')
    print('  1. 📻 正式新闻腔 — 标准播音，适合时政、财经、官方消息')
    print('  2. ☀️ 轻松早报腔 — 亲切自然，适合日常热点、生活资讯')
    print('  3. 💹 财经严肃腔 — 专业理性，适合股市、产业、数据')
    print('  4. 🚀 科技快评腔 — 简洁有力带点评，适合 AI、互联网、新产品')
    print('  💡 也可以直接输入你想要的风格描述，如"幽默风趣"、"严肃深度"等')
    try:
        style_choice = input('  > ').strip()
    except (EOFError, KeyboardInterrupt):
        style_choice = ''

    # 如果是数字，使用映射；否则直接使用输入的文本
    if style_choice in STYLES:
        style = STYLES[style_choice]
    elif style_choice:
        style = style_choice
    else:
        style = ''  # 空字符串表示自动匹配

    # 3. 播报形式
    print()
    print('🎙️ 请选择播报形式（直接回车默认单人口播）：')
    print('  1. 🎤 单人口播')
    print('  2. 🗣️ 双人对话式播报')
    try:
        format_choice = input('  > ').strip()
    except (EOFError, KeyboardInterrupt):
        format_choice = ''

    broadcast_format = FORMATS.get(format_choice, '单人口播')

    # 4. 音色选择
    print()
    voice_map_short = {'1': '年轻活力的女生', '2': '沉稳的中年男性', '3': '温柔的女生',
                       '4': '专业新闻主播', '5': '情感丰富的声音'}
    
    if broadcast_format == '双人对话式播报':
        print('🎵 双人对话播报需要为主播和评论员分别选择音色：')
        print()
        print('  【主播音色】（直接回车默认沉稳的中年男性）：')
        print('    1. 🌸 年轻活力的女生')
        print('    2. 💼 沉稳的中年男性（默认）')
        print('    3. 🎀 温柔的女生')
        print('    4. 📻 专业新闻主播')
        print('    5. 🎭 情感丰富的声音')
        print('    💡 也可以直接输入你想要的音色描述，如"成熟男声"、"甜美女生"等')
        try:
            host_voice_choice = input('    > ').strip()
        except (EOFError, KeyboardInterrupt):
            host_voice_choice = ''
        
        print()
        print('  【评论员音色】（直接回车默认年轻活力的女生）：')
        print('    1. 🌸 年轻活力的女生（默认）')
        print('    2. 💼 沉稳的中年男性')
        print('    3. 🎀 温柔的女生')
        print('    4. 📻 专业新闻主播')
        print('    5. 🎭 情感丰富的声音')
        print('    💡 也可以直接输入你想要的音色描述，如"成熟男声"、"甜美女生"等')
        try:
            commentator_voice_choice = input('    > ').strip()
        except (EOFError, KeyboardInterrupt):
            commentator_voice_choice = ''
        
        voice_map_short = {'1': '年轻活力的女生', '2': '沉稳的中年男性', '3': '温柔的女生',
                           '4': '专业新闻主播', '5': '情感丰富的声音'}
        
        # 如果是数字，使用映射；否则直接使用输入的文本
        if host_voice_choice in voice_map_short:
            host_voice = voice_map_short[host_voice_choice]
        elif host_voice_choice:
            host_voice = host_voice_choice
        else:
            host_voice = '沉稳的中年男性'
            
        if commentator_voice_choice in voice_map_short:
            commentator_voice = voice_map_short[commentator_voice_choice]
        elif commentator_voice_choice:
            commentator_voice = commentator_voice_choice
        else:
            commentator_voice = '年轻活力的女生'
            
        voice = f'主播:{host_voice},评论员:{commentator_voice}'
    else:
        print('🎵 请选择播报音色（直接回车默认年轻活力的女生）：')
        print('  1. 🌸 年轻活力的女生')
        print('  2. 💼 沉稳的中年男性')
        print('  3. 🎀 温柔的女生')
        print('  4. 📻 专业新闻主播')
        print('  5. 🎭 情感丰富的声音')
        print('  💡 也可以直接输入你想要的音色描述，如"成熟男声"、"甜美女生"等')
        try:
            voice_choice = input('  > ').strip()
        except (EOFError, KeyboardInterrupt):
            voice_choice = ''
            
        voice_map_short = {'1': '年轻活力的女生', '2': '沉稳的中年男性', '3': '温柔的女生',
                           '4': '专业新闻主播', '5': '情感丰富的声音'}
        
        # 如果是数字，使用映射；否则直接使用输入的文本
        if voice_choice in voice_map_short:
            voice = voice_map_short[voice_choice]
        elif voice_choice:
            voice = voice_choice
        else:
            voice = '年轻活力的女生'

    # 5. 输出目录
    print()
    print('📁 输出目录（直接回车默认 workspace/news/）：')
    try:
        output_dir = input('  > ').strip()
    except (EOFError, KeyboardInterrupt):
        output_dir = ''

    if not output_dir:
        workspace = os.path.expanduser('~/.openclaw/workspace')
        base_dir = os.path.join(workspace, 'news')
        # 用时间戳 + 关键词创建子目录
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        keyword_safe = re.sub(r'[\\/:*?"<>|]', '', keyword)[:30]
        output_dir = os.path.join(base_dir, f'{timestamp_str}_{keyword_safe}')
        os.makedirs(output_dir, exist_ok=True)
        print(f'[OK] 输出目录: {output_dir}')

    return {
        'keyword': keyword,
        'style': style,
        'format': broadcast_format,
        'voice': voice,
        'output_dir': output_dir,
        'need_deep_analysis': need_deep_analysis,
        'deep_analysis_style': deep_analysis_style,
        'deep_analysis_voice': deep_analysis_voice,
    }


def map_voice(voice_desc):
    """将音色描述映射到 edge-tts 声音 ID"""
    if not voice_desc:
        return 'zh-CN-XiaoxiaoNeural', '年轻活力的女生（默认）'

    desc_lower = voice_desc.lower()
    for keyword, voice_id in VOICE_MAP.items():
        if keyword in desc_lower:
            return voice_id, VOICE_LABELS.get(voice_id, voice_id)

    return 'zh-CN-XiaoxiaoNeural', '年轻活力的女生（默认）'


def auto_detect_style(keyword, news_items):
    """根据关键词和新闻内容自动匹配播报风格"""
    text = keyword + ' ' + ' '.join(item.get('title', '') for item in news_items[:5])

    for style_name, keywords in STYLE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                return style_name

    return '轻松早报腔'  # 默认


def fetch_news_tavily(keyword, limit=10):
    """使用 Tavily Search 搜索新闻"""
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        print('  [WARN] TAVILY_API_KEY 未设置，跳过 Tavily 搜索')
        return []
    
    try:
        url = 'https://api.tavily.com/search'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'query': keyword,
            'max_results': limit,
            'include_answer': True,
            'search_depth': 'advanced'
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        items = []
        for r in result.get('results', []):
            # 获取 source，如果为空则尝试从 URL 提取
            source = r.get('source', '')
            if not source:
                # 从 URL 提取域名作为来源
                url = r.get('url', '')
                if url:
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    domain = parsed.netloc
                    # 移除 www. 前缀
                    if domain.startswith('www.'):
                        domain = domain[4:]
                    source = domain
                else:
                    source = '未知来源'
            
            item = {
                'title': r.get('title', ''),
                'content': r.get('content', ''),
                'url': r.get('url', ''),
                'source': source,
                'time': '',
                'credibility': get_credibility_for_source(source),
                'source_type': get_source_type_for_source(source),
                'tags': generate_tags_from_title(r.get('title', ''), r.get('content', '')),
            }
            items.append(item)
        
        print(f'  [OK] Tavily 搜索找到 {len(items)} 条新闻')
        return items
    except Exception as e:
        print(f'  [WARN] Tavily 搜索失败: {e}')
        return []


def generate_tags_from_title(title, content=''):
    """根据标题和正文生成标签
    
    标签体系：
    - 【权威】权威媒体发布
    - 【突发】突发事件
    - 【数据】数据/统计/财报类
    - 【体育】体育新闻
    - 【新品】新品发布
    - 【文化】文物/艺术/历史/文化
    - 【政治】政治/外交/政策
    - 【经济】经济/金融/商业
    - 【科技】科技/AI/互联网/芯片
    - 【社会】社会/民生/教育/医疗
    - 【国际】国际/外交/跨国
    - 【资讯】其他类型（默认）
    """
    text = (title + ' ' + content).lower()
    tags = []
    
    # 判断可信度标签
    if any(w in text for w in ['新华社', '央视', 'cctv', '人民网', '人民日报', 'reuters', 'ap', 'bloomberg', 'bbc']):
        tags.append('【权威】')
    
    # 判断事件类型标签（按优先级排序）
    
    # 1. 突发事件（最高优先级）
    if any(w in text for w in ['突发', '刚刚', '紧急', '地震', '事故', '爆炸', '火灾', '坍塌', '袭击']):
        tags.append('【突发】')
    
    # 2. 文化类（文物、艺术、历史）
    elif any(w in text for w in ['文物', '归还', '博物馆', '展览', '考古', '遗址', '遗产', '圆明园', '拍卖', '艺术品', '古董']):
        tags.append('【文化】')
    
    # 3. 体育类
    elif any(w in text for w in ['冠军', '夺冠', '胜利', '击败', '比赛', '决赛', '世界杯', '奥运会', '联赛', '球员', '球队']):
        tags.append('【体育】')
    
    # 4. 科技类
    elif any(w in text for w in ['ai', '人工智能', '芯片', '科技', '互联网', '发布', '新品', '上市', '推出', '华为', '苹果', '谷歌', '算法', '模型']):
        tags.append('【科技】')
    
    # 5. 经济/财经类
    elif any(w in text for w in ['数据', '统计', '报告', '财报', 'gdp', 'cpi', '股市', '股价', '上涨', '下跌', '涨停', '跌停', '经济', '金融', '银行', '投资']):
        tags.append('【经济】')
    
    # 6. 政治/外交类
    elif any(w in text for w in ['法案', '通过', '议会', '国会', '总统', '总理', '外交', '制裁', '协议', '谈判', '签署', '政策', '政府']):
        tags.append('【政治】')
    
    # 7. 国际类
    elif any(w in text for w in ['国际', '跨国', '美国', '中国', '法国', '日本', '德国', '英国', '俄罗斯', '北约', '联合国', '欧盟']):
        tags.append('【国际】')
    
    # 8. 社会民生类
    elif any(w in text for w in ['教育', '医疗', '就业', '住房', '养老', '社保', '民生', '社会', '犯罪', '法律']):
        tags.append('【社会】')
    
    return tags if tags else ['【资讯】']


def fetch_news_via_web_search(keyword, limit=10):
    """使用 Tavily API 直接搜索新闻（作为 Tavily Search 的备选/重试机制）
    
    当主 Tavily 搜索失败时，使用相同的 API Key 直接调用 Tavily API。
    这实际上是 Tavily 搜索的重试机制，使用相同的 API 但可能有不同的网络路径。
    """
    try:
        print(f'  尝试使用 Tavily API (备选) 搜索: {keyword}...')
        
        # 构造搜索查询（添加新闻相关关键词以优化结果）
        search_query = f'{keyword} 新闻'
        
        # 获取 Tavily API Key
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            print('  [WARN] TAVILY_API_KEY 未设置，跳过 Tavily 备选搜索')
            return []
        
        # 直接调用 Tavily API（与 fetch_news_tavily 相同，但可能有不同的网络路径）
        url = 'https://api.tavily.com/search'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'query': search_query,
            'max_results': limit,
            'include_answer': True,
            'search_depth': 'basic'  # 使用 basic 模式可能更快
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        items = []
        for r in result.get('results', []):
            # 获取 source
            source = r.get('source', '')
            if not source:
                url = r.get('url', '')
                if url:
                    source = _extract_domain(url)
                else:
                    source = '未知来源'
            
            item = {
                'title': r.get('title', ''),
                'content': r.get('content', ''),
                'url': r.get('url', ''),
                'source': source,
                'time': '',
                'credibility': get_credibility_for_source(source),
                'source_type': get_source_type_for_source(source),
                'tags': generate_tags_from_title(r.get('title', ''), r.get('content', '')),
            }
            items.append(item)
        
        print(f'  [OK] Tavily API (备选) 搜索找到 {len(items)} 条新闻')
        return items
    except Exception as e:
        print(f'  [WARN] Tavily API (备选) 搜索失败: {e}')
        return []


def fetch_news_via_baidu_search(keyword, limit=10):
    """使用 Baidu Search 技能搜索新闻（作为 Tavily 的备选）
    
    通过调用 Baidu AI Search API 获取新闻搜索结果。
    需要配置 BAIDU_API_KEY 环境变量。
    """
    try:
        print(f'  尝试使用 Baidu Search 搜索: {keyword}...')
        
        # 获取 Baidu API Key
        api_key = os.getenv('BAIDU_API_KEY')
        if not api_key:
            print('  [WARN] BAIDU_API_KEY 未设置，跳过 Baidu 搜索')
            return []
        
        # 构造搜索查询
        search_query = f'{keyword} 新闻'
        
        # 调用 Baidu AI Search API
        url = 'https://qianfan.baidubce.com/v2/ai_search/web_search'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'X-Appbuilder-From': 'openclaw',
            'Content-Type': 'application/json'
        }
        
        # 计算日期范围（最近7天）
        from datetime import datetime, timedelta
        end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        request_body = {
            'messages': [
                {
                    'content': search_query,
                    'role': 'user'
                }
            ],
            'search_source': 'baidu_search_v2',
            'resource_type_filter': [{'type': 'web', 'top_k': limit}],
            'search_filter': {
                'range': {
                    'page_time': {
                        'gte': start_date,
                        'lt': end_date
                    }
                }
            }
        }
        
        response = requests.post(url, json=request_body, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        # 检查是否有错误
        if 'code' in result:
            print(f'  [WARN] Baidu API 返回错误: {result.get("message", "未知错误")}')
            return []
        
        # 解析结果
        references = result.get('references', [])
        items = []
        
        for r in references[:limit]:
            title = r.get('title', '')
            content = r.get('content', '')
            url = r.get('url', '')
            source = _extract_domain(url) if url else '未知来源'
            
            item = {
                'title': title,
                'content': content,
                'url': url,
                'source': source,
                'time': r.get('page_time', ''),
                'credibility': get_credibility_for_source(source),
                'source_type': get_source_type_for_source(source),
                'tags': generate_tags_from_title(title, content),
            }
            items.append(item)
        
        print(f'  [OK] Baidu Search 搜索找到 {len(items)} 条新闻')
        return items
    except Exception as e:
        print(f'  [WARN] Baidu Search 搜索失败: {e}')
        return []


def _extract_domain(url):
    """从 URL 中提取域名"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return '未知来源'


def fetch_news_multi_source(keyword, limit=15):
    """多源新闻搜索 + 去重 + 可信度标注
    
    搜索优先级：
    1. Tavily Search（优先，高级模式）
    2. Baidu Search（备选，国内搜索）
    3. Tavily API（备选2，基础模式重试）
    4. news-aggregator-skill（备选3）
    """
    all_items = []
    
    print('  [INFO] 开始多源新闻搜索...')
    
    # 策略 1：优先使用 Tavily Search
    print('  尝试策略1: Tavily Search...')
    tavily_items = fetch_news_tavily(keyword, limit)
    if tavily_items:
        all_items.extend(tavily_items)
        print(f'  [OK] Tavily 搜索成功，获取 {len(tavily_items)} 条新闻')
    
    # 如果 Tavily 结果不足，尝试备选方案
    if len(all_items) < 3:
        print('  Tavily 结果不足，尝试备选方案...')
        
        # 策略 2：使用 Baidu Search（国内搜索，适合中文新闻）
        print('  尝试策略2: Baidu Search...')
        baidu_items = fetch_news_via_baidu_search(keyword, limit)
        if baidu_items:
            all_items.extend(baidu_items)
            print(f'  [OK] Baidu Search 获取 {len(baidu_items)} 条新闻')
        
        # 策略 3：使用 Tavily API 备选（基础模式重试）
        if len(all_items) < 3:
            print('  尝试策略3: Tavily API (备选/基础模式)...')
            web_items = fetch_news_via_web_search(keyword, limit)
            if web_items:
                all_items.extend(web_items)
                print(f'  [OK] Tavily API (备选) 获取 {len(web_items)} 条新闻')
        
        # 策略 4：尝试 news-aggregator-skill
        if len(all_items) < 3:
            print('  尝试策略4: news-aggregator-skill...')
            try:
                from news_aggregator import fetch_via_aggregator
                aggregator_items = fetch_via_aggregator(keyword, limit)
                for item in aggregator_items:
                    item['credibility'] = get_credibility_for_source(item.get('source', ''))
                    item['source_type'] = get_source_type_for_source(item.get('source', ''))
                    item['tags'] = generate_tags(item)
                    all_items.append(item)
                print(f'  [OK] news-aggregator 获取 {len(aggregator_items)} 条新闻')
            except Exception as e:
                print(f'  [WARN] news-aggregator 失败: {e}')

    # 去重
    all_items = deduplicate_news(all_items)

    # 按时间倒序排序（最新的在前）
    all_items.sort(key=lambda x: -parse_time_to_timestamp(x.get('time', '')))

    return all_items[:limit]


def get_credibility_for_source(source):
    """根据来源判断可信度
    
    可信度等级：
    - 高：官方权威媒体、国际知名媒体
    - 中：主流商业媒体、知名垂直媒体、官方机构网站
    - 低：自媒体、社交媒体、内容聚合平台、未知来源
    """
    source_lower = (source or '').lower()
    
    # 高可信度：官方权威媒体
    high_cred_sources = [
        '新华社', '央视', 'cctv', '人民网', '人民日报', '光明日报', '经济日报', '中国日报',
        'reuters', 'ap', 'bloomberg', 'bbc', 'cnn', 'nytimes', 'wsj', 'ft.com',
        '法新社', 'afp', '共同社', 'kyodo', '俄新社', 'tass',
        'gov.cn', '政府', '外交部', '国防部', '联合国', 'un.org',
        '新华社', 'xinhua', 'chinadaily', 'cctv.com', 'people.com.cn'
    ]
    
    # 中可信度：主流商业媒体、知名垂直媒体
    medium_cred_sources = [
        '腾讯', 'qq.com', '新浪', 'sina', '网易', '163.com', '搜狐', 'sohu',
        '凤凰', 'ifeng', '财新', 'caixin', '第一财经', 'cbn',
        '36kr', '虎嗅', 'huxiu', '华尔街', 'wallstreet', 'ftchinese',
        '知乎', 'zhihu', '豆瓣', 'douban', 'bilibili', 'github',
        '汽车之家', 'autohome', '36氪', '品玩', 'pingwest',
        '澎湃新闻', 'thepaper', '界面', 'jiemian', '新京报', 'bjnews',
        '联合早报', 'zaobao', '星洲日报', '明报', '南华早报', 'scmp'
    ]
    
    if any(w in source_lower for w in high_cred_sources):
        return '高'
    elif any(w in source_lower for w in medium_cred_sources):
        return '中'
    else:
        return '低'


def get_source_type_for_source(source):
    """根据来源判断类型
    
    来源类型：
    - 权威媒体：官方媒体、国际知名媒体
    - 主流门户：大型商业门户网站
    - 垂直门户：行业专业媒体
    - 社交媒体：社交平台、论坛
    - 自媒体：个人/机构自媒体账号
    - 其他：无法分类的来源
    """
    source_lower = (source or '').lower()
    
    # 权威媒体
    if any(w in source_lower for w in [
        '新华社', '央视', 'cctv', '人民网', '人民日报', '光明日报', '经济日报',
        'reuters', 'ap', 'bloomberg', 'bbc', 'cnn', 'nytimes', 'wsj', 'ft.com',
        '法新社', 'afp', '共同社', 'kyodo', '俄新社', 'tass',
        'gov.cn', '政府', '外交部', '国防部', '联合国'
    ]):
        return '权威媒体'
    
    # 主流门户
    elif any(w in source_lower for w in [
        '腾讯', 'qq.com', '新浪', 'sina', '网易', '163.com', '搜狐', 'sohu',
        '凤凰', 'ifeng', 'msn', 'yahoo'
    ]):
        return '主流门户'
    
    # 垂直门户
    elif any(w in source_lower for w in [
        '36kr', '虎嗅', 'huxiu', '华尔街', 'wallstreet', 'ftchinese',
        '财新', 'caixin', '第一财经', 'cbn', '澎湃', 'thepaper',
        '界面', 'jiemian', '新京报', 'bjnews', '知乎', 'zhihu',
        '汽车之家', 'autohome', '懂车帝', 'dongchedi',
        '联合早报', 'zaobao', '星洲日报', '明报', '南华早报', 'scmp'
    ]):
        return '垂直门户'
    
    # 社交媒体
    elif any(w in source_lower for w in [
        'weibo', '微博', 'twitter', 'x.com', 'facebook', 'v2ex',
        'reddit', 'quora', '豆瓣', 'douban', '小红书', 'xiaohongshu'
    ]):
        return '社交媒体'
    
    # 自媒体/视频平台
    elif any(w in source_lower for w in [
        'youtube', 'youtu.be', 'bilibili', 'b23.tv', '抖音', 'douyin',
        '快手', 'kuaishou', '公众号', '今日头条', 'toutiao'
    ]):
        return '自媒体'
    
    else:
        return '其他'


def generate_tags(item):
    """生成新闻标签 - 供 news-aggregator 使用
    
    复用 generate_tags_from_title 的逻辑
    """
    return generate_tags_from_title(item.get('title', ''), item.get('content', ''))


def generate_deep_analysis(news_items, keyword, language='zh'):
    """生成事件深度解读播报文案 - 调用大模型API
    
    Args:
        news_items: 新闻列表
        keyword: 关键词
        language: 输出语言，'zh' 或 'en'
    """
    # 合并新闻内容
    news_content_parts = []
    for i, item in enumerate(news_items[:5], 1):
        title = item.get('title', '')
        content = item.get('content', '')
        source = item.get('source', '未知来源')
        time_str = item.get('time', '')
        
        news_content_parts.append(f'【新闻{i}】')
        news_content_parts.append(f'标题：{title}')
        news_content_parts.append(f'来源：{source}')
        if time_str:
            news_content_parts.append(f'时间：{time_str}')
        news_content_parts.append(f'内容：{content}')
        news_content_parts.append('')
    
    news_content = '\n'.join(news_content_parts)
    
    # 根据语言选择提示词
    if language == 'en':
        prompt = DEEP_ANALYSIS_PROMPT_EN.format(news_content=news_content)
        system_message = 'You are a professional financial analyst, skilled at writing in-depth analysis articles.'
    else:
        prompt = DEEP_ANALYSIS_PROMPT.format(news_content=news_content)
        system_message = '你是一位专业的财经评论分析师，擅长撰写深度解读文章。'
    
    print(f'  正在调用大模型生成深度解读文案 ({language})...')
    
    # 使用统一的 LLM API 调用函数
    analysis_text = call_llm_api(prompt, system_message)
    
    if analysis_text:
        print(f'  [OK] 大模型生成完成，共 {len(analysis_text)} 字符')
        return analysis_text
    
    # 回退：使用模板生成
    print('  回退到模板生成...')
    return _generate_deep_analysis_fallback(news_items, keyword, language)


def _generate_deep_analysis_fallback(news_items, keyword):
    """深度解读文案生成（模板回退方案）"""
    analysis_lines = [
        f'# 📊 {keyword} 事件深度解读',
        '',
        '## 一、事件核心梳理',
        '',
    ]
    
    # 核心梳理：综合所有新闻标题
    core_titles = [item.get('title', '') for item in news_items[:3]]
    analysis_lines.append(f'近期，{"；".join(core_titles)}。这一事件引发了广泛关注。')
    analysis_lines.append('')
    
    # 背景与前因
    analysis_lines.append('## 二、事件背景与前因')
    analysis_lines.append('')
    sources = list(set(item.get('source', '') for item in news_items[:5] if item.get('source')))
    if sources:
        analysis_lines.append(f'据{"、".join(sources[:3])}等多家媒体报道，')
    analysis_lines.append('该事件的发生与当前行业环境密切相关。从政策层面看，相关领域正处于调整期；')
    analysis_lines.append('从市场层面看，各方力量正在重新博弈。')
    analysis_lines.append('')
    
    # 多维度影响分析
    analysis_lines.append('## 三、多维度影响分析')
    analysis_lines.append('')
    analysis_lines.append('**对行业的影响**：该事件将对相关行业产生深远影响，可能改变行业竞争格局。')
    analysis_lines.append('')
    analysis_lines.append('**对市场的影响**：短期内可能引发市场波动，中长期看有利于行业健康发展。')
    analysis_lines.append('')
    analysis_lines.append('**对相关企业的影响**：涉及企业需要调整战略，应对新的挑战和机遇。')
    analysis_lines.append('')
    analysis_lines.append('**对普通用户/公众的影响**：最终可能传导至终端，影响用户的选择和体验。')
    analysis_lines.append('')
    
    # 利益博弈与各方态度
    analysis_lines.append('## 四、利益博弈与各方态度')
    analysis_lines.append('')
    analysis_lines.append('从各方反应来看，不同主体的立场存在差异：')
    analysis_lines.append('- **监管部门**：关注合规性和市场秩序，倾向于规范引导')
    analysis_lines.append('- **行业企业**：希望在竞争中获得优势，同时呼吁公平竞争环境')
    analysis_lines.append('- **消费者群体**：更关注实际利益和服务体验')
    analysis_lines.append('')
    
    # 趋势判断与启示
    analysis_lines.append('## 五、趋势判断与启示')
    analysis_lines.append('')
    analysis_lines.append('**短期趋势**：事件将持续发酵，各方反应将进一步明朗。')
    analysis_lines.append('')
    analysis_lines.append('**中长期趋势**：行业将加速洗牌，头部效应可能加剧。')
    analysis_lines.append('')
    analysis_lines.append('**风险点**：政策变化、市场波动、竞争加剧等不确定性因素。')
    analysis_lines.append('')
    analysis_lines.append('**机会点**：对于能够适应变化、把握趋势的企业和个人，存在弯道超车的机会。')
    analysis_lines.append('')
    analysis_lines.append('**可落地启示**：建议相关方密切关注事态发展，及时调整策略，做好风险预案。')
    analysis_lines.append('')
    
    analysis_text = '\n'.join(analysis_lines)
    print(f'  模板生成完成，共 {len(analysis_text)} 字符')
    
    return analysis_text


def call_llm_api(prompt, system_message='你是一位专业的新闻播报撰稿人，擅长撰写口语化、适合朗读的新闻文案。'):
    """调用大模型 API 生成内容
    
    使用 OpenClaw 默认模型配置，自动识别模型提供商并调用。
    配置从 openclaw.json 动态读取，支持任意模型提供商。
    """
    result = _call_model_api_direct(prompt, system_message)
    if result:
        return result
    
    return None


def _call_model_api_direct(prompt, system_message):
    """调用大模型 API
    
    使用 OpenClaw 默认模型配置，自动识别提供商并调用。
    支持 DashScope、Kimi、Ollama 等任意配置好的提供商。
    """
    try:
        import requests
        
        # 获取 OpenClaw 默认模型配置
        model_config = _get_default_model_config()
        
        if not model_config:
            print('  [WARN] 未找到模型配置')
            return None
        
        api_key = model_config.get('api_key')
        api_base = model_config.get('base_url')
        model = model_config.get('model')
        provider = model_config.get('provider')
        
        if not api_key:
            print(f'  [WARN] 未找到 {provider} 的 API Key')
            return None
        
        if not api_base:
            print(f'  [WARN] 未找到 {provider} 的 API Base URL')
            return None
        
        print(f'  [INFO] 使用模型: {provider}/{model}')
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        data = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 3000,
            'stream': False
        }
        
        response = requests.post(
            f'{api_base}/chat/completions',
            headers=headers,
            json=data,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f'  [OK] 通过 {model} 生成成功')
            return content
        else:
            print(f'  [WARN] API 调用失败: {response.status_code} - {response.text[:200]}')
            return None
            
    except Exception as e:
        print(f'  [WARN] API 调用异常: {e}')
        return None


def deduplicate_news(items, threshold=0.7):
    """基于标题相似度去重"""
    if not items:
        return []

    unique = []
    seen_hashes = set()

    for item in items:
        title = item.get('title', '')
        # 生成标题的简化的 hash（去除标点、转小写）
        title_norm = re.sub(r'[^\w\u4e00-\u9fff]', '', title).lower()
        title_hash = hashlib.md5(title_norm.encode('utf-8')).hexdigest()[:12]

        # 检查是否重复
        is_dup = False
        for seen_hash in seen_hashes:
            if title_hash == seen_hash:
                is_dup = True
                break

        if not is_dup:
            # 进一步检查语义相似度
            for existing in unique:
                existing_title = re.sub(r'[^\w\u4e00-\u9fff]', '', existing.get('title', '')).lower()
                ratio = SequenceMatcher(None, title_norm, existing_title).ratio()
                if ratio > threshold:
                    # 保留可信度更高的
                    cred_order = {'高': 0, '中': 1, '低': 2}
                    if cred_order.get(item.get('credibility', '低'), 2) < cred_order.get(existing.get('credibility', '低'), 2):
                        unique.remove(existing)
                        unique.append(item)
                    is_dup = True
                    break

        if not is_dup:
            seen_hashes.add(title_hash)
            unique.append(item)

    return unique


def parse_time_to_timestamp(time_str):
    """解析时间字符串为时间戳（用于排序）"""
    if not time_str:
        return 0

    try:
        # 尝试多种格式
        for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%d', '%m/%d/%Y', '%d %b %Y']:
            try:
                dt = datetime.strptime(str(time_str).strip(), fmt)
                return dt.timestamp()
            except ValueError:
                continue
    except Exception:
        pass

    # 包含"Today"或"今天"的视为最新
    if any(w in str(time_str).lower() for w in ['today', '今天', 'real-time']):
        return datetime.now().timestamp()

    return 0


def generate_three_level_summary(news_content):
    """生成三级摘要"""
    # 这里由 LLM 生成，脚本提供模板
    # 实际使用时需要调用 LLM API

    summary = {
        'quick_20s': '',
        'detail_60s': '',
        'checklist': [],
    }

    # 简单提取（LLM 未可用时的降级方案）
    title = news_content.get('title', '')
    content = news_content.get('content', '')[:500]
    source = news_content.get('source', '')

    # 20 秒速报：80-100字，不得少于80字
    quick_text = f'{title}。据{source}报道，{content[:200]}'
    if len(quick_text) < 80:
        # 如果内容不足80字，补充内容详情
        quick_text = f'{title}。据{source}报道，{content[:300]}'
    summary['quick_20s'] = quick_text[:100] if len(quick_text) > 100 else quick_text
    
    # 60 秒解读：200-300字，不得少于200字
    detail_text = f'今天关注一条新闻：{title}。据{source}报道，{content[:600]}'
    if len(detail_text) < 200:
        # 如果内容不足200字，尝试补充更多内容
        detail_text = f'今天关注一条新闻：{title}。据{source}报道，{content[:800]}'
    summary['detail_60s'] = detail_text[:300] if len(detail_text) > 300 else detail_text

    # 要点清单
    summary['checklist'] = [
        f'事件：{title}',
        f'来源：{source}',
        f'时间：{news_content.get("time", "未知")}',
    ]

    return summary


def generate_broadcast_script(news_items, style, broadcast_format, keyword, language='zh'):
    """生成播报文案
    
    Args:
        news_items: 新闻列表
        style: 播报风格
        broadcast_format: 播报形式（单人口播/双人对话式播报）
        keyword: 关键词
        language: 输出语言，'zh' 或 'en'
    """

    # 自动检测风格
    if not style:
        style = auto_detect_style(keyword, news_items)

    # 生成三级摘要
    summaries = []
    for item in news_items:
        summary = generate_three_level_summary(item)
        item['summary'] = summary
        summaries.append(summary)

    # 根据风格生成文案
    if broadcast_format == '双人对话式播报':
        script = generate_dual_host_script(news_items, style, keyword, language)
    else:
        script = generate_single_host_script(news_items, style, keyword, language)

    return script


def generate_single_host_script(news_items, style, keyword, language='zh'):
    """单人口播文案 - 调用大模型API生成
    
    Args:
        news_items: 新闻列表
        style: 播报风格
        keyword: 关键词
        language: 输出语言，'zh' 或 'en'
    """
    
    # 构建新闻内容
    news_content_parts = []
    for i, item in enumerate(news_items[:5], 1):
        title = item.get('title', '')
        content = item.get('content', '')
        source = item.get('source', '未知来源')
        time_str = item.get('time', '')
        credibility = item.get('credibility', '中')
        tags = ''.join(item.get('tags', ['【资讯】']))
        
        news_content_parts.append(f'【新闻{i}】')
        news_content_parts.append(f'标题：{title}')
        news_content_parts.append(f'来源：{source}')
        news_content_parts.append(f'可信度：{credibility}')
        news_content_parts.append(f'标签：{tags}')
        if time_str:
            news_content_parts.append(f'时间：{time_str}')
        news_content_parts.append(f'内容：{content}')
        news_content_parts.append('')
    
    news_content = '\n'.join(news_content_parts)
    
    # 根据语言选择提示词
    if language == 'en':
        prompt = SINGLE_HOST_PROMPT_EN.format(style=style, news_content=news_content)
        system_message = 'You are a professional news anchor, skilled at writing colloquial news broadcast scripts suitable for reading aloud.'
    else:
        prompt = SINGLE_HOST_PROMPT.format(style=style, news_content=news_content)
        system_message = '你是一位专业的新闻主播，擅长撰写口语化、适合朗读的新闻播报文案。'
    
    print(f'  正在调用大模型生成单人口播文案（风格：{style}，语言：{language}）...')
    
    # 调用大模型API
    script = call_llm_api(prompt, system_message)
    
    if script:
        print(f'  [OK] 大模型生成完成，共 {len(script)} 字符')
        return script
    else:
        print('  [WARN] 大模型调用失败，回退到模板生成...')
        return _generate_single_host_script_fallback(news_items, style, keyword, language)


def _generate_single_host_script_fallback(news_items, style, keyword):
    """单人口播文案模板回退方案"""
    
    openings = {
        '正式新闻腔': '各位听众朋友大家好，欢迎收听新闻播报。',
        '轻松早报腔': '早上好！欢迎收听今天的轻松新闻早报。',
        '财经严肃腔': '各位投资者大家好，欢迎收听今日财经观察。',
        '科技快评腔': '大家好，欢迎来到科技快评时间。',
    }

    transitions = {
        '正式新闻腔': ['接下来关注', '再来看一条消息', '另一方面'],
        '轻松早报腔': ['再来聊聊', '还有一条有意思的', '另外值得关注的是'],
        '财经严肃腔': ['市场方面', '从行业来看', '数据层面'],
        '科技快评腔': ['再来看', '还有一条值得关注的', '点评一下'],
    }

    closings = {
        '正式新闻腔': '以上就是本次播报的全部内容，感谢您的收听。',
        '轻松早报腔': '以上就是今天的新闻播报，祝你有美好的一天！',
        '财经严肃腔': '以上就是今日的财经观察，感谢关注。',
        '科技快评腔': '以上就是今天的科技速览，我们下期再见！',
    }

    opening = openings.get(style, openings['轻松早报腔'])
    transition_list = transitions.get(style, transitions['轻松早报腔'])
    closing = closings.get(style, closings['轻松早报腔'])

    lines = [opening, '']

    for i, item in enumerate(news_items):
        summary = item.get('summary', {})
        detail = summary.get('detail_60s', item.get('title', ''))

        if i > 0:
            t = transition_list[i % len(transition_list)]
            lines.append(f'{t}：')
            lines.append('')

        credibility = item.get('credibility', '中')
        tags = ''.join(item.get('tags', ['【资讯】']))

        lines.append(f'[{tags}]')
        lines.append(detail)
        lines.append(f'该消息来源为{item.get("source", "未知")}，可信度{credibility}。')
        lines.append('')

    lines.append(closing)

    return '\n'.join(lines)


def generate_dual_host_script(news_items, style, keyword, language='zh'):
    """双人对话播报文案 - 调用大模型API生成
    
    Args:
        news_items: 新闻列表
        style: 播报风格
        keyword: 关键词
        language: 输出语言，'zh' 或 'en'
    """
    
    # 构建新闻内容
    news_content_parts = []
    for i, item in enumerate(news_items[:5], 1):
        title = item.get('title', '')
        content = item.get('content', '')
        source = item.get('source', '未知来源')
        time_str = item.get('time', '')
        credibility = item.get('credibility', '中')
        tags = ''.join(item.get('tags', ['【资讯】']))
        
        news_content_parts.append(f'【新闻{i}】')
        news_content_parts.append(f'标题：{title}')
        news_content_parts.append(f'来源：{source}')
        news_content_parts.append(f'可信度：{credibility}')
        news_content_parts.append(f'标签：{tags}')
        if time_str:
            news_content_parts.append(f'时间：{time_str}')
        news_content_parts.append(f'内容：{content}')
        news_content_parts.append('')
    
    news_content = '\n'.join(news_content_parts)
    
    # 根据语言选择提示词
    if language == 'en':
        prompt = DUAL_HOST_PROMPT_EN.format(style=style, news_content=news_content)
        system_message = 'You are a professional news host and commentator, skilled at writing natural, interactive dialogue-style news broadcast scripts.'
    else:
        prompt = DUAL_HOST_PROMPT.format(style=style, news_content=news_content)
        system_message = '你是一位专业的新闻主播和评论员，擅长撰写自然流畅、有互动感的对话式新闻播报文案。'
    
    print(f'  正在调用大模型生成双人对话文案（风格：{style}，语言：{language}）...')
    
    # 调用大模型API
    script = call_llm_api(prompt, system_message)
    
    if script:
        print(f'  [OK] 大模型生成完成，共 {len(script)} 字符')
        return script
    else:
        print('  [WARN] 大模型调用失败，回退到模板生成...')
        return _generate_dual_host_script_fallback(news_items, style, keyword, language)


def _generate_dual_host_script_fallback(news_items, style, keyword):
    """双人对话播报文案模板回退方案"""
    
    host_name = '晓晓'
    commentator_name = '云深'

    openings = {
        '正式新闻腔': f'{host_name}：各位听众朋友大家好，欢迎收听新闻播报，我是{host_name}。\n{commentator_name}：大家好，我是评论员{commentator_name}。',
        '轻松早报腔': f'{host_name}：早上好！欢迎收听今天的新闻节目，我是{host_name}。\n{commentator_name}：大家好，我是{commentator_name}，今天我们来聊聊热门新闻。',
        '财经严肃腔': f'{host_name}：各位投资者大家好，欢迎收听今日财经观察，我是{host_name}。\n{commentator_name}：大家好，我是{commentator_name}。',
        '科技快评腔': f'{host_name}：大家好，欢迎来到科技快评，我是{host_name}。\n{commentator_name}：我是{commentator_name}，今天我们来看看有什么新鲜事。',
    }

    opening = openings.get(style, openings['轻松早报腔'])

    lines = [opening, '']

    for i, item in enumerate(news_items):
        title = item.get('title', '')
        summary = item.get('summary', {})
        quick = summary.get('quick_20s', title)
        detail = summary.get('detail_60s', title)
        checklist = summary.get('checklist', [])

        tags = ''.join(item.get('tags', ['【资讯】']))
        credibility = item.get('credibility', '中')

        if i == 0:
            lines.append(f'{host_name}：首先关注今天的一条重要新闻。')
            lines.append(f'')
        else:
            lines.append(f'{host_name}：接下来看另一条值得关注的消息。')
            lines.append(f'')

        lines.append(f'{commentator_name}：{quick}')
        lines.append(f'')
        lines.append(f'{host_name}：能详细说说吗？')
        lines.append(f'')
        lines.append(f'{commentator_name}：{detail}')
        lines.append(f'')

        if checklist:
            lines.append(f'{host_name}：有什么要点可以总结的？')
            lines.append(f'')
            lines.append(f'{commentator_name}：主要有这么几点：')
            for point in checklist[:3]:
                lines.append(f'其一，{point}。')
            lines.append(f'')

        lines.append(f'{host_name}：这条消息来源是{item.get("source", "未知")}，可信度{credibility}。')
        lines.append(f'')

    lines.append(f'{host_name}：以上就是本次播报的全部内容。')
    lines.append(f'{commentator_name}：我们下次再见！')

    return '\n'.join(lines)

    return '\n'.join(lines)


def _extract_core_entities(keyword, news_items):
    """从关键词和新闻标题中提取核心实体，用于优化图片搜索
    
    例如：
    - "张雪机车首次亮相广交会" → ["张雪机车", "广交会", "摩托车"]
    - "华为 Mate80 发布" → ["华为", "Mate80", "手机"]
    """
    entities = []
    
    # 1. 提取关键词中的核心名词（去除动词和时间词）
    # 简单规则：去除常见动词、时间词、副词
    stop_words = ['首次', '亮相', '发布', '宣布', '举行', '召开', '进行', '开展', 
                  '今天', '昨日', '近日', '最新', '首次', '正式', '重磅', '突发']
    
    # 尝试提取品牌/产品名（通常是前几个字符）
    keyword_clean = keyword
    for sw in stop_words:
        keyword_clean = keyword_clean.replace(sw, '')
    keyword_clean = keyword_clean.strip()
    
    if keyword_clean:
        entities.append(keyword_clean)
    
    # 2. 从新闻标题中提取高频实体词
    if news_items:
        from collections import Counter
        import re
        
        # 提取所有标题中的名词性词汇（简单规则：2-8个字符的词组）
        all_titles = ' '.join([item.get('title', '') for item in news_items[:5]])
        # 匹配中文词组（2-8个字）
        words = re.findall(r'[\u4e00-\u9fa5]{2,8}', all_titles)
        # 统计词频
        word_freq = Counter(words)
        # 取高频词（出现2次以上）
        top_words = [w for w, c in word_freq.most_common(3) if c >= 1 and len(w) >= 2]
        entities.extend(top_words)
    
    # 3. 添加类别词作为兜底
    category_hints = {
        '机车': '摩托车',
        '摩托': '摩托车',
        '汽车': '汽车',
        '电动车': '电动汽车',
        '手机': '智能手机',
        '芯片': '半导体芯片',
        'AI': '人工智能',
        '无人机': '无人机',
        '广交会': '广交会 展会',
        '车展': '汽车展览',
    }
    
    for hint, category in category_hints.items():
        if hint in keyword and category not in entities:
            entities.append(category)
            break
    
    # 去重并保持顺序
    seen = set()
    unique_entities = []
    for e in entities:
        if e not in seen and len(e) >= 2:
            seen.add(e)
            unique_entities.append(e)
    
    return unique_entities[:3]  # 最多返回3个实体


def _fetch_image_from_news_source(news_items):
    """从新闻源网页抓取配图 - 优化版
    
    抓取策略优先级：
    1. og:image（Open Graph 标准，社交媒体分享图）
    2. article 标签内的首图
    3. 内容区域的大图（>300px）
    4. 任何包含关键词 alt 文本的图片
    """
    try:
        from bs4 import BeautifulSoup
        
        for item in news_items[:5]:  # 尝试前5条新闻
            url = item.get('url', '')
            if not url or not url.startswith('http'):
                continue
            
            try:
                response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                img_url = None
                
                # 策略1: Open Graph 图片（最可靠）
                og_img = soup.find('meta', property='og:image')
                if og_img and og_img.get('content'):
                    img_url = og_img['content']
                    print(f'    [INFO] 从 {source_name} 获取 og:image')
                
                # 策略2: Twitter 卡片图
                if not img_url:
                    twitter_img = soup.find('meta', attrs={'name': 'twitter:image'})
                    if twitter_img and twitter_img.get('content'):
                        img_url = twitter_img['content']
                        print(f'    [INFO] 从 {source_name} 获取 twitter:image')
                
                # 策略3: article 标签内的首图
                if not img_url:
                    article = soup.find('article')
                    if article:
                        img = article.find('img')
                        if img:
                            img_url = img.get('src') or img.get('data-src')
                            if img_url:
                                print(f'    [INFO] 从 {source_name} article 获取图片')
                
                if img_url:
                    # 处理相对路径
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        from urllib.parse import urljoin
                        img_url = urljoin(url, img_url)
                    
                    # 下载图片
                    img_response = requests.get(img_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': url
                    }, timeout=15)
                    
                    if len(img_response.content) >= 10240:
                        with open(cover_path, 'wb') as f:
                            f.write(img_response.content)
                        print(f'  [OK] 新闻源封面图已保存: {cover_path}')
                        return cover_path
                        
            except Exception as e:
                print(f'    [WARN] 从 {item.get("source", "未知")} 抓取失败: {e}')
                continue
        
    except ImportError:
        print('  [WARN] BeautifulSoup 未安装，跳过网页抓取')
    except Exception as e:
        print(f'  [WARN] 新闻源抓取失败: {e}')
    
    # 方案 2: AI 生成
    print('  尝试方案2: AI 生成配图...')
    try:
        autoglm_skill = os.path.expanduser('~/.agents/skills/autoglm-generate-image')
        if os.path.exists(autoglm_skill):
            import subprocess
            script_path = os.path.join(autoglm_skill, 'scripts', 'generate.py')
            if os.path.exists(script_path):
                # 构建更精确的提示词
                prompt = f'{keyword} 新闻配图，专业摄影风格，高清，适合新闻播报封面，16:9 横版构图'
                result = subprocess.run(
                    [sys.executable, script_path,
                     '--prompt', prompt,
                     '--output', cover_path],
                    capture_output=True, text=True, timeout=120)
                if result.returncode == 0 and os.path.exists(cover_path):
                    print(f'  [OK] AI 生成封面图已保存: {cover_path}')
                    return cover_path
    except Exception as e:
        print(f'  [WARN] AI 生成失败: {e}')
    
    # 方案 3: 图库搜索（兜底）
    print('  尝试方案3: Unsplash 图库搜索...')
    
    # 检查是否配置了 Unsplash Key
    if not UNSPLASH_KEY:
        print('  [WARN] 未配置 Unsplash API Key，跳过图库搜索')
        print('  [INFO] 配置方式：')
        print('    1. 在 ~/.openclaw/openclaw.json 中添加：')
        print('       {"custom": {"unsplash": {"accessKey": "你的Key"}}}')
        print('    2. 或设置环境变量：UNSPLASH_ACCESS_KEY')
    else:
        try:
            # 提取核心实体优化搜索
            from collections import Counter
            entities = []
            
            # 从关键词提取
            stop_words = ['首次', '亮相', '发布', '宣布', '举行', '召开', '今天', '昨日']
            keyword_clean = keyword
            for sw in stop_words:
                keyword_clean = keyword_clean.replace(sw, '')
            if keyword_clean.strip():
                entities.append(keyword_clean.strip())
            
            # 从新闻标题提取高频词
            if news_items_cache:
                all_titles = ' '.join([item.get('title', '') for item in news_items_cache[:5]])
                words = re.findall(r'[\u4e00-\u9fa5]{2,8}', all_titles)
                word_freq = Counter(words)
                top_words = [w for w, c in word_freq.most_common(2) if c >= 1]
                entities.extend(top_words)
            
            # 构建搜索查询
            search_queries = entities[:2] if entities else [keyword, 'news']
            
            for q in search_queries:
                print(f'    [INFO] Unsplash 搜索: {q}')
                r = requests.get('https://api.unsplash.com/search/photos',
                                 params={'query': q, 'per_page': 3, 'orientation': 'landscape'},
                                 headers={'Authorization': f'Client-ID {UNSPLASH_KEY}'},
                                 timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    if data.get('results'):
                        for img in data['results']:
                            img_url = img['urls']['regular']
                            img_data = requests.get(img_url, timeout=15).content
                            if len(img_data) >= 10240:
                                with open(cover_path, 'wb') as f:
                                    f.write(img_data)
                                print(f'  [OK] Unsplash 封面图已保存: {cover_path}')
                                print(f'    图片来源: {img["user"]["name"]}')
                                return cover_path
        except Exception as e:
            print(f'  [WARN] Unsplash 搜索失败: {e}')
    
    print('  [WARN] 所有图片搜索方案均失败，未生成封面图')
    return None


def generate_audio(script, voice_desc, output_dir, broadcast_format='单人口播', output_filename=None):
    """生成播报音频 - 多方案支持
    
    Args:
        script: 播报文案
        voice_desc: 音色描述
        output_dir: 输出目录
        broadcast_format: 播报形式（单人口播/双人对话式播报）
        output_filename: 输出文件名（可选，默认为'播报.mp3'或'播报_对话版.mp3'）
    """
    os.makedirs(output_dir, exist_ok=True)

    # 清理文案（去除 Markdown 标记）
    clean_script = re.sub(r'[#*>_\[\]`]', '', script).strip()

    # 方案 1: CellCog / audio-cog
    print('  尝试方案1: CellCog/audio-cog...')
    cellcog_result = try_cellcog_audio(clean_script, voice_desc, output_dir, broadcast_format, output_filename)
    if cellcog_result:
        return cellcog_result

    # 方案 2: edge-tts（免费兜底）
    print('  回退到方案2: edge-tts...')
    return generate_edge_tts_audio(clean_script, voice_desc, output_dir, broadcast_format, output_filename)


def try_cellcog_audio(script, voice_desc, output_dir, broadcast_format='单人口播', output_filename=None):
    """尝试使用 CellCog / audio-cog 生成音频"""
    # 检测 CellCog 是否可用
    cellcog_available = False
    audio_cog_available = False

    # 检查环境变量
    if os.environ.get('CELLCOG_API_KEY'):
        cellcog_available = True

    # 检查 audio-cog 技能
    audio_cog_skill = os.path.expanduser('~/.agents/skills/audio-cog')
    if os.path.exists(audio_cog_skill):
        audio_cog_available = True

    if not cellcog_available and not audio_cog_available:
        print('  CellCog/audio-cog 未检测到，跳过')
        return None

    voice_id, voice_label = map_voice(voice_desc)
    
    # 确定输出文件名
    if output_filename:
        dst_filename = output_filename
    elif broadcast_format == '双人对话式播报':
        dst_filename = '播报_对话版.mp3'
    else:
        dst_filename = '播报.mp3'

    # CellCog SDK 方式
    if cellcog_available:
        try:
            from cellcog import CellCogClient
            client = CellCogClient()

            voice_name = 'Lively_Girl'  # 默认
            if '男' in voice_desc or '男声' in voice_desc or '沉稳' in voice_desc:
                voice_name = 'Deep_Voice_Man'
            elif '温柔' in voice_desc:
                voice_name = 'Calm_Woman'

            result = client.create_chat(
                prompt=f'Generate TTS audio using MiniMax provider with {voice_name} voice. Read this news script:\n\n{script}',
                task_label='news-podcast',
                chat_mode='agent',
                timeout=120
            )

            if result and result.get('downloaded_files'):
                for f in result['downloaded_files']:
                    src = f.get('path', '')
                    if src:
                        dst = os.path.join(output_dir, dst_filename)
                        import shutil
                        shutil.copy2(src, dst)
                        file_size = os.path.getsize(dst) / 1024
                        print(f'[OK] CellCog 音频已保存: {dst} ({file_size:.1f} KB)')
                        return dst
        except Exception as e:
            print(f'  CellCog 失败: {e}')

    # audio-cog 技能方式
    if audio_cog_available:
        try:
            import subprocess
            script_path = os.path.join(audio_cog_skill, 'scripts', 'generate.py')
            if os.path.exists(script_path):
                result = subprocess.run(
                    [sys.executable, script_path,
                     '--text', script, '--voice', voice_id, '--output',
                     os.path.join(output_dir, dst_filename)],
                    capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    audio_path = os.path.join(output_dir, dst_filename)
                    if os.path.exists(audio_path):
                        file_size = os.path.getsize(audio_path) / 1024
                        print(f'[OK] audio-cog 音频已保存: {audio_path} ({file_size:.1f} KB)')
                        return audio_path
        except Exception as e:
            print(f'  audio-cog 失败: {e}')

    return None


def generate_edge_tts_audio(script, voice_desc, output_dir, broadcast_format='单人口播', output_filename=None):
    """使用 edge-tts 生成音频（免费兜底）"""
    import asyncio
    import edge_tts

    if broadcast_format == '双人对话式播报':
        return generate_dual_audio(script, output_dir)

    # 单人口播
    voice_id, _ = map_voice(voice_desc)
    print(f'  使用音色: {VOICE_LABELS.get(voice_id, voice_id)} ({voice_id})')

    # 确定输出文件名
    if output_filename:
        audio_path = os.path.join(output_dir, output_filename)
    else:
        audio_path = os.path.join(output_dir, '播报.mp3')

    async def _tts():
        communicate = edge_tts.Communicate(script, voice_id)
        await communicate.save(audio_path)

    asyncio.run(_tts())

    if os.path.exists(audio_path):
        file_size = os.path.getsize(audio_path) / 1024
        print(f'[OK] 音频已保存: {audio_path} ({file_size:.1f} KB)')
        return audio_path

    return None


def generate_dual_audio(script, output_dir, host_voice=None, commentator_voice=None):
    """双人对话音频生成：逐句交替生成，按对话顺序拼接

    ⚠️ 关键原则：
    1. 逐句拆分：每行独立作为一段音频生成，不可合并
    2. 交替音色：主播和评论员使用不同的 voice_id
    3. 顺序拼接：严格按文案中的对话顺序拼接
    4. 临时文件：每句生成独立 mp3 到临时目录，拼接完成后清理
    """
    import asyncio
    import edge_tts
    import shutil

    if host_voice is None:
        host_voice = DEFAULT_HOST_VOICE
    if commentator_voice is None:
        commentator_voice = DEFAULT_COMMENTATOR_VOICE

    # 第一步：逐句解析播报文案，按对话顺序提取每一句
    dialogue = []  # [(speaker, text), ...]
    for line in script.split('\n'):
        line = line.strip()
        if not line:
            continue
        # 支持中英文对话标记
        if line.startswith('晓晓：') or line.startswith('主播：') or \
           line.startswith('HOST:') or line.startswith('Host:') or \
           line.startswith('**HOST:**') or line.startswith('**Host:**'):
            # 去除标记和 Markdown 格式
            content = line
            for marker in ['晓晓：', '主播：', 'HOST:', 'Host:', '**HOST:**', '**Host:**']:
                if content.startswith(marker):
                    content = content[len(marker):].strip()
                    break
            if content.strip():
                dialogue.append(('host', content.strip()))
        elif line.startswith('云深：') or line.startswith('评论员：') or \
             line.startswith('COMMENTATOR:') or line.startswith('Commentator:') or \
             line.startswith('**COMMENTATOR:**') or line.startswith('**Commentator:**'):
            # 去除标记和 Markdown 格式
            content = line
            for marker in ['云深：', '评论员：', 'COMMENTATOR:', 'Commentator:', '**COMMENTATOR:**', '**Commentator:**']:
                if content.startswith(marker):
                    content = content[len(marker):].strip()
                    break
            if content.strip():
                dialogue.append(('commentator', content.strip()))

    if not dialogue:
        print('[WARN] 未找到对话行，回退到单人生成')
        return generate_edge_tts_audio(script, '', output_dir, '单人口播')

    print(f'  对话行数: {len(dialogue)}')
    print(f'  主播音色: {VOICE_LABELS.get(host_voice, host_voice)}')
    print(f'  评论员音色: {VOICE_LABELS.get(commentator_voice, commentator_voice)}')

    # 第二步：创建临时目录
    tmp_dir = os.path.join(output_dir, '_temp_dialogue')
    os.makedirs(tmp_dir, exist_ok=True)

    audio_files = []  # 按对话顺序保存音频路径

    async def generate_line(text, voice_id, path):
        communicate = edge_tts.Communicate(text, voice_id)
        await communicate.save(path)

    async def generate_all():
        for i, (speaker, text) in enumerate(dialogue):
            filename = f'line_{i:03d}.mp3'
            filepath = os.path.join(tmp_dir, filename)

            if speaker == 'host':
                voice = host_voice
                label = '主播'
            else:
                voice = commentator_voice
                label = '评论员'

            # 限制单句长度，避免 edge-tts 错误
            max_len = 500
            if len(text) > max_len:
                text = text[:max_len] + '...'

            print(f'  [{i+1:2d}/{len(dialogue)}] {label}: {text[:30]}...')
            try:
                await generate_line(text, voice, filepath)
                audio_files.append(filepath)
            except Exception as e:
                print(f'    [WARN] 生成失败，跳过: {e}')
                continue

    asyncio.run(generate_all())
    print(f'  所有行音频生成完毕，共 {len(audio_files)} 段')

    # 第三步：按对话顺序拼接
    final_path = os.path.join(output_dir, '播报_对话版.mp3')

    # 查找 ffmpeg
    ffmpeg_exe = find_ffmpeg()

    if ffmpeg_exe:
        # 使用 ffmpeg concat
        import subprocess
        list_path = os.path.join(tmp_dir, 'filelist.txt')
        with open(list_path, 'w', encoding='utf-8') as f:
            for af in audio_files:
                f.write("file '" + af.replace('\\', '/') + "'\n")

        cmd = [
            ffmpeg_exe, '-y', '-f', 'concat', '-safe', '0',
            '-i', list_path, '-c', 'copy', final_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if os.path.exists(final_path):
            size = os.path.getsize(final_path) / 1024
            print(f'[OK] 对话版音频已生成: {final_path} ({size:.1f} KB)')
        else:
            print(f'[WARN] ffmpeg 拼接失败，尝试 pydub...')
            final_path = _fallback_concat(audio_files, output_dir)
    else:
        print('[INFO] ffmpeg 未找到，使用 pydub 拼接...')
        final_path = _fallback_concat(audio_files, output_dir)

    # 清理临时文件
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print('  临时文件已清理')

    return final_path if os.path.exists(final_path) else None


def find_ffmpeg():
    """查找 ffmpeg 可执行文件"""
    import subprocess

    # 先尝试 PATH
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=3)
        if result.returncode == 0:
            return 'ffmpeg'
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 尝试 winget 安装路径
    winget_packages = os.path.expanduser(
        r'~\AppData\Local\Microsoft\WinGet\Packages')
    if os.path.exists(winget_packages):
        for d in os.listdir(winget_packages):
            if 'FFmpeg' in d:
                pkg_dir = os.path.join(winget_packages, d)
                for sub in os.listdir(pkg_dir):
                    if sub.startswith('ffmpeg-'):
                        exe = os.path.join(pkg_dir, sub, 'bin', 'ffmpeg.exe')
                        if os.path.exists(exe):
                            return exe
    return None


def _fallback_concat(audio_files, output_dir):
    """使用 pydub 拼接音频（ffmpeg 不可用时的备选）"""
    try:
        from pydub import AudioSegment
        segments = []
        for af in audio_files:
            if os.path.exists(af):
                segments.append(AudioSegment.from_mp3(af))

        if segments:
            combined = segments[0]
            for seg in segments[1:]:
                combined += seg
            final_path = os.path.join(output_dir, '播报_对话版.mp3')
            combined.export(final_path, format='mp3')
            size = os.path.getsize(final_path) / 1024
            print(f'[OK] pydub 拼接完成: {final_path} ({size:.1f} KB)')
            return final_path
    except ImportError:
        print('[WARN] pydub 未安装')
    except Exception as e:
        print(f'[WARN] pydub 拼接失败: {e}')

    # 最终兜底：生成独立文件
    print('[INFO] 生成独立的主播/评论员音频文件')
    return None


def save_summary_document(keyword, news_items, script, output_dir):
    """保存新闻摘要文档"""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    date_str = datetime.now().strftime('%Y-%m-%d')

    lines = [
        f'# 📰 新闻摘要：{keyword}',
        '',
        f'> **生成时间**：{timestamp}',
        f'> **关键词**：{keyword}',
        '',
        '---',
        '',
        '![封面图](cover.jpg)',
        '',
        '---',
        '',
        '## 一、新闻列表',
        '',
    ]

    for i, item in enumerate(news_items, 1):
        title = item.get('title', '未知标题')
        source = item.get('source', '') or '未知来源'
        tags = ''.join(item.get('tags', ['【资讯】']))
        time_str = item.get('time', '')
        url = item.get('url', '')

        lines.append(f'### {i}. {title}')
        lines.append(f'- 【新闻来源】{source}')
        lines.append(f'- 【事件标签】{tags}')
        if time_str:
            lines.append(f'- 【时间】{time_str}')
        if url:
            lines.append(f'- 【链接】{url}')
        lines.append('')

        # 三级摘要
        summary = item.get('summary', {})
        if summary.get('quick_20s'):
            lines.append(f'**20 秒速报：** {summary["quick_20s"]}')
            lines.append('')
        if summary.get('detail_60s'):
            lines.append(f'**60 秒解读：** {summary["detail_60s"]}')
            lines.append('')
        if summary.get('checklist'):
            lines.append('**要点清单：**')
            for point in summary['checklist']:
                lines.append(f'- {point}')
            lines.append('')

        lines.append('---')
        lines.append('')

    # 播报文案
    lines.append('## 二、播报文案')
    lines.append('')
    lines.append('```')
    lines.append(script)
    lines.append('```')
    lines.append('')

    # 来源声明
    sources = list(set(item.get('source', '未知') for item in news_items))
    lines.append('---')
    lines.append('')
    lines.append(f'*本文综合自{", ".join(sources)}等公开报道*')
    lines.append(f'*生成时间：{timestamp}*')
    lines.append('')

    content = '\n'.join(lines)

    filename = f'新闻摘要_{keyword.replace(" ", "_")}_{date_str}.md'
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)

    print(f'[OK] 摘要文档已保存: {filepath}')
    return filepath

    return filepath


def save_broadcast_script(script, keyword, output_dir):
    """保存纯文本播报稿"""
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d')

    filename = f'播报文案_{keyword.replace(" ", "_")}_{date_str}.txt'
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(script)

    print(f'[OK] 播报文案已保存: {filepath}')
    return filepath


def save_title_and_labels(news_items, output_dir):
    """保存标题和标签文件（固定文件名 titleAndLabels.txt）"""
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, 'titleAndLabels.txt')

    lines = []
    for i, item in enumerate(news_items, 1):
        title = item.get('title', '未知标题')
        source = item.get('source', '') or '未知来源'
        tags = ''.join(item.get('tags', ['【资讯】']))
        time_str = item.get('time', '')

        lines.append(f'【新闻标题】{title}')
        lines.append(f'【新闻来源】{source}')
        lines.append(f'【事件标签】{tags}')
        if time_str:
            lines.append(f'【时间】{time_str}')
        lines.append('')  # 空行分隔每条新闻

    content = '\n'.join(lines)

    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)

    print(f'[OK] 标题标签文件已保存: {filepath}')
    return filepath


def save_deep_analysis(analysis_text, keyword, output_dir):
    """保存深度解读文案（固定文件名 深度解读文案.txt）"""
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, '深度解读文案.txt')
    
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(analysis_text)
    
    print(f'[OK] 深度解读文案已保存: {filepath}')
    return filepath


def main():
    """主流程"""

    # Step 0：检查是否有命令行参数传入的配置
    config = None
    if len(sys.argv) > 1:
        input_text = ' '.join(sys.argv[1:])
        print(f'[INFO] 检测到命令行参数，尝试解析配置...')
        parsed_config = parse_config_from_text(input_text)
        if parsed_config and parsed_config.get('is_complete_config'):
            print('[OK] 成功解析完整配置，跳过交互环节')
            config = parsed_config
    
    # Step 1：收集用户输入（如果配置未从命令行解析成功）
    if config is None:
        config = prompt_user_for_input()

    keyword = config['keyword']
    style = config['style']
    broadcast_format = config['format']
    voice = config['voice']
    need_deep_analysis = config.get('need_deep_analysis', False)
    deep_analysis_style = config.get('deep_analysis_style', '正式新闻腔')
    deep_analysis_voice = config.get('deep_analysis_voice', '沉稳的中年男性')
    
    # 输出目录优先级：环境变量 > config['output_dir'] > 默认生成
    output_dir = None
    
    # 1. 优先从环境变量获取输出目录（批量生成时使用）
    env_output_dir = os.environ.get('_NEWS_PODCAST_OUTPUT_DIR')
    if env_output_dir:
        output_dir = env_output_dir
        print(f'[INFO] 从环境变量获取输出目录: {output_dir}')
    
    # 2. 如果环境变量没有，使用 config 中的输出目录
    if not output_dir and config.get('output_dir'):
        output_dir = config['output_dir']
        print(f'[INFO] 从配置获取输出目录: {output_dir}')
    
    # 3. 如果都没有，使用默认生成
    if not output_dir:
        workspace = os.path.expanduser('~/.openclaw/workspace')
        base_dir = os.path.join(workspace, 'news')
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        keyword_safe = re.sub(r'[\\/:*?"<>|]', '', keyword)[:30]
        output_dir = os.path.join(base_dir, f'{timestamp_str}_{keyword_safe}')
        print(f'[INFO] 使用默认输出目录: {output_dir}')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    print()
    print('=' * 60)
    print(f'📰 Auto News Podcast v2.0')
    print(f'关键词: {keyword}')
    print(f'风格: {style or "自动匹配"}')
    print(f'形式: {broadcast_format}')
    print(f'音色: {voice or "默认"}')
    if need_deep_analysis:
        print(f'深度解读: ✅ 是')
        print(f'  解读风格: {deep_analysis_style}')
        print(f'  解读音色: {deep_analysis_voice}')
    print(f'输出目录: {output_dir}')
    print('=' * 60)

    # Step 2：搜索新闻
    print('\n[Step 2] 多源搜索新闻...')
    news_items = fetch_news_multi_source(keyword, limit=15)
    print(f'  找到 {len(news_items)} 条新闻')

    if not news_items:
        print('[ERROR] 未找到任何新闻，请检查网络连接或关键词')
        sys.exit(1)

    # 保存到全局缓存（供图片搜索 fallback 使用）
    global news_items_cache
    news_items_cache = news_items

    # 显示新闻列表
    for i, item in enumerate(news_items[:5], 1):
        tags = ''.join(item.get('tags', ['【资讯】']))
        cred = item.get('credibility', '中')
        title = item.get('title', '')[:50]
        print(f'  {i}. [{tags}] [{cred}] {title}')

    # Step 3：生成三级摘要
    print('\n[Step 3] 生成三级摘要...')
    for item in news_items[:5]:
        summary = generate_three_level_summary(item)
        item['summary'] = summary

    # 获取语言设置（从配置中获取，默认为中文）
    language = config.get('language', 'zh')
    
    # Step 4：生成播报文案
    print('\n[Step 4] 生成播报文案...')
    script = generate_broadcast_script(news_items[:5], style, broadcast_format, keyword, language)
    print(f'  播报文案长度: {len(script)} 字符')

    # 保存播报文案
    script_path = save_broadcast_script(script, keyword, output_dir)

    # Step 5：保存标题标签文件
    print('\n[Step 5] 保存标题标签文件...')
    title_labels_path = save_title_and_labels(news_items[:5], output_dir)

    # Step 6：搜索配图
    print('\n[Step 6] 搜索封面图...')
    cover_path = search_cover_image(keyword, output_dir, news_items)

    # Step 7：保存摘要文档
    print('\n[Step 7] 保存摘要文档...')
    summary_path = save_summary_document(keyword, news_items[:5], script, output_dir)

    # Step 8：生成播报音频
    print('\n[Step 8] 生成播报音频...')
    audio_path = generate_audio(script, voice, output_dir, broadcast_format)

    # Step 9：事件深度解读播报（如果需要）
    deep_analysis_path = None
    deep_analysis_audio_path = None
    if config.get('need_deep_analysis'):
        print('\n[Step 9] 生成事件深度解读播报...')
        
        # 生成深度解读文案
        print('  生成深度解读文案...')
        analysis_text = generate_deep_analysis(news_items[:5], keyword, language)
        deep_analysis_path = save_deep_analysis(analysis_text, keyword, output_dir)
        
        # 生成深度解读音频
        print('  生成深度解读音频...')
        da_voice = config.get('deep_analysis_voice', '沉稳的中年男性')
        deep_analysis_audio_path = generate_audio(
            analysis_text, da_voice, output_dir, '单人口播', '事件深度解读.mp3'
        )

    # 总结
    print('\n' + '=' * 60)
    print('✅ 生成完成!')
    print(f'  📄 {summary_path}')
    print(f'  📝 {script_path}')
    print(f'  📋 {title_labels_path}')
    if cover_path:
        print(f'  🖼️ {cover_path}')
    if audio_path:
        print(f'  🎵 {audio_path}')
    if deep_analysis_path:
        print(f'  📊 {deep_analysis_path}')
    if deep_analysis_audio_path:
        print(f'  🎙️ {deep_analysis_audio_path}')
    print('=' * 60)


# ========== news_aggregator 子模块 ==========

class news_aggregator:
    @staticmethod
    def fetch_via_aggregator(keyword, limit=15):
        """调用 news-aggregator-skill 获取新闻"""
        aggregator_path = os.path.expanduser(
            '~/.agents/skills/news-aggregator-skill/scripts/fetch_news.py')

        if not os.path.exists(aggregator_path):
            print(f'[WARN] news-aggregator-skill 未找到')
            return []

        import subprocess

        cmd = [sys.executable, '-X', 'utf8', aggregator_path,
               '--source', 'weibo,wallstreetcn,36kr,tencent,github',
               '--limit', str(limit), '--no-save']

        if keyword:
            cmd.extend(['--keyword', keyword])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout.strip())
        except Exception as e:
            print(f'[WARN] 搜索失败: {e}')

        return []


def run_with_config(user_input_text):
    """
    使用用户输入文本中的配置直接运行（无需交互）
    
    参数:
        user_input_text: 包含完整配置的文本，例如：
            "【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】"
    
    返回:
        dict: 包含生成结果信息的字典
    """
    print(f'[INFO] 解析用户输入配置...')
    parsed_config = parse_config_from_text(user_input_text)
    
    if not parsed_config:
        print('[ERROR] 无法从输入中解析出有效配置')
        print('[INFO] 请确保输入格式正确，例如：')
        print('  【关键词信息，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读】')
        return {'success': False, 'error': '配置解析失败'}
    
    if not parsed_config.get('is_complete_config'):
        print('[ERROR] 配置不完整，缺少必要参数')
        print('[INFO] 完整配置需要包含：风格、形式、音色（单人口播）或主播+评论员音色（双人对话）')
        return {'success': False, 'error': '配置不完整'}
    
    print('[OK] 配置解析成功，开始执行...')
    
    # 设置输出目录（如果未指定）
    if not parsed_config.get('output_dir'):
        workspace = os.path.expanduser('~/.openclaw/workspace')
        base_dir = os.path.join(workspace, 'news')
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        keyword_safe = re.sub(r'[\\/:*?"<>|]', '', parsed_config['keyword'])[:30]
        parsed_config['output_dir'] = os.path.join(base_dir, f'{timestamp_str}_{keyword_safe}')
        os.makedirs(parsed_config['output_dir'], exist_ok=True)
    
    # 将配置注入到 sys.argv，让 main() 可以读取
    sys.argv = [sys.argv[0], user_input_text]
    
    # 执行主流程
    try:
        main()
        return {
            'success': True,
            'config': parsed_config,
            'output_dir': parsed_config['output_dir']
        }
    except Exception as e:
        print(f'[ERROR] 执行失败: {e}')
        return {'success': False, 'error': str(e)}


def parse_batch_configs(text):
    """
    从用户输入文本中解析批量播报配置
    
    支持多条配置，每条配置用【】包裹，例如：
    【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
    【宝马X5最新信息，风格是科技快评腔，形式是单人口播，用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
    【奔驰S级最新信息，风格是正式新闻，其他用默认值】
    
    返回:
        list: 配置字典列表，每个字典包含一条新闻播报的完整配置
    """
    # 提取所有【】或[]包裹的配置
    config_matches = re.findall(r'[【\[](.+?)[】\]]', text)
    
    if not config_matches:
        return []
    
    configs = []
    for config_text in config_matches:
        parsed = parse_config_from_text(f'【{config_text}】')
        if parsed and parsed.get('keyword'):
            configs.append(parsed)
    
    return configs


def fill_config_with_defaults(config):
    """
    使用默认值填充不完整的配置
    
    默认值：
    - 风格：自动匹配（空字符串表示自动匹配）
    - 形式：单人口播
    - 音色：年轻活力的女生
    - 深度解读：根据关键词自动判断
    - 深度解读风格：正式新闻腔
    - 深度解读音色：沉稳的中年男性
    """
    # 如果风格为空，保持为空（表示自动匹配）
    if not config.get('style'):
        config['style'] = ''
    
    # 如果形式为空，使用默认值
    if not config.get('format'):
        config['format'] = '单人口播'
    
    # 如果音色为空，使用默认值
    if not config.get('voice'):
        config['voice'] = '年轻活力的女生'
    
    # 深度解读相关配置
    if config.get('need_deep_analysis') is None:
        # 根据关键词自动判断是否需要深度解读
        config['need_deep_analysis'] = not is_broad_keyword(config['keyword'])
    
    if not config.get('deep_analysis_style'):
        config['deep_analysis_style'] = '正式新闻腔'
    
    if not config.get('deep_analysis_voice'):
        config['deep_analysis_voice'] = '沉稳的中年男性'
    
    # 输出目录会在执行时自动生成
    if not config.get('output_dir'):
        config['output_dir'] = ''
    
    # 标记为完整配置
    config['is_complete_config'] = True
    
    return config


def generate_config_summary_table(configs):
    """
    生成配置清单表格
    
    返回:
        str: Markdown格式的表格
    """
    lines = [
        '# 📋 新闻播报配置清单',
        '',
        '| 序号 | 关键词 | 风格 | 形式 | 音色 | 深度解读 | 状态 |',
        '|------|--------|------|------|------|----------|------|',
    ]
    
    for i, config in enumerate(configs, 1):
        keyword = config['keyword']
        style = config.get('style', '自动匹配') or '自动匹配'
        format_type = config.get('format', '单人口播')
        voice = config.get('voice', '年轻活力的女生')
        
        # 简化音色显示
        if '主播:' in voice and '评论员:' in voice:
            # 提取主播和评论员音色
            host_match = re.search(r'主播:([^,]+)', voice)
            commentator_match = re.search(r'评论员:([^,]+)', voice)
            if host_match and commentator_match:
                voice_short = f"主播:{host_match.group(1)[:6]}.../评论员:{commentator_match.group(1)[:6]}..."
            else:
                voice_short = '双人对话'
        else:
            # 单人口播，显示简化音色
            if len(voice) > 12:
                voice_short = voice[:12] + '...'
            else:
                voice_short = voice
        
        # 深度解读信息显示
        if config.get('need_deep_analysis'):
            da_voice = config.get('deep_analysis_voice', '沉稳的中年男性')
            # 简化音色显示
            if len(da_voice) > 8:
                da_voice_short = da_voice[:8] + '...'
            else:
                da_voice_short = da_voice
            deep_analysis = f'✅({da_voice_short})'
        else:
            deep_analysis = '❌'
        
        status = '⏳ 待生成'
        
        lines.append(f'| {i} | {keyword} | {style} | {format_type} | {voice_short} | {deep_analysis} | {status} |')
    
    lines.append('')
    lines.append(f'**总计：{len(configs)} 条新闻播报**')
    lines.append('')
    
    return '\n'.join(lines)


def run_single_broadcast(config, base_output_dir):
    """
    执行单条新闻播报生成
    
    参数:
        config: 配置字典
        base_output_dir: 基础输出目录
    
    返回:
        dict: 执行结果
    """
    keyword = config['keyword']
    
    # 设置输出目录
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    keyword_safe = re.sub(r'[\\/:*?"<>|]', '', keyword)[:30]
    output_dir = os.path.join(base_output_dir, f'{timestamp_str}_{keyword_safe}')
    os.makedirs(output_dir, exist_ok=True)
    config['output_dir'] = output_dir
    
    print(f'\n{"="*60}')
    print(f'📰 正在生成: {keyword}')
    print(f'{"="*60}')
    
    try:
        # 根据语言选择配置格式
        language = config.get('language', 'zh')
        
        # 如果使用默认配置，直接构建简单的配置文本
        if config.get('use_defaults'):
            if language == 'en':
                config_text = f"[{keyword}, use default config]"
            else:
                config_text = f"【{keyword}，使用默认配置】"
        elif language == 'en':
            # 英文配置格式
            config_text = f"[{keyword}"
            if config.get('style'):
                # 反向映射中文风格到英文
                style_en = config['style']
                for en, zh in STYLE_MAP_EN.items():
                    if zh == style_en:
                        style_en = en
                        break
                config_text += f", style is {style_en}"
            config_text += f", format is {config['format']}"
            if '主播:' in config.get('voice', ''):
                # 双人对话格式
                host_voice = config['voice'].split('主播:')[1].split(',')[0] if '主播:' in config['voice'] else ''
                commentator_voice = config['voice'].split('评论员:')[1] if '评论员:' in config['voice'] else ''
                # 反向映射到英文
                for en, zh in VOICE_MAP_EN.items():
                    if zh == host_voice:
                        host_voice = en
                        break
                for en, zh in VOICE_MAP_EN.items():
                    if zh == commentator_voice:
                        commentator_voice = en
                        break
                config_text += f", host voice is {host_voice}, commentator voice is {commentator_voice}"
            else:
                voice_en = config['voice']
                for en, zh in VOICE_MAP_EN.items():
                    if zh == voice_en:
                        voice_en = en
                        break
                config_text += f", voice is {voice_en}"
            if config.get('need_deep_analysis'):
                config_text += f", need deep analysis"
                if config.get('deep_analysis_voice'):
                    da_voice_en = config['deep_analysis_voice']
                    for en, zh in VOICE_MAP_EN.items():
                        if zh == da_voice_en:
                            da_voice_en = en
                            break
                    config_text += f", deep analysis voice is {da_voice_en}"
            else:
                config_text += f", no deep analysis"
            config_text += "]"
        else:
            # 中文配置格式（原有逻辑）
            config_text = f"【{keyword}"
            if config.get('style'):
                config_text += f"，风格是{config['style']}"
            config_text += f"，形式是{config['format']}"
            if '主播:' in config.get('voice', ''):
                config_text += f"，{config['voice']}"
            else:
                config_text += f"，用{config['voice']}音色"
            if config.get('need_deep_analysis'):
                config_text += f"，需要深度解读"
                if config.get('deep_analysis_voice'):
                    config_text += f"，深度解读音色是{config['deep_analysis_voice']}"
            else:
                config_text += f"，不需要深度解读"
            config_text += "】"
        
        # 使用环境变量传递输出目录（更可靠）
        os.environ['_NEWS_PODCAST_OUTPUT_DIR'] = output_dir
        
        sys.argv = [sys.argv[0], config_text]
        
        # 执行主流程
        main()
        
        # 清理环境变量
        if '_NEWS_PODCAST_OUTPUT_DIR' in os.environ:
            del os.environ['_NEWS_PODCAST_OUTPUT_DIR']
        
        return {
            'success': True,
            'keyword': keyword,
            'output_dir': output_dir,
            'error': None
        }
    except Exception as e:
        print(f'[ERROR] 生成失败: {e}')
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'keyword': keyword,
            'output_dir': output_dir,
            'error': str(e)
        }


def run_batch_broadcast(user_input_text):
    """
    批量生成新闻播报
    
    参数:
        user_input_text: 包含多条配置的文本，每条配置用【】包裹，例如：
            【华为Mate80发布，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
            【宝马X5最新信息，风格是科技快评腔，形式是单人口播，用温柔女生音色，需要深度解读，深度解读音色是活力年轻女生】
            【奔驰S级最新信息，风格是正式新闻，其他用默认值】
    
    返回:
        dict: 批量生成结果
    """
    print('=' * 60)
    print('📰 Auto News Podcast - 批量生成模式')
    print('=' * 60)
    
    # Step 1: 解析批量配置
    print('\n[Step 1] 解析批量配置...')
    configs = parse_batch_configs(user_input_text)
    
    if not configs:
        print('[ERROR] 未找到有效的配置信息')
        print('[INFO] 请确保输入格式正确，例如：')
        print('  【关键词信息，风格是科技快评腔，形式是双人对话，主播用沉稳中年男性音色，评论员用温柔女生音色，需要深度解读】')
        return {'success': False, 'error': '配置解析失败'}
    
    print(f'[OK] 解析到 {len(configs)} 条配置')
    
    # Step 2: 使用默认值填充不完整的配置
    print('\n[Step 2] 填充默认配置...')
    filled_configs = []
    for config in configs:
        filled_config = fill_config_with_defaults(config)
        filled_configs.append(filled_config)
    print(f'[OK] 已填充默认值')
    
    # Step 3: 生成配置清单表格
    print('\n[Step 3] 生成配置清单...')
    config_table = generate_config_summary_table(filled_configs)
    print(config_table)
    
    # 保存配置清单到文件
    workspace = os.path.expanduser('~/.openclaw/workspace')
    base_dir = os.path.join(workspace, 'news')
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    batch_output_dir = os.path.join(base_dir, f'batch_{timestamp_str}')
    os.makedirs(batch_output_dir, exist_ok=True)
    
    config_table_path = os.path.join(batch_output_dir, '配置清单.md')
    with open(config_table_path, 'w', encoding='utf-8-sig') as f:
        f.write(config_table)
    print(f'[OK] 配置清单已保存: {config_table_path}')
    
    # Step 4: 逐条执行生成
    print('\n' + '=' * 60)
    print('[Step 4] 开始逐条生成新闻播报...')
    print('=' * 60)
    
    results = []
    success_count = 0
    error_count = 0
    
    for i, config in enumerate(filled_configs, 1):
        print(f'\n{"-"*60}')
        print(f'📰 [{i}/{len(filled_configs)}] 开始生成第 {i} 条')
        print(f'{"-"*60}')
        
        result = run_single_broadcast(config, batch_output_dir)
        results.append(result)
        
        if result['success']:
            success_count += 1
            print(f'\n✅ 第 {i} 条生成成功: {result["keyword"]}')
        else:
            error_count += 1
            print(f'\n❌ 第 {i} 条生成失败: {result["keyword"]}')
            print(f'   错误: {result["error"]}')
    
    # Step 5: 生成结果汇总
    print('\n' + '=' * 60)
    print('📊 批量生成完成 - 结果汇总')
    print('=' * 60)
    print(f'总计: {len(filled_configs)} 条')
    print(f'成功: {success_count} 条 ✅')
    print(f'失败: {error_count} 条 ❌')
    print(f'输出目录: {batch_output_dir}')
    
    # 生成结果汇总文件
    summary_lines = [
        '# 📊 批量生成结果汇总',
        '',
        f'**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'**总计**: {len(filled_configs)} 条',
        f'**成功**: {success_count} 条 ✅',
        f'**失败**: {error_count} 条 ❌',
        f'**输出目录**: `{batch_output_dir}`',
        '',
        '## 详细结果',
        '',
        '| 序号 | 关键词 | 状态 | 输出目录 | 错误信息 |',
        '|------|--------|------|----------|----------|',
    ]
    
    for i, result in enumerate(results, 1):
        status = '✅ 成功' if result['success'] else '❌ 失败'
        output_dir_short = result['output_dir'].replace(batch_output_dir, '...') if result['output_dir'] else '-'
        error_info = result.get('error', '') or '-'
        if len(error_info) > 50:
            error_info = error_info[:50] + '...'
        summary_lines.append(f'| {i} | {result["keyword"]} | {status} | {output_dir_short} | {error_info} |')
    
    summary_lines.append('')
    summary_lines.append('## 生成的文件')
    summary_lines.append('')
    summary_lines.append('每条新闻播报包含以下文件：')
    summary_lines.append('- 新闻摘要_*.md')
    summary_lines.append('- 播报文案_*.txt')
    summary_lines.append('- titleAndLabels.txt')
    summary_lines.append('- cover.jpg')
    summary_lines.append('- 播报.mp3（或 播报_对话版.mp3）')
    summary_lines.append('- 深度解读文案.txt（可选）')
    summary_lines.append('- 事件深度解读.mp3（可选）')
    summary_lines.append('')
    
    if error_count > 0:
        summary_lines.append('## 错误详情')
        summary_lines.append('')
        for i, result in enumerate(results, 1):
            if not result['success']:
                summary_lines.append(f'### 第 {i} 条: {result["keyword"]}')
                summary_lines.append(f'```')
                summary_lines.append(result.get('error', '未知错误'))
                summary_lines.append(f'```')
                summary_lines.append('')
    
    summary_content = '\n'.join(summary_lines)
    summary_path = os.path.join(batch_output_dir, '生成结果汇总.md')
    with open(summary_path, 'w', encoding='utf-8-sig') as f:
        f.write(summary_content)
    print(f'\n[OK] 结果汇总已保存: {summary_path}')
    
    print('\n' + '=' * 60)
    print('✅ 批量生成任务全部完成!')
    print('=' * 60)
    
    return {
        'success': True,
        'total': len(filled_configs),
        'success_count': success_count,
        'error_count': error_count,
        'output_dir': batch_output_dir,
        'results': results
    }


if __name__ == '__main__':
    main()
