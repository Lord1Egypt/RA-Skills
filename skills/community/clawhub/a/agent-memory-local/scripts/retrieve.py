#!/usr/bin/env python3
"""
Local-first memory retrieval with vector-first + fallback scan.

Features:
- Auto-refresh stale index when source memory files change
- Chinese-friendly phrase anchors and synonym expansion
- Strong-anchor filtering for route/config/root-cause questions
- Optional SiliconFlow rerank enhancement (default on when API key is available)
- Explainable output with overlap/anchor/recency fields
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

from common import INDEX_FILE, LEARNINGS_MD, MEMORY_MD, META_FILE, WORKSPACE, list_daily_memory_files

BUILD_SCRIPT = Path(__file__).resolve().parent / 'build_index.py'
DIM = 512
TOKEN_RE = re.compile(r"[A-Za-z0-9_\-\u4e00-\u9fff]{2,}")
DATE_RE = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")

RERANK_URL = 'https://api.siliconflow.cn/v1/rerank'
RERANK_MODEL = 'BAAI/bge-reranker-v2-m3'
RERANK_ENABLED_DEFAULT = True
RERANK_MIN_RESULTS = 2
RERANK_TOP_N = 10
RERANK_TIMEOUT = 20
RERANK_MIN_SCORE = 0.08

AUTO_REBUILD_DEFAULT = True
AUTO_REBUILD_TIMEOUT = 60
MAX_FALLBACK_FILES = 24

CANDIDATE_MULTIPLIER = 4
CANDIDATE_MAX = 24
MIN_BASE_SCORE = 0.18
MIN_OVERLAP_FOR_WEAK_BASE = 2
MIN_FINAL_SCORE = 0.16
MIN_ZERO_OVERLAP_BASE = 0.62
STRICT_ANCHOR_BASE = 0.68

SYNONYMS = {
    '截屏': ['截图', 'screen', 'screenshot'],
    '截图': ['截屏', 'screen', 'screenshot'],
    '提醒': ['待办', 'todo', 'reminder'],
    '宿主': ['windows', 'host', '主机'],
    '周一': ['星期一', 'monday'],
    '星期一': ['周一', 'monday'],
    '掉线': ['断联', '中断', '失联', '异常'],
    '断联': ['掉线', '中断', '失联', '异常'],
    '插件': ['plugin', 'extensions', '扩展'],
    '重启': ['restart', '重载', 'gateway'],
    '报错': ['错误', 'error', '异常', '失败'],
    '原因': ['根因', 'why', 'because'],
    '根因': ['原因', 'why', 'because'],
}

PHRASE_HINTS = [
    'memory_search', 'memory-retrieval', 'memory retrieval', '记忆搜索', '记忆检索', '主路由', '默认入口',
    '检索路由', '路由变化', '更新后', '飞书', 'feishu', '断联', '掉线', '失联', '中断', '插件',
    '插件重复', 'duplicate plugin id', 'gateway timeout', '宿主', '截图', '截屏', '提醒', '周一',
]

LOW_SIGNAL_PATTERNS = [
    re.compile(r'人设示例语气'),
    re.compile(r'参考，不必逐字照搬'),
    re.compile(r'典型架构（纯向量）'),
    re.compile(r'现在最合理的路线'),
    re.compile(r'当前状态$'),
    re.compile(r'我给你的直球建议'),
    re.compile(r'做“记忆问句改写器”'),
    re.compile(r'已经变好的'),
]
EXAMPLE_LINE_PATTERNS = [re.compile(r'^→\s*`.+`$'), re.compile(r'^-\s*`.+`$')]
MIN_TEXT_LEN = 18


def tokenize(text: str) -> List[str]:
    raw = [m.group(0).lower() for m in TOKEN_RE.finditer(text)]
    tokens = list(raw)
    seen = set(tokens)
    text_lower = text.lower()
    for phrase in PHRASE_HINTS:
        needle = phrase.lower()
        if needle in text_lower and needle not in seen:
            tokens.append(needle)
            seen.add(needle)
    return tokens


def hash_index(tok: str) -> int:
    h = hashlib.sha1(tok.encode()).digest()
    return int.from_bytes(h[:4], 'little') % DIM


def normalize(vec: List[float]) -> List[float]:
    n = math.sqrt(sum(v * v for v in vec))
    if n == 0:
        return vec
    return [v / n for v in vec]


def embed_query(q: str, dim: int) -> List[float]:
    vec = [0.0] * dim
    for t in tokenize(q):
        vec[hash_index(t) % dim] += 1.0
    return normalize(vec)


def dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def recency_bonus(file_rel: str) -> float:
    m = DATE_RE.search(file_rel)
    if not m:
        return 0.45
    try:
        d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        delta = max(0, (dt.date.today() - d).days)
        return max(0.0, 1.0 - min(delta, 30) / 30.0)
    except Exception:
        return 0.45


def expand_tokens(tokens: List[str]) -> List[str]:
    expanded = list(tokens)
    for t in list(tokens):
        for s in SYNONYMS.get(t, []):
            expanded.append(s.lower())
    return expanded


def weekday_boost(query_tokens: set[str], rec_text: str) -> float:
    text = rec_text.lower()
    if ('周一' in query_tokens or '星期一' in query_tokens or 'monday' in query_tokens) and ('周一' in text or '星期一' in text or 'monday' in text):
        return 0.08
    return 0.0


def domain_phrase_boost(query_tokens: set[str], rec_text: str) -> float:
    text = rec_text.lower()
    boost = 0.0
    def has(*words: str) -> bool:
        return any(w in text for w in words)
    if ('宿主' in query_tokens or 'windows' in query_tokens or 'host' in query_tokens) and has('windows', '宿主', 'host'):
        boost += 0.08
    if ('截屏' in query_tokens or '截图' in query_tokens or 'screenshot' in query_tokens) and has('截屏', '截图', 'screenshot'):
        boost += 0.08
    if '提醒' in query_tokens and has('提醒', 'reminder'):
        boost += 0.06
    if ('飞书' in query_tokens or 'feishu' in query_tokens) and has('飞书', 'feishu'):
        boost += 0.08
    if ('插件' in query_tokens or 'plugin' in query_tokens or '扩展' in query_tokens) and has('插件', 'plugin', '扩展'):
        boost += 0.08
    if ('重启' in query_tokens or 'restart' in query_tokens) and has('重启', 'restart', 'gateway'):
        boost += 0.06
    if ('掉线' in query_tokens or '断联' in query_tokens) and has('掉线', '断联', '失联', '中断'):
        boost += 0.08
    if ('报错' in query_tokens or '错误' in query_tokens or 'error' in query_tokens) and has('报错', '错误', 'error', '失败', '异常'):
        boost += 0.06
    if ('原因' in query_tokens or '根因' in query_tokens or 'why' in query_tokens) and has('原因', '根因'):
        boost += 0.08
    if ('memory_search' in query_tokens or '记忆搜索' in query_tokens) and has('memory_search', '记忆搜索'):
        boost += 0.08
    if ('memory-retrieval' in query_tokens or 'memory retrieval' in query_tokens or '记忆检索' in query_tokens) and has('memory-retrieval', 'memory retrieval', '记忆检索'):
        boost += 0.08
    if ('主路由' in query_tokens or '默认入口' in query_tokens) and has('主路由', '默认入口'):
        boost += 0.08
    return boost


def list_source_files() -> List[Path]:
    files: List[Path] = []
    if MEMORY_MD.exists():
        files.append(MEMORY_MD)
    if LEARNINGS_MD.exists():
        files.append(LEARNINGS_MD)
    files.extend(list_daily_memory_files())
    return files


def source_state() -> Dict[str, Any]:
    files = list_source_files()
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
    return {'file_count': len(files), 'source_latest_mtime': round(latest_mtime, 6), 'source_latest_file': latest_file}


def load_meta() -> Dict[str, Any]:
    if not META_FILE.exists():
        return {}
    try:
        return json.loads(META_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def auto_rebuild_enabled() -> bool:
    raw = os.environ.get('MEMORY_AUTO_REBUILD', '').strip().lower()
    if raw in {'0', 'false', 'off', 'no'}:
        return False
    if raw in {'1', 'true', 'on', 'yes'}:
        return True
    return AUTO_REBUILD_DEFAULT


def python_cmd() -> List[str]:
    if PY311.exists():
        return [str(PY311)]
    py = shutil.which('py')
    if py:
        return [py, '-3.11']
    if sys.executable:
        return [sys.executable]
    return [shutil.which('python') or 'python']


def ensure_index_ready() -> Dict[str, Any]:
    src = source_state()
    state: Dict[str, Any] = {'auto_rebuild': auto_rebuild_enabled(), **src}
    if not INDEX_FILE.exists() or not META_FILE.exists():
        state['status'] = 'missing'
    else:
        meta = load_meta()
        state['meta'] = meta
        built_source_mtime = float(meta.get('source_latest_mtime', 0.0) or 0.0)
        meta_file_count = int(meta.get('file_count', 0) or 0)
        if built_source_mtime + 1e-6 < float(src.get('source_latest_mtime', 0.0)) or meta_file_count != int(src.get('file_count', 0)):
            state['status'] = 'stale'
        else:
            state['status'] = 'fresh'
            return state

    if not state['auto_rebuild']:
        return state

    try:
        proc = subprocess.run([*python_cmd(), str(BUILD_SCRIPT)], cwd=str(WORKSPACE), capture_output=True, text=True, timeout=AUTO_REBUILD_TIMEOUT, check=True)
        rebuilt_meta = load_meta()
        state['status'] = 'rebuilt'
        state['rebuilt'] = True
        state['meta'] = rebuilt_meta
        stdout = (proc.stdout or '').strip()
        if stdout:
            try:
                state['build'] = json.loads(stdout.splitlines()[-1])
            except Exception:
                state['build_stdout'] = stdout[-240:]
        return state
    except Exception as e:
        state['status'] = 'rebuild_failed'
        state['error'] = type(e).__name__
        return state


def summarize_index_state(state: Dict[str, Any]) -> Dict[str, Any]:
    out = {'status': state.get('status', 'unknown'), 'auto_rebuild': bool(state.get('auto_rebuild')), 'source_latest_file': state.get('source_latest_file', '')}
    meta = state.get('meta') or {}
    if meta:
        out['built_at'] = meta.get('built_at')
        out['chunks'] = meta.get('chunks')
        out['file_count'] = meta.get('file_count', len(meta.get('files') or []))
    if state.get('status') == 'rebuild_failed':
        out['error'] = state.get('error')
    if state.get('status') == 'rebuilt':
        out['rebuilt'] = True
    return out


def rerank_enabled() -> bool:
    raw = os.environ.get('MEMORY_RERANK', '').strip().lower()
    if raw in {'0', 'false', 'off', 'no'}:
        return False
    if raw in {'1', 'true', 'on', 'yes'}:
        return True
    return RERANK_ENABLED_DEFAULT


def load_siliconflow_key() -> str | None:
    for env_name in ('SILICONFLOW_API_KEY', 'API_KEY'):
        val = os.environ.get(env_name)
        if val:
            return val
    return None


def select_rerank_subset(hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    qualified = []
    for h in hits:
        if h.get('overlap', 0) >= 2 or h.get('semantic', 0.0) >= 0.32 or h.get('score', 0.0) >= 0.30:
            qualified.append(h)
    return qualified[: min(RERANK_TOP_N, len(qualified))]


def normalize_hit_key(hit: Dict[str, Any]) -> tuple[str, str]:
    text = re.sub(r'\s+', ' ', (hit.get('text') or '')).strip().lower()
    return hit.get('file', ''), text


def dedupe_hits(hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for hit in hits:
        key = normalize_hit_key(hit)
        if key in seen:
            continue
        seen.add(key)
        out.append(hit)
    return out


def apply_rerank(query: str, hits: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rerank_enabled():
        return {'enabled': False, 'applied': False, 'reason': 'disabled'}
    if len(hits) < RERANK_MIN_RESULTS:
        return {'enabled': True, 'applied': False, 'reason': 'too_few_results'}

    subset = select_rerank_subset(hits)
    if len(subset) < RERANK_MIN_RESULTS:
        return {'enabled': True, 'applied': False, 'reason': 'no_qualified_subset'}

    api_key = load_siliconflow_key()
    if not api_key:
        return {'enabled': True, 'applied': False, 'reason': 'no_api_key'}

    documents = [f"{h.get('title', '')}\n{h.get('text', '')}".strip() for h in subset]
    payload = json.dumps({'model': RERANK_MODEL, 'query': query, 'documents': documents}).encode('utf-8')
    req = urllib.request.Request(
        RERANK_URL,
        data=payload,
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=RERANK_TIMEOUT) as resp:
            data = json.loads(resp.read().decode('utf-8', errors='ignore'))
    except urllib.error.HTTPError as e:
        return {'enabled': True, 'applied': False, 'reason': f'http_{e.code}', 'status': e.code}
    except Exception as e:
        return {'enabled': True, 'applied': False, 'reason': type(e).__name__}

    results = data.get('results') or []
    if not results:
        return {'enabled': True, 'applied': False, 'reason': 'empty_results'}

    reranked_by_key: dict[tuple[str, str], Dict[str, Any]] = {}
    weak_count = 0
    for item in results:
        idx = item.get('index')
        score = item.get('relevance_score')
        if idx is None or score is None or idx < 0 or idx >= len(subset):
            continue
        if float(score) < RERANK_MIN_SCORE:
            weak_count += 1
            continue
        hit = dict(subset[idx])
        hit['rerank_score'] = round(float(score), 6)
        hit['score_before_rerank'] = hit.get('score')
        hit['score'] = round((float(score) * 0.55) + (float(hit.get('semantic', 0.0)) * 0.25) + (float(hit.get('score', 0.0)) * 0.20), 4)
        reranked_by_key[normalize_hit_key(hit)] = hit

    if not reranked_by_key:
        return {'enabled': True, 'applied': False, 'reason': 'all_scores_too_low', 'weak_scores': weak_count}

    merged = [reranked_by_key.get(normalize_hit_key(hit), hit) for hit in hits]
    merged.sort(key=lambda x: (x.get('rerank_score', -1.0), x.get('score', 0.0), x.get('semantic', 0.0)), reverse=True)
    hits[:] = dedupe_hits(merged)
    return {'enabled': True, 'applied': True, 'model': RERANK_MODEL, 'provider': 'siliconflow', 'reranked': len(reranked_by_key), 'subset': len(subset), 'weak_scores': weak_count}


def candidate_pool_size(k: int) -> int:
    return min(max(k * CANDIDATE_MULTIPLIER, k), CANDIDATE_MAX)


def query_anchor_terms(query: str) -> set[str]:
    anchors: set[str] = set()
    q_lower = query.lower()
    if any(x in q_lower for x in ['memory_search', 'memory-retrieval', 'memory retrieval']):
        anchors.update({'memory_search', 'memory-retrieval', 'memory retrieval'})
    if any(x in query for x in ['记忆搜索', '记忆检索', '主路由', '默认入口', '检索路由', '路由变化', '更新后']):
        anchors.update({'记忆搜索', '记忆检索', '主路由', '默认入口', '检索路由', '路由变化', '更新后'})
    if '飞书' in query or 'feishu' in q_lower:
        anchors.update({'飞书', 'feishu'})
    if any(x in query for x in ['断联', '掉线', '失联', '中断']):
        anchors.update({'断联', '掉线', '失联', '中断'})
    if 'duplicate plugin id' in q_lower:
        anchors.add('duplicate plugin id')
    if 'gateway timeout' in q_lower:
        anchors.add('gateway timeout')
    return anchors


def matched_anchor_terms(anchors: set[str], doc_tokens: set[str], doc_text: str) -> List[str]:
    if not anchors:
        return []
    text_lower = doc_text.lower()
    hits = []
    for anchor in sorted(anchors):
        if anchor.lower() in doc_tokens or anchor.lower() in text_lower:
            hits.append(anchor.lower())
    return hits


def keep_candidate(*, base: float, overlap_cnt: int, text_body: str, reasoning_query: bool, final_score: float, strict_anchor_query: bool, anchor_hit_cnt: int) -> bool:
    if len(text_body) < MIN_TEXT_LEN and overlap_cnt < 2:
        return False
    if strict_anchor_query and anchor_hit_cnt == 0:
        if overlap_cnt < 2 or base < STRICT_ANCHOR_BASE:
            return False
    if overlap_cnt == 0 and anchor_hit_cnt == 0 and base < MIN_ZERO_OVERLAP_BASE:
        return False
    if base < MIN_BASE_SCORE and overlap_cnt < MIN_OVERLAP_FOR_WEAK_BASE:
        return False
    if final_score < MIN_FINAL_SCORE:
        return False
    if reasoning_query and overlap_cnt == 0 and anchor_hit_cnt == 0:
        return False
    return True


def vector_search(query: str, k: int) -> Dict[str, Any]:
    index_state = ensure_index_ready()
    if not INDEX_FILE.exists() or not META_FILE.exists():
        return {'mode': 'fallback', 'reason': 'index_missing', 'results': [], 'index_status': summarize_index_state(index_state)}

    meta = index_state.get('meta') or load_meta()
    dim = int(meta.get('dim', DIM))
    q_tokens = tokenize(query)
    q_tokens_expanded = expand_tokens(q_tokens)
    q_set = set(q_tokens_expanded)
    if not q_tokens_expanded:
        return {'mode': 'fallback', 'reason': 'empty_query', 'results': [], 'index_status': summarize_index_state(index_state)}

    qv = embed_query(' '.join(q_tokens_expanded), dim)
    reasoning_query = any(t in query for t in ['为什么', '为何', '怎么', '原因', '根因'])
    anchor_terms = query_anchor_terms(query)
    strict_anchor_query = bool(anchor_terms)
    scored = []

    bad_lines = 0
    with INDEX_FILE.open('r', encoding='utf-8') as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                bad_lines += 1
                continue
            base = dot(qv, rec.get('vector', []))
            text_for_overlap = f"{rec.get('title', '')}\n{rec.get('text', '')}"
            text_body = rec.get('text', '').strip()
            d_tokens = set(tokenize(text_for_overlap))
            overlap_terms = sorted(q_set & d_tokens)
            overlap_cnt = len(overlap_terms)
            overlap_ratio = overlap_cnt / max(1, len(q_set))
            anchor_hits = matched_anchor_terms(anchor_terms, d_tokens, text_for_overlap)
            recent = recency_bonus(rec.get('file', ''))
            wboost = weekday_boost(q_set, text_for_overlap)
            pboost = domain_phrase_boost(q_set, text_for_overlap)
            low_signal_penalty = 0.0
            title = rec.get('title', '')
            for pat in LOW_SIGNAL_PATTERNS:
                if pat.search(title):
                    low_signal_penalty += 0.08
            compact_text = text_body.replace('“', '"').replace('”', '"').strip()
            for pat in EXAMPLE_LINE_PATTERNS:
                if pat.search(compact_text) and len(compact_text) <= 120:
                    low_signal_penalty += 0.40
                    break
            final_score = (base * 0.56) + (overlap_ratio * 0.24) + (recent * 0.04) + wboost + pboost - low_signal_penalty
            if not keep_candidate(base=base, overlap_cnt=overlap_cnt, text_body=text_body, reasoning_query=reasoning_query, final_score=final_score, strict_anchor_query=strict_anchor_query, anchor_hit_cnt=len(anchor_hits)):
                continue
            scored.append((final_score, base, overlap_cnt, overlap_terms, anchor_hits, recent, wboost, pboost, rec))

    scored.sort(key=lambda x: x[0], reverse=True)
    pool = scored[:candidate_pool_size(k)]
    hits = [{
        'score': round(s, 4),
        'semantic': round(base, 4),
        'overlap': int(ov),
        'file': r['file'],
        'title': r.get('title', ''),
        'text': r.get('text', '')[:380],
        'explain': {
            'overlap_terms': terms[:6],
            'anchor_hits': anchor_hits[:6],
            'recency': round(recency, 3),
            'weekday_boost': round(wb, 3),
            'phrase_boost': round(pb, 3),
        },
    } for s, base, ov, terms, anchor_hits, recency, wb, pb, r in pool]
    hits = dedupe_hits(hits)
    if not hits:
        return {'mode': 'fallback', 'reason': 'no_hits', 'results': [], 'index_status': summarize_index_state(index_state)}
    rerank_meta = apply_rerank(query, hits)
    hits = dedupe_hits(hits)
    payload = {
        'mode': 'vector',
        'results': hits[:k],
        'rerank': rerank_meta,
        'candidate_pool': len(pool),
        'index_status': summarize_index_state(index_state),
        'query_profile': {'reasoning_query': reasoning_query, 'anchor_terms': sorted(anchor_terms)[:8]},
    }
    if bad_lines:
        payload['warnings'] = {'bad_index_lines_skipped': bad_lines}
    return payload


def fallback_search(query: str, k: int) -> List[Dict[str, Any]]:
    q = query.lower().strip()
    if not q:
        return []
    q_tokens = set(expand_tokens(tokenize(q)))
    files = [MEMORY_MD, LEARNINGS_MD]
    files.extend(list(reversed(list_daily_memory_files()))[:MAX_FALLBACK_FILES])
    out = []
    seen: set[tuple[str, str]] = set()
    for p in files:
        if not p.exists():
            continue
        rel = str(p.relative_to(WORKSPACE))
        for ln in p.read_text(encoding='utf-8', errors='ignore').splitlines():
            s = ln.strip()
            if not s:
                continue
            s_low = s.lower()
            if q in s_low or (q_tokens and (q_tokens & set(tokenize(s_low)))):
                key = (rel, re.sub(r'\s+', ' ', s_low))
                if key in seen:
                    continue
                seen.add(key)
                out.append({'score': 1.0, 'file': rel, 'title': rel, 'text': s[:380]})
                if len(out) >= k:
                    return out
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python3 retrieve.py "query" [k]', file=sys.stderr)
        return 2
    query = sys.argv[1]
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    res = vector_search(query, k)
    if res.get('mode') == 'vector':
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    fallback = fallback_search(query, k)
    print(json.dumps({'mode': 'fallback', 'reason': res.get('reason', 'unknown'), 'results': fallback, 'index_status': res.get('index_status')}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
