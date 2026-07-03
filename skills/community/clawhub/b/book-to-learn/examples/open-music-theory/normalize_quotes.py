#!/usr/bin/env python3
"""
中文引号规范化工具。
确保所有中文文本中使用中文双引号 \u201c...\u201d 而非英文直引号 \"。

用法:
  from normalize_quotes import normalize_chinese_quotes, normalize_dict_quotes

  text = normalize_chinese_quotes('他说"你好"')
  # 输出: 他说\u201c你好\u201d

  data = {'coreIdeaZh': '这是"重点"内容'}
  normalize_dict_quotes(data, ['coreIdeaZh', 'explanationZh', 'quoteZh'])
  # data 中所有指定字段的引号被规范化
"""

def normalize_chinese_quotes(text):
    """
    将文本中的英文直双引号 \" 替换为中文双引号 \u201c...\u201d。
    按左右交替规则配对：第一个 \" → \u201c，第二个 \" → \u201d，以此类推。

    Args:
        text: 待处理的文本字符串（可以为 None 或空）

    Returns:
        规范化后的文本。如果输入为 None 或非字符串，原样返回。
    """
    if not isinstance(text, str) or not text:
        return text

    result = []
    is_open = True
    for ch in text:
        if ch == '"':
            result.append('\u201c' if is_open else '\u201d')
            is_open = not is_open
        else:
            result.append(ch)
    return ''.join(result)


def normalize_dict_quotes(d, keys):
    """
    对字典中指定 key 的值做引号规范化（原地修改）。

    Args:
        d: 字典对象（可以为 None）
        keys: 需要规范化的 key 列表
    """
    if not isinstance(d, dict):
        return
    for key in keys:
        if key in d and isinstance(d[key], str):
            d[key] = normalize_chinese_quotes(d[key])


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

# terminologyZh 是 dict 类型，需要单独处理
def normalize_terminology_zh(terms_dict):
    """规范化 terminologyZh 中的所有中文译名。"""
    if not isinstance(terms_dict, dict):
        return terms_dict
    for key, value in terms_dict.items():
        if isinstance(value, str):
            terms_dict[key] = normalize_chinese_quotes(value)
    return terms_dict


# 一步规范化：对 translation JSON + payload 做完整引号修正
def normalize_all(zh=None, payload=None, language='en'):
    """
    对翻译 JSON 和 payload 的所有中文文本字段做引号规范化。

    Args:
        zh: translation JSON dict (英文书的翻译)
        payload: items.json 中的单条知识点
        language: 'zh' 或 'en'。中文书模式下同时规范化 payload

    Returns:
        (zh, payload) 元组（原地修改）
    """
    if zh:
        normalize_dict_quotes(zh, ZH_TEXT_KEYS)
        if 'terminologyZh' in zh:
            normalize_terminology_zh(zh['terminologyZh'])

    # 中文书模式：payload 中的字段即中文文本，也需规范化
    if payload and language == 'zh':
        normalize_dict_quotes(payload, PAYLOAD_CHINESE_KEYS)
        # 术语列表
        if 'terminology' in payload and isinstance(payload['terminology'], list):
            payload['terminology'] = [
                normalize_chinese_quotes(t) if isinstance(t, str) else t
                for t in payload['terminology']
            ]

    # 英文书模式：payload 是英文，但 relatedLinks 和 chapter 可能含中文
    if payload and language == 'en':
        if 'chapter' in payload:
            payload['chapter'] = normalize_chinese_quotes(payload['chapter'])

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

    # 测试 dict
    d = {'coreIdeaZh': '这是"重-要"内容', 'explanationZh': '包含"链接"的文本'}
    normalize_dict_quotes(d, ['coreIdeaZh', 'explanationZh', 'notExist'])
    assert d['coreIdeaZh'] == '这是\u201c重-要\u201d内容'
    assert d['explanationZh'] == '包含\u201c链接\u201d的文本'

    # 测试 terminologyZh
    terms = {'resilience': '韧-性', 'scalability': '可"扩展"性'}
    normalize_terminology_zh(terms)
    assert terms['scalability'] == '可\u201c扩展\u201d性'

    print('✅ 所有自测通过')
