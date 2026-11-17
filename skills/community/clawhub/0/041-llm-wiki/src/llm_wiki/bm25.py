"""
确定性本地 BM25 检索

纯标准库实现,无第三方依赖、无网络、无模型下载:
- 分词:英文按词(小写),中文按单字 + 二字滑窗,过滤停用词
- 排序:BM25Okapi(Robertson 非负 idf,k1=1.5, b=0.75)
- 同样的语料与查询永远得到同样的分数,可测试、可复现

作为 linker/retrieval 的确定性基线:embedding 不可用时检索质量
仍然可靠;embedding 可用时作为可解释的混合信号之一。
"""

import math
import re

# 与 linker 共用同一份停用词表(linker 从此处导入,避免重复维护)
STOP_WORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "must",
    "shall",
    "can",
    "need",
    "dare",
    "ought",
    "used",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
    "at",
    "by",
    "from",
    "as",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "between",
    "under",
    "and",
    "but",
    "or",
    "yet",
    "so",
    "if",
    "because",
    "although",
    "though",
    "while",
    "where",
    "when",
    "that",
    "which",
    "who",
    "whom",
    "whose",
    "what",
    "this",
    "these",
    "those",
    "的",
    "了",
    "在",
    "是",
    "我",
    "有",
    "和",
    "就",
    "不",
    "人",
    "都",
    "一",
    "一个",
    "上",
    "也",
    "很",
    "到",
    "说",
    "要",
    "去",
    "你",
    "会",
    "着",
    "没有",
    "看",
    "好",
    "自己",
    "这",
    "那",
    "啊",
}

_EN_WORD = re.compile(r"[a-zA-Z]{2,}")
_ZH_RUN = re.compile(r"[一-鿿]+")


def tokenize(text: str) -> list[str]:
    """中英文混合分词,输出保序 token 列表(含重复,供词频统计)。"""
    tokens: list[str] = [
        w
        for w in (m.group(0).lower() for m in _EN_WORD.finditer(text))
        if w not in STOP_WORDS
    ]
    for run in _ZH_RUN.findall(text):
        for i, ch in enumerate(run):
            if ch not in STOP_WORDS:
                tokens.append(ch)
            if i + 1 < len(run):
                tokens.append(run[i : i + 2])
    return tokens


class BM25:
    """BM25Okapi:对固定语料做多查询打分。"""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.n_docs = len(docs)
        self.doc_len = [len(d) for d in docs]
        self.avgdl = sum(self.doc_len) / self.n_docs if self.n_docs else 0.0
        self.df: dict[str, int] = {}
        self.tf: list[dict[str, int]] = []
        for doc in docs:
            freq: dict[str, int] = {}
            for token in doc:
                freq[token] = freq.get(token, 0) + 1
            self.tf.append(freq)
            for token in freq:
                self.df[token] = self.df.get(token, 0) + 1

    def idf(self, term: str) -> float:
        """Robertson idf,恒非负。"""
        n = self.df.get(term, 0)
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def scores(self, query: list[str]) -> list[float]:
        """对语料中每篇文档打分,与构造顺序一致。"""
        unique_terms = [t for t in dict.fromkeys(query) if t in self.df]
        if not unique_terms:
            return [0.0] * self.n_docs

        term_weights = {term: self.idf(term) * (self.k1 + 1) for term in unique_terms}
        results: list[float] = []
        for i in range(self.n_docs):
            score = 0.0
            length_norm = (
                self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avgdl)
                if self.avgdl > 0
                else self.k1
            )
            tf_i = self.tf[i]
            for term, weight in term_weights.items():
                f = tf_i.get(term, 0)
                if f == 0:
                    continue
                score += weight * f / (f + length_norm)
            results.append(score)
        return results
