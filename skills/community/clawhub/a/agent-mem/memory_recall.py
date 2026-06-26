#!/usr/bin/env python3
import math
"""
记忆召回模块 V3 - 集成 OpenClaw 向量搜索
- 按段落分块、过滤噪音
- 混合：向量搜索（语义） + 本地文件搜索（关键词）
"""

import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict
from datetime import datetime

HOME = Path.home()
STATE_V2 = HOME / '.agent-mem/memory-engine-state.json'
MEMORY_MD = HOME / '.agent-mem/MEMORY.md'

CATEGORY_NAMES = {
    "person": "👤 人物",
    "work": "💼 工作",
    "tech": "⚙️ 技术",
    "preference": "❤️ 偏好",
    "schedule": "📅 日程",
    "insight": "💡 洞察",
    "system_change": "🔧 系统变更",
    "general": "📝 一般"
}

NOISE_PATTERNS = [
    r'^<!\-\-\s*openclaw:dreaming:',
    r'^Candidate:',
    r'^Reflections:',
    r'^Theme:',
    r'^Light Sleep',
    r'^REM Sleep',
]



class BM25:
    """简易BM25实现（不依赖外部库）"""
    def __init__(self, corpus):
        self.corpus = corpus
        self.k1 = 1.5
        self.b = 0.75
        self._build_index()
    
    def _build_index(self):
        self.tokenized = [self._tokenize(d) for d in self.corpus]
        self.avgdl = sum(len(t) for t in self.tokenized) / max(len(self.tokenized), 1)
        self.N = len(self.tokenized)
        self.idf = {}
        from collections import Counter
        doc_freq = Counter()
        for tokens in self.tokenized:
            doc_freq.update(set(tokens))
        for word, freq in doc_freq.items():
            self.idf[word] = math.log((self.N - freq + 0.5) / (freq + 0.5) + 1)
    
    def _tokenize(self, text):
        import re
        tokens = []
        for part in re.findall(r'[a-zA-Z]+|[\u4e00-\u9fff]', text.lower()):
            if re.match(r'[a-zA-Z]+', part):
                tokens.append(part)
            else:
                tokens.extend(list(part))
        return tokens
    
    def score(self, query):
        q_tokens = set(self._tokenize(query))
        scores = []
        for tokens in self.tokenized:
            score = 0.0
            doc_len = len(tokens)
            for q in q_tokens:
                if q in self.idf:
                    tf = tokens.count(q)
                    score += self.idf[q] * (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl))
            scores.append(score)
        return scores


class MultiSignalFusion:
    """多信号融合排序器：向量 + BM25 + 时间"""
    
    @staticmethod
    def fuse(vector_results, bm25_results, time_bias=0.2):
        scores = {}
        max_v = max((r.get('distance', 0) for r in vector_results), default=1)
        for r in vector_results:
            key = r.get('text', '')
            scores[key] = {'vector': 1 - (r['distance'] / max_v), 'source': r.get('source', ''), 'text': key}
        
        for r in bm25_results:
            key = r.get('text', '')
            if key in scores:
                scores[key]['bm25'] = r.get('score', 0)
            else:
                scores[key] = {'bm25': r.get('score', 0), 'source': r.get('source', ''), 'text': key}
        
        now = __import__('datetime').datetime.now()
        for key, s in scores.items():
            src = s.get('source', '')
            if src.endswith('.md'):
                try:
                    date_str = src.replace('.md', '')[:10]
                    dt = __import__('datetime').datetime.strptime(date_str, '%Y-%m-%d')
                    days_old = (now - dt).days
                    s['time_score'] = math.exp(-days_old / 14)
                except:
                    s['time_score'] = 0.5
            else:
                s['time_score'] = 0.5
        
        for key, s in scores.items():
            v = s.get('vector', 0)
            b = s.get('bm25', 0)
            t = s.get('time_score', 0.5)
            s['fusion_score'] = v * 0.5 + b * 0.3 + t * 0.2
        
        return sorted(scores.values(), key=lambda x: x['fusion_score'], reverse=True)[:10]

class MemoryRecall:
    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        if STATE_V2.exists():
            with open(STATE_V2, 'r') as f:
                return json.load(f)
        return {'stats': {'by_category': {}}}

    def _is_noise(self, text: str) -> bool:
        for pattern in NOISE_PATTERNS:
            if re.match(pattern, text.strip()):
                return True
        return False

    def _vector_search(self, query: str, max_results: int = 8) -> List[Dict]:
        """调用 OpenClaw 内置向量搜索"""
        try:
            result = subprocess.run(
                ['openclaw', 'memory', 'search', query, '--max-results', str(max_results)],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return []

            # 解析输出
            results = []
            blocks = re.split(r'\n## \d+\n', result.stdout)
            if len(blocks) <= 1:
                # 尝试按分数分割
                blocks = re.split(r'\n\d+\.\d+ ', result.stdout)

            for block in blocks:
                block = block.strip()
                if not block or len(block) < 20:
                    continue

                # 提取分数
                score_match = re.match(r'^(\d+\.\d+)\s+', block)
                score = float(score_match.group(1)) if score_match else 0.0
                if score_match:
                    block = block[score_match.end():]

                # 提取来源
                source_match = re.match(r'(.+?:\d+-\d+)\n', block)
                source = source_match.group(1) if source_match else 'unknown'

                if self._is_noise(block):
                    continue

                results.append({
                    'text': block[:300],
                    'source': source,
                    'score': score,
                    'type': 'vector_search'
                })

            return results
        except (subprocess.TimeoutExpired, Exception) as e:
            return []

    def _keyword_search(self, query: str, days: int = 30) -> List[Dict]:
        """本地关键词搜索（兜底）"""
        memory_dir = HOME / '.agent-mem/memory'
        results = []
        cutoff = datetime.now().timestamp() - (days * 86400)

        for f in sorted(memory_dir.glob('*.md'), key=lambda x: -x.stat().st_mtime):
            if f.name.startswith('.') or re.match(r'^\d{4}-\d{2}-\d{2}-\d{4}\.md$', f.name):
                continue
            if f.stat().st_mtime < cutoff:
                continue

            with open(f, 'r') as fp:
                content = fp.read()

            if query.lower() not in content.lower():
                continue

            # 按段落提取
            sections = self._extract_sections(content, query)
            for s in sections:
                if self._is_noise(s['text']) or self._is_noise(s.get('header', '')):
                    continue
                results.append({
                    'text': s['text'][:300],
                    'header': s.get('header', ''),
                    'source': f.name,
                    'type': 'keyword_search'
                })

        return results

    def _extract_sections(self, content: str, keyword: str = None) -> List[Dict]:
        sections = []
        current_section = []
        current_header = ""

        for line in content.split('\n'):
            if line.startswith('#'):
                if current_section:
                    text = '\n'.join(current_section).strip()
                    if text and len(text) > 15:
                        sections.append({'header': current_header, 'text': text})
                current_header = line.strip()
                current_section = []
            else:
                current_section.append(line)

        if current_section:
            text = '\n'.join(current_section).strip()
            if text and len(text) > 15:
                sections.append({'header': current_header, 'text': text})

        if keyword:
            kw = keyword.lower()
            return [s for s in sections if kw in s['text'].lower() or kw in s['header'].lower()]
        return sections

    def recall(self, query: str, limit: int = 10) -> str:
        """混合召回：向量搜索 + 关键词搜索"""
        results = []

        # 1. 向量语义搜索（主）
        vector_results = self._vector_search(query, max_results=8)
        results.extend(vector_results)

        # 2. 关键词搜索（补充）
        keyword_results = self._keyword_search(query)
        for r in keyword_results:
            r['score'] = 0.3  # 关键词匹配给基础分
            results.append(r)

        # 3. MEMORY.md 搜索
        if MEMORY_MD.exists():
            with open(MEMORY_MD, 'r') as f:
                sections = self._extract_sections(f.read(), query)
            for s in sections:
                if not self._is_noise(s['text']):
                    results.append({
                        'text': s['text'][:300],
                        'header': s.get('header', ''),
                        'source': 'MEMORY.md',
                        'score': 0.5,
                        'type': 'memory_md'
                    })

        if not results:
            return f"ℹ️ 未找到与「{query}」相关的记忆"

        # 按分数排序，去重
        results.sort(key=lambda x: x.get('score', 0), reverse=True)
        seen = set()
        unique = []
        for r in results:
            key = r.get('text', '')[:80]
            if key not in seen:
                seen.add(key)
                unique.append(r)

        # 格式化输出
        output = f"🔍 搜索「{query}」找到 {len(unique)} 条相关记忆：\n\n"
        for r in unique[:limit]:
            source = r.get('source', 'unknown')
            text = r.get('text', '')[:200]
            score = r.get('score', 0)
            rtype = r.get('type', '')

            if rtype == 'vector_search':
                output += f"🎯 [{score:.2f}] {source}\n   {text}\n\n"
            elif rtype == 'keyword_search':
                output += f"📄 [{source}] {r.get('header', '')}\n   {text}\n\n"
            else:
                output += f"📌 [{source}] {r.get('header', '')}\n   {text}\n\n"

        by_cat = self.state.get('stats', {}).get('by_category', {})
        if by_cat:
            output += "📊 记忆库分类：\n"
            for cat, cnt in sorted(by_cat.items(), key=lambda x: -x[1])[:5]:
                output += f"  - {CATEGORY_NAMES.get(cat, cat)}: {cnt}条\n"

        return output

    def get_recent_memories(self, days: int = 7) -> str:
        memory_dir = HOME / '.agent-mem/memory'
        recent_files = []
        cutoff = datetime.now().timestamp() - (days * 86400)

        for f in memory_dir.glob('*.md'):
            if f.name.startswith('.') or re.match(r'^\d{4}-\d{2}-\d{2}-\d{4}\.md$', f.name):
                continue
            if f.stat().st_mtime > cutoff:
                recent_files.append(f)

        if not recent_files:
            return f"ℹ️ 最近{days}天没有记忆文件"

        output = f"📅 最近{days}天记忆 ({len(recent_files)}个文件)：\n\n"
        for f in sorted(recent_files, key=lambda x: -x.stat().st_mtime)[:10]:
            with open(f, 'r') as fp:
                content = fp.read()
            sections = self._extract_sections(content)
            meaningful = [s for s in sections if not self._is_noise(s.get('header', ''))]
            date = f.stem[:10]
            preview = meaningful[0]['text'][:100] if meaningful else content[:100]
            output += f"**{date}**: {preview}...\n\n"

        return output

    def get_context_for_topic(self, topic: str) -> str:
        return self.recall(topic, limit=15)


if __name__ == '__main__':
    import sys
    recall = MemoryRecall()
    if len(sys.argv) < 2:
        print("用法: memory_recall.py <查询词> [--recent N]")
        sys.exit(1)

    if sys.argv[1] == '--recent':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(recall.get_recent_memories(days))
    else:
        print(recall.recall(sys.argv[1]))
