# -*- coding: utf-8 -*-
"""
Content Cleaner - 内容清洗标准化模块
用于清洗 Web Search（Tavily）返回的原始内容中的噪音。
核心策略：质量评分制 → 低于阈值直接丢弃事件正文，只保留标题。
"""
import re
import zhconv

# ─────────────────────────────────────────────
# 截断检测与句末补全工具
# ─────────────────────────────────────────────

SENTENCE_END_CHARS = '。？！?!.'


def to_simplified(text):
    """将繁体中文转换为简体中文"""
    return zhconv.convert(text, 'zh-cn')

def is_truncated_content(text: str) -> bool:
    """
    判断文本（事件正文/内容）是否在句子中途截断（不可用）。

    适用场景：事件正文、内容字段。
    判断标准：
    1. 文本极短（< 20 字符）→ 截断残留
    2. 括号未闭合 → 来源截断
    3. 以省略符结尾 → 截断
    4. 以字母/数字结尾 + 无句末标点 → 截断
    """
    if not text or not isinstance(text, str):
        return True
    s = text.strip()
    if not s:
        return True
    if len(s) < 20:
        return True
    if s.count('(') > s.count(')') or s.count('（') > s.count('）'):
        return True
    if any(s.rstrip().endswith(m) for m in ['...', '…']):
        return True
    last_char = s[-1] if s else ''
    # 仅 ASCII 字母/数字才表示英文章节截断（中文不在此列）
    if last_char.encode('utf-8', errors='ignore').isascii() and last_char.isalnum():
        if not any(s.rstrip().endswith(p) for p in SENTENCE_END_CHARS):
            return True
    return False


def ensure_sentence_end(text: str) -> str:
    """
    确保文本以完整句子结尾。
    如果文本末尾无句末标点（。？！?!.），则补上句号 '。'。
    如果文本已完整（有句末标点），保持原样。
    
    注意：已截断的文本（is_truncated 返回 True）不应调用此函数，
    应直接丢弃，而非补全。
    """
    if not text or not isinstance(text, str):
        return text
    
    s = text.strip()
    if not s:
        return s
    
    # 检查是否已有完整句子结尾
    if any(s.rstrip().endswith(p) for p in SENTENCE_END_CHARS):
        return s  # 已完整，保持原样
    
    # 无句末标点 → 补上句号
    return s + '。'


def is_meaningful_enterprise_item(item: dict) -> bool:
    """
    判断企业动态条目是否有实际内容（不被截断污染）。
    用于 batch_clean_enterprise 过滤阶段。
    
    判断标准：
    1. 公司名有实质内容（≥ 4 字符，不含纯数字/标点）
    2. 事件正文非截断（is_truncated 返回 False）
    3. 事件正文长度 ≥ 20 字符（短于 20 基本是残留碎片）
    """
    company = (item.get('公司') or '').strip()
    event = (item.get('事件') or '').strip()
    
    # 公司名必须有实质内容
    if len(company) < 4:
        return False
    
    # 公司名不能是纯数字/标点/英文单词
    if re.match(r'^[\d\s.,;:\'\"、。！？?!]+$', company):
        return False
    
    # 事件正文必须非截断
    if is_truncated_content(event):
        return False
    
    # 事件正文必须有内容
    if len(event) < 20:
        return False
    
    return True


def is_meaningful_policy_item(item: dict) -> bool:
    """
    判断政策动态条目是否有实质内容。
    
    判断标准：
    1. 标题有实质内容（≥ 6 字符）
    2. 标题非截断
    3. 内容非截断（或内容为空但标题可独立作为摘要）
    """
    title = (item.get('标题') or '').strip()
    content = (item.get('内容') or '').strip()
    
    if len(title) < 6:
        return False
    
    # 标题截断 → 视为无效（政策动态标题不可截断）
    if is_truncated_content(title):
        return False
    
    # 内容如果存在且非截断 → 通过
    if content and not is_truncated(content):
        return True
    
    # 内容为空或截断 → 仅当标题足够长（≥ 30 字符）时可接受
    if len(title) >= 30:
        return True
    
    return False

# -*- coding: utf-8 -*-
"""
Content Cleaner - 内容清洗标准化模块
用于清洗 Web Search（Tavily）返回的原始内容中的噪音。
核心策略：
  1. 编码质量检测 → 乱码直接丢弃
  2. 质量评分制 → 质量过低时事件正文降级为标题
  3. 多轮正则清洗
"""
import re

# ─────────────────────────────────────────────
# 噪音词集合（用于快速查找）
# ─────────────────────────────────────────────
NOISE_WORDS = {
    'logo', 'user_photo', 'search button', 'search result',
    'home', 'close', 'login', 'logout', 'sign up', 'sign in',
    '打开app', '下载app', 'app下载', '下载财经app', '更多资讯',
    '热门资讯', '海量资讯', '扫码下载', '点击下载',
    '首页', '下载', '登录', '注册', '退出', '搜索', '关于',
    '行情', '资讯', '财经', '港美股', '关闭',
    'cmoney', '华盛通', '富途证券', '雪球', '智通财经',
    '东方财富', '同花顺', '华尔街见闻',
    'source', 'about us', 'advertisement', 'sponsored', 'copyright',
    '######', '#####', '####', '###', '##', '#',
    '------', '-----', '----', '---', '--',
    '======', '=====', '====', '===', '==',
    # ── 导航/标签栏碎片词 ──
    '要闻', '金融', '评论', '产经', '创投', '滚动',
    '公司', '新股', '基金', '港美股',
    '京', '津', '冀', '晋', '蒙', '辽', '吉', '黑',
    '沪', '苏', '浙', '皖', '闽', '赣', '鲁', '豫',
    '鄂', '湘', '粤', '桂', '琼', '渝', '川', '黔',
    '滇', '藏', '陕', '甘', '青', '宁', '新',
    '财经', '股票', '期货', '外汇', '债券', '理财',
    '视频', '直播', '品牌', '活动', '一带一路',
    '大湾区', '文旅', '投资通',
}

# 预编译噪音正则
_NOISE_REGEX = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r'^\s*#{1,6}\s*[\u4e00-\u9fffA-Za-z0-9]+\s*#*\s*$',
        r'^\s*#{1,6}\s*$',
        r'^\s*ETF\s+#{0,5}.*About\s+Us.*#*\s*$',
        r'^\s*About\s+Us.*$',
        r'^\s*AI\s+Recommended.*$',
        r'^\s*Recommended\s+Charts.*$',
        r'^搜索结果', r'^搜索历史清空', r'^打开App', r'^APP下载',
        r'^热门资讯\s*>\s*正文', r'^#+\s*热门资讯',
        r'^\s*>\s*正文',
        r'^繁體', r'^简体中文', r'^繁體中文', r'^英文',
        r'^語言', r'^Language',
        r'^\s*\|\s*CMoney\s*\|', r'^\s*\|?\s*富途\s*\|?', r'^\s*\|?\s*雪球\s*\|?',
        r'^\s*[\u4e00-\u9fff]{1,4}\s+[\u4e00-\u9fff]{1,4}\s+[\u4e00-\u9fff]{1,4}\s*$',
        r'\[\s*PDF\s*\]',
        r'第\s*\d+\s*页[/\s]第\s*\d+\s*页?',
        r'^\s*<\s*[\u4e00-\u9fff()0-9\s]+\s*>\s*$',
        r'^\s*\[[\u4e00-\u9fff()0-9\s]+\]\s*$',
        r'\[\s*\.\.\.\s*\]', r'\(\s*\.\.\.\s*\)',
        r'来源[：:]\s*[^\n]{2,30}$',
        r'时间[：:]\s*[\d\-\/\s年岳月日:]+',
        r'\s+\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?\s+\d{1,2}:\d{1,2}\s*$',
        r'\s+\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?\s*$',
        r'[\u4e00-\u9fff]{2,6}\s+\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{1,2}',
        r'第一财经\s+[\u4e00-\u9fff]{2,4}\s+\d{4}[-/]\d{1,2}[-/]\d{1,2}',
        r'福布斯中国新版网站试运营中.*',
        r'如需浏览旧版.*APP下载.*',
        r'未经授权.*转载.*',
        r'责任编辑\s*：?\s*[^\n]{0,20}$',
        r'海量资讯.*$', r'更多财经资讯.*$',
        r'^.*CMoney.*$', r'^.*富途.*$', r'^.*雪球.*$',
        r'^.*东方财富.*$', r'^.*华盛通.*$', r'^.*同花顺.*$',
        r'^[a-zA-Z]{1,15}\s*$',
        r'^\s*[|\\/_－-]{3,}\s*$',
        r'^[　\s]+$',
        # ── 导航/标签栏噪声行 ──
        # 连续3+个短词（省市区/栏目简称）拼成的碎片行，如"要闻 金融 评论 产经 创投 ..."
        r'^[\u4e00-\u9fff]{1,4}\s+[\u4e00-\u9fff]{1,4}\s+[\u4e00-\u9fff]{1,4}\s+[\u4e00-\u9fff]{1,4}(\s+[\u4e00-\u9fff]{1,4})+$',
        # 一行内出现5个以上（含）省/直辖市/自治区/特别行政区简称
        r'^(?:京|津|冀|晋|蒙|辽|吉|黑|沪|苏|浙|皖|闽|赣|鲁|豫|鄂|湘|粤|桂|琼|渝|川|黔|滇|藏|陕|甘|青|宁|新){5,}.*$',
        # 明显是导航菜单的碎片的行（短词+短词+短词 无动词）
        r'^[\u4e00-\u9fff]{1,4}\s+(?:[\u4e00-\u9fff]{1,4}\s+){5,}[\u4e00-\u9fff]{1,4}\s*$',
        # 单行超长且全由短词（含省简称/栏目词）组成（非正文）
        r'^(?:要闻|金融|评论|产经|创投|滚动|新股|基金|股票|期货|外汇|债券|理财|视频|直播)[\s\u4e00-\u9fff]{20,}$',
    ]
]


def is_noisy_line(line):
    if not line or len(line.strip()) < 2:
        return True
    s = line.strip()
    if s.lower() in NOISE_WORDS:
        return True
    for regex in _NOISE_REGEX:
        if regex.match(s):
            return True
    return False


def check_encoding_quality(text):
    """
    检测文本编码质量。
    返回 True 表示编码正常，返回 False 表示严重乱码应丢弃。
    """
    if not text:
        return False
    # 统计可疑字符
    total = len(text)
    # 非ASCII、非CJK、非常用符号的字符（如各种乱码块）
    bad_chars = len(re.findall(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', text))
    # 控制字符比例
    if total > 0 and bad_chars / total > 0.05:
        return False
    return True


def calc_content_quality(text):
    """
    计算内容质量分数 [0, 1]。
    低于 0.3 → 事件正文不可用，降级为标题。
    """
    if not text or len(text) < 20:
        return 0.0
    total = len(text)
    chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
    ratio = chinese / total if total > 0 else 0
    lines = text.split('\n')
    noisy_count = sum(1 for l in lines if is_noisy_line(l))
    noise_line_ratio = noisy_count / max(1, len(lines))
    # 中文占比 × 0.6 + 噪音行少 × 0.4
    score = ratio * 0.6 + (1 - noise_line_ratio) * 0.4
    return max(0.0, min(1.0, score))


def clean_content(text):
    """清洗正文：逐行过滤噪音 → 行内清理 → 合并前3段 → 截断至350字"""
    if not text:
        return ''
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line or is_noisy_line(line):
            continue
        line = re.sub(r'#{1,6}', '', line)
        line = re.sub(r'\s*\|\s*CMoney\s*\|?', '', line, flags=re.IGNORECASE)
        line = re.sub(r'\s*\|?\s*富途\s*\|?', '', line)
        line = re.sub(r'\s*\|?\s*雪球\s*\|?', '', line)
        line = re.sub(r'\s*来源[：:]\s*', '。', line)
        line = re.sub(r'\s*时间[：:]\s*[\d\-\/\s年岳月日:]+', '', line)
        line = re.sub(r'\[\s*PDF\s*\]', '', line)
        line = re.sub(r'第\s*\d+\s*页[/\s]第\s*\d+\s*页?', '', line)
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'\[\s*\.\.\.\s*\]', '...', line)
        line = re.sub(r'\(\s*\.\.\.\s*\)', '(...)', line)
        line = re.sub(r'\s{2,}', ' ', line)
        line = re.sub(r'[\u3000]+', '', line)
        line = line.strip()
        if len(line) >= 10:
            cleaned.append(line)
    if not cleaned:
        return ''
    result = ' '.join(cleaned[:3])
    result = result[:350] + '...' if len(result) > 350 else result
    # 繁→简转换（clean_title/clean_policy_item 已在各自入口转换公司/标题，此处补转换正文内容）
    return to_simplified(result)


def clean_title(text):
    """清洗标题"""
    if not text:
        return ''
    text = text.strip()
    text = re.sub(r'^\s*\[\s*PDF\s*\]\s*', '', text)
    text = re.sub(r'新浪财经热点小时报[丨|][^\n]*$', '', text)
    text = re.sub(r'新浪财经[^\n]*小时报[^\n]*$', '', text)
    text = re.sub(r'新浪财经[^\n]*热点速递[^\n]*$', '', text)
    text = re.sub(r'[|_－-][^\n|_-]{2,20}$', '', text)
    text = re.sub(r'[-_]\s*[^\n-]+$', '', text)
    text = re.sub(r'\s+[\u4e00-\u9fff]{2,4}\s+\d{4}[-/]\d{1,2}[-/]\d{1,2}\s*$', '', text)
    text = re.sub(r'\s+\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{1,2}\s*$', '', text)
    text = re.sub(r'[，。、；：]{3,}', '。', text)
    text = text.strip()
    return text if len(text) >= 6 else ''


def clean_policy_item(raw):
    """清洗单条政策动态"""
    title_raw = (raw.get('标题') or raw.get('title') or '').strip()
    content_raw = (raw.get('内容') or raw.get('content') or '').strip()

    # 编码质量检测
    if not check_encoding_quality(title_raw) or not check_encoding_quality(content_raw):
        return None

    clean_t = clean_title(title_raw)
    if not clean_t:
        return None

    # 内容质量判断
    quality = calc_content_quality(content_raw)
    if quality >= 0.3:
        clean_c = clean_content(content_raw)
    else:
        clean_c = ''

    if not clean_c or len(clean_c) < 30:
        clean_c = clean_t[:200]

    # 截断检测：内容截断 → 丢弃整条数据
    if is_truncated_content(clean_c):
        return None

    # 补句末标点
    clean_t = ensure_sentence_end(clean_t)
    clean_c = ensure_sentence_end(clean_c)

    return {
        '标题': clean_t,
        '内容': clean_c,
        '来源': to_simplified((raw.get('来源') or raw.get('source') or '').strip()),
        '链接': to_simplified((raw.get('链接') or raw.get('url') or '').strip()),
        '时间': to_simplified((raw.get('时间') or raw.get('published_date') or '').strip())
    }


def clean_enterprise_item(raw):
    """清洗单条企业动态"""
    company_raw = (raw.get('公司') or raw.get('title') or '').strip()
    event_raw = (raw.get('事件') or raw.get('content') or '').strip()

    # 编码质量检测
    if not check_encoding_quality(company_raw) or not check_encoding_quality(event_raw):
        return None

    clean_c = clean_title(company_raw)
    if not clean_c:
        return None

    # 清理公司名媒体后缀
    clean_c = re.sub(r'[|｜]\s*CMoney\s*$', '', clean_c, flags=re.IGNORECASE)
    clean_c = re.sub(r'[|｜]\s*富途\s*$', '', clean_c)
    clean_c = re.sub(r'[|｜]\s*雪球\s*$', '', clean_c)
    clean_c = re.sub(r'[|｜]\s*[\u4e00-\u9fff]+\s*$', '', clean_c)
    clean_c = re.sub(r'[-_]\s*[^\n-]+$', '', clean_c)
    clean_c = clean_c.strip()
    if len(clean_c) < 4:
        return None

    quality = calc_content_quality(event_raw)
    if quality >= 0.3:
        clean_e = clean_content(event_raw)
    else:
        clean_e = ''

    # 截断检测：事件正文截断 → 丢弃整条数据
    if is_truncated_content(clean_e):
        return None

    if not clean_e or len(clean_e) < 20:
        clean_c = to_simplified(clean_c)
        clean_e = clean_c
    else:
        clean_c = to_simplified(clean_c)

    # 补句末标点 + 繁→简
    clean_c = to_simplified(ensure_sentence_end(clean_c))
    clean_e = to_simplified(ensure_sentence_end(clean_e))

    return {
        '公司': clean_c,
        '事件': clean_e,
        '时间': to_simplified((raw.get('时间') or raw.get('published_date') or '').strip()),
        '来源': to_simplified((raw.get('来源') or raw.get('source') or '').strip())
    }


def batch_clean_policy(items):
    seen = set()
    result = []
    for item in (items or []):
        c = clean_policy_item(item)
        if not c:
            continue
        key = c['标题'][:30]
        if key in seen:
            continue
        seen.add(key)
        result.append(c)
    return result


def batch_clean_enterprise(items):
    seen = set()
    result = []
    for item in (items or []):
        c = clean_enterprise_item(item)
        if not c:
            continue
        key = c['公司'][:20] + c['事件'][:20]
        if key in seen:
            continue
        seen.add(key)
        result.append(c)
    return result


def clean_calendar_item(raw):
    """清洗单条经济数据日历条目"""
    time_raw = (raw.get('时间') or raw.get('title') or '').strip()
    event_raw = (raw.get('事件') or raw.get('content') or '').strip()

    if not time_raw or len(time_raw) < 4:
        return None
    if not event_raw or len(event_raw) < 5:
        return None

    # 编码质量检测
    if not check_encoding_quality(time_raw) or not check_encoding_quality(event_raw):
        return None

    # 时间字段：只清洗标题（去来源后缀）
    clean_t = clean_title(time_raw)
    if not clean_t:
        clean_t = time_raw[:60]  # 保底用原始

    # 事件字段：质量评分
    quality = calc_content_quality(event_raw)
    if quality >= 0.3:
        clean_e = clean_content(event_raw)
    else:
        clean_e = event_raw[:200]

    return {
        '时间': to_simplified(clean_t),
        '事件': to_simplified(clean_e)
    }


def batch_clean_calendar(items):
    """批量清洗经济日历数据"""
    seen = set()
    result = []
    for item in (items or []):
        c = clean_calendar_item(item)
        if not c:
            continue
        key = c['时间'][:20] + c['事件'][:20]
        if key in seen:
            continue
        seen.add(key)
        result.append(c)
    return result
