"""
AutoDream Engine - 主引擎

平台无关的记忆整理核心逻辑。
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

from .stages.orientation import OrientationStage
from .stages.gather import GatherStage
from .stages.consolidate import ConsolidateStage
from .stages.prune import PruneStage
from .utils.state import DreamState, StateManager
from .analytics import AnalyticsLogger


class AutoDreamEngine:
    """
    AutoDream 通用引擎
    
    四阶段记忆整理流程：
    1. Orientation - 建立记忆状态地图
    2. Gather Signal - 提取高价值信号
    3. Consolidation - 合并、去重、删除过时
    4. Prune and Index - 更新索引
    
    参数:
        adapter: 平台适配器（如 OpenClawAdapter）
        config: 配置字典
    """
    
    def __init__(self, adapter: Any, config: Optional[Dict] = None):
        self.adapter = adapter
        self.config = config or self._default_config()
        self.state_manager = StateManager(adapter.memory_dir / "autodream")
        self.analytics = AnalyticsLogger(adapter.memory_dir / "autodream")
        
        # 初始化阶段
        self.orientation = OrientationStage(adapter, self.config)
        self.gather = GatherStage(adapter, self.config)
        self.consolidate = ConsolidateStage(adapter, self.config)
        self.prune = PruneStage(adapter, self.config)
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            # 触发条件
            "hours_since_last_run": 24,
            "min_sessions_since_last": 5,
            "memory_md_max_lines": 200,
            
            # 性能限制
            "session_scan_interval_ms": 10 * 60 * 1000,  # 10 分钟
            "max_memory_files": 200,
            "frontmatter_max_lines": 30,
            
            # 整理策略
            "enable_contradiction_detection": True,
            "enable_stale_detection": True,
            "enable_relative_date_parsing": True,
            
            # Analytics
            "enable_analytics": True,
            "version": "1.0.0",
        }
    
    def should_trigger(self) -> bool:
        """
        检查是否应该触发整理
        
        触发条件：
        1. 距离上次运行 ≥ 24 小时
        2. 新增会话 ≥ 5 个
        3. MEMORY.md 行数 ≤ 200
        """
        state = self.state_manager.load()
        
        # 检查时间门控
        now = datetime.now(timezone.utc)
        if state.last_run:
            hours_since = (now - state.last_run).total_seconds() / 3600
            if hours_since < self.config["hours_since_last_run"]:
                return False
        
        # 检查 Session 扫描节流
        now_ts = now.timestamp() * 1000
        if state.last_session_scan_ts:
            interval = self.config["session_scan_interval_ms"]
            if now_ts - state.last_session_scan_ts < interval:
                return False
        
        # 检查会话数量
        session_count = self.adapter.count_sessions_since(state.last_run_ts or 0)
        if session_count < self.config["min_sessions_since_last"]:
            return False
        
        # 检查 MEMORY.md 行数
        memory_lines = self.adapter.get_memory_md_lines()
        if memory_lines > self.config["memory_md_max_lines"]:
            return False
        
        return True
    
    def run(self, force: bool = False) -> Dict:
        """
        执行完整的四阶段流程
        
        参数:
            force: 强制运行，忽略触发条件
            
        返回:
            包含各阶段结果的字典
        """
        start_time = time.time()
        
        # 检查触发条件
        if not force and not self.should_trigger():
            return {"skipped": True, "reason": "触发条件不满足"}
        
        # 初始化状态
        self.state_manager.write(DreamState(status="running"))
        self.state_manager.update_phase("orientation")
        
        # Analytics: 开始事件
        if self.config.get("enable_analytics", True):
            self.analytics.log("autodream_started", {
                "trigger": "force" if force else "auto",
            })
        
        try:
            # 阶段 1: Orientation
            orientation_result = self.orientation.execute()
            self.state_manager.update_phase("gather", entries_processed=len(orientation_result.get("entries", [])))
            
            # 阶段 2: Gather
            gather_result = self.gather.execute(orientation_result)
            self.state_manager.update_phase("consolidate", entries_processed=len(gather_result.get("entries", [])))
            
            # 阶段 3: Consolidate
            consolidate_result = self.consolidate.execute(gather_result)
            self.state_manager.update_phase("prune", entries_processed=len(consolidate_result.get("final_entries", [])))
            
            # 阶段 4: Prune
            prune_result = self.prune.execute(consolidate_result)
            
            # 完成
            duration = time.time() - start_time
            self.state_manager.complete()
            
            # Analytics: 完成事件
            if self.config.get("enable_analytics", True):
                self.analytics.log("autodream_completed", {
                    "duration_seconds": duration,
                    "entries_processed": len(consolidate_result.get("final_entries", [])),
                    "pruned_count": consolidate_result.get("pruned_count", 0),
                    "merged_count": consolidate_result.get("merged_count", 0),
                })
            
            # 更新 Session 扫描时间
            state = self.state_manager.load()
            state.last_session_scan_ts = datetime.now(timezone.utc).timestamp() * 1000
            self.state_manager.write(state)
            
            return {
                "ok": True,
                "orientation": orientation_result,
                "gather": gather_result,
                "consolidation": consolidate_result,
                "prune": prune_result,
                "duration_seconds": duration,
            }
            
        except Exception as e:
            # 失败处理
            self.state_manager.fail(str(e))
            
            if self.config.get("enable_analytics", True):
                self.analytics.log("autodream_failed", {
                    "error": str(e),
                })
            
            raise
    
    def get_state(self) -> DreamState:
        """获取当前状态"""
        return self.state_manager.load()
    
    def get_analytics(self) -> List[Dict]:
        """获取 Analytics 事件列表"""
        return self.analytics.read_all()
