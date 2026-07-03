#!/usr/bin/env python3
"""
中文引号规范化工具。
确保所有中文文本中使用中文双引号 \u201c...\u201d 而非英文直引号 "。

用法:
  from normalize_quotes import normalize_chinese_quotes, normalize_dict_quotes

  text = normalize_chinese_quotes('他说"你好"')
  # 输出: 他说\u201c你好\u201d

  data = {'coreIdeaZh': '这是"重点"内容'}
  normalize_dict_quotes(data, ['coreIdeaZh', 'explanationZh', 'quoteZh'])
  # data 中所有指定字段的引号被规范化
"""

import re

def normalize_chinese_quotes(text):
    """
    将文本中的英文直双引号 " 替换为中文双引号 \u201c...\u201d。
    按左右交替规则配对：第一个 " → \u201c，第二个 " → \u201d，以此类推。

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

    result = []
    is_open = True
    for ch in text:
        if ch == '"':
            result.append('\u201c' if is_open else '\u201d')
            is_open = not is_open
        else:
            result.append(ch)
    return ''.join(result)


def _is_chinese_dominant(s):
    """判断字符串是否以中文为主（中文字符占比 > 30%）。"""
    if not s:
        return False
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', s))
    return chinese_chars / len(s) > 0.3


def normalize_chinese_text_only(text):
    """
    智能引号规范化：仅对中文文本段落中的引号进行替换，
    英文术语/代码片段中的引号保持原样。

    策略：将文本按引号对分割，对每对引号内的内容判断语言属性。
    若引号内内容以中文为主（中文字符 > 30%），则将该对引号替换为中文引号；
    否则保持英文引号。

    此函数更安全，可用于混合中英文的文本字段（如 coreIdeaZh 中可能含英文术语）。
    """
    if not isinstance(text, str) or not text:
        return text

    # 找到所有被引号包围的片段
    parts = []
    i = 0
    last_end = 0

    while i < len(text):
        if text[i] == '"':
            # 找到配对的结束引号
            j = i + 1
            while j < len(text) and text[j] != '"':
                j += 1

            if j < len(text):
                # 找到了配对
                quoted_content = text[i+1:j]
                # 判断引号内内容是否以中文为主
                if _is_chinese_dominant(quoted_content):
                    # 中文内容 → 替换为中文引号
                    parts.append(text[last_end:i])  # 引号前的内容
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
                # 未找到配对，这是单个引号
                # 检查上下文判断
                context = text[max(0, i-20):i]
                if _is_chinese_dominant(context):
                    parts.append(text[last_end:i])
                    parts.append('\u201c' if (text[:i].count('"') % 2 == 0) else '\u201d')
                    last_end = i + 1
                i += 1
                continue
        i += 1

    # 添加剩余内容
    parts.append(text[last_end:])
    return ''.join(parts)


def normalize_dict_quotes(d, keys, smart=False):
    """
    对字典中指定 key 的值做引号规范化（原地修改）。

    Args:
        d: 字典对象（可以为 None）
        keys: 需要规范化的 key 列表
        smart: 是否使用智能模式（normalize_chinese_text_only），
               适用于可能混有英文术语的中文字段
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
               中文字段，仅替换中文环境中的引号，保留英文术语中的引号

    Returns:
        (zh, payload) 元组（原地修改）
    """
    if zh:
        normalize_dict_quotes(zh, ZH_TEXT_KEYS, smart=smart)
        if 'terminologyZh' in zh:
            normalize_terminology_zh(zh['terminologyZh'], smart=smart)

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

    # 测试 dict
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
    print(f'Smart test input: {smart_text!r}')
    print(f'Smart test output: {smart_result!r}')
    assert '"key-value"' in smart_result, f'English term quotes should stay: {smart_result!r}'
    assert '\u201c哈希函数\u201d' in smart_result, f'Chinese term quotes should be converted: {smart_result!r}'

    # 测试纯英文不被误改
    en_text = 'He said "hello" and she said "goodbye"'
    en_result = normalize_chinese_text_only(en_text)
    assert en_result == en_text, f'Pure English should NOT be modified: {en_result!r}'

    # 测试 normalize_all 智能模式
    zh = {'coreIdeaZh': '哈希表是一种"key-value"存储结构，其中"哈希函数"是核心'}
    payload = {'coreIdea': 'A "key-value" store', 'chapter': '第一章'}
    zh_out, payload_out = normalize_all(zh, payload, 'en', smart=True)
    assert '"key-value"' in zh_out['coreIdeaZh'], f'Smart mode should preserve English quotes: {zh_out["coreIdeaZh"]!r}'
    assert '\u201c哈希函数\u201d' in zh_out['coreIdeaZh'], f'Smart mode should convert Chinese quotes: {zh_out["coreIdeaZh"]!r}'
    assert payload_out['coreIdea'] == 'A "key-value" store', f'English payload should NOT be touched: {payload_out["coreIdea"]!r}'

    print('✅ 所有自测通过')
