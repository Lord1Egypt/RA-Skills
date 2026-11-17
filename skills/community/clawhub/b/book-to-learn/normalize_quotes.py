#!/usr/bin/env python3
"""
中文引号规范化工具。
确保所有中文文本中使用中文双引号 \u201c...\u201d 而非英文直引号 "。

**代码/URL 保护**（2026-10 v1.6.1）：处理前先把行内代码 `...`、围栏代码块 ```...```、
URL 替换为占位符，处理完再还原——保证 `print("你好")`、`https://a.com/s?q="数据"`
这类内容里的直引号绝不会被误改成中文弯引号。

用法:
  from normalize_quotes import normalize_chinese_quotes, normalize_dict_quotes

  # 智能模式（默认推荐）：仅中文语境替换，英文术语/代码/URL 保持原样
  text = normalize_chinese_text_only('他说"你好"，这是 `print("hi")` 的输出')
  # 输出: 他说\u201c你好\u201d，这是 `print("hi")` 的输出

  data = {'coreIdeaZh': '这是"重点"内容'}
  normalize_dict_quotes(data, ['coreIdeaZh', 'explanationZh', 'quoteZh'])
  # data 中所有指定字段的引号被规范化（默认 smart=True）
"""

import re

# 需要掩码保护的区段：围栏代码块 > 行内代码 > URL（交替顺序保证长匹配优先）
# URL 允许包含直引号与 CJK 字符（如 ?q="数据"），遇到空白/中文标点/弯引号即停
_PROTECT_RE = re.compile(
    r'```[\s\S]*?```'
    r'|`[^`\n]*`'
    r'|https?://[^\s\u201c\u201d\u2018\u2019，。；：！？、（）「」『』【】]*'
)
_PH_RE = re.compile('\x00(\\d+)\x00')


def _mask(text):
    """把代码/URL 区段替换为 \\x00n\\x00 占位符。返回 (新文本, 还原表)。"""
    store = []

    def _sub(m):
        store.append(m.group(0))
        return '\x00%d\x00' % (len(store) - 1)

    return _PROTECT_RE.sub(_sub, text), store


def _unmask(text, store):
    return _PH_RE.sub(lambda m: store[int(m.group(1))], text)


def _is_chinese_dominant(s):
    """判断字符串是否以中文为主（中文字符占比 > 30%）。"""
    if not s:
        return False
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', s))
    return chinese_chars / len(s) > 0.3


def _adjacent_cjk(text, i):
    """位置 i 的引号是否紧邻任一中文字符（前后 1 字符）。"""
    before = text[i - 1] if i > 0 else ''
    after = text[i + 1] if i + 1 < len(text) else ''
    cjk = re.compile(r'[\u4e00-\u9fff]')
    return bool(cjk.match(before) or cjk.match(after))


def normalize_chinese_quotes(text):
    """
    将文本中的英文直双引号 " 替换为中文双引号 \u201c...\u201d。
    按左右交替规则配对：第一个 " → \u201c，第二个 " → \u201d，以此类推。

    代码块/行内代码/URL 内的引号会被保护，不做替换。

    注意：此函数对传入的所有文本统一处理，不区分中英文。
    因此只应对已知为中文文本的字段调用（如 coreIdeaZh、explanationZh 等）。
    英文字段（如 coreIdea、explanation 等）不应调用此函数。

    Args:
        text: 待处理的文本字符串（可以为 None 或空）

    Returns:
        规范化后的文本。如果输入为 None 或非字符串，原样返回。
    """
    if not isinstance(text, str) or not text:
        return text

    masked, store = _mask(text)
    result = []
    is_open = True
    for ch in masked:
        if ch == '"':
            result.append('\u201c' if is_open else '\u201d')
            is_open = not is_open
        else:
            result.append(ch)
    return _unmask(''.join(result), store)


def normalize_chinese_text_only(text):
    """
    智能引号规范化：仅对中文文本段落中的引号进行替换，
    英文术语/代码片段/URL 中的引号保持原样。

    策略：
    1. 先掩码行内代码/代码块/URL（其中的引号绝不参与配对与替换）；
    2. 将剩余文本按引号对分割，对每对引号内的内容判断语言属性：
       若以中文为主（中文字符 > 30%），则替换为中文引号；否则保持英文引号；
    3. 引号对必须有资格才处理：开引号须紧邻中文字符（否则如 27" 这类英寸
       标记会与后文真实中文引号错误配对）；未配对的单个引号同样要求紧邻中文。

    此函数更安全，可用于混合中英文的文本字段（如 coreIdeaZh 中可能含英文术语）。
    """
    if not isinstance(text, str) or not text:
        return text

    masked, store = _mask(text)

    # 找到所有被引号包围的片段
    parts = []
    i = 0
    last_end = 0

    while i < len(masked):
        if masked[i] == '"':
            # 找到配对的结束引号
            j = i + 1
            while j < len(masked) and masked[j] != '"':
                j += 1

            if j < len(masked):
                # 找到了配对
                # 开引号必须紧邻中文字符才有资格按中文引号处理：
                # 否则（如 27" 对角线 这类英寸标记）会与后文真实中文引号错误配对
                if not _adjacent_cjk(masked, i):
                    i += 1
                    continue
                quoted_content = masked[i + 1:j]
                # 判断引号内内容是否以中文为主
                if _is_chinese_dominant(quoted_content):
                    # 中文内容 → 替换为中文引号
                    parts.append(masked[last_end:i])  # 引号前的内容
                    parts.append('\u201c')
                    parts.append(quoted_content)
                    parts.append('\u201d')
                    last_end = j + 1
                    i = j + 1
                    continue
                else:
                    # 英文内容 → 保持原样，跳过这一对
                    i = j + 1
                    continue
            else:
                # 未找到配对：单个引号。仅当紧邻中文字符才转换，否则原样保留
                # （英寸标记 27"、英文缩写等不应被误改）
                if _adjacent_cjk(masked, i):
                    parts.append(masked[last_end:i])
                    parts.append('\u201c' if (masked[:i].count('"') % 2 == 0) else '\u201d')
                    last_end = i + 1
                i += 1
                continue
        i += 1

    # 添加剩余内容
    parts.append(masked[last_end:])
    return _unmask(''.join(parts), store)


def normalize_dict_quotes(d, keys, smart=True):
    """
    对字典中指定 key 的值做引号规范化（原地修改）。

    Args:
        d: 字典对象（可以为 None）
        keys: 需要规范化的 key 列表
        smart: 是否使用智能模式（默认 True，推荐）——仅中文语境替换，
               英文术语/代码/URL 中的引号保持原样。smart=False 为
               全量交替替换（仍保护代码/URL），只用于已知纯中文的字段
    """
    if not isinstance(d, dict):
        return
    func = normalize_chinese_text_only if smart else normalize_chinese_quotes
    for key in keys:
        if key in d and isinstance(d[key], str):
            d[key] = func(d[key])


# 翻译 JSON 中的中文文本字段（英文书翻译模式）
ZH_TEXT_KEYS = [
    'topicZh',
    'coreIdeaZh',
    'explanationZh',
    'quoteZh',
    'applicationZh',
    'note',
]

# payload 中可能包含中文文本的字段（中文书模式 & 术语翻译）
PAYLOAD_CHINESE_KEYS = [
    'topic',
    'coreIdea',
    'explanation',
    'quote',
    'application',
    'chapter',
]


# 列表型中文文本字段（元素可能是字符串或 {href, textZh} 结构）
def _normalize_str_list(lst, func):
    return [func(x) if isinstance(x, str) else x for x in lst]


# terminologyZh 是 dict 类型，需要单独处理
def normalize_terminology_zh(terms_dict, smart=True):
    """规范化 terminologyZh 中的所有中文译名。"""
    if not isinstance(terms_dict, dict):
        return terms_dict
    func = normalize_chinese_text_only if smart else normalize_chinese_quotes
    for key, value in terms_dict.items():
        if isinstance(value, str):
            terms_dict[key] = func(value)
    return terms_dict


# 一步规范化：对 translation JSON + payload 做完整引号修正
def normalize_all(zh=None, payload=None, language='en', smart=True):
    """
    对翻译 JSON 和 payload 的所有中文文本字段做引号规范化。

    Args:
        zh: translation JSON dict (英文书的翻译)
        payload: items.json 中的单条知识点
        language: 'zh' 或 'en'。中文书模式下同时规范化 payload
        smart: 是否使用智能模式（默认 True），对可能混有英文术语的
               中文字段，仅替换中文环境中的引号，保留英文术语/代码/URL 中的引号

    Returns:
        (zh, payload) 元组（原地修改）
    """
    if zh:
        normalize_dict_quotes(zh, ZH_TEXT_KEYS, smart=smart)
        if 'terminologyZh' in zh:
            normalize_terminology_zh(zh['terminologyZh'], smart=smart)
        # 列表型字段：pointsZh（字符串列表）与 relatedLinksZh（{href, textZh} 列表）
        func = normalize_chinese_text_only if smart else normalize_chinese_quotes
        if isinstance(zh.get('pointsZh'), list):
            zh['pointsZh'] = _normalize_str_list(zh['pointsZh'], func)
        if isinstance(zh.get('relatedLinksZh'), list):
            zh['relatedLinksZh'] = [
                {**item, 'textZh': func(item['textZh'])}
                if isinstance(item, dict) and isinstance(item.get('textZh'), str) else item
                for item in zh['relatedLinksZh']
            ]

    # 中文书模式：payload 中的字段即中文文本，也需规范化
    if payload and language == 'zh':
        normalize_dict_quotes(payload, PAYLOAD_CHINESE_KEYS, smart=smart)
        # 术语列表
        if 'terminology' in payload and isinstance(payload['terminology'], list):
            func = normalize_chinese_text_only if smart else normalize_chinese_quotes
            payload['terminology'] = [
                func(t) if isinstance(t, str) else t
                for t in payload['terminology']
            ]
        # 要点列表（长图引擎用）
        if isinstance(payload.get('points'), list):
            func = normalize_chinese_text_only if smart else normalize_chinese_quotes
            payload['points'] = _normalize_str_list(payload['points'], func)

    # 英文书模式：payload 是英文，但 chapter 可能含中文
    if payload and language == 'en':
        if 'chapter' in payload:
            payload['chapter'] = normalize_chinese_text_only(payload['chapter'])

    return zh, payload


if __name__ == '__main__':
    # 自测
    test_text = '他说"你好"，她说"再见"'
    result = normalize_chinese_quotes(test_text)
    expected = '他说\u201c你好\u201d，她说\u201c再见\u201d'
    assert result == expected, f'Expected: {expected!r}, Got: {result!r}'

    # 测试奇数引号
    test_odd = '"你好"世界"'
    result_odd = normalize_chinese_quotes(test_odd)
    expected_odd = '\u201c你好\u201d世界\u201c'
    assert result_odd == expected_odd, f'Expected: {expected_odd!r}, Got: {result_odd!r}'

    # 测试空值和 None
    assert normalize_chinese_quotes(None) is None
    assert normalize_chinese_quotes('') == ''

    # 测试 dict（默认 smart=True）
    d = {'coreIdeaZh': '这是"重-要"内容', 'explanationZh': '包含"链接"的文本'}
    normalize_dict_quotes(d, ['coreIdeaZh', 'explanationZh', 'notExist'])
    assert d['coreIdeaZh'] == '这是\u201c重-要\u201d内容'
    assert d['explanationZh'] == '包含\u201c链接\u201d的文本'

    # 测试 terminologyZh
    terms = {'resilience': '韧-性', 'scalability': '可"扩展"性'}
    normalize_terminology_zh(terms, smart=False)
    assert terms['scalability'] == '可\u201c扩展\u201d性'

    # 测试智能模式：中文文本中的英文术语不应被改
    smart_text = '哈希表是一种"key-value"存储结构，其中"哈希函数"是核心'
    smart_result = normalize_chinese_text_only(smart_text)
    assert '"key-value"' in smart_result, f'English term quotes should stay: {smart_result!r}'
    assert '\u201c哈希函数\u201d' in smart_result, f'Chinese term quotes should be converted: {smart_result!r}'

    # 测试纯英文不被误改
    en_text = 'He said "hello" and she said "goodbye"'
    en_result = normalize_chinese_text_only(en_text)
    assert en_result == en_text, f'Pure English should NOT be modified: {en_result!r}'

    # —— v1.6.1 新增：代码 / URL / 未配对引号保护 ——
    code_text = '调用 `print("你好")` 函数输出"结果"'
    code_result = normalize_chinese_text_only(code_text)
    assert '`print("你好")`' in code_result, f'inline code must be protected: {code_result!r}'
    assert '\u201c结果\u201d' in code_result, f'Chinese quotes still converted: {code_result!r}'

    fence_text = '示例如下：\n```\nprint("hi")\n```\n这就是"示例"'
    fence_result = normalize_chinese_text_only(fence_text)
    assert 'print("hi")' in fence_result, f'fenced code must be protected: {fence_result!r}'
    assert '\u201c示例\u201d' in fence_result

    url_text = '访问 https://a.com/s?q="数据" 查看"结果"'
    url_result = normalize_chinese_text_only(url_text)
    assert 'https://a.com/s?q="数据"' in url_result, f'URL must be protected: {url_result!r}'
    assert '\u201c结果\u201d' in url_result

    url_raw = normalize_chinese_quotes('访问 https://a.com/s?q="数据" 查看')
    assert 'https://a.com/s?q="数据"' in url_raw, f'URL must be protected in raw mode: {url_raw!r}'

    inch = '屏幕尺寸 27" 对角线，他说"好"'
    inch_result = normalize_chinese_text_only(inch)
    assert '27"' in inch_result, f'inch mark must stay: {inch_result!r}'
    assert '\u201c好\u201d' in inch_result

    cross = '他说"详见 https://a.com/x?p="q" 的文档"'
    cross_result = normalize_chinese_text_only(cross)
    assert cross_result == '他说\u201c详见 https://a.com/x?p="q" 的文档\u201d', \
        f'cross-boundary mismatch: {cross_result!r}'

    zh = {'pointsZh': ['第一"点"', '第二点'], 'relatedLinksZh': [{'href': 'https://a.com', 'textZh': '带"引号"的标题'}]}
    normalize_all(zh, None, 'en', smart=True)
    assert zh['pointsZh'][0] == '第一\u201c点\u201d'
    assert zh['relatedLinksZh'][0]['textZh'] == '带\u201c引号\u201d的标题'

    zh2 = {'coreIdeaZh': '哈希表是一种"key-value"存储结构，其中"哈希函数"是核心'}
    payload = {'coreIdea': 'A "key-value" store', 'chapter': '第一章'}
    zh_out, payload_out = normalize_all(zh2, payload, 'en', smart=True)
    assert '"key-value"' in zh_out['coreIdeaZh'], f'Smart mode should preserve English quotes: {zh_out["coreIdeaZh"]!r}'
    assert '\u201c哈希函数\u201d' in zh_out['coreIdeaZh'], f'Smart mode should convert Chinese quotes: {zh_out["coreIdeaZh"]!r}'
    assert payload_out['coreIdea'] == 'A "key-value" store', f'English payload should NOT be touched: {payload_out["coreIdea"]!r}'

    print('[OK] 所有自测通过')
