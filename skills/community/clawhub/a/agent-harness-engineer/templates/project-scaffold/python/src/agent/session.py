#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: agent.session
# 说明: 会话管理，实现不可变的会话日志
# 修改建议: 如需扩展，继承SessionManager类
# ============================================
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class SessionEvent:
    """会话事件"""
    id: str
    type: str  # user_message, assistant_message, tool_use, tool_result
    content: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class SessionManager:
    """会话管理器"""
    
    def __init__(self, storage_path: str = "memory/sessions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.current_session_id: Optional[str] = None
        self.events: List[SessionEvent] = []
    
    def create_session(self) -> str:
        """创建新会话"""
        session_id = str(uuid.uuid4())
        self.current_session_id = session_id
        self.events = []
        logger.info(f"Created session: {session_id}")
        return session_id
    
    def add_event(self, event_type: str, content: str, metadata: Dict[str, Any] = None):
        """添加事件"""
        event = SessionEvent(
            id=str(uuid.uuid4()),
            type=event_type,
            content=content,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        self.events.append(event)
        self._persist_event(event)
    
    def _persist_event(self, event: SessionEvent):
        """持久化事件"""
        if not self.current_session_id:
            return
        
        session_file = self.storage_path / f"{self.current_session_id}.jsonl"
        with open(session_file, "a") as f:
            f.write(json.dumps({
                "id": event.id,
                "type": event.type,
                "content": event.content,
                "timestamp": event.timestamp,
                "metadata": event.metadata
            }) + "\n")
    
    def get_session_history(self, session_id: str) -> List[SessionEvent]:
        """获取会话历史"""
        session_file = self.storage_path / f"{session_id}.jsonl"
        if not session_file.exists():
            return []
        
        events = []
        with open(session_file, "r") as f:
            for line in f:
                data = json.loads(line)
                events.append(SessionEvent(**data))
        return events
    
    def list_sessions(self) -> List[str]:
        """列出所有会话"""
        sessions = []
        for file in self.storage_path.glob("*.jsonl"):
            sessions.append(file.stem)
        return sessions
