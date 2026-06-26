#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Query Agent - 自然语言记忆查询助手（增强版）
集成定时同步功能，支持自动同步检查、状态查询和配置管理
"""

import sqlite3
import re
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
import hashlib

# 数据库路径
DB_PATH = Path(__file__).parent / "memory.db"
# 配置文件路径
CONFIG_PATH = Path(__file__).parent / "memory_query_config.json"
# 状态文件路径
STATE_PATH = Path(__file__).parent / "memory_query_state.json"
# 记忆目录
MEMORY_DIR = Path(__file__).parent / "memory"

# 默认配置
DEFAULT_CONFIG = {
    "sync": {
        "interval_minutes": 15,
        "auto_sync": True,
        "check_on_query": True
    },
    "query": {
        "default_limit": 10,
        "fuzzy_match": True
    },
    "log": {
        "enabled": True,
        "path": str(Path(__file__).parent / "memory_query.log")
    }
}

# 默认状态
DEFAULT_STATE = {
    "last_sync": None,
    "last_sync_timestamp": 0,
    "synced_files": [],
    "total_records": 0,
    "pending_files": [],
    "sync_count": 0
}

# 意图识别模式
PATTERNS = {
    "时间范围": ["什么时候", "何时", "时间", "日期", "号", "日"],
    "内容搜索": ["什么", "哪些", "关于", "找", "搜索"],
    "统计": ["多少", "几个", "统计", "数量", "总共"],
    "最近": ["最近", "最新", "上个", "这个", "近"],
    "类型": ["类型", "哪种", "什么类型"],
}

# SQL 模板
SQL_TEMPLATES = {
    "time_query": "SELECT * FROM memories WHERE created_at BETWEEN ? AND ? ORDER BY created_at DESC",
    "keyword_search": "SELECT * FROM memories WHERE content LIKE ? OR name LIKE ? OR description LIKE ? ORDER BY created_at DESC",
    "count": "SELECT COUNT(*) FROM memories WHERE content LIKE ?",
    "recent": "SELECT * FROM memories ORDER BY created_at DESC LIMIT ?",
    "type_filter": "SELECT * FROM memories WHERE type = ? ORDER BY created_at DESC",
    "type_count": "SELECT COUNT(*) FROM memories WHERE type = ?",
    "all": "SELECT * FROM memories ORDER BY created_at DESC",
}


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else CONFIG_PATH
        self.config = self.load()
    
    def load(self) -> Dict:
        """加载配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return DEFAULT_CONFIG.copy()
    
    def save(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default=None):
        """获取配置值（支持点号访问嵌套）"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value):
        """设置配置值（支持点号访问嵌套）"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()
    
    def update_config(self, updates: Dict):
        """批量更新配置"""
        for key, value in updates.items():
            self.set(key, value)


class StateManager:
    """状态管理器"""
    
    def __init__(self, state_path: Optional[str] = None):
        self.state_path = Path(state_path) if state_path else STATE_PATH
        self.state = self.load()
    
    def load(self) -> Dict:
        """加载状态"""
        if self.state_path.exists():
            try:
                with open(self.state_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return DEFAULT_STATE.copy()
    
    def save(self):
        """保存状态"""
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False, default=str)
    
    def update(self, updates: Dict):
        """更新状态"""
        self.state.update(updates)
        self.save()
    
    def get(self, key: str, default=None):
        """获取状态值"""
        return self.state.get(key, default)


class MemoryDatabase:
    """记忆数据库管理类"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.config_manager = ConfigManager()
        self.state_manager = StateManager()
        self.init_db()
    
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在以及是否有正确的列
        cursor.execute("PRAGMA table_info(memories)")
        columns = {col[1] for col in cursor.fetchall()}
        
        # 检查是否缺少必要的列（旧版本兼容）
        required_columns = {'name', 'source_file', 'type', 'content', 'created_at'}
        if columns and not required_columns.issubset(columns):
            # 删除旧表重新创建
            cursor.execute("DROP TABLE IF EXISTS memories")
            columns = set()
        
        if not columns:
            # 创建记忆表
            cursor.execute("""
                CREATE TABLE memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    type TEXT,
                    content TEXT,
                    source_file TEXT UNIQUE,
                    created_at TEXT,
                    classified_type TEXT,
                    confidence TEXT,
                    file_hash TEXT,
                    indexed_at TEXT DEFAULT (datetime('now'))
                )
            """)
            
            # 创建索引
            cursor.execute("CREATE INDEX idx_type ON memories(type)")
            cursor.execute("CREATE INDEX idx_created_at ON memories(created_at)")
            cursor.execute("CREATE INDEX idx_content ON memories(content)")
            cursor.execute("CREATE INDEX idx_source_file ON memories(source_file)")
            
            conn.commit()
        
        conn.close()
    
    def load_from_markdown(self, memory_dir: Optional[str] = None) -> int:
        """从 markdown 文件加载/同步记忆"""
        if memory_dir is None:
            memory_dir = MEMORY_DIR
        else:
            memory_dir = Path(memory_dir)
        
        if not memory_dir.exists():
            print(f"⚠️  记忆目录不存在：{memory_dir}")
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取已同步的文件列表
        cursor.execute("SELECT source_file, file_hash FROM memories")
        existing_files = {row[0]: row[1] for row in cursor.fetchall()}
        
        count = 0
        updated_count = 0
        synced_files = []
        pending_files = []
        
        for md_file in memory_dir.glob("*.md"):
            if md_file.name.startswith(".") or md_file.name == "MEMORY.md":
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8')
                file_hash = hashlib.md5(content.encode()).hexdigest()
                
                # 检查文件是否需要更新
                if md_file.name in existing_files:
                    if existing_files[md_file.name] == file_hash:
                        # 文件未变化，跳过
                        synced_files.append(md_file.name)
                        continue
                
                # 解析并插入/更新
                memory = self._parse_markdown(md_file, content)
                if memory:
                    cursor.execute("""
                        INSERT OR REPLACE INTO memories 
                        (name, description, type, content, source_file, created_at, classified_type, confidence, file_hash)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        memory['name'],
                        memory['description'],
                        memory['type'],
                        memory['content'],
                        memory['source_file'],
                        memory['created_at'],
                        memory['classified_type'],
                        memory['confidence'],
                        file_hash
                    ))
                    count += 1
                    updated_count += 1
                    synced_files.append(md_file.name)
                else:
                    pending_files.append(md_file.name)
                    
            except Exception as e:
                pending_files.append(md_file.name)
                if self.config_manager.get('log.enabled', True):
                    self._log(f"解析 {md_file.name} 失败：{e}")
        
        conn.commit()
        
        # 获取总记录数
        cursor.execute("SELECT COUNT(*) FROM memories")
        total_records = cursor.fetchone()[0]
        
        conn.close()
        
        # 更新状态
        self.state_manager.update({
            'last_sync': datetime.now().isoformat(),
            'last_sync_timestamp': datetime.now().timestamp(),
            'synced_files': synced_files,
            'total_records': total_records,
            'pending_files': pending_files,
            'sync_count': self.state_manager.get('sync_count', 0) + 1
        })
        
        return updated_count
    
    def _parse_markdown(self, file_path: Path, content: str) -> Optional[Dict]:
        """解析 markdown 文件"""
        name = file_path.stem
        description = ""
        mem_type = "memory"
        classified_type = ""
        confidence = ""
        created_at = datetime.now().isoformat()
        
        # 尝试从内容中提取信息
        lines = content.split('\n')
        in_frontmatter = False
        
        for i, line in enumerate(lines):
            if line.startswith('---') and i == 0:
                in_frontmatter = True
                continue
            elif line.startswith('---') and in_frontmatter:
                break
            elif in_frontmatter:
                if line.startswith('description:'):
                    description = line.replace('description:', '').strip().strip('"\'')
                elif line.startswith('type:') or line.startswith('classified_type:'):
                    classified_type = line.split(':')[1].strip()
                    mem_type = classified_type
                elif line.startswith('confidence:'):
                    confidence = line.split(':')[1].strip()
        
        # 提取创建时间（从文件名或内容）
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path.name)
        if date_match:
            created_at = f"{date_match.group(1)}T00:00:00"
        
        return {
            'name': name,
            'description': description or name,
            'type': mem_type,
            'content': content[:2000],  # 限制内容长度
            'source_file': file_path.name,
            'created_at': created_at,
            'classified_type': classified_type,
            'confidence': confidence
        }
    
    def query(self, sql: str, params: tuple = ()) -> List[Dict]:
        """执行查询"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql, params)
            results = [dict(row) for row in cursor.fetchall()]
            return results
        except Exception as e:
            raise Exception(f"查询失败：{e}")
        finally:
            conn.close()
    
    def clear(self):
        """清空数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memories")
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """获取数据库统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # 总记录数
        cursor.execute("SELECT COUNT(*) FROM memories")
        stats['total_records'] = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute("SELECT type, COUNT(*) FROM memories GROUP BY type")
        stats['by_type'] = dict(cursor.fetchall())
        
        # 最新记录时间
        cursor.execute("SELECT MAX(created_at) FROM memories")
        stats['latest_record'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def _log(self, message: str):
        """记录日志"""
        if not self.config_manager.get('log.enabled', True):
            return
        
        log_path = self.config_manager.get('log.path')
        if log_path:
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    timestamp = datetime.now().isoformat()
                    f.write(f"[{timestamp}] {message}\n")
            except:
                pass


class IntentRecognizer:
    """意图识别器"""
    
    def __init__(self):
        self.patterns = PATTERNS
    
    def recognize(self, question: str) -> Dict[str, Any]:
        """识别用户意图"""
        intent = {
            'type': 'search',  # search, count, time, type_filter
            'keywords': [],
            'time_range': None,
            'limit': self._get_default_limit(),
            'question': question
        }
        
        # 检测统计意图
        if any(kw in question for kw in self.patterns['统计']):
            intent['type'] = 'count'
        
        # 检测时间范围
        time_exprs = [
            ('今天', lambda: (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'))),
            ('昨天', lambda: ((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))),
            ('最近', lambda: None),
            ('上个月', lambda: None),
            ('这个月', lambda: None),
        ]
        
        for expr, func in time_exprs:
            if expr in question:
                intent['time_range'] = expr
                break
        
        # 提取类型过滤
        type_match = re.search(r'(feedback|user|project|reference|memory)', question)
        if type_match:
            intent['type_filter'] = type_match.group(1)
        
        # 提取数字限制
        num_match = re.search(r'(\d+) 条', question)
        if num_match:
            intent['limit'] = int(num_match.group(1))
        
        # 提取关键词 - 改进版本
        # 中文分词较复杂，这里使用简化的方法：按常见词分割
        stop_words = {'我', '的', '什么', '有', '哪些', '关于', '找', '搜索', '显示', '看', '条', '记录', '记忆', 
                     '查询', '一下', '帮我', '请', '找出来', '找出', '所有', '请帮我', '帮我查', '看一下',
                     '吗', '呢', '吧', '啊', '呀', '嘛', '这个', '那个', '一些', '一些'}
        
        # 使用更智能的分词：先移除疑问词和语气词，然后提取有意义的词
        text = question
        for sw in stop_words:
            text = text.replace(sw, ' ')
        
        # 提取剩余的词（至少 2 个字符或包含字母）
        candidates = re.findall(r'[\u4e00-\u9fa5]{2,}|[a-zA-Z][a-zA-Z0-9]*|[\u4e00-\u9fa5][a-zA-Z0-9]+', text)
        keywords = [c for c in candidates if c.strip()]
        
        intent['keywords'] = keywords
        return intent
    
    def _get_default_limit(self):
        """获取默认限制数"""
        try:
            config = ConfigManager()
            return config.get('query.default_limit', 10)
        except:
            return 10


class SQLGenerator:
    """SQL 生成器"""
    
    def __init__(self):
        self.templates = SQL_TEMPLATES
    
    def generate(self, intent: Dict) -> tuple:
        """根据意图生成 SQL 查询"""
        sql = ""
        params = ()
        
        intent_type = intent.get('type', 'search')
        time_range = intent.get('time_range')
        keywords = intent.get('keywords', [])
        type_filter = intent.get('type_filter')
        limit = intent.get('limit', 10)
        
        # 类型过滤
        if type_filter:
            if intent_type == 'count':
                sql = self.templates['type_count']
                params = (type_filter,)
            else:
                sql = self.templates['type_filter']
                params = (type_filter,)
        # 时间范围
        elif time_range:
            sql = self.templates['time_query']
            params = ('2020-01-01', '2030-12-31')
        # 关键词搜索
        elif keywords:
            if intent_type == 'count':
                sql = self.templates['count']
                params = (f"%{keywords[0]}%",)
            else:
                sql = self.templates['keyword_search']
                search_term = f"%{keywords[0]}%" if keywords else "%%"
                params = (search_term, search_term, search_term)
        # 最近查询
        else:
            sql = self.templates['recent']
            params = (limit,)
        
        return sql, params


class ResultInterpreter:
    """结果解释器"""
    
    def interpret(self, results: List[Dict], intent: Dict) -> str:
        """将查询结果解释为自然语言"""
        intent_type = intent.get('type', 'search')
        
        # 统计结果（特殊处理）
        if intent_type == 'count':
            if results and 'COUNT(*)' in results[0]:
                count = results[0]['COUNT(*)']
                return f"📊 统计结果：共找到 {count} 条相关记忆。"
            elif results:
                # 其他类型的计数
                count = list(results[0].values())[0]
                return f"📊 统计结果：共找到 {count} 条相关记忆。"
            else:
                return "📊 统计结果：共找到 0 条相关记忆。"
        
        # 空结果
        if not results:
            return "🧠 没有找到相关记忆。"
        
        # 列表结果
        output = f"🧠 找到 {len(results)} 条相关记忆：\n\n"
        
        for i, result in enumerate(results[:10], 1):
            name = result.get('name', '无题')
            description = result.get('description', '')
            created_at = result.get('created_at', '')
            mem_type = result.get('type', 'memory')
            source = result.get('source_file', '')
            
            date_str = created_at[:10] if created_at else '未知日期'
            output += f"{i}. [{date_str}] **{name}** ({mem_type})\n"
            if description and description != name:
                output += f"   {description}\n"
            if source:
                output += f"   📄 来源：{source}\n"
            output += "\n"
        
        if len(results) > 10:
            output += f"\n... 还有 {len(results) - 10} 条记录\n"
        
        return output


class MemoryQueryAgent:
    """记忆查询代理 - 主类（集成同步功能）"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.db = MemoryDatabase(db_path)
        self.intent_recognizer = IntentRecognizer()
        self.sql_generator = SQLGenerator()
        self.result_interpreter = ResultInterpreter()
        self.config_manager = ConfigManager()
        self.state_manager = StateManager()
    
    def needs_sync(self) -> bool:
        """检查是否需要同步"""
        if not self.config_manager.get('sync.auto_sync', True):
            return False
        
        last_sync = self.state_manager.get('last_sync_timestamp', 0)
        interval = self.config_manager.get('sync.interval_minutes', 15) * 60
        
        # 检查是否超过同步间隔
        if datetime.now().timestamp() - last_sync > interval:
            return True
        
        # 检查是否有新文件
        if not MEMORY_DIR.exists():
            return False
        
        current_files = set()
        for md_file in MEMORY_DIR.glob("*.md"):
            if md_file.name.startswith(".") or md_file.name == "MEMORY.md":
                continue
            current_files.add(md_file.name)
        
        synced_files = set(self.state_manager.get('synced_files', []))
        new_files = current_files - synced_files
        
        return len(new_files) > 0
    
    def sync_memories(self, memory_dir: Optional[str] = None) -> int:
        """同步记忆"""
        print("🔄 正在同步记忆数据...")
        count = self.db.load_from_markdown(memory_dir)
        print(f"✅ 同步完成，更新 {count} 条记录")
        return count
    
    def ask(self, question: str, auto_sync: bool = True) -> str:
        """
        主查询接口（带自动同步检查）
        输入：自然语言问题
        输出：自然语言答案
        """
        try:
            # 1. 自动同步检查
            if auto_sync and self.config_manager.get('sync.check_on_query', True):
                if self.needs_sync():
                    print("🔄 检测到记忆数据已更新，正在同步...")
                    self.sync_memories()
            
            # 2. 理解意图
            intent = self.intent_recognizer.recognize(question)
            
            # 3. 生成 SQL
            sql, params = self.sql_generator.generate(intent)
            
            # 4. 执行查询
            results = self.db.query(sql, params)
            
            # 5. 解释结果
            answer = self.result_interpreter.interpret(results, intent)
            
            return answer
            
        except Exception as e:
            return f"❌ 查询出错：{str(e)}"
    
    def reload_memories(self, memory_dir: Optional[str] = None) -> int:
        """重新加载记忆"""
        self.db.clear()
        return self.db.load_from_markdown(memory_dir)
    
    def get_sync_status(self) -> str:
        """获取同步状态"""
        last_sync = self.state_manager.get('last_sync', '从未')
        total_records = self.state_manager.get('total_records', 0)
        synced_files = self.state_manager.get('synced_files', [])
        pending_files = self.state_manager.get('pending_files', [])
        sync_count = self.state_manager.get('sync_count', 0)
        
        # 获取数据库统计
        try:
            stats = self.db.get_stats()
            db_records = stats['total_records']
            by_type = stats.get('by_type', {})
        except:
            db_records = total_records
            by_type = {}
        
        output = "📊 同步状态\n"
        output += "=" * 50 + "\n"
        output += f"最后同步：{last_sync}\n"
        output += f"同步次数：{sync_count}\n"
        output += f"数据库记录：{db_records} 条\n"
        output += f"已同步文件：{len(synced_files)} 个\n"
        
        if pending_files:
            output += f"⚠️  待同步/失败：{len(pending_files)} 个\n"
        
        if by_type:
            output += "\n按类型统计:\n"
            for mem_type, count in by_type.items():
                output += f"  - {mem_type}: {count} 条\n"
        
        return output
    
    def update_config(self, key: str, value):
        """更新配置"""
        self.config_manager.set(key, value)
        print(f"✅ 配置已更新：{key} = {value}")


# 命令行接口（增强版）
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='记忆查询助手（增强版）')
    parser.add_argument('question', nargs='?', help='自然语言问题')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    parser.add_argument('--reload', action='store_true', help='重新加载记忆')
    # 新增参数
    parser.add_argument('--memory-dir', help='记忆目录路径')
    parser.add_argument('--sync-status', action='store_true', help='查询同步状态')
    parser.add_argument('--sync-now', action='store_true', help='手动触发同步')
    parser.add_argument('--config', nargs=2, metavar=('KEY', 'VALUE'), help='设置配置（如：sync.interval_minutes 15）')
    parser.add_argument('--no-auto-sync', action='store_true', help='禁用自动同步')
    
    args = parser.parse_args()
    
    agent = MemoryQueryAgent()
    
    # 设置配置
    if args.config:
        key, value = args.config
        # 尝试转换为数字
        try:
            value = int(value)
        except:
            try:
                value = float(value)
            except:
                pass
        agent.update_config(key, value)
        return
    
    # 查询同步状态
    if args.sync_status:
        print(agent.get_sync_status())
        return
    
    # 手动同步
    if args.sync_now:
        agent.sync_memories(args.memory_dir)
        print("\n" + agent.get_sync_status())
        return
    
    # 重新加载
    if args.reload or args.memory_dir:
        print("🔄 正在加载记忆...")
        count = agent.reload_memories(args.memory_dir)
        print(f"✅ 已加载 {count} 条记忆\n")
    
    # 交互模式
    if args.interactive:
        print("🤔 记忆查询助手已启动（输入 'quit' 退出）")
        print("=" * 50)
        
        while True:
            try:
                question = input("\n您想问什么？> ").strip()
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break
                if question:
                    answer = agent.ask(question, auto_sync=not args.no_auto_sync)
                    print(f"\n{answer}")
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误：{e}")
    
    # 单次查询
    elif args.question:
        answer = agent.ask(args.question, auto_sync=not args.no_auto_sync)
        print(answer)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
