"""
状态管理工具

Task 生命周期追踪。
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class DreamState:
    """
    Dream 状态数据类
    
    字段:
        status: 状态 (running/completed/failed)
        started_at: 开始时间 (ISO 格式)
        completed_at: 完成时间 (ISO 格式，可选)
        phase: 当前阶段 (orientation/gather/consolidate/prune)
        entries_processed: 已处理条目数
        error: 错误信息 (可选)
        last_run: 上次运行时间 (ISO 格式，可选)
        last_run_ts: 上次运行时间戳 (秒)
        last_session_scan_ts: 上次 Session 扫描时间戳 (毫秒)
    """
    status: str = "running"
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    phase: str = "orientation"
    entries_processed: int = 0
    error: Optional[str] = None
    last_run: Optional[str] = None
    last_run_ts: float = 0
    last_session_scan_ts: float = 0
    
    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "DreamState":
        """从字典创建"""
        return cls(**data)


class StateManager:
    """
    状态管理器
    
    管理 .dream_state.json 文件的读写。
    
    用法:
        state_manager = StateManager(Path("/path/to/memory/autodream"))
        state = state_manager.load()
        state_manager.update_phase("gather")
        state_manager.complete()
    """
    
    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.state_file = state_dir / ".dream_state.json"
        
        # 确保目录存在
        state_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> DreamState:
        """
        加载状态
        
        如果文件不存在，返回默认状态。
        """
        if not self.state_file.exists():
            return DreamState()
        
        try:
            content = self.state_file.read_text(encoding="utf-8")
            data = json.loads(content)
            return DreamState.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return DreamState()
    
    def write(self, state: DreamState) -> None:
        """
        写入状态
        
        参数:
            state: 状态对象
        """
        self.state_dir.mkdir(parents=True, exist_ok=True)
        content = json.dumps(state.to_dict(), indent=2, ensure_ascii=False)
        self.state_file.write_text(content, encoding="utf-8")
    
    def update_phase(self, phase: str, entries_processed: int = None) -> None:
        """
        更新阶段
        
        参数:
            phase: 阶段名称 (orientation/gather/consolidate/prune)
            entries_processed: 已处理条目数 (可选)
        """
        state = self.load()
        state.phase = phase
        if entries_processed is not None:
            state.entries_processed = entries_processed
        self.write(state)
    
    def complete(self) -> None:
        """标记完成"""
        state = self.load()
        state.status = "completed"
        state.completed_at = datetime.now(timezone.utc).isoformat()
        self.write(state)
    
    def fail(self, error: str) -> None:
        """
        标记失败
        
        参数:
            error: 错误信息
        """
        state = self.load()
        state.status = "failed"
        state.completed_at = datetime.now(timezone.utc).isoformat()
        state.error = error
        self.write(state)
    
    def is_running(self) -> bool:
        """检查是否正在运行"""
        state = self.load()
        return state.status == "running"
    
    def get_last_run(self) -> Optional[datetime]:
        """获取上次运行时间"""
        state = self.load()
        if state.completed_at:
            return datetime.fromisoformat(state.completed_at)
        return None
