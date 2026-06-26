#!/usr/bin/env python3
"""
增强纠正记录器 - 集成 NeverOnce 修正优先级理念

核心特性：
1. 修正优先级（固定10/10）
2. 修正永不衰减
3. 有效性反馈系统
4. FTS5 全文搜索（SQLite）
5. 向后兼容现有 corrections.md 格式
"""

import os
import json
import sqlite3
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
import logging
from contextlib import contextmanager
import fcntl

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/enhanced-correction-logger.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CorrectionLogger:
    """增强纠正记录器 - 集成 NeverOnce 理念"""
    
    # NeverOnce 常量定义
    CORRECTION_PRIORITY = 10  # 修正固定优先级
    NEVER_DECAY = True        # 修正永不衰减
    DEFAULT_IMPORTANCE = 5    # 普通记忆默认重要性
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化增强纠正记录器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        
        # 文件路径（保持向后兼容）
        corrections_file = self.config.get(
            'corrections_file', 
            '~/self-improving/corrections.md'
        )
        self.corrections_file = Path(corrections_file).expanduser()
        
        # SQLite 数据库路径（新增）
        db_file = self.config.get(
            'enhanced_db_file',
            '~/self-improving/corrections_enhanced.db'
        )
        self.db_file = Path(db_file).expanduser()
        
        # 配置参数
        self.max_lines_per_file = self.config.get('max_lines_per_file', 1000)
        archive_dir = self.config.get('archive_directory', '~/self-improving/archive/')
        self.archive_directory = Path(archive_dir).expanduser()
        
        # 创建目录
        self.corrections_file.parent.mkdir(parents=True, exist_ok=True)
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self.archive_directory.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        # 缓存
        self._stats_cache = None
        self._stats_cache_time = 0
        self._cache_ttl = 60
        
        logger.info(f"纠正记录器初始化完成 (v2.0.0 with NeverOnce enhancements)")
        logger.info(f"  - 兼容文件: {self.corrections_file}")
        logger.info(f"  - 增强数据库: {self.db_file}")
    
    def _init_database(self):
        """初始化 SQLite 数据库（支持 FTS5）"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # 启用外键和 WAL 模式（更好并发）
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("PRAGMA journal_mode = WAL")
            
            # 创建修正表（增强元数据）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS corrections (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    agent_response TEXT NOT NULL,
                    corrected_response TEXT NOT NULL,
                    priority INTEGER DEFAULT 10,
                    never_decay BOOLEAN DEFAULT TRUE,
                    context_json TEXT,
                    tags_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    -- 有效性反馈字段
                    times_surfaced INTEGER DEFAULT 0,
                    times_helped INTEGER DEFAULT 0,
                    effectiveness_score REAL DEFAULT 0.0,
                    last_feedback_at TIMESTAMP,
                    -- 兼容性字段
                    markdown_line TEXT,
                    source_file TEXT
                )
            ''')
            
            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_corrections_priority 
                ON corrections(priority DESC)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_corrections_effectiveness 
                ON corrections(effectiveness_score DESC)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_corrections_timestamp 
                ON corrections(timestamp DESC)
            ''')
            
            # 创建 FTS5 虚拟表用于全文搜索
            try:
                cursor.execute('''
                    CREATE VIRTUAL TABLE IF NOT EXISTS corrections_fts 
                    USING fts5(
                        id UNINDEXED,
                        user_input,
                        agent_response,
                        corrected_response,
                        context_json,
                        tags_json,
                        content='corrections',
                        content_rowid='rowid'
                    )
                ''')
                logger.info("FTS5 全文搜索表创建成功")
            except sqlite3.OperationalError as e:
                logger.warning(f"FTS5 表创建失败（可能不支持）: {e}")
                # 创建普通全文索引作为后备
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS corrections_fts_fallback (
                        id TEXT PRIMARY KEY,
                        search_text TEXT,
                        FOREIGN KEY(id) REFERENCES corrections(id)
                    )
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_fts_fallback 
                    ON corrections_fts_fallback(search_text)
                ''')
            
            conn.commit()
            conn.close()
            logger.info(f"数据库初始化完成: {self.db_file}")
            
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    @contextmanager
    def _get_connection(self):
        """获取数据库连接上下文管理器"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row  # 返回字典样式的行
            yield conn
        finally:
            if conn:
                conn.close()
    
    def log_correction_with_priority(
        self,
        user_input: str,
        agent_response: str,
        corrected_response: str,
        context: Dict[str, Any] = None,
        priority: int = CORRECTION_PRIORITY,
        never_decay: bool = NEVER_DECAY,
        tags: List[str] = None
    ) -> str:
        """
        记录带优先级的修正（NeverOnce 核心理念）
        
        Args:
            user_input: 用户输入/纠正内容
            agent_response: 代理原始回应
            corrected_response: 纠正后的正确回应
            context: 上下文信息字典
            priority: 修正优先级（默认10/10）
            never_decay: 是否永不衰减（默认True）
            tags: 标签列表
            
        Returns:
            修正ID
        """
        # 生成修正ID
        timestamp = datetime.now().isoformat()
        unique_str = f"{timestamp}{user_input}{agent_response}{corrected_response}"
        correction_id = f"corr_enh_{hashlib.md5(unique_str.encode()).hexdigest()[:12]}"
        
        # 准备上下文和标签
        context_json = json.dumps(context, ensure_ascii=False) if context else "{}"
        tags_json = json.dumps(tags, ensure_ascii=False) if tags else "[]"
        
        # 准备 Markdown 格式（向后兼容）
        display_time = datetime.now().strftime("%Y‑%m‑%d %H:%M:%S")
        context_str = ""
        if context:
            try:
                context_str = f" [上下文: {json.dumps(context, ensure_ascii=False)[:100]}...]"
            except (TypeError, ValueError):
                context_str = f" [上下文: {str(context)[:100]}...]"
        
        markdown_line = (
            f"- **{display_time}** 用户纠正: {user_input} | "
            f"代理回应: {agent_response} | "
            f"纠正后: {corrected_response}{context_str}\n"
        )
        
        try:
            # 1. 写入数据库（增强存储）
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO corrections (
                        id, timestamp, user_input, agent_response, corrected_response,
                        priority, never_decay, context_json, tags_json, markdown_line,
                        source_file
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    correction_id, timestamp, user_input, agent_response, corrected_response,
                    priority, never_decay, context_json, tags_json, markdown_line,
                    str(self.corrections_file)
                ))
                
                # 2. 更新 FTS5 索引
                try:
                    cursor.execute('''
                        INSERT INTO corrections_fts (rowid, id, user_input, agent_response, 
                                                     corrected_response, context_json, tags_json)
                        VALUES (last_insert_rowid(), ?, ?, ?, ?, ?, ?)
                    ''', (
                        correction_id, user_input, agent_response, corrected_response,
                        context_json, tags_json
                    ))
                except sqlite3.OperationalError:
                    # FTS5 不可用，使用后备方案
                    search_text = f"{user_input} {agent_response} {corrected_response}"
                    cursor.execute('''
                        INSERT INTO corrections_fts_fallback (id, search_text)
                        VALUES (?, ?)
                    ''', (correction_id, search_text))
                
                conn.commit()
            
            # 3. 写入 Markdown 文件（向后兼容）
            self._append_to_markdown_file(markdown_line)
            
            logger.info(f"修正记录成功: {correction_id} (优先级: {priority}, 永不衰减: {never_decay})")
            return correction_id
            
        except Exception as e:
            logger.error(f"修正记录失败: {e}")
            raise
    
    def _append_to_markdown_file(self, line: str):
        """向后兼容：追加到 Markdown 文件"""
        try:
            # 检查文件行数，必要时归档
            if self.corrections_file.exists():
                with open(self.corrections_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                if len(lines) >= self.max_lines_per_file:
                    self._archive_markdown_file()
            
            # 追加新行（使用文件锁避免并发写入冲突）
            with open(self.corrections_file, 'a', encoding='utf-8') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write(line)
                fcntl.flock(f, fcntl.LOCK_UN)
                
        except Exception as e:
            logger.error(f"Markdown 文件写入失败: {e}")
    
    def _archive_markdown_file(self):
        """归档 Markdown 文件"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = self.archive_directory / f"corrections_archive_{timestamp}.md"
            
            if self.corrections_file.exists():
                self.corrections_file.rename(archive_file)
                logger.info(f"已归档修正文件: {archive_file}")
                
        except Exception as e:
            logger.error(f"文件归档失败: {e}")
    
    def record_helped_feedback(
        self,
        correction_id: str,
        was_helpful: bool,
        feedback_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        记录修正有效性反馈（NeverOnce .helped() 理念）
        
        Args:
            correction_id: 修正ID
            was_helpful: 是否真正有帮助
            feedback_context: 反馈上下文
            
        Returns:
            更新后的修正信息
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 获取当前状态
                cursor.execute('''
                    SELECT times_surfaced, times_helped, effectiveness_score, priority
                    FROM corrections 
                    WHERE id = ?
                ''', (correction_id,))
                
                row = cursor.fetchone()
                if not row:
                    raise ValueError(f"修正不存在: {correction_id}")
                
                times_surfaced = row['times_surfaced'] + 1
                times_helped = row['times_helped'] + (1 if was_helpful else 0)
                priority = row['priority']
                
                # 计算新的有效性分数
                # 公式: (帮助次数 / 展示次数) * 优先级因子
                effectiveness_score = 0.0
                if times_surfaced > 0:
                    base_score = times_helped / times_surfaced
                    # 优先级因子：高优先级修正更看重有效性
                    priority_factor = min(1.0, priority / 10.0)
                    effectiveness_score = base_score * priority_factor
                
                # 更新数据库
                cursor.execute('''
                    UPDATE corrections 
                    SET times_surfaced = ?,
                        times_helped = ?,
                        effectiveness_score = ?,
                        last_feedback_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (times_surfaced, times_helped, effectiveness_score, correction_id))
                
                conn.commit()
                
                result = {
                    'correction_id': correction_id,
                    'was_helpful': was_helpful,
                    'times_surfaced': times_surfaced,
                    'times_helped': times_helped,
                    'effectiveness_score': effectiveness_score,
                    'priority': priority,
                    'feedback_context': feedback_context
                }
                
                logger.info(f"反馈记录成功: {correction_id} "
                           f"(有帮助: {was_helpful}, 有效性: {effectiveness_score:.2f})")
                return result
                
        except Exception as e:
            logger.error(f"反馈记录失败: {e}")
            raise
    
    def check_corrections_for_action(
        self,
        planned_action: str,
        threshold: float = 0.7,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        检查计划行动的相关修正（NeverOnce .check() 理念）
        
        Args:
            planned_action: 计划执行的行动/查询
            threshold: 相关性阈值（0.0-1.0）
            max_results: 最大返回结果数
            
        Returns:
            相关修正列表（按优先级和相关性排序）
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 尝试使用 FTS5 搜索（如果可用）
                try:
                    # BM25 相关性搜索
                    cursor.execute('''
                        SELECT 
                            c.id, c.user_input, c.corrected_response, c.priority,
                            c.never_decay, c.effectiveness_score,
                            bm25(corrections_fts) as relevance_score
                        FROM corrections_fts
                        JOIN corrections c ON corrections_fts.id = c.id
                        WHERE corrections_fts MATCH ?
                        ORDER BY 
                            c.priority DESC,
                            relevance_score DESC,
                            c.effectiveness_score DESC
                        LIMIT ?
                    ''', (planned_action, max_results))
                    
                except (sqlite3.OperationalError, AttributeError):
                    # FTS5 不可用，使用简单文本匹配
                    search_terms = planned_action.lower().split()
                    query_terms = []
                    params = []
                    
                    for term in search_terms:
                        if len(term) > 2:  # 忽略太短的词
                            query_terms.append("(user_input LIKE ? OR corrected_response LIKE ?)")
                            params.extend([f'%{term}%', f'%{term}%'])
                    
                    if not query_terms:
                        return []
                    
                    where_clause = " OR ".join(query_terms)
                    cursor.execute(f'''
                        SELECT 
                            id, user_input, corrected_response, priority,
                            never_decay, effectiveness_score,
                            1.0 as relevance_score  -- 简单匹配，默认相关性1.0
                        FROM corrections
                        WHERE {where_clause}
                        ORDER BY 
                            priority DESC,
                            effectiveness_score DESC,
                            timestamp DESC
                        LIMIT ?
                    ''', params + [max_results])
                
                results = []
                for row in cursor.fetchall():
                    result = dict(row)
                    # 计算综合分数：优先级权重 + 相关性 + 有效性
                    priority_weight = result['priority'] / 10.0
                    relevance = result.get('relevance_score', 0.5)
                    effectiveness = result['effectiveness_score']
                    
                    combined_score = (
                        priority_weight * 0.4 +  # 优先级权重 40%
                        relevance * 0.4 +        # 相关性权重 40%
                        effectiveness * 0.2      # 有效性权重 20%
                    )
                    
                    result['combined_score'] = combined_score
                    result['should_warn'] = combined_score >= threshold
                    
                    results.append(result)
                
                # 按综合分数排序
                results.sort(key=lambda x: x['combined_score'], reverse=True)
                
                logger.info(f"行动检查完成: '{planned_action}' -> {len(results)} 条相关修正")
                return results
                
        except Exception as e:
            logger.error(f"行动检查失败: {e}")
            return []
    
    def get_corrections_by_priority(
        self,
        min_priority: int = 5,
        max_priority: int = 10,
        include_decayable: bool = True,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        按优先级获取修正
        
        Args:
            min_priority: 最低优先级
            max_priority: 最高优先级
            include_decayable: 是否包含可衰减的修正
            limit: 返回数量限制
            
        Returns:
            修正列表（按优先级降序排序）
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                where_clauses = ["priority BETWEEN ? AND ?"]
                params = [min_priority, max_priority]
                
                if not include_decayable:
                    where_clauses.append("never_decay = TRUE")
                
                where_sql = " AND ".join(where_clauses)
                
                cursor.execute(f'''
                    SELECT 
                        id, timestamp, user_input, corrected_response,
                        priority, never_decay, context_json, tags_json,
                        times_surfaced, times_helped, effectiveness_score
                    FROM corrections
                    WHERE {where_sql}
                    ORDER BY priority DESC, effectiveness_score DESC, timestamp DESC
                    LIMIT ?
                ''', params + [limit])
                
                results = []
                for row in cursor.fetchall():
                    result = dict(row)
                    # 解析 JSON 字段
                    if result.get('context_json'):
                        result['context'] = json.loads(result['context_json'])
                    if result.get('tags_json'):
                        result['tags'] = json.loads(result['tags_json'])
                    
                    results.append(result)
                
                return results
                
        except Exception as e:
            logger.error(f"按优先级获取修正失败: {e}")
            return []
    
    def get_correction_stats_enhanced(self) -> Dict[str, Any]:
        """
        获取增强的修正统计信息
        
        Returns:
            包含优先级分布、有效性统计、学习进度的详细报告
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # 基础统计
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_corrections,
                        COUNT(CASE WHEN never_decay = TRUE THEN 1 END) as never_decay_count,
                        COUNT(CASE WHEN effectiveness_score > 0.7 THEN 1 END) as highly_effective_count,
                        AVG(priority) as avg_priority,
                        AVG(effectiveness_score) as avg_effectiveness
                    FROM corrections
                ''')
                stats.update(dict(cursor.fetchone()))
                
                # 优先级分布
                cursor.execute('''
                    SELECT 
                        priority,
                        COUNT(*) as count,
                        AVG(effectiveness_score) as avg_effectiveness
                    FROM corrections
                    GROUP BY priority
                    ORDER BY priority DESC
                ''')
                stats['priority_distribution'] = [
                    dict(row) for row in cursor.fetchall()
                ]
                
                # 有效性分布
                cursor.execute('''
                    SELECT 
                        CASE 
                            WHEN effectiveness_score >= 0.8 THEN 'high'
                            WHEN effectiveness_score >= 0.5 THEN 'medium'
                            ELSE 'low'
                        END as effectiveness_level,
                        COUNT(*) as count,
                        AVG(priority) as avg_priority
                    FROM corrections
                    GROUP BY effectiveness_level
                    ORDER BY effectiveness_level DESC
                ''')
                stats['effectiveness_distribution'] = [
                    dict(row) for row in cursor.fetchall()
                ]
                
                # 时间趋势（最近30天）
                cursor.execute('''
                    SELECT 
                        DATE(timestamp) as date,
                        COUNT(*) as daily_count,
                        AVG(priority) as avg_priority,
                        AVG(effectiveness_score) as avg_effectiveness
                    FROM corrections
                    WHERE DATE(timestamp) >= DATE('now', '-30 days')
                    GROUP BY DATE(timestamp)
                    ORDER BY date DESC
                ''')
                stats['daily_trend'] = [
                    dict(row) for row in cursor.fetchall()
                ]
                
                # 缓存结果
                self._stats_cache = stats
                self._stats_cache_time = time.time()
                
                return stats
                
        except Exception as e:
            logger.error(f"获取增强统计失败: {e}")
            return {}
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        checks = {
            'database_accessible': False,
            'markdown_file_writable': False,
            'fts5_available': False,
            'total_corrections': 0,
            'avg_effectiveness': 0.0
        }
        
        try:
            # 检查数据库
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM corrections")
                checks['total_corrections'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT AVG(effectiveness_score) FROM corrections")
                checks['avg_effectiveness'] = cursor.fetchone()[0] or 0.0
                
                # 检查 FTS5
                try:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='corrections_fts'")
                    checks['fts5_available'] = cursor.fetchone() is not None
                except:
                    checks['fts5_available'] = False
                
                checks['database_accessible'] = True
            
            # 检查 Markdown 文件
            try:
                if not self.corrections_file.exists():
                    # 尝试创建文件
                    with open(self.corrections_file, 'w', encoding='utf-8') as f:
                        f.write("# 纠正记录\n\n")
                else:
                    # 尝试追加（测试可写性）
                    with open(self.corrections_file, 'a', encoding='utf-8'):
                        pass
                checks['markdown_file_writable'] = True
            except:
                checks['markdown_file_writable'] = False
            
            # 总体健康状态
            checks['healthy'] = (
                checks['database_accessible'] and 
                checks['markdown_file_writable']
            )
            checks['timestamp'] = datetime.now().isoformat()
            
            return checks
            
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return {
                'healthy': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


# 向后兼容的包装器


    # ===== 兼容性方法 (v1.0.0 API) =====
    
    def log_correction(
        self,
        user_input: str,
        agent_response: str,
        corrected_response: str,
        context: Dict[str, Any] = None
    ) -> str:
        """
        原始 log_correction 方法 - 兼容性包装器
        
        调用增强版本 log_correction_with_priority，使用默认参数：
        - priority: 10 (CORRECTION_PRIORITY)
        - never_decay: True (NEVER_DECAY)
        - tags: None
        """
        return self.log_correction_with_priority(
            user_input=user_input,
            agent_response=agent_response,
            corrected_response=corrected_response,
            context=context,
            priority=self.CORRECTION_PRIORITY,
            never_decay=self.NEVER_DECAY,
            tags=None
        )
    
    def get_recent_corrections(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        原始 get_recent_corrections 方法 - 兼容性包装器
        
        返回最近修正的简化版本
        """
        # 获取所有修正（按优先级排序）
        recent = self.get_corrections_by_priority(min_priority=1, max_priority=10, limit=limit)
        
        # 转换为原始格式
        simplified = []
        for corr in recent:
            simplified.append({
                'id': corr.get('id'),
                'user_input': corr.get('user_input'),
                'corrected_response': corr.get('corrected_response'),
                'timestamp': corr.get('timestamp'),
                'priority': corr.get('priority', 5),
                'context': corr.get('context', {})
            })
        
        return simplified
    
    def get_stats(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        原始 get_stats 方法 - 兼容性包装器
        
        返回基础统计信息
        """
        # 健康检查
        health = self.health_check()
        
        # 增强统计
        enhanced_stats = self.get_correction_stats_enhanced()
        
        return {
            'total_corrections': enhanced_stats.get('total_corrections', 0),
            'healthy': health.get('healthy', False),
            'file_path': str(self.corrections_file),
            'max_lines_per_file': self.max_lines_per_file,
            'archive_directory': str(self.archive_directory),
            'database_accessible': health.get('database_accessible', False),
            'fts5_available': health.get('fts5_available', False),
            'version': '2.0.0',
            'note': '使用 get_correction_stats_enhanced() 获取详细统计'
        }
def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="增强纠正记录器")
    parser.add_argument('--log', action='store_true', help='记录新修正')
    parser.add_argument('--user-input', help='用户输入')
    parser.add_argument('--agent-response', help='代理回应')
    parser.add_argument('--corrected-response', help='纠正后回应')
    parser.add_argument('--check', help='检查计划行动')
    parser.add_argument('--stats', action='store_true', help='显示统计')
    parser.add_argument('--health', action='store_true', help='健康检查')
    
    args = parser.parse_args()
    
    logger = EnhancedCorrectionLogger()
    
    if args.log:
        if not all([args.user_input, args.agent_response, args.corrected_response]):
            print("错误: 记录修正需要 --user-input, --agent-response, --corrected-response")
            return
        
        correction_id = logger.log_correction_with_priority(
            user_input=args.user_input,
            agent_response=args.agent_response,
            corrected_response=args.corrected_response,
            context={"source": "cli"}
        )
        print(f"修正记录成功: {correction_id}")
    
    elif args.check:
        results = logger.check_corrections_for_action(args.check)
        if results:
            print(f"找到 {len(results)} 条相关修正:")
            for i, result in enumerate(results, 1):
                print(f"{i}. [{result['priority']}/10] {result['user_input'][:80]}...")
                print(f"   纠正: {result['corrected_response'][:80]}...")
                print(f"   分数: {result['combined_score']:.2f} {'⚠️' if result['should_warn'] else ''}")
        else:
            print("未找到相关修正")
    
    elif args.stats:
        stats = logger.get_correction_stats_enhanced()
        print(f"总修正数: {stats.get('total_corrections', 0)}")
        print(f"平均优先级: {stats.get('avg_priority', 0):.1f}/10")
        print(f"平均有效性: {stats.get('avg_effectiveness', 0):.2f}")
        print(f"永不衰减修正: {stats.get('never_decay_count', 0)}")
    
    elif args.health:
        health = logger.health_check()
        status = "✅ 健康" if health.get('healthy') else "❌ 不健康"
        print(f"状态: {status}")
        for key, value in health.items():
            if key not in ['healthy', 'timestamp', 'error']:
                print(f"  {key}: {value}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()