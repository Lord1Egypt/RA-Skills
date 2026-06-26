#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from common import INDEX_DIR, INDEX_FILE, LEARNINGS_MD, MEMORY_MD, META_FILE, WORKSPACE, list_daily_memory_files

DIM = 512
TOKEN_RE = re.compile(r"[A-Za-z0-9_\-\u4e00-\u9fff]{2,}")
PHRASE_HINTS = [
    'memory_search', 'memory-retrieval', 'memory retrieval', '记忆搜索', '记忆检索',
    '主路由', '默认入口', '检索路由', '路由变化', '更新后', '飞书', 'feishu', '断联', '掉线', '失联', '中断',
    '插件', '插件重复', 'duplicate plugin id', 'gateway timeout', '宿主', '截图', '截屏', '提醒', '周一',
]


@dataclass
class Chunk:
    chunk_id: str
    file: str
    title: str
    text: str


def list_source_files() -> List[Path]:
    files: List[Path] = []
    if MEMORY_MD.exists():
        files.append(MEMORY_MD)
    if LEARNINGS_MD.exists():
        files.append(LEARNINGS_MD)
    files.extend(list_daily_memory_files())
    return files


def split_chunks(path: Path) -> Iterable[Chunk]:
    txt = path.read_text(encoding='utf-8', errors='ignore')
    rel = str(path.relative_to(WORKSPACE))
    title = ''
    buff: list[str] = []
    idx = 0

    def flush():
        nonlocal buff, idx
        if not buff:
            return None
        content = '\n'.join(buff).strip()
        buff = []
        if len(content) < 8:
            return None
        idx += 1
        cid = hashlib.sha1(f'{rel}::{idx}::{content[:80]}'.encode()).hexdigest()[:16]
        return Chunk(chunk_id=cid, file=rel, title=title or rel, text=content)

    for line in txt.splitlines():
        s = line.strip()
        if s.startswith('#'):
            out = flush()
            if out:
                yield out
            title = s.lstrip('# ').strip()
            continue
        if s.startswith('- ') or s.startswith('* '):
            out = flush()
            if out:
                yield out
            buff.append(s)
            out = flush()
            if out:
                yield out
            continue
        if not s:
            out = flush()
            if out:
                yield out
            continue
        buff.append(s)

    out = flush()
    if out:
        yield out


def tokenize(text: str) -> list[str]:
    raw = [m.group(0).lower() for m in TOKEN_RE.finditer(text)]
    tokens = list(raw)
    seen = set(tokens)
    lowered = text.lower()
    for phrase in PHRASE_HINTS:
        if phrase.lower() in lowered and phrase.lower() not in seen:
            tokens.append(phrase.lower())
            seen.add(phrase.lower())
    return tokens


def hash_index(tok: str) -> int:
    h = hashlib.sha1(tok.encode()).digest()
    return int.from_bytes(h[:4], 'little') % DIM


def normalize(vec: list[float]) -> list[float]:
    n = math.sqrt(sum(v * v for v in vec))
    if n == 0:
        return vec
    return [v / n for v in vec]


def collect_source_state(files: list[Path]) -> dict:
    latest_mtime = 0.0
    latest_file = ''
    for p in files:
        try:
            mtime = p.stat().st_mtime
        except OSError:
            continue
        if mtime >= latest_mtime:
            latest_mtime = mtime
            latest_file = str(p.relative_to(WORKSPACE))
    return {
        'file_count': len(files),
        'source_latest_mtime': round(latest_mtime, 6),
        'source_latest_file': latest_file,
    }


def main() -> int:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    files = list_source_files()
    chunks: list[Chunk] = []
    for f in files:
        chunks.extend(split_chunks(f))

    df = Counter()
    tokenized = []
    for c in chunks:
        toks = tokenize(f'{c.title}\n{c.text}')
        tokenized.append(toks)
        for t in set(toks):
            df[t] += 1

    n_docs = max(1, len(chunks))
    with INDEX_FILE.open('w', encoding='utf-8') as out:
        for c, toks in zip(chunks, tokenized):
            tf = Counter(toks)
            vec = [0.0] * DIM
            for t, cnt in tf.items():
                i = hash_index(t)
                idf = math.log((n_docs + 1) / (df[t] + 1)) + 1.0
                vec[i] += cnt * idf
            rec = {
                'id': c.chunk_id,
                'file': c.file,
                'title': c.title,
                'text': c.text,
                'vector': normalize(vec),
            }
            out.write(json.dumps(rec, ensure_ascii=False) + '\n')

    source_state = collect_source_state(files)
    meta = {
        'dim': DIM,
        'chunks': len(chunks),
        'files': [str(p.relative_to(WORKSPACE)) for p in files],
        'built_at': dt.datetime.now(dt.timezone.utc).isoformat(),
        'workspace': str(WORKSPACE),
        **source_state,
    }
    META_FILE.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'ok': True, **meta}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
