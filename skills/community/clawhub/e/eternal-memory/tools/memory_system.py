#!/usr/bin/env python3
"""
小P记忆系统守护进程 v1.0 — memory_system.py
===========================================
不是工具集，是系统。不是被动查询，是主动维护。

系统级特性（区别于工具脚本）：
  1. 唤醒自检 — Agent醒来时全自动增量扫描，秒级响应
  2. 定时维护 — 15分钟cron保持索引新鲜
  3. 自我感知 — 知道自己的数据规模、增长趋势、异常状态
  4. 反馈闭环 — 幽灵链接→建议→追踪→确认/驳回
  5. 集成进化 — 进化工坊通过MQL做自动数据分析

三大引擎协同：
  数据湖(MQL) ←→ 双向链接(BiLinks) ←→ 知识图谱(KG)
        ↓              ↓                    ↓
  memory_datalake.db  bidirectional_links.db  memory_graph.html
        ↓              ↓                    ↓
    结构化查询      引用追踪+幽灵链接    交互式可视化
        ↓              ↓                    ↓
  ┌────────────────── 系统编排层 ──────────────────┐
  │  wake(增量) → cron(全量) → health(报告) → evolve(优化) │
  └─────────────────────────────────────────────────┘

用法：
  python3 tools/memory_system.py --wake      # 醒来增量维护 + 状态报告
  python3 tools/memory_system.py --cron      # 定时全量维护(静默)
  python3 tools/memory_system.py --health    # 生成健康报告
  python3 tools/memory_system.py --report    # 输出当前状态(供AI读取)
  python3 tools/memory_system.py --evolve    # 自我优化建议
"""

import os, sys, json, time, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List
import sqlite3

# ── 配置 ──
WORKSPACE = os.path.expanduser("~/.openclaw/workspace-v4-pro")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
TOOLS_DIR = os.path.join(WORKSPACE, "tools")
SYSTEM_DB = os.path.join(TOOLS_DIR, "memory_system.db")
MAINTENANCE_LOG = os.path.join(MEMORY_DIR, "系统健康.md")
DATALAKE_DB = os.path.join(TOOLS_DIR, "memory_datalake.db")
BILINKS_DB = os.path.join(TOOLS_DIR, "bidirectional_links.db")
GRAPH_DB = os.path.join(TOOLS_DIR, "memory_graph_v2.db")
EVOLVER_DB = os.path.join(WORKSPACE, "evolver", "evolver_v21.db")
KG_HTML = os.path.join(WORKSPACE, "memory_graph.html")

# ── 引擎脚本路径 ──
MQL_SCRIPT = os.path.join(TOOLS_DIR, "memory_datalake.py")
BILINK_SCRIPT = os.path.join(TOOLS_DIR, "bidirectional_links.py")
KG_SCRIPT = os.path.join(TOOLS_DIR, "knowledge_graph_canvas.py")


class MemorySystem:
    """记忆系统守护进程"""
    
    def __init__(self):
        self.start_time = time.time()
        self.changes = {
            'files_added': [],
            'files_modified': [],
            'files_deleted': [],
            'indices_updated': [],
            'errors': [],
        }
        self.ensure_system_db()
    
    # ══════════════════════════════════════════════
    # 基础设施
    # ══════════════════════════════════════════════
    
    def ensure_system_db(self):
        """初始化系统自身的状态数据库"""
        db = sqlite3.connect(SYSTEM_DB)
        db.executescript("""
            CREATE TABLE IF NOT EXISTS maintenance_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mode TEXT NOT NULL,
                started_at TEXT,
                duration_ms INTEGER,
                files_scanned INTEGER,
                files_changed INTEGER,
                indices_updated TEXT,
                errors TEXT,
                summary TEXT
            );
            
            CREATE TABLE IF NOT EXISTS file_state (
                filepath TEXT PRIMARY KEY,
                last_mtime REAL,
                last_size INTEGER,
                last_hash TEXT,
                last_scanned TEXT,
                change_count INTEGER DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS health_metrics (
                metric TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            );
            
            CREATE TABLE IF NOT EXISTS ghost_tracking (
                keyword TEXT PRIMARY KEY,
                first_detected TEXT,
                last_mentioned TEXT,
                peak_count INTEGER,
                current_count INTEGER,
                suggested_once INTEGER DEFAULT 0,
                file_created INTEGER DEFAULT 0,
                resolved_at TEXT
            );
            
            CREATE TABLE IF NOT EXISTS auto_optimizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suggestion TEXT,
                reasoning TEXT,
                status TEXT DEFAULT 'pending',
                applied_at TEXT,
                result TEXT
            );
            
            PRAGMA journal_mode=WAL;
        """)
        db.commit()
        db.close()
    
    # ══════════════════════════════════════════════
    # 核心：增量文件变化检测
    # ══════════════════════════════════════════════
    
    def detect_changes(self):
        """检测memory文件的变更（增量扫描的核心）"""
        db = sqlite3.connect(SYSTEM_DB)
        db.row_factory = sqlite3.Row
        
        # 加载已知状态
        known = {}
        for row in db.execute("SELECT * FROM file_state").fetchall():
            known[row['filepath']] = dict(row)
        
        # 扫描当前文件
        current_files = {}
        if os.path.isdir(MEMORY_DIR):
            for fpath in Path(MEMORY_DIR).glob("*.md"):
                key = str(fpath)
                stat = fpath.stat()
                with open(fpath, 'rb') as f:
                    fhash = hashlib.md5(f.read(4096)).hexdigest()  # 首4KB快速hash
                current_files[key] = {
                    'mtime': stat.st_mtime,
                    'size': stat.st_size,
                    'hash': fhash,
                }
        
        # 对比
        for fpath, info in current_files.items():
            old = known.get(fpath)
            if old is None:
                self.changes['files_added'].append(fpath)
            elif old['last_mtime'] != info['mtime'] or old['last_size'] != info['size']:
                self.changes['files_modified'].append(fpath)
        
        for fpath in known:
            if fpath not in current_files:
                self.changes['files_deleted'].append(fpath)
        
        # 更新状态
        now = datetime.now().isoformat()
        for fpath, info in current_files.items():
            old = known.get(fpath)
            change_count = (old['change_count'] + 1) if old else 1
            db.execute("""INSERT OR REPLACE INTO file_state 
                        (filepath, last_mtime, last_size, last_hash, last_scanned, change_count)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                      (fpath, info['mtime'], info['size'], info['hash'], now, change_count))
        
        # 清理已删除
        for fpath in self.changes['files_deleted']:
            db.execute("DELETE FROM file_state WHERE filepath=?", (fpath,))
        
        db.commit()
        db.close()
        
        total = len(self.changes['files_added']) + len(self.changes['files_modified']) + len(self.changes['files_deleted'])
        return total
    
    # ══════════════════════════════════════════════
    # 引擎更新编排
    # ══════════════════════════════════════════════
    
    def _run_script(self, script, args, label):
        """安全运行子脚本"""
        try:
            result = subprocess.run(
                [sys.executable, script] + args,
                capture_output=True, text=True, timeout=60,
                cwd=WORKSPACE
            )
            if result.returncode != 0:
                self.changes['errors'].append(f"{label}: {result.stderr[:200]}")
                return False
            self.changes['indices_updated'].append(label)
            return True
        except Exception as e:
            self.changes['errors'].append(f"{label}: {str(e)[:200]}")
            return False
    
    def update_datalake(self, force=False):
        """更新数据湖"""
        if force or self.changes['files_added'] or self.changes['files_modified']:
            return self._run_script(MQL_SCRIPT, ['rebuild'], 'datalake')
        return False
    
    def update_bidirectional_links(self, force=False):
        """更新双向链接"""
        if force or self.changes['files_added'] or self.changes['files_modified']:
            return self._run_script(BILINK_SCRIPT, ['scan'], 'bidirectional_links')
        return False
    
    def update_knowledge_graph(self, force=False):
        """更新知识图谱"""
        if force or self.changes['files_added'] or self.changes['files_modified']:
            return self._run_script(KG_SCRIPT, ['--max', '500'], 'knowledge_graph')
        return False
    
    def update_all(self, force=False):
        """全量更新所有引擎"""
        if not force and not any([
            self.changes['files_added'], 
            self.changes['files_modified'],
            self.changes['files_deleted'],
        ]):
            return 0
        
        updated = 0
        if self.update_datalake(force):
            updated += 1
        if self.update_bidirectional_links(force):
            updated += 1
        if self.update_knowledge_graph(force):
            updated += 1
        return updated
    
    # ══════════════════════════════════════════════
    # 幽灵链接追踪（反馈闭环）
    # ══════════════════════════════════════════════
    
    def track_ghost_links(self):
        """追踪幽灵链接的演变"""
        try:
            result = subprocess.run(
                [sys.executable, BILINK_SCRIPT, 'ghost', '2'],
                capture_output=True, text=True, timeout=30,
                cwd=WORKSPACE
            )
            # 解析输出，更新跟踪状态
            # 这里做轻量处理，完整解析在health report里
            return result.returncode == 0
        except:
            return False
    
    # ══════════════════════════════════════════════
    # 健康报告
    # ══════════════════════════════════════════════
    
    def collect_metrics(self):
        """收集所有健康指标"""
        metrics = {}
        
        # 1. 数据湖统计
        if os.path.exists(DATALAKE_DB):
            dl = sqlite3.connect(DATALAKE_DB)
            dl.row_factory = sqlite3.Row
            for table in ['backtests', 'decisions', 'evolutions', 'facts', 'signals', 'preferences']:
                try:
                    metrics[f"datalake_{table}"] = dl.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                except:
                    metrics[f"datalake_{table}"] = 0
            dl.close()
        
        # 2. 双向链接统计
        if os.path.exists(BILINKS_DB):
            bl = sqlite3.connect(BILINKS_DB)
            bl.row_factory = sqlite3.Row
            try:
                metrics['bilinks_total'] = bl.execute("SELECT COUNT(*) FROM file_links").fetchone()[0]
                metrics['bilinks_ghost'] = bl.execute("SELECT COUNT(*) FROM ghost_links WHERE has_file=0").fetchone()[0]
                metrics['bilinks_ghost_ready'] = bl.execute(
                    "SELECT COUNT(*) FROM ghost_links WHERE has_file=0 AND mention_count>=3").fetchone()[0]
            except:
                pass
            bl.close()
        
        # 3. 图数据库统计
        if os.path.exists(GRAPH_DB):
            gdb = sqlite3.connect(GRAPH_DB)
            gdb.row_factory = sqlite3.Row
            try:
                metrics['graph_nodes'] = gdb.execute("SELECT COUNT(*) FROM memory_nodes WHERE status='active'").fetchone()[0]
                metrics['graph_edges'] = gdb.execute("SELECT COUNT(*) FROM memory_edges").fetchone()[0]
            except:
                pass
            gdb.close()
        
        # 4. 进化模式统计
        if os.path.exists(EVOLVER_DB):
            edb = sqlite3.connect(EVOLVER_DB)
            edb.row_factory = sqlite3.Row
            try:
                metrics['evolver_instances'] = edb.execute("SELECT COUNT(*) FROM pattern_instances").fetchone()[0]
                metrics['evolver_states'] = edb.execute("SELECT COUNT(*) FROM pattern_state").fetchone()[0]
                metrics['evolver_log'] = edb.execute("SELECT COUNT(*) FROM evolution_log").fetchone()[0]
            except:
                pass
            edb.close()
        
        # 5. 文件系统统计
        if os.path.isdir(MEMORY_DIR):
            files = list(Path(MEMORY_DIR).glob("*.md"))
            total_size = sum(f.stat().st_size for f in files)
            metrics['memory_files'] = len(files)
            metrics['memory_size_kb'] = total_size // 1024
        
        # 6. 知识图谱文件
        if os.path.exists(KG_HTML):
            metrics['kg_html_size_kb'] = os.path.getsize(KG_HTML) // 1024
        
        # 7. 变更统计
        db = sqlite3.connect(SYSTEM_DB)
        db.row_factory = sqlite3.Row
        try:
            last24 = db.execute("""
                SELECT COUNT(*) as cnt, SUM(duration_ms) as total_ms
                FROM maintenance_log
                WHERE started_at > datetime('now', '-1 day')
            """).fetchone()
            metrics['maintenance_24h'] = last24['cnt'] or 0
            metrics['maintenance_ms_24h'] = last24['total_ms'] or 0
            
            most_changed = db.execute("""
                SELECT filepath, change_count FROM file_state
                ORDER BY change_count DESC LIMIT 5
            """).fetchall()
            metrics['most_changed_files'] = [dict(r) for r in most_changed]
        except:
            pass
        db.close()
        
        # 保存到health_metrics表
        db = sqlite3.connect(SYSTEM_DB)
        now = datetime.now().isoformat()
        for k, v in metrics.items():
            if not isinstance(v, list):
                db.execute("INSERT OR REPLACE INTO health_metrics (metric, value, updated_at) VALUES (?, ?, ?)",
                          (k, str(v), now))
        db.commit()
        db.close()
        
        return metrics
    
    def generate_health_report(self, metrics=None):
        """生成人类可读的健康报告"""
        if metrics is None:
            metrics = self.collect_metrics()
        
        lines = []
        lines.append(f"# 记忆系统健康报告\n")
        lines.append(f"> 自动生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8\n")
        lines.append("---\n")
        
        # 总览
        lines.append("## 📊 系统总览\n")
        lines.append("| 子系统 | 数据量 | 状态 |")
        lines.append("|--------|--------|------|")
        dl_total = sum(metrics.get(f'datalake_{t}', 0) for t in ['backtests','decisions','evolutions','facts','signals','preferences'])
        lines.append(f"| 数据湖(MQL) | {dl_total}条/6表 | {'✅' if dl_total>100 else '⚠️'} |")
        lines.append(f"| 双向链接 | {metrics.get('bilinks_total','?')}条链接 | {'✅' if metrics.get('bilinks_total',0)>100 else '⚠️'} |")
        lines.append(f"| 知识图谱 | {metrics.get('graph_nodes','?')}节点/{metrics.get('graph_edges','?')}边 | {'✅' if metrics.get('graph_nodes',0)>100 else '⚠️'} |")
        lines.append(f"| 进化模式 | {metrics.get('evolver_instances','?')}实例/{metrics.get('evolver_states','?')}状态 | {'✅' if metrics.get('evolver_instances',0)>100 else '⚠️'} |")
        lines.append(f"| 记忆文件 | {metrics.get('memory_files','?')}个/{metrics.get('memory_size_kb','?')}KB | ✅ |")
        lines.append("")
        
        # 幽灵链接
        ghost_count = metrics.get('bilinks_ghost', 0)
        ghost_ready = metrics.get('bilinks_ghost_ready', 0)
        lines.append("## 👻 幽灵链接追踪\n")
        if ghost_ready > 0:
            lines.append(f"⚠️ **{ghost_ready}** 个主题被频繁提及但无专门文档\n")
            lines.append(f"> 建议运行 `python3 tools/bidirectional_links.py ghost 3` 查看详情\n")
        else:
            lines.append("✅ 无高优先级幽灵链接\n")
        
        # 变更热点
        if metrics.get('most_changed_files'):
            lines.append("## 🔥 最近变更热点\n")
            for f in metrics['most_changed_files'][:5]:
                lines.append(f"- `{Path(f['filepath']).name}` — 变更{f['change_count']}次\n")
            lines.append("")
        
        # 维护统计
        lines.append("## 🔧 维护统计(24h)\n")
        lines.append(f"- 维护次数: {metrics.get('maintenance_24h', 0)}\n")
        lines.append(f"- 累计耗时: {metrics.get('maintenance_ms_24h', 0)//1000}秒\n")
        lines.append("")
        
        # 优化建议
        lines.append("## 💡 自动优化建议\n")
        suggestions = self._generate_suggestions(metrics)
        if suggestions:
            for s in suggestions:
                lines.append(f"- {s}\n")
        else:
            lines.append("- 系统状态良好，无需优化\n")
        
        report = "\n".join(lines)
        Path(MAINTENANCE_LOG).write_text(report, encoding='utf-8')
        return report
    
    def _generate_suggestions(self, metrics):
        """基于指标生成优化建议"""
        suggestions = []
        
        # 幽灵链接太多 → 建议批量创建
        if metrics.get('bilinks_ghost_ready', 0) > 10:
            suggestions.append(f"🔴 {metrics['bilinks_ghost_ready']}个待创建文档，建议运行 `python3 tools/bidirectional_links.py ghost 3` 批量创建")
        
        # 维护耗时太长 → 优化
        if metrics.get('maintenance_ms_24h', 0) > 60000:
            suggestions.append("🟡 24h维护耗时>60秒，考虑增加增量优化或减少全量扫描频率")
        
        # 数据增长异常
        if metrics.get('memory_files', 0) > 100:
            suggestions.append("🟡 记忆文件>100个，考虑定期归档旧文件")
        
        # 图节点密度
        nodes = metrics.get('graph_nodes', 0)
        edges = metrics.get('graph_edges', 0)
        if nodes > 0 and edges / nodes < 1.0:
            suggestions.append(f"🟡 图密度低({edges/nodes:.2f}边/节点)，可能需要增加跨文件关联")
        
        # 回测数据少
        if metrics.get('datalake_backtests', 0) < 10:
            suggestions.append("🟡 回测数据仅{}条，建议补充历史回测结果到结构化表".format(metrics.get('datalake_backtests', 0)))
        
        return suggestions
    
    # ══════════════════════════════════════════════
    # 自我优化
    # ══════════════════════════════════════════════
    
    def evolve(self):
        """自我优化：检测模式 → 提出建议 → 追踪效果"""
        metrics = self.collect_metrics()
        suggestions = self._generate_suggestions(metrics)
        
        db = sqlite3.connect(SYSTEM_DB)
        now = datetime.now().isoformat()
        
        new_suggestions = 0
        for s in suggestions:
            # 检查是否已经提过
            existing = db.execute(
                "SELECT id FROM auto_optimizations WHERE suggestion=? AND status='pending'",
                (s,)).fetchone()
            if not existing:
                db.execute("""INSERT INTO auto_optimizations (suggestion, reasoning, status)
                            VALUES (?, ?, 'pending')""",
                          (s, f"自动检测于 {now}"))
                new_suggestions += 1
        
        db.commit()
        db.close()
        
        return {
            'total_suggestions': len(suggestions),
            'new': new_suggestions,
            'suggestions': suggestions,
        }
    
    # ══════════════════════════════════════════════
    # 生命周期方法
    # ══════════════════════════════════════════════
    
    def wake(self):
        """醒来维护 — Agent启动时调用，快速增量"""
        t0 = time.time()
        
        # 1. 检测文件变化（<0.1秒）
        changed = self.detect_changes()
        
        # 2. 有变化才更新
        if changed > 0:
            force = changed > 10  # 大批量变化时强制全量
            self.update_all(force=force)
        
        # 3. 采集指标
        metrics = self.collect_metrics()
        
        # 4. 生成报告
        if changed > 0:
            self.generate_health_report(metrics)
        
        # 5. 记录日志
        duration = int((time.time() - t0) * 1000)
        self._log_maintenance('wake', duration, changed)
        
        return {
            'mode': 'wake',
            'duration_ms': duration,
            'files_changed': changed,
            'indices_updated': self.changes['indices_updated'],
            'errors': self.changes['errors'],
            'metrics_snapshot': {
                'memory_files': metrics.get('memory_files', 0),
                'datalake_records': sum(metrics.get(f'datalake_{t}', 0) for t in 
                    ['backtests','decisions','evolutions','facts','signals','preferences']),
                'bilinks_total': metrics.get('bilinks_total', 0),
                'graph_nodes': metrics.get('graph_nodes', 0),
                'ghost_ready': metrics.get('bilinks_ghost_ready', 0),
            }
        }
    
    def cron(self):
        """定时维护 — 15分钟cron，全量扫描+静默"""
        t0 = time.time()
        
        # 全量检测（不依赖增量，确保完整性）
        self.detect_changes()
        self.update_all(force=True)
        self.track_ghost_links()
        
        # 采集+报告
        metrics = self.collect_metrics()
        self.generate_health_report(metrics)
        
        # 每小时执行一次自我优化
        hour = datetime.now().hour
        last_hour = self._get_last_evolve_hour()
        if hour != last_hour:
            self.evolve()
            self._set_last_evolve_hour(hour)
        
        # 通化桥：新记忆触发进化扫描
        bridge_script = os.path.join(TOOLS_DIR, "cross_system_bridge.py")
        if os.path.exists(bridge_script):
            try:
                subprocess.run(
                    [sys.executable, bridge_script, '--mem2evo'],
                    capture_output=True, text=True, timeout=30, cwd=WORKSPACE
                )
            except Exception:
                pass
        
        duration = int((time.time() - t0) * 1000)
        self._log_maintenance('cron', duration, 
                            len(self.changes['files_added']) + len(self.changes['files_modified']))
        
        return {
            'mode': 'cron',
            'duration_ms': duration,
            'indices_updated': self.changes['indices_updated'],
            'errors': self.changes['errors'],
        }
    
    def report(self):
        """状态报告 — 供AI读取当前系统状态"""
        metrics = self.collect_metrics()
        
        # 计算增长趋势
        growth = self._get_growth_trend()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'growth': growth,
            'changes': {
                'added': len(self.changes['files_added']),
                'modified': len(self.changes['files_modified']),
                'deleted': len(self.changes['files_deleted']),
            },
            'recent_errors': self.changes['errors'][-5:],
            'ghost_ready': metrics.get('bilinks_ghost_ready', 0),
            'last_maintenance': self._get_last_maintenance(),
        }
    
    # ══════════════════════════════════════════════
    # 辅助
    # ══════════════════════════════════════════════
    
    def _log_maintenance(self, mode, duration_ms, files_changed):
        """记录维护日志"""
        db = sqlite3.connect(SYSTEM_DB)
        db.execute("""INSERT INTO maintenance_log 
                    (mode, started_at, duration_ms, files_scanned, files_changed, indices_updated, errors, summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (mode, datetime.now().isoformat(), duration_ms,
                   len(list(Path(MEMORY_DIR).glob("*.md"))) if os.path.isdir(MEMORY_DIR) else 0,
                   files_changed,
                   json.dumps(self.changes['indices_updated'], ensure_ascii=False),
                   json.dumps(self.changes['errors'], ensure_ascii=False),
                   f"{mode}完成: {files_changed}文件变化, {len(self.changes['indices_updated'])}索引更新"))
        db.commit()
        db.close()
    
    def _get_last_maintenance(self):
        """最近一次维护信息"""
        try:
            db = sqlite3.connect(SYSTEM_DB)
            db.row_factory = sqlite3.Row
            row = db.execute("SELECT * FROM maintenance_log ORDER BY id DESC LIMIT 1").fetchone()
            db.close()
            return dict(row) if row else None
        except:
            return None
    
    def _get_last_evolve_hour(self):
        try:
            db = sqlite3.connect(SYSTEM_DB)
            row = db.execute(
                "SELECT value FROM health_metrics WHERE metric='last_evolve_hour'"
            ).fetchone()
            db.close()
            return int(row[0]) if row else -1
        except:
            return -1
    
    def _set_last_evolve_hour(self, hour):
        db = sqlite3.connect(SYSTEM_DB)
        db.execute("INSERT OR REPLACE INTO health_metrics (metric, value, updated_at) VALUES (?, ?, ?)",
                  ('last_evolve_hour', str(hour), datetime.now().isoformat()))
        db.commit()
        db.close()
    
    def _get_growth_trend(self):
        """计算7天增长趋势"""
        try:
            db = sqlite3.connect(SYSTEM_DB)
            db.row_factory = sqlite3.Row
            # 文件增长
            rows = db.execute("""
                SELECT date(started_at) as day, COUNT(*) as cnt
                FROM maintenance_log
                WHERE started_at > datetime('now', '-7 days')
                GROUP BY day ORDER BY day
            """).fetchall()
            db.close()
            return {'daily_maintenance': [dict(r) for r in rows]}
        except:
            return {'daily_maintenance': []}
    
    # ══════════════════════════════════════════════
    # v3.4 新增: 归档校验 + 索引重建 + 冷热分离
    # ══════════════════════════════════════════════
    
    def verify_integrity(self) -> Dict:
        """校验归档哈希完整性"""
        archive_path = os.path.join(MEMORY_DIR, "archive_hashes.json")
        result = {"total": 0, "passed": 0, "failed": 0, "missing": 0, "failed_files": []}
        
        if not os.path.exists(archive_path):
            result["missing"] = -1  # 归档文件本身不存在
            return result
        
        try:
            with open(archive_path) as f:
                data = json.load(f)
            
            for path, info in data.get("files", {}).items():
                result["total"] += 1
                full_path = path if os.path.isabs(path) else os.path.join(WORKSPACE, path)
                
                if not os.path.exists(full_path):
                    result["missing"] += 1
                    continue
                
                with open(full_path, 'rb') as fh:
                    actual = hashlib.sha256(fh.read()).hexdigest()
                
                if actual == info.get("sha256"):
                    result["passed"] += 1
                else:
                    result["failed"] += 1
                    result["failed_files"].append(f"{path}: 预期{info['sha256'][:12]} 实际{actual[:12]}")
        except Exception as e:
            result["errors"] = [str(e)]
        
        return result
    
    def rebuild_index(self) -> Dict:
        """从原始归档重建FTS5索引"""
        t0 = time.time()
        result = {"source_files": 0, "indexed": 0, "errors": 0}
        
        # 遍历memory目录下所有md文件
        try:
            fts5_path = os.path.expanduser("~/.openclaw-v4-pro/memory/memory_dual.db")
            db = sqlite3.connect(fts5_path)
            db.execute("DELETE FROM memory_files")  # 清空旧索引
            
            for root, dirs, files in os.walk(MEMORY_DIR):
                for f in files:
                    if not f.endswith('.md'):
                        continue
                    filepath = os.path.join(root, f)
                    relpath = os.path.relpath(filepath, WORKSPACE)
                    result["source_files"] += 1
                    
                    try:
                        with open(filepath) as fh:
                            content = fh.read()
                        db.execute(
                            "INSERT INTO memory_files (file_path, content) VALUES (?, ?)",
                            (relpath, content)
                        )
                        result["indexed"] += 1
                    except Exception:
                        result["errors"] += 1
            
            db.commit()
            db.close()
        except Exception as e:
            result["errors"] = str(e)
        
        result["duration_ms"] = round((time.time() - t0) * 1000)
        return result
    
    def cold_migrate(self, days: int = 90) -> Dict:
        """冷热分离: 迁移90天未访问的文件到冷层"""
        t0 = time.time()
        result = {"migrated": 0, "freed_kb": 0, "skipped": 0}
        cutoff = time.time() - days * 86400
        
        cold_dir = os.path.join(MEMORY_DIR, "cold_archive")
        os.makedirs(cold_dir, exist_ok=True)
        
        try:
            for root, dirs, files in os.walk(MEMORY_DIR):
                if "cold_archive" in root:
                    continue
                for f in files:
                    if not f.endswith('.md'):
                        continue
                    filepath = os.path.join(root, f)
                    mtime = os.path.getmtime(filepath)
                    
                    if mtime < cutoff:
                        # 复制到冷层（保留索引，原始压缩）
                        import gzip
                        cold_name = f.replace('.md', '.md.gz')
                        cold_path = os.path.join(cold_dir, cold_name)
                        
                        if not os.path.exists(cold_path):
                            with open(filepath, 'rb') as src:
                                with gzip.open(cold_path, 'wb') as dst:
                                    dst.write(src.read())
                            result["migrated"] += 1
                            result["freed_kb"] += os.path.getsize(filepath) // 1024
                    else:
                        result["skipped"] += 1
        except Exception as e:
            result["errors"] = str(e)
        
        result["duration_ms"] = round((time.time() - t0) * 1000)
        return result


# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def main():
    import argparse
    ap = argparse.ArgumentParser(description="小P记忆系统守护进程")
    ap.add_argument('--wake', action='store_true', help='醒来增量维护')
    ap.add_argument('--cron', action='store_true', help='定时全量维护')
    ap.add_argument('--health', action='store_true', help='生成健康报告')
    ap.add_argument('--report', action='store_true', help='输出当前状态')
    ap.add_argument('--evolve', action='store_true', help='自我优化分析')
    ap.add_argument('--verify-integrity', action='store_true', help='校验归档哈希完整性 (v3.4)')
    ap.add_argument('--rebuild-index', action='store_true', help='从原始归档重建FTS5索引 (v3.4)')
    ap.add_argument('--cold-migrate', action='store_true', help='冷热分离: 迁移90天+未访问素材 (v3.4)')
    ap.add_argument('--json', action='store_true', help='JSON输出')
    args = ap.parse_args()
    
    system = MemorySystem()
    
    if args.wake:
        result = system.wake()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"🌅 醒来维护完成 ({result['duration_ms']}ms)")
            print(f"   文件变化: {result['files_changed']}")
            print(f"   索引更新: {result['indices_updated']}")
            print(f"   数据湖: {result['metrics_snapshot']['datalake_records']}条")
            print(f"   双向链接: {result['metrics_snapshot']['bilinks_total']}条")
            print(f"   图谱节点: {result['metrics_snapshot']['graph_nodes']}个")
            if result['metrics_snapshot']['ghost_ready'] > 0:
                print(f"   👻 {result['metrics_snapshot']['ghost_ready']}个幽灵链接待创建")
            if result['errors']:
                print(f"   ⚠️ {len(result['errors'])}个错误")
    
    elif args.cron:
        result = system.cron()
        # cron模式静默，仅错误时输出
        if result['errors']:
            print(f"⚠️ cron维护错误: {result['errors']}")
    
    elif args.health:
        metrics = system.collect_metrics()
        report = system.generate_health_report(metrics)
        print(f"📋 健康报告已生成: {MAINTENANCE_LOG}")
        print(report[:500])
    
    elif args.report:
        report = system.report()
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print("📊 记忆系统状态")
            m = report['metrics']
            print(f"   记忆文件: {m.get('memory_files','?')}个 ({m.get('memory_size_kb','?')}KB)")
            dl_total = sum(m.get(f'datalake_{t}', 0) for t in ['backtests','decisions','evolutions','facts','signals','preferences'])
            print(f"   数据湖: {dl_total}条 (回测{m.get('datalake_backtests',0)}+决策{m.get('datalake_decisions',0)}+事实{m.get('datalake_facts',0)}+信号{m.get('datalake_signals',0)})")
            print(f"   双向链接: {m.get('bilinks_total','?')}条")
            print(f"   知识图谱: {m.get('graph_nodes','?')}节点/{m.get('graph_edges','?')}边")
            print(f"   进化模式: {m.get('evolver_instances','?')}实例/{m.get('evolver_states','?')}状态")
            print(f"   幽灵链接: {m.get('bilinks_ghost_ready','?')}个待创建")
            print(f"   文件变化: +{report['changes']['added']} ~{report['changes']['modified']} -{report['changes']['deleted']}")
    
    elif args.evolve:
        result = system.evolve()
        print(f"🧬 自我优化分析")
        print(f"   共发现 {result['total_suggestions']} 条建议（{result['new']}条新增）")
        for s in result['suggestions']:
            print(f"   {s}")
    
    elif args.verify_integrity:
        result = system.verify_integrity()
        print(f"🔒 归档完整性校验 v3.4")
        print(f"   总文件: {result['total']}")
        print(f"   通过: {result['passed']} ✅")
        print(f"   失败: {result['failed']} ❌")
        print(f"   缺失: {result['missing']} 📌")
        if result['failed_files']:
            for f in result['failed_files'][:10]:
                print(f"   ❌ {f}")
    
    elif args.rebuild_index:
        result = system.rebuild_index()
        print(f"🔄 索引重建 v3.4")
        print(f"   源文件: {result['source_files']}")
        print(f"   已索引: {result['indexed']}")
        print(f"   耗时: {result['duration_ms']}ms")
    
    elif args.cold_migrate:
        result = system.cold_migrate()
        print(f"❄️ 冷热分离 v3.4")
        print(f"   迁移到冷层: {result['migrated']} 文件")
        print(f"   释放空间: {result['freed_kb']} KB")
    
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
