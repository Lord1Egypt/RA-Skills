# -*- coding: utf-8 -*-
"""评论词频分析（可选功能）。

依赖 jieba（仅在使用 --analyze 时导入）。停用词默认取自技能内 ``assets/stopwords.txt``，
也可通过 ``--stopwords`` 传入自定义文件（每行一个词）。

用法（作为库调用）：
    from analyze import analyze_comments
    words = analyze_comments(texts, top_n=50, stopwords_path=None, min_len=2)
"""

from __future__ import annotations

import os
import re

_DEFAULT_STOPWORDS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets", "stopwords.txt"
)

# 仅含标点/空白/表情符号的 token 直接丢弃
_NOISE_RE = re.compile(r"^[\s\W_]+$|^[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F02F]+$")
# 抖音 [表情] / [赞] / [玫瑰] 等括号标记，分词前先剔除
_BRACKET_RE = re.compile(r"\[[^\]]*\]")


def load_stopwords(path: str | None = None) -> set:
    """加载停用词集合；默认用技能自带 assets/stopwords.txt。"""
    p = path or _DEFAULT_STOPWORDS
    stop: set = set()
    if not os.path.exists(p):
        return stop
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if w and not w.startswith("#"):
                stop.add(w)
    return stop


def analyze_comments(
    texts: list[str],
    top_n: int = 50,
    stopwords_path: str | None = None,
    min_len: int = 2,
):
    """对一批评论文本做 jieba 分词 + 停用词过滤 + 词频统计。

    Args:
        texts: 评论文本列表。
        top_n: 返回词频最高的前 N 个词。
        stopwords_path: 自定义停用词文件（否则用默认表）。
        min_len: 词的最小长度（按字符数），过短的词（如单字）默认丢弃。

    Returns:
        ``[{"word": ..., "count": ...}, ...]`` 按词频降序，最多 top_n 个。
    """
    try:
        import jieba
    except ImportError as exc:  # noqa: BLE001
        raise ImportError(
            "词频分析需要 jieba：运行 `pip install jieba` "
            "（或技能内 scripts/requirements.txt）"
        ) from exc

    stop = load_stopwords(stopwords_path)
    counter: dict[str, int] = {}
    for text in texts:
        if not text:
            continue
        text = _BRACKET_RE.sub(" ", text)  # 去 [表情]/[赞] 等括号标记
        for tok in jieba.cut(text):
            w = tok.strip()
            if not w or len(w) < min_len:
                continue
            if w in stop:
                continue
            if _NOISE_RE.match(w):
                continue
            counter[w] = counter.get(w, 0) + 1

    ranked = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]
    return [{"word": w, "count": c} for w, c in ranked]


if __name__ == "__main__":
    import sys
    import json

    sample = sys.argv[1:] or ["这个产品真的太好用了，性价比超高，强烈推荐！", "性价比确实高，已下单"]
    print(json.dumps(analyze_comments(sample, top_n=20), ensure_ascii=False, indent=2))
