#!/usr/bin/env python3
"""
知识引擎 V1 - 专业知识库检索系统
区别于记忆引擎（记录事实），知识引擎专门管理结构化领域知识
支持：语义搜索 + 分类检索 + 自动索引 + 交叉引用
"""
import json, hashlib, re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings

class KnowledgeEngine:
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.knowledge_dirs = [
            memory_dir / 'knowledge',
            memory_dir / 'feishu-knowledge',
        ]
        self.state_file = memory_dir / '.knowledge-engine-state.json'
        self.state = self._load_state()
        
        # 独立的knowledge向量库（跟memory分开）
        self.client = chromadb.PersistentClient(
            path=str(memory_dir / '.chroma-knowledge'),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
    
    def _load_state(self) -> Dict:
        if self.state_file.exists():
            try: return json.load(open(self.state_file))
            except: pass
        return {
            'last_index': None,
            'total_chunks': 0,
            'by_category': {},
            'indexed_files': []
        }
    
    def _save_state(self):
        self.state['last_index'] = datetime.now().isoformat()
        json.dump(self.state, open(self.state_file, 'w'), indent=2, ensure_ascii=False)
    
    def _chunk_md(self, content: str, source: str, category: str = 'general') -> List[Dict]:
        """将md文件拆分成语义块"""
        chunks = []
        lines = content.split('\n')
        current_section = '概述'
        current_chunk = []
        
        for line in lines:
            # 检测标题（知识点分割点）
            if line.startswith('## ') or line.startswith('### '):
                # 保存上一个chunk
                if current_chunk:
                    text = '\n'.join(current_chunk).strip()
                    if len(text) > 50:
                        chunks.append({
                            'text': text[:1000],
                            'section': current_section,
                            'source': source,
                            'category': category,
                        })
                current_section = line.strip('# ').strip()
                current_chunk = [line]
            elif line.strip() and not line.startswith('>') and not line.startswith('---'):
                current_chunk.append(line)
            elif not line.strip() and current_chunk:
                # 空行也保留，但太长就断开
                text = '\n'.join(current_chunk).strip()
                if len(text) > 1000:
                    if current_chunk:
                        chunks.append({
                            'text': '\n'.join(current_chunk).strip()[:1000],
                            'section': current_section,
                            'source': source,
                            'category': category,
                        })
                    current_chunk = []
                else:
                    current_chunk.append(line)
        
        # 最后一个chunk
        if current_chunk:
            text = '\n'.join(current_chunk).strip()
            if len(text) > 50:
                chunks.append({
                    'text': text[:1000],
                    'section': current_section,
                    'source': source,
                    'category': category,
                })
        
        return chunks
    
    def _categorize(self, filename: str, content: str) -> str:
        """自动分类知识文件（中文优先）"""
        name = filename
        # 广告/投放
        if any(k in name for k in ['广告','投放','ads','kuaishou','tencent','千川','信息流','ROI']):
            return '广告投放'
        # 技术
        if any(k in name for k in ['技术','tech','python','代码','编程']):
            return '技术开发'
        # 金融
        if any(k in name for k in ['金融','crypto','投资','基金','股票','币']):
            return '金融投资'
        # 内容创作
        if any(k in name for k in ['创作','文案','脚本','小红书','社媒','视频','混剪','漫剧']):
            return '内容创作'
        # 数据
        if any(k in name for k in ['数据','分析','报表']):
            return '数据分析'
        # 财务法务
        if any(k in name for k in ['财务','法务','合同','税务']):
            return '财务法务'
        # 安全
        if any(k in name for k in ['安全','security']):
            return '安全'
        # 系统规则
        if any(k in name for k in ['调度','dispatch','规则','intent','关键词']):
            return '系统规则'
        # 学习沉淀
        if any(k in name for k in ['学习沉淀','知识库','学习']):
            return '系统工具'
        # 用内容判断
        if '广告' in content[:200]:
            return '广告投放'
        if '技术' in content[:200]:
            return '技术开发'
        return '通用'
    
    def index_agent_knowledge(self):
        """扫描各Agent本地知识文件，索引到统一知识库"""
        agents_dir = Path.home() / '.agent-mem/agents'
        if not agents_dir.exists(): return 0
        
        total = 0
        for agent_dir in sorted(agents_dir.iterdir()):
            agent_agent_dir = agent_dir / 'agent'
            if not agent_agent_dir.exists(): continue
            agent_name = agent_dir.name
            
            # 只扫描真正的知识文件（跳过系统文件）
            skip_patterns = ['IDENTITY', 'SOUL', 'AGENTS', 'TOOLS', 'MEMORY', 'DREAMS',
                           'HEARTBEAT', 'LEARNING', 'ACTIVATION', 'BOOTSTRAP',
                           'USER', 'SECURITY', 'models.json', 'README']
            
            for f in sorted(agent_agent_dir.glob('*.md')):
                fname = f.name.upper()
                if any(p in fname for p in skip_patterns): continue
                if f.stat().st_size < 200: continue  # 太小的文件跳过
                
                try:
                    content_text = f.read_text(encoding='utf-8', errors='ignore')
                    chunks = self._chunk_md(content_text, f.name, 'agent_knowledge')
                    
                    for chunk in chunks:
                        cid = hashlib.md5((agent_name + chunk['text']).encode()).hexdigest()[:16]
                        existing = self.collection.get(ids=[cid])
                        if existing and existing['ids']: continue
                        
                        self.collection.add(
                            documents=[chunk['text']],
                            metadatas=[{
                                'source': f.name,
                                'section': chunk['section'],
                                'category': 'agent_knowledge',
                                'source_agent': agent_name,  # 标记所属Agent
                            }],
                            ids=[cid]
                        )
                        total += 1
                except: continue
        return total

    def search(self, query: str, n: int = 5, category: str = None, agent: str = None) -> List[Dict]:
        """搜索知识库（先搜Agent私有知识，再搜共享知识，合并排序）"""
        all_results = []
        seen_ids = set()
        
        if agent and agent in self.AGENT_CATEGORIES:
            # Step 1: Agent私有知识（最高优先级）
            private = self.collection.query(
                query_texts=[query],
                n_results=n,
                where={"source_agent": agent}
            )
            if private and private['ids']:
                for i in range(len(private['ids'][0])):
                    cid = private['ids'][0][i]
                    if cid not in seen_ids:
                        seen_ids.add(cid)
                        all_results.append({
                            'text': private['documents'][0][i],
                            'distance': private['distances'][0][i] * 0.7,  # 私有知识加权
                            'source': private['metadatas'][0][i].get('source', ''),
                            'section': private['metadatas'][0][i].get('section', ''),
                            'category': 'agent_knowledge',
                            'source_agent': agent,
                        })
            
            # Step 2: 该Agent分类的共享知识
            allowed = self.AGENT_CATEGORIES[agent]
            shared = self.collection.query(
                query_texts=[query],
                n_results=n * 2,
                where={"category": {"$in": allowed}}
            )
            if shared and shared['ids']:
                for i in range(len(shared['ids'][0])):
                    cid = shared['ids'][0][i]
                    if cid not in seen_ids:
                        seen_ids.add(cid)
                        all_results.append({
                            'text': shared['documents'][0][i],
                            'distance': shared['distances'][0][i],
                            'source': shared['metadatas'][0][i].get('source', ''),
                            'section': shared['metadatas'][0][i].get('section', ''),
                            'category': shared['metadatas'][0][i].get('category', ''),
                        })
        else:
            # 无Agent指定：全库搜索
            where = {"category": category} if category else None
            results = self.collection.query(
                query_texts=[query], n_results=n,
                where=where if where else None
            )
            if results and results['ids']:
                for i in range(len(results['ids'][0])):
                    all_results.append({
                        'text': results['documents'][0][i],
                        'distance': results['distances'][0][i],
                        'source': results['metadatas'][0][i].get('source', ''),
                        'section': results['metadatas'][0][i].get('section', ''),
                        'category': results['metadatas'][0][i].get('category', ''),
                    })
        
        return sorted(all_results, key=lambda x: x['distance'])[:n]
    
    def index_all(self):
        """索引所有知识文件"""
        total = 0
        categories = {}
        indexed = []
        
        for kdir in self.knowledge_dirs:
            if not kdir.exists(): continue
            for f in sorted(kdir.glob('*.md')):
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    category = self._categorize(f.name, content)
                    chunks = self._chunk_md(content, f.name, category)
                    
                    for chunk in chunks:
                        cid = hashlib.md5(chunk['text'].encode()).hexdigest()[:16]
                        # 避免重复
                        existing = self.collection.get(ids=[cid])
                        if existing and existing['ids']:
                            continue
                        
                        self.collection.add(
                            documents=[chunk['text']],
                            metadatas=[{
                                'source': chunk['source'],
                                'section': chunk['section'],
                                'category': chunk['category'],
                            }],
                            ids=[cid]
                        )
                        total += 1
                        categories[chunk['category']] = categories.get(chunk['category'], 0) + 1
                    
                    indexed.append(f.name)
                except Exception as e:
                    print(f"⚠️ 索引失败 {f.name}: {e}")
        
        self.state['total_chunks'] = total
        self.state['by_category'] = categories
        self.state['indexed_files'] = indexed
        self._save_state()
        return total, categories
    
    # Agent → 允许的知识分类映射
    AGENT_CATEGORIES = {
        'advertising-agent':    ['广告投放', '通用', '系统工具'],
        'media-buyer':          ['广告投放', '通用', '系统工具'],
        'short-drama-expert':   ['广告投放', '通用', '系统工具'],
        'tech-expert':          ['技术开发', '通用', '系统工具'],
        'code-architect':       ['技术开发', '通用', '系统工具'],
        'code-reviewer':        ['技术开发', '通用', '系统工具'],
        'data-assistant':       ['数据分析', '通用', '系统工具'],
        'data-analyst':         ['数据分析', '通用', '系统工具'],
        'finance-assistant':    ['金融投资', '通用', '系统工具'],
        'stock-analyst':        ['金融投资', '通用', '系统工具'],
        'finance-legal':        ['财务法务', '通用', '系统工具'],
        'agent-admin':           ['系统规则', '系统工具', '通用', '技术开发'],
        'designer':             ['设计创意', '通用', '系统工具'],
        'xiaohongshu-agent':    ['内容创作', '通用', '系统工具'],
        'marketing-assistant':  ['内容创作', '通用', '系统工具'],
        'security-expert':      ['安全', '通用', '系统工具'],
        'prompt-optimizer':     ['系统规则', '通用', '系统工具'],
        'intelligence-officer': ['通用', '系统工具'],
        'product-selector':     ['通用', '系统工具'],
        'main':                 ['通用', '系统工具'],
    }
    
    def query(self, question: str, n: int = 5) -> Dict:
        """知识问答 - 搜索 + 返回相关上下文"""
        results = self.search(question, n)
        return {
            'question': question,
            'results': results,
            'total_found': len(results),
        }
    
    def get_stats(self) -> Dict:
        return {
            'total_chunks': self.collection.count(),
            'categories': self.state.get('by_category', {}),
            'indexed_files': len(self.state.get('indexed_files', [])),
            'last_index': self.state.get('last_index'),
        }

if __name__ == '__main__':
    home = Path.home()
    ke = KnowledgeEngine(home / '.agent-mem/memory')
    
    print("📚 知识引擎 - 建索引...")
    total, cats = ke.index_all()
    print(f"   索引了 {total} 个知识块, 分类: {len(cats)} 个")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"     {cat}: {count}")
    
    print("\n🔍 搜索测试:")
    for q in ['快手广告规则', 'Python代码示例', '加密货币', '调度规则']:
        r = ke.search(q, n=2)
        print(f"\n  \"{q}\":")
        for item in r:
            dist = item['distance']
            star = '⭐' if dist < 0.3 else '👍' if dist < 0.5 else '📄'
            print(f"    {star} [{dist:.3f}] [{item['category']}] {item['text'][:50]}...")
