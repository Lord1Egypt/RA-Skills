"""
文本处理工具

摘要生成、段落切分、关键词提取等。
纯Python实现，无外部依赖。
"""

import re
from typing import List


def count_chinese_chars(text: str) -> int:
    """统计中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def generate_summary(text: str, max_chars: int = 100) -> str:
    """
    生成文本摘要（提取式：取前1-2句）

    无外部依赖，适用于知识库文档的快速摘要。
    智能体在需要更精确摘要时可自行处理。
    """
    sentences = re.split(r'[。！？!?\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return text[:max_chars]

    # 取前1-2句，不超过max_chars
    summary = sentences[0]
    if len(summary) < max_chars and len(sentences) > 1:
        second = sentences[1]
        if len(summary) + len(second) + 1 <= max_chars:
            summary = summary + "。" + second
        else:
            summary = summary + "。"

    return summary[:max_chars]


def chunk_text(text: str, chunk_size: int = 300) -> List[str]:
    """
    将文本切分为段落（用于向量索引）

    按句号切分，每段不超过chunk_size字。
    """
    sentences = re.split(r'([。！？!?])', text)
    chunks = []
    current = ""

    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
        if count_chinese_chars(current + sentence) > chunk_size and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current += sentence

    if len(sentences) % 2 == 1 and sentences[-1].strip():
        current += sentences[-1]

    if current.strip():
        chunks.append(current.strip())

    return [c for c in chunks if c.strip()]


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """
    提取关键词（基于词频的简易方法）

    无jieba时使用字频；有jieba时自动使用分词。
    """
    try:
        import jieba
        words = [w for w in jieba.cut(text) if len(w) >= 2 and w.strip()]
    except ImportError:
        # 降级：提取双字组合
        chars = re.findall(r'[\u4e00-\u9fff]', text)
        words = [chars[i] + chars[i + 1] for i in range(len(chars) - 1)]

    # 过滤停用词
    stop_words = {"的是", "在了", "一个", "我们", "他们", "她们", "这个", "那个",
                  "不是", "没有", "就是", "也是", "可以", "已经", "因为", "所以",
                  "但是", "如果", "虽然", "而且", "或者", "以及", "还是", "什么",
                  "怎么", "这样", "那样", "这些", "那些", "自己", "大家"}
    words = [w for w in words if w not in stop_words]

    # 词频统计
    from collections import Counter
    counter = Counter(words)
    return [w for w, _ in counter.most_common(top_n)]


def split_sentences(text: str) -> List[str]:
    """将文本切分为句子（支持省略号和破折号）"""
    text = text.replace("……", "||ELLIPSIS||").replace("——", "||DASH||")
    parts = re.split(r'([。！？!?])', text)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        s = parts[i].strip() + parts[i + 1]
        if s.strip():
            sentences.append(s.strip())
    if len(parts) % 2 == 1 and parts[-1].strip():
        sentences.append(parts[-1].strip())

    result = []
    for s in sentences:
        s = s.replace("||ELLIPSIS||", "……").replace("||DASH||", "——")
        sub_parts = re.split(r'(……|——)', s)
        current = ""
        for part in sub_parts:
            if part in ("……", "——"):
                current += part
                if current.strip():
                    result.append(current.strip())
                current = ""
            else:
                current += part
        if current.strip():
            result.append(current.strip())

    return result
