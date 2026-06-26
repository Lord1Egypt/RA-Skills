from .config import config
from .chunker import TextChunker
import re


class VectorContextStore:
    def __init__(self):
        self.embedding = None
        self.chunker = TextChunker()
        self.vector_db = None
        self.chunks = []

    def add_long_text(self, long_text: str):
        self.chunks = self.chunker.split_text(long_text)

    def retrieve_relevant_context(self, query: str, k: int = 3) -> str:
        if not self.chunks:
            return ""

        return self._keyword_based_retrieval(query, k)

    def _keyword_based_retrieval(self, query: str, k: int = 3) -> str:
        query_keywords = set(self._extract_keywords(query))

        scored_chunks = []
        for idx, chunk_text in self.chunks:
            chunk_keywords = set(self._extract_keywords(chunk_text))
            overlap = len(query_keywords & chunk_keywords)
            score = overlap / max(len(query_keywords), 1)
            scored_chunks.append((score, chunk_text))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [text for _, text in scored_chunks[:k]]

        if top_chunks:
            return "\n\n【相关上下文】\n" + "\n\n".join(top_chunks)
        return ""

    def _extract_keywords(self, text: str) -> list:
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', text)
        words = text.split()

        stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        keywords = [w for w in words if len(w) > 1 and w not in stopwords]
        return keywords
