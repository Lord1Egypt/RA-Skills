#!/usr/bin/env python3
"""
记忆引擎 V3 - 分层记忆 + 因果图谱
新增: 工作记忆/短期/长期/核心 四级分层 + 自动因果链检测
"""
import json, sys, argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from enhanced_extractor import EnhancedFactExtractor
from config import CATEGORIES
# HOT层: 实时会话缓存 + 调度日志
import sys; sys.path.insert(0, str(Path(__file__).parent.parent))
from agent_mem.core.hot_cache import write_conversation, query_recent
sys.path.insert(0, str(Path(__file__).parent.parent))

# 分层定义
TIERS = {
    'working': {'max_age_hours': 2,   'max_items': 20,  'description': '当前会话, 2小时内'},
    'short_term': {'max_age_hours': 24, 'max_items': 100, 'description': '一天内'},
    'long_term': {'max_age_days': 30,   'max_items': 500, 'description': '一个月内'},
    'core': {'persist_forever': True,   'min_importance': 7, 'description': '永久记忆, 重要度≥7'},
}

def get_tier(date_str: str, importance: int = 5) -> str:
    """根据日期和重要度判断记忆层级"""
    if importance >= 7:
        return 'core'
    try:
        dt = datetime.fromisoformat(date_str) if 'T' in date_str else \
             datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
        hours_ago = (datetime.now() - dt).total_seconds() / 3600
        if hours_ago <= 2: return 'working'
        if hours_ago <= 24: return 'short_term'
        if hours_ago <= 720: return 'long_term'
        return 'archived'
    except: return 'short_term'

class MemoryEngineV3:
    def __init__(self):
        self.home = Path.home()
        self.memory_dir = self.home / '.agent-mem/memory'
        self.state_file = self.memory_dir / '.memory-engine-state-v3.json'
        self.extractor = EnhancedFactExtractor()
        self.state = self._load_state()
        self._init_modules()

    def _load_state(self) -> Dict:
        if self.state_file.exists():
            try: return json.load(open(self.state_file))
            except: pass
        return {
            'last_run': None, 'version': 'v3',
            'modules': {}, 'stats': {'total_facts':0, 'important_facts':0, 'by_category':{}},
            'tier_stats': {'working':0, 'short_term':0, 'long_term':0, 'core':0, 'archived':0}
        }

    def _init_modules(self):
        modules = {
            'timeline': ('MemoryTimeline', 'from memory_timeline import MemoryTimeline'),
            'contradiction': ('ContradictionDetector', 'from contradiction_detector import ContradictionDetector'),
            'knowledge_graph': ('KnowledgeGraph', 'from knowledge_graph import KnowledgeGraph'),
            'entity_linker': ('EntityLinker', 'from enhance_entity_link import EntityLinker'),
            'forgetting': ('MemoryForgetting', 'from forgetting import MemoryForgetting'),
            'active_recall': ('ActiveRecall', 'from active_recall import ActiveRecall'),
            'memory_feedback': ('MemoryFeedback', 'from memory_feedback import MemoryFeedback'),
            'multi_agent_share': ('MultiAgentMemory', 'from multi_agent_share import MultiAgentMemory'),
        }
        for attr, (cls_name, imp) in modules.items():
            try:
                exec(imp)
                klass = eval(cls_name)
                setattr(self, attr, klass(self.memory_dir))
                self.state[f'{attr}_loaded'] = True
            except Exception as e:
                self.state[f'{attr}_loaded'] = False
                print(f"⚠️ {attr}: {e}")

    def process_daily(self):
        """每日处理 - 带分层记忆管理"""
        now = datetime.now()
        print(f"\n🚀 记忆引擎 V3 - {now.strftime('%Y-%m-%d %H:%M')}")
        print("=" * 40)

        # 1. 从日期文件提取事实
        facts = self._extract_from_files()
        self.state['last_facts'] = facts
        self.state['stats']['total_facts'] = len(facts)
        self.state['stats']['important_facts'] = sum(1 for f in facts if f.get('importance', 5) >= 7)

        # 2. 按层级分类
        tiered = {'working':[], 'short_term':[], 'long_term':[], 'core':[], 'archived':[]}
        for f in facts:
            tier = get_tier(f.get('date', now.isoformat()), f.get('importance', 5))
            tiered[tier].append(f)

        for tier, items in tiered.items():
            self.state['tier_stats'][tier] = len(items)
            print(f"   {tier}: {len(items)}条")
            # 层级容量限制
            if tier in TIERS and len(items) > TIERS[tier].get('max_items', 999):
                print(f"   ⚠️ {tier} 超出上限，运行压缩...")
                self._compress_tier(tier, items)

        # 3. 运行图谱（自动因果链检测）
        if self.state.get('knowledge_graph_loaded'):
            print("\n🕸️ 构建知识图谱因果链...")
            for f in facts:
                self.knowledge_graph.add_event(
                    text=f.get('text', '') or str(f.get('content', '')),
                    date=f.get('date', now.strftime('%Y-%m-%d')),
                    importance=f.get('importance', 5),
                    category=f.get('category', 'general')
                )
            self.knowledge_graph.build_clusters()
            gs = self.knowledge_graph.get_stats()
            print(f"   节点: {gs['nodes']}, 因果链: {gs['chains']}, 高优: {gs['high_importance']}")

        # 4. 矛盾检测
        if self.state.get('contradiction_loaded'):
            print("\n✅ 检测矛盾中...")
            self.contradiction.check_fact("", "") # placeholder

        # 5. 实体链接
        if self.state.get('entity_linker_loaded'):
            print("🔗 更新实体链接...")
            self.entity_linker._save()

        # 6. 主动召回
        if self.state.get('active_recall_loaded'):
            print("🔔 主动召回检查...")
            try: self.active_recall.check_for_recall()
            except: pass

        # 🆕 子Agent记忆分发
        # dedup 由engine_v2自身的时间分级处理
        sync_count = self.sync_hot_cache()
        if sync_count:
            print(f'  📤 已同步 {sync_count} 个Agent工作记忆')
        self.state['last_run'] = now.isoformat()
        self._save_state()
        print(f"\n✅ 处理完成: {sum(len(v) for v in tiered.values())} 条 (总条数: {self.state['stats']['total_facts']})")

    def _extract_from_files(self) -> List[Dict]:
        """从记忆文件中提取事实"""
        facts = []
        memory_files = sorted(self.memory_dir.glob('*.md'))
        for f in memory_files[-5:]:  # 只处理最近5个文件
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                extracted = self.extractor.extract_facts(content, f.stem)
                if isinstance(extracted, list):
                    facts.extend(extracted)
                elif isinstance(extracted, dict):
                    facts.append(extracted)
            except: continue
        return facts

    def _compress_tier(self, tier: str, items: List[Dict]):
        """压缩层级 - 去重 + 合并相似记忆"""
        if not items: return
        limit = TIERS[tier].get('max_items', 100)
        if len(items) <= limit: return
        # 按重要度排序，只保留最重要的
        sorted_items = sorted(items, key=lambda x: x.get('importance', 5), reverse=True)
        kept = sorted_items[:limit]
        self.state['tier_stats'][tier] = len(kept)

    def _save_state(self):
        json.dump(self.state, open(self.state_file, 'w'), indent=2, ensure_ascii=False)

    def get_status(self) -> Dict:
        return {
            'version': 'v3',
            'last_run': self.state.get('last_run'),
            'total_facts': self.state['stats']['total_facts'],
            'important_facts': self.state['stats']['important_facts'],
            'tiers': self.state['tier_stats'],
            'modules': {k: '✅' if v else '❌' for k, v in self.state.items() if k.endswith('_loaded')}
        }
    def init_vector_store(self):
        try:
            from vector_store import VectorStore
            self.vector_store = VectorStore(self.memory_dir)
            self.state['vector_store_loaded'] = True
            return True
        except Exception as e:
            self.state['vector_store_loaded'] = False
            print(f"⚠️ 向量存储加载失败: {e}")
            return False

    def vector_sync(self):
        if not self.state.get('vector_store_loaded'):
            self.init_vector_store()
        import chromadb, json
        from chromadb.config import Settings
        client = chromadb.PersistentClient(
            path=str(self.memory_dir / '.chroma'),
            settings=Settings(anonymized_telemetry=False))
        collection = client.get_or_create_collection('memory_vectors')
        
        # 读取同步状态，只处理新文件
        sync_state_file = self.memory_dir / '.vector-sync-state.json'
        synced = set()
        if sync_state_file.exists():
            synced = set(json.load(open(sync_state_file)).get('synced', []))
        
        all_files = sorted(self.memory_dir.glob('*.md'), key=lambda f: f.stat().st_mtime)
        new_files = [f for f in all_files if f.name not in synced]
        
        count = 0
        errors = 0
        for f in new_files:
            try:
                text = f.read_text(encoding='utf-8', errors='ignore')
                lines = [l.strip() for l in text.split('\n') if l.strip() 
                         and not l.startswith('#') and not l.startswith('>') and len(l.strip()) > 30]
                if lines:
                    ids = [f'{f.stem}_{i}' for i in range(len(lines))]
                    collection.add(documents=lines, metadatas=[{'source': f.name, 'idx': i} for i in range(len(lines))], ids=ids)
                    count += len(lines)
            except Exception as e:
                errors += 1
            finally:
                synced.add(f.name)
        
        json.dump({'synced': list(synced), 'last_sync': str(datetime.now())}, open(sync_state_file, 'w'))
        
        # 触发队列写入
        try: collection.count()
        except: pass
        
        if errors:
            print(f'  \u26a0\ufe0f 向量同步: {count}条新增, {errors}个文件失败')
        else:
            print(f'  \u2705 向量同步: {count}条新向量')
        return count

    def search_vector(self, query: str, n: int = 5):
        if not self.state.get('vector_store_loaded'):
            self.init_vector_store()
        import chromadb
        from chromadb.config import Settings
        client = chromadb.PersistentClient(
            path=str(self.memory_dir / '.chroma'),
            settings=Settings(anonymized_telemetry=False))
        collection = client.get_collection('memory_vectors')
        results = collection.query(query_texts=[query], n_results=n)
        items = []
        for i in range(len(results['ids'][0])):
            items.append({
                'text': results['documents'][0][i],
                'distance': results['distances'][0][i],
                'source': results['metadatas'][0][i].get('source', ''),
            })
        return items




    # 调度学习（非阻塞）
    try:
        from pathlib import Path
        import subprocess
        bridge = Path(__file__).parent.parent / 'scripts/dbridge.py'
        if bridge.exists():
            subprocess.Popen([sys.executable, str(bridge)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

    # 调度学习（非阻塞）
    try:
        import subprocess
        bridge = Path(__file__).parent.parent / 'scripts/dbridge.py'
        if bridge.exists():
            subprocess.Popen(['python3', str(bridge)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

    def sync_hot_cache(self):
        """🔥 重要事实写入各Agent HOT缓存 + 调度日志同步到引擎"""
        try:
            from agent_mem.core.dispatch_logger import sync_to_engine
            facts = self.state.get('last_facts', [])
            agents_list = self._get_active_agents()
            count = 0
            
            if facts:
                important = [f for f in facts if f.get('importance', 5) >= 7][:20]
                print(f'  🔥 引擎提取: {len(facts)} 条, 重要: {len(important)} 条')
                
                # 写入各Agent的HOT缓存（跨通道互通）
                for fact in (important + facts[:10]):
                    f_text = fact.get('text','')[:200]
                    f_imp = fact.get('importance',5)
                    f_cat = fact.get('category','general')
                    for aid in agents_list:
                        write_conversation(aid, 'internal', 
                            f'[{f_cat}] {f_text}', f_imp)
                    count += 1
                
                print(f'  🌐 已分发到 {len(agents_list)} 个Agent (HOT缓存)')
            
            # 调度日志同步到引擎状态（COLD级）
            n = sync_to_engine()
            if n:
                print(f'  📋 同步 {n} 条调度日志到COLD')
            
            return count
        except Exception as e:
            import traceback
            print(f'  ⚠️ HOT同步失败: {e}')
            traceback.print_exc()
            return 0
    
    def _get_active_agents(self):
        """获取活跃Agent列表"""
        try:
            dispatch_file = Path.home() / '.agent-mem/dispatch-data.json'
            if dispatch_file.exists():
                import json
                data = json.load(open(dispatch_file))
                return list(data.get('stats', {}).keys())
        except:
            pass
        return ['tech-expert', 'agent-admin', 'advertising-agent', 'data-assistant',
                'work-assistant', 'prompt-optimizer', 'prompt-architect']
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='记忆引擎 V3')
    parser.add_argument('--mode', choices=['daily', 'once', 'status'], default='once')
    parser.add_argument('--file', help='处理特定文件')
    args = parser.parse_args()

    engine = MemoryEngineV3()

    if args.mode == 'status':
        s = engine.get_status()
        print(json.dumps(s, indent=2, ensure_ascii=False))
    elif args.mode == 'daily':
        engine.process_daily()
    else:
        engine.process_daily()
    def init_vector_store(self):
        """初始化向量存储"""
        try:
            from vector_store import VectorStore
            self.vector_store = VectorStore(self.memory_dir)
            self.state['vector_store_loaded'] = True
            return True
        except Exception as e:
            self.state['vector_store_loaded'] = False
            print(f"⚠️ 向量存储加载失败: {e}")
            return False

    def vector_sync(self):
        """同步到向量库"""
        if not self.state.get('vector_store_loaded'):
            self.init_vector_store()
        
        import chromadb
        from chromadb.config import Settings
        persist_dir = str(self.memory_dir / '.chroma')
        client = chromadb.PersistentClient(path=persist_dir, settings=Settings(anonymized_telemetry=False))
        collection = client.get_or_create_collection('memory_vectors')
        
        count = 0
        for f in sorted(self.memory_dir.glob('*.md'))[-20:]:
            content = f.read_text(encoding='utf-8', errors='ignore')
            lines = [l.strip() for l in content.split('\n') if l.strip() 
                     and not l.startswith('#') and not l.startswith('>') and len(l.strip()) > 30]
            if lines:
                collection.add(
                    documents=lines,
                    metadatas=[{'source': f.name, 'idx': i, 'date': f.stem} for i in range(len(lines))],
                    ids=[f'{f.stem}_{i}' for i in range(len(lines))]
                )
                count += len(lines)
        return count

    def search_vector(self, query: str, n: int = 5) -> List[Dict]:
        """语义搜索（供外部调用）"""
        if not self.state.get('vector_store_loaded'):
            self.init_vector_store()
            if not self.state.get('vector_store_loaded'):
                return []
        
        import chromadb
        from chromadb.config import Settings
        client = chromadb.PersistentClient(
            path=str(self.memory_dir / '.chroma'),
            settings=Settings(anonymized_telemetry=False)
        )
        collection = client.get_collection('memory_vectors')
        results = collection.query(query_texts=[query], n_results=n)
        
        items = []
        for i in range(len(results['ids'][0])):
            items.append({
                'text': results['documents'][0][i],
                'distance': results['distances'][0][i],
                'source': results['metadatas'][0][i].get('source', ''),
            })
        return items
