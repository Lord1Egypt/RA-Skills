#!/usr/bin/env python3
"""
DND Lens — 共享 RAG 检索引擎

功能：
  对 world_cards.jsonl（知识卡）做 BM25 检索，支撑三大子技能：
    - world-lore  ：世界观对话 / 费伦编年史查询
    - module-forge：生成模组时检索地点 / 派系 / 怪物素材
    - echo-map    ：真实经历映射时检索氛围 / 怪物 / 地点参照

设计原则（对齐 dnd-dm-skill 三层架构）：
  - 纯标准库，零外部依赖，离线可跑
  - 中文采用「单字 + 二元」分词（无需 jieba），英文按词切分
  - 路径自解析：脚本位置 -> skill 根 -> data/，可用环境变量 DND_LENS_DATA 覆盖

用法：
  python lens_rag.py "深水城 历史" --top-k 8
  python lens_rag.py "提夫林 来历" --types race monster --top-k 5
  python lens_rag.py --chronicle "阴影王朝" --top-k 12
"""

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

# ----------------------------------------------------------------------------
# 路径解析
# ----------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent          # .../dnd-dm-skill/scripts
SKILL_DIR = SCRIPT_DIR.parent                         # .../dnd-dm-skill


def resolve_data_dir() -> Path:
    env = os.environ.get("DND_LENS_DATA")
    if env:
        return Path(env)
    return SKILL_DIR / "data"


DATA_DIR = resolve_data_dir()
WORLD_CARDS = DATA_DIR / "world_cards.jsonl"

# 知识卡类型全集（用于 --types 过滤与编年史聚合）
CARD_TYPES = [
    "cosmology", "deity", "race", "class", "monster",
    "setting", "location", "faction", "event",
    "adventure_hook", "chronicle", "texture",
]
CHRONICLE_TYPES = ["chronicle", "event", "location", "faction", "deity"]


# ----------------------------------------------------------------------------
# 分词：英文单词 + 中文单字 + 中文二元
# ----------------------------------------------------------------------------
_CJK = re.compile(r"[一-鿿]")
_LATIN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    if not text:
        return []
    text = str(text)
    tokens: list[str] = []
    # 英文 / 数字
    tokens += [t.lower() for t in _LATIN.findall(text)]
    # 中文单字 + 二元
    cjk = _CJK.findall(text)
    tokens += [jk for jk in cjk]  # 单字
    tokens += [cjk[i] + cjk[i + 1] for i in range(len(cjk) - 1)]  # 二元
    return tokens


# ----------------------------------------------------------------------------
# BM25
# ----------------------------------------------------------------------------
class BM25:
    def __init__(self, corpus: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs = corpus
        self.n = len(corpus)
        self.df = {}
        for doc in corpus:
            for term in set(doc):
                self.df[term] = self.df.get(term, 0) + 1
        self.avgdl = sum(len(d) for d in corpus) / self.n if self.n else 0.0
        # 预计算 idf
        self.idf = {}
        for term, freq in self.df.items():
            self.idf[term] = math.log(1 + (self.n - freq + 0.5) / (freq + 0.5))

    def score(self, query: list[str], doc: list[str]) -> float:
        if not doc:
            return 0.0
        dl = len(doc)
        scores = {}
        for term in doc:
            scores[term] = scores.get(term, 0) + 1
        total = 0.0
        for term in query:
            if term not in self.idf:
                continue
            f = scores.get(term, 0)
            if f == 0:
                continue
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            total += self.idf[term] * (f * (self.k1 + 1)) / denom
        return total


# ----------------------------------------------------------------------------
# 世界透镜索引
# ----------------------------------------------------------------------------
class WorldLens:
    def __init__(self, cards_path: Path = WORLD_CARDS):
        self.cards_path = cards_path
        self.cards: list[dict] = []
        self.bm25: BM25 | None = None
        self._load()

    def _load(self):
        if not self.cards_path.exists():
            raise FileNotFoundError(f"知识卡文件不存在: {self.cards_path}")
        with open(self.cards_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    self.cards.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        corpus = [tokenize(self._card_text(c)) for c in self.cards]
        self.bm25 = BM25(corpus)

    @staticmethod
    def _card_text(c: dict) -> str:
        parts = [c.get("title", ""), c.get("body", "")]
        parts += c.get("tags", []) or []
        meta = c.get("metadata", {}) or {}
        parts += [str(v) for v in meta.values()]
        return " ".join(parts)

    def search(self, query: str, top_k: int = 8, types: list[str] | None = None) -> list[dict]:
        """返回带 _score 的知识卡列表（已按分数降序）。"""
        q_tokens = tokenize(query)
        if not q_tokens:
            return []
        scored = []
        for idx, card in enumerate(self.cards):
            if types and card.get("type") not in types:
                continue
            s = self.bm25.score(q_tokens, tokenize(self._card_text(card)))
            if s > 0:
                scored.append((s, idx))
        scored.sort(key=lambda x: x[0], reverse=True)
        out = []
        for s, idx in scored[:top_k]:
            card = dict(self.cards[idx])
            card["_score"] = round(s, 4)
            out.append(card)
        return out

    def chronicle(self, topic: str, top_k: int = 12) -> list[dict]:
        """编年史专用：优先聚合 chronicle/event/location/faction/deity。"""
        return self.search(topic, top_k=top_k, types=CHRONICLE_TYPES)

    def render(self, cards: list[dict], with_body: bool = True) -> str:
        """把检索结果渲染成可供 LLM 引用的知识摘要。"""
        if not cards:
            return "（未检索到相关知识卡）"
        lines = []
        for i, c in enumerate(cards, 1):
            head = f"[{i}] ({c.get('type')}) {c.get('title')}  · 来源: {c.get('source_file','?')}"
            if c.get("source_section"):
                head += f" / {c['source_section']}"
            lines.append(head)
            if with_body:
                body = (c.get("body") or "").strip()
                if body:
                    lines.append(body[:600])
            lines.append("")
        return "\n".join(lines)


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(
        description="DND Lens RAG 检索（BM25，中文二元分词，离线）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("query", nargs="*", help="检索词（空格分隔）")
    p.add_argument("--top-k", type=int, default=8, help="返回卡片数（默认 8）")
    p.add_argument("--types", nargs="+", choices=CARD_TYPES,
                   help="限定知识卡类型过滤")
    p.add_argument("--chronicle", action="store_true",
                   help="编年史模式：聚合 chronicle/event/location/faction/deity")
    p.add_argument("--no-body", action="store_true", help="只输出标题，不输出正文")
    p.add_argument("--json", action="store_true", help="输出原始 JSON（含 _score）")
    args = p.parse_args()

    lens = WorldLens()
    query = " ".join(args.query)
    if not query and not args.chronicle:
        p.error("请提供检索词，或使用 --chronicle TOPIC")

    if args.chronicle:
        cards = lens.chronicle(query or "", top_k=args.top_k)
    else:
        cards = lens.search(query, top_k=args.top_k, types=args.types)

    if args.json:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
    else:
        print(f"# 检索词：{query or '(编年史)'}")
        print(f"# 命中 {len(cards)} 张知识卡\n")
        print(lens.render(cards, with_body=not args.no_body))


if __name__ == "__main__":
    main()
