from __future__ import annotations

import re
from typing import Iterable


STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "for", "in", "on", "at", "by",
    "is", "are", "was", "were", "be", "been", "with", "from", "as", "that",
    "this", "it", "its", "their", "our", "will", "has", "have", "had",
    "宣布", "发布", "推出", "上线", "完成", "获得", "进行", "相关", "最新", "正式",
    "公司", "企业", "方面", "此次", "其中", "表示", "消息", "今日", "近日"
}


def normalize_text(text: str | None) -> str:
    """
    基础文本归一化：
    - 小写
    - 去HTML残留空白
    - 去多余标点
    - 空白折叠
    """
    if not text:
        return ""

    text = text.lower().strip()

    # 全角空格 -> 半角空格
    text = text.replace("\u3000", " ")

    # 常见连接符统一
    text = text.replace("—", "-").replace("–", "-").replace("_", " ")

    # 去 URL
    text = re.sub(r"https?://\S+", " ", text)

    # 保留中英文、数字、空格；其余多转为空格
    text = re.sub(r"[^0-9a-z\u4e00-\u9fff\s]", " ", text)

    # 空白折叠
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_title(title: str | None) -> str:
    """
    标题归一化，适合做去重比对。
    """
    text = normalize_text(title)

    # 去常见媒体前后缀噪音
    patterns = [
        r"^快讯\s+",
        r"^独家\s+",
        r"^重磅\s+",
        r"\s+全文$",
        r"\s+更新$",
    ]
    for p in patterns:
        text = re.sub(p, "", text)

    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_text(text: str | None) -> list[str]:
    """
    简单分词：
    - 英文按空格切
    - 中文连续文本先按空格切；对未分开的中文保留整段
    """
    normalized = normalize_text(text)
    if not normalized:
        return []

    tokens = normalized.split()

    result: list[str] = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token in STOPWORDS:
            continue
        if len(token) == 1 and not token.isdigit():
            continue
        result.append(token)

    return result


def jaccard_similarity(tokens_a: Iterable[str], tokens_b: Iterable[str]) -> float:
    set_a = set(tokens_a)
    set_b = set(tokens_b)

    if not set_a or not set_b:
        return 0.0

    inter = set_a & set_b
    union = set_a | set_b
    return len(inter) / len(union)


def contains_financing_signal(text: str | None) -> bool:
    t = normalize_text(text)
    signals = [
        "融资", "募资", "天使轮", "种子轮", "a轮", "b轮", "c轮",
        "funding", "raised", "series a", "series b", "series c", "financing"
    ]
    return any(s in t for s in signals)


def contains_product_signal(text: str | None) -> bool:
    t = normalize_text(text)
    signals = [
        "发布", "推出", "上线", "开源", "模型", "平台", "系统",
        "launch", "launched", "released", "unveiled", "model", "platform"
    ]
    return any(s in t for s in signals)


def contains_policy_signal(text: str | None) -> bool:
    t = normalize_text(text)
    signals = [
        "政策", "法规", "监管", "法案", "战略",
        "policy", "regulation", "act", "framework", "guideline"
    ]
    return any(s in t for s in signals)