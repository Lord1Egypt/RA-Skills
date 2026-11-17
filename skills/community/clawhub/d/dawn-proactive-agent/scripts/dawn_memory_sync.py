#!/usr/bin/env python3
"""
dawn_memory_sync.py - L1↔L3 状态回填Hook
=========================================

将L1(session-state.json)的当前持仓代码，自动去L3(LanceDB)检索
该票近3次的交易教训和历史关联，预热到会话上下文。

用法:
  python dawn_memory_sync.py                # 运行同步
  python dawn_memory_sync.py --verbose      # 详细输出
  python dawn_memory_sync.py --to-context    # 输出预热上下文文本
"""

import os, sys, json, time
import lancedb
from sentence_transformers import SentenceTransformer
import numpy as np

WS = os.path.expanduser(r'~\.openclaw\workspace')
DB_PATH = r'C:\Users\chen\vecdb\data'
MODEL_NAME = 'all-MiniLM-L6-v2'

# HuggingFace镜像（国内网络）
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_OFFLINE'] = 'false'

ETF_NAME_MAP = {
    '515580': '科技100ETF',
    '588090': '科创50ETF',
    '560910': '电池ETF',
    '513110': '纳指ETF',
}


def get_current_holdings():
    """从session-state.json读取当前持仓"""
    ss_path = os.path.join(WS, 'session-state.json')
    if not os.path.exists(ss_path):
        return []
    try:
        with open(ss_path, 'r', encoding='utf-8') as f:
            ss = json.load(f)
        holdings = ss.get('holdings', [])
        if not holdings:
            # 也可能是代码字符串列表
            for k in ('holdings', 'positions', 'portfolio'):
                v = ss.get(k, [])
                if v:
                    holdings = v
                    break
        return holdings
    except Exception as e:
        print(f'[WARN] 读取session-state失败: {e}')
        return []


def search_l3_for_ticker(ticker: str, top_k: int = 3):
    """在LanceDB中搜索与持仓相关的记忆"""
    try:
        db = lancedb.connect(DB_PATH)
        tables = db.list_tables()
        if 'memories' not in tables:
            return []

        tbl = db.open_table('memories')
        model = SentenceTransformer(MODEL_NAME)

        # 构建搜索关键词
        name = ETF_NAME_MAP.get(ticker, '')
        queries = [f"{ticker} ETF", name, f"{name} 教训"]
        queries = [q for q in queries if q.strip()]

        all_results = []
        seen_ids = set()

        for q in queries:
            q_vec = model.encode(q, normalize_embeddings=True)
            results = tbl.search(q_vec).limit(top_k).to_list()
            for r in results:
                rid = r.get('id', '')
                if rid and rid not in seen_ids:
                    seen_ids.add(rid)
                    # 计算置信度
                    distance = r.get('_distance', 0)
                    confidence = max(0, 1.0 - distance)
                    all_results.append({
                        'id': rid,
                        'text': r.get('text', '')[:200],
                        'confidence': round(confidence, 3),
                        'source': r.get('source', 'unknown'),
                        'created_at': str(r.get('created_at', '')),
                    })

        # 按置信度排序
        all_results.sort(key=lambda x: -x['confidence'])
        return all_results[:top_k]

    except Exception as e:
        print(f'[WARN] LanceDB搜索失败: {e}')
        return []


def _search_graph_for_strategy(verbose=False):
    # 从策略实体搜索教训关联
    try:
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        from dawn_memory_graph import DawnMemoryGraph
        g = DawnMemoryGraph()
        results = []
        for sid in ['strategy_competition_portfolio']:
            entity = g.get_entity(sid)
            if not entity: continue
            rels = g.get_relations(sid, max_depth=1, min_quality=0.55)
            for r in rels:
                d = r.get('description', '')
                results.append({'source':'graph','text':'['+r['rel']+'] '+r['source_name']+': '+d,'confidence':round(r['quality'],2)})
        return results
    except Exception as e:
        if verbose: print('[WARN] 图谱策略搜索失败:', e)
        return []

def build_warmup_context(verbose: bool = False):
    """构建预热上下文文本"""
    holdings = get_current_holdings()
    if not holdings:
        if verbose:
            print('[SYNC] 当前无持仓，跳过预热')
        return ''

    if verbose:
        codes = ', '.join(holdings)
        names = ', '.join([ETF_NAME_MAP.get(c, c) for c in holdings])
        print(f'[SYNC] 当前持仓: {codes} ({names})')
        print(f'[SYNC] 正在L3+L2图谱检索相关历史记忆...')

    context_parts = []
    total = 0

    for ticker in holdings:
        name = ETF_NAME_MAP.get(ticker, ticker)
        
        # L3向量搜索
        memories = search_l3_for_ticker(ticker, top_k=3)
        
        # 图谱搜索（补充）
        graph_results = _search_graph_for_strategy(verbose)
        
        all_results = memories + graph_results

        if all_results:
            if verbose:
                print(f'[SYNC] {name}({ticker}): L3={len(memories)}条 + 图谱={len(graph_results)}条')
            context_parts.append(f"## 持仓预热: {name} ({ticker})")
            for i, m in enumerate(all_results, 1):
                snippet = m['text'].replace('\n', ' ').strip()
                if len(snippet) > 200:
                    snippet = snippet[:200] + '...'
                src = m.get('source', '?')
                context_parts.append(f"  {i}. [{src}|{m['confidence']:.2f}] {snippet}")
            total += len(all_results)
        else:
            if verbose:
                print(f'[SYNC] {name}({ticker}): 无记忆')

    if total == 0:
        return ''

    return '\n'.join(context_parts)


def save_warmup_cache(context: str):
    """保存预热上下文到临时文件"""
    cache_path = os.path.join(WS, 'memory', '.warmup_cache.md')
    if context:
        header = f"<!-- warmup: {time.strftime('%Y-%m-%d %H:%M:%S')} -->\n"
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(header + context + '\n')
        return True
    else:
        if os.path.exists(cache_path):
            os.remove(cache_path)
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description='L1↔L3 状态回填')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    parser.add_argument('--to-context', action='store_true', help='输出预热上下文文本')

    args = parser.parse_args()

    context = build_warmup_context(verbose=args.verbose or args.to_context)

    if args.to_context:
        if context:
            print(context)
        else:
            print('[OK] 无预热上下文')
    else:
        saved = save_warmup_cache(context)
        if saved:
            print(f'[OK] 预热上下文已写入 memory/.warmup_cache.md')
        else:
            print('[OK] 无预热数据，已清空缓存')


if __name__ == '__main__':
    main()
