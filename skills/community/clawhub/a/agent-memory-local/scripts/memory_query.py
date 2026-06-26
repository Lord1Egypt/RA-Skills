#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

BASE = Path(__file__).resolve().parent
RETRIEVE = BASE / 'retrieve.py'
PY311 = Path(r'D:/Python311/python.exe')
TOKEN_RE = re.compile(r'[A-Za-z0-9_\-\u4e00-\u9fff]{2,}')
PHRASE_HINTS = [
    'memory_search', 'memory-retrieval', 'memory retrieval', '记忆搜索', '记忆检索', '主路由', '默认入口',
    '检索路由', '路由变化', '更新后', '飞书', 'feishu', '断联', '掉线', '失联', '中断', '插件',
    'duplicate plugin id', 'gateway timeout', '宿主', '截图', '截屏', '提醒', '周一',
]
STOPWORDS = {
    '昨天', '今天', '前天', '这轮', '为什么', '为何', '怎么', '一下', '现在', '当前', '那个', '这个',
    '是不是', '可以', '继续', '已经', '还是', '然后', '之后', '之前', '我们', '你们', '就是', '因为', '所以',
    '如果', '但是', '而且', '还有', '那个问题', '这个问题', '变了',
}
ANCHOR_TERMS = {
    'memory_search', 'memory-retrieval', 'memory retrieval', '记忆搜索', '记忆检索', '主路由', '默认入口',
    '检索路由', '飞书', 'feishu', '断联', '掉线', '失联', '中断', 'gateway timeout', 'duplicate plugin id',
}


def tokenize(text: str) -> list[str]:
    raw = [m.group(0).lower() for m in TOKEN_RE.finditer(text)]
    tokens = list(raw)
    seen = set(tokens)
    lowered = text.lower()
    for phrase in PHRASE_HINTS:
        needle = phrase.lower()
        if needle in lowered and needle not in seen:
            tokens.append(needle)
            seen.add(needle)
    return tokens


def run_query(q: str, k: int) -> dict:
    out = subprocess.check_output([*python_cmd(), str(RETRIEVE), q, str(k)], text=True, env=os.environ.copy())
    return json.loads(out)


def uniq_keep_order(items: Iterable[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def simplify_query(q: str) -> str:
    tokens = []
    for tok in tokenize(q):
        if len(tok) < 2 or tok in STOPWORDS:
            continue
        tokens.append(tok)
    tokens = uniq_keep_order(tokens)
    return ' '.join(tokens[:10]) if tokens else q


def expand_query(q: str) -> str:
    parts = [q]
    today = date.today()
    if '昨天' in q:
        parts.append((today - timedelta(days=1)).isoformat())
    if '今天' in q:
        parts.append(today.isoformat())
    if '前天' in q:
        parts.append((today - timedelta(days=2)).isoformat())
    if '更新后' in q or '变了' in q:
        parts.extend(['更新', '变更', '记忆检索', '检索路由', '主路由', '默认入口'])
    if '记忆搜索' in q or '记忆检索' in q or 'memory_search' in q.lower():
        parts.extend(['memory_search', 'memory-retrieval', 'memory retrieval', '记忆搜索', '记忆检索'])
    if '飞书' in q or 'feishu' in q.lower():
        parts.extend(['飞书', 'feishu'])
    if any(x in q for x in ['掉线', '断联', '失联', '中断']):
        parts.extend(['断联', '掉线', 'gateway timeout', 'duplicate plugin id', '插件'])
    return ' '.join(uniq_keep_order([p for p in parts if p]))


def intent_rewrites(q: str) -> list[str]:
    today = date.today()
    y = (today - timedelta(days=1)).isoformat()
    d2 = (today - timedelta(days=2)).isoformat()
    rewrites: list[str] = []
    if '飞书' in q and any(x in q for x in ['掉线', '断联', '失联', '中断']):
        rewrites.extend([
            '飞书 断联 duplicate plugin id gateway timeout',
            'feishu duplicate plugin id gateway timeout',
            '飞书 插件重复 gateway timeout',
            f'{y} 飞书 duplicate plugin id gateway timeout',
        ])
    if any(x in q for x in ['更新后', '变了']) and any(x in q for x in ['记忆搜索', '记忆检索', 'memory_search']):
        rewrites.extend([
            '记忆检索 主路由 默认入口 变更 memory_search memory-retrieval',
            'memory_search 本地 memory-retrieval 主路由 变更',
            '本地 tools/memory-retrieval 主路由 memory_search 备用 增强',
            f'{y} 更新 记忆检索 默认入口 路由变化',
        ])
    if '昨天' in q and '为什么' in q:
        rewrites.extend([f'{y} 原因 根因 修复', f'{y} 故障 原因 处理'])
    if '前天' in q and '为什么' in q:
        rewrites.extend([f'{d2} 原因 根因 修复', f'{d2} 故障 原因 处理'])
    if '为什么' in q and '变了' in q:
        rewrites.extend(['默认入口 变更 路由变化', '更新后 默认入口 改动'])
    return uniq_keep_order([x for x in rewrites if x and x != q])


def score_payload(original_query: str, used_query: str, payload: dict) -> float:
    results = payload.get('results') or []
    if not results:
        return -10_000.0
    top = results[0]
    top_text = f"{top.get('file', '')} {top.get('title', '')} {top.get('text', '')}".lower()
    original_tokens = set(tokenize(original_query))
    used_tokens = set(tokenize(used_query))
    overlap = int(top.get('overlap', 0) or 0)
    semantic = float(top.get('semantic', 0.0) or 0.0)
    score = float(top.get('score', 0.0) or 0.0)
    total = score * 100 + semantic * 45 + overlap * 20
    matched_original = sum(1 for t in original_tokens if t in top_text)
    matched_used = sum(1 for t in used_tokens if t in top_text)
    total += matched_original * 8 + matched_used * 4
    if any(x in original_query for x in ['为什么', '为何', '原因', '根因']) and overlap == 0:
        total -= 60
    if any(t in ANCHOR_TERMS for t in original_tokens):
        total += sum(10 for t in original_tokens if t in ANCHOR_TERMS and t in top_text)
    return total


def emit(query: str, used_query: str, retried: bool, payload: dict, attempted_queries: list[str], selection_score: float) -> int:
    print(json.dumps({'query': query, 'used_query': used_query, 'retried': retried, 'attempted_queries': attempted_queries, 'selection_score': round(selection_score, 3), **payload}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: memory_query.py "query" [k]', file=sys.stderr)
        return 2
    q = sys.argv[1].strip()
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    candidates = uniq_keep_order([q, simplify_query(q), expand_query(q), *intent_rewrites(q)])
    best_payload = None
    best_query = q
    best_score = -10_000.0
    for cand in candidates:
        payload = run_query(cand, k)
        current_score = score_payload(q, cand, payload)
        if current_score > best_score:
            best_score = current_score
            best_payload = payload
            best_query = cand
    if best_payload is None:
        best_payload = {'mode': 'fallback', 'reason': 'no_attempts', 'results': []}
    return emit(q, best_query, best_query != q, best_payload, candidates, best_score)


if __name__ == '__main__':
    raise SystemExit(main())
