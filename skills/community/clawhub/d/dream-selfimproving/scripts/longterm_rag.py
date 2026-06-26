#!/usr/bin/env python3
"""
Dream Long-Term Memory (RAG Layer)

MetaGPT 风格的短长记忆合并：
- 当 short-term recall 溢出（> MEMORY_K）时，自动晋升老条目到长记忆
- 长记忆用 JSONL 文件存储，简单关键词检索
- 蒸馏时把长记忆也纳入上下文

用法:
  python longterm_rag.py --promote           # 晋升老条目
  python longterm_rag.py --query "关键词"     # 搜索长记忆
  python longterm_rag.py --status             # 查看状态
"""

# Windows UTF-8 fix
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ─── 配置 ────────────────────────────────────────────────

def get_workspace():
    ws = os.environ.get('OPENCLAW_WORKSPACE', '')
    if ws:
        return Path(ws)
    return Path(__file__).resolve().parents[3]

WORKSPACE = get_workspace()
MEMORY_DIR = WORKSPACE / 'memory'
RAG_DIR = MEMORY_DIR / '.rag'
LONGTERM_FILE = RAG_DIR / 'longterm.jsonl'
RECALL_FILE = MEMORY_DIR / '.dreams' / 'short-term-recall.json'

MEMORY_K = 200          # 短记忆最大容量
PROMOTE_AFTER_DAYS = 30  # 超过此天数且未被召回则晋升
MAX_PROMOTE = 20        # 每次最多晋升数量

# ─── 文件操作 ────────────────────────────────────────────

def ensure_rag_dir():
    RAG_DIR.mkdir(exist_ok=True)
    if not LONGTERM_FILE.exists():
        LONGTERM_FILE.write_text('', encoding='utf-8')

def load_recall():
    if not RECALL_FILE.exists():
        return {}
    try:
        return json.loads(RECALL_FILE.read_text(encoding='utf-8')).get('entries', {})
    except:
        return {}

def save_recall(entries):
    data = {'entries': entries}
    RECALL_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

def load_longterm():
    if not LONGTERM_FILE.exists():
        return []
    entries = []
    try:
        lines = LONGTERM_FILE.read_text(encoding='utf-8').strip().split('\n')
        for line in reversed(lines):
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except:
                    continue
    except:
        pass
    return list(reversed(entries))

# ─── 晋升逻辑 ────────────────────────────────────────────

def promote_to_longterm(max_promote=MAX_PROMOTE):
    """
    将太久未被召回的条目晋升到长记忆。

    条件：
    - age > PROMOTE_AFTER_DAYS（30天）
    - recallCount < 3（未被频繁召回）
    """
    ensure_rag_dir()
    recall_entries = load_recall()
    
    if len(recall_entries) <= MEMORY_K:
        print(f"  Short-term entries {len(recall_entries)} <= {MEMORY_K}, no promotion needed")
        return 0
    
    now = datetime.now()
    promoted = []
    to_remove = []
    
    for key, entry in recall_entries.items():
        last_recalled = entry.get('lastRecalledAt', '')
        recall_count = entry.get('recallCount', 0)
        
        # 计算年龄（从最后召回或创建时间）
        if last_recalled:
            try:
                last_dt = datetime.fromisoformat(last_recalled.replace('Z', '+00:00'))
                age_days = (now - last_dt.replace(tzinfo=None)).total_seconds() / 86400
            except:
                continue
        else:
            created = entry.get('createdAt', '')
            if not created:
                continue
            try:
                created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                age_days = (now - created_dt.replace(tzinfo=None)).total_seconds() / 86400
            except:
                continue
        
        # 晋升条件：太旧 + 召回次数少
        if age_days > PROMOTE_AFTER_DAYS and recall_count < 3:
            entry['promotedAt'] = now.isoformat()
            entry['originalKey'] = key
            promoted.append(entry)
            to_remove.append(key)
    
    if not promoted:
        print(f"  [Note] No entries meet criteria (age > {PROMOTE_AFTER_DAYS} days AND recallCount < 3)")
        return 0
    
    # 追加到长记忆文件
    count = 0
    with LONGTERM_FILE.open('a', encoding='utf-8') as f:
        for entry in promoted[:max_promote]:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            count += 1
    
    # 从短记忆移除被晋升的条目
    for key in to_remove[:max_promote]:
        recall_entries.pop(key, None)
    save_recall(recall_entries)
    
    print(f"  晋升 {count} 条到长记忆")
    return count

# ─── 检索逻辑 ────────────────────────────────────────────

def query_longterm(query, k=5):
    """
    在长记忆中搜索与 query 相关的条目。
    使用简单关键词匹配（类似 MetaGPT 的 BM25 简化版）。
    """
    entries = load_longterm()
    if not entries:
        return []
    
    query_words = set(query.lower().split())
    query_words = {w for w in query_words if len(w) >= 2}
    
    scored = []
    for entry in entries:
        content = entry.get('snippet', '') or entry.get('content', '')
        content_lower = content.lower()
        
        matches = sum(1 for w in query_words if w in content_lower)
        if matches > 0:
            scored.append((matches, entry))
    
    scored.sort(key=lambda x: -x[0])
    return [e for _, e in scored[:k]]

# ─── 状态查看 ────────────────────────────────────────────

def show_status():
    recall_entries = load_recall()
    longterm_entries = load_longterm()
    
    print(f"\n[Dream] Long-Term Memory Status")
    print(f"  Short-term recall: {len(recall_entries)} 条 (max: {MEMORY_K})")
    print(f"  Long-term (RAG):   {len(longterm_entries)} 条")
    
    if len(recall_entries) > MEMORY_K:
        overflow = len(recall_entries) - MEMORY_K
        print(f"  [!] Overflow {overflow} 条, run --promote")
    else:
        print(f"  [OK] Short-term within limit")
    
    if longterm_entries:
        print(f"\nRecent promoted entries:")
        for e in longterm_entries[-3:]:
            snippet = (e.get('snippet', '') or e.get('content', ''))[:50]
            promoted = e.get('promotedAt', '')[:10]
            print(f"    [{promoted}] {snippet}...")

# ─── CLI ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Dream Long-Term Memory')
    parser.add_argument('--promote', action='store_true', help='晋升老条目到长记忆')
    parser.add_argument('--query', type=str, help='搜索长记忆')
    parser.add_argument('--status', action='store_true', help='查看状态')
    parser.add_argument('--k', type=int, default=5, help='返回结果数量')
    
    args = parser.parse_args()
    
    if args.status:
        show_status()
    elif args.promote:
        count = promote_to_longterm()
        if count > 0:
            show_status()
    elif args.query:
        results = query_longterm(args.query, k=args.k)
        if results:
            print(f"\n[Search] '{args.query}' results:")
            for i, e in enumerate(results, 1):
                snippet = (e.get('snippet', '') or e.get('content', ''))[:80]
                print(f"  {i}. {snippet}...")
        else:
            print(f"\n[Search] No results")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
