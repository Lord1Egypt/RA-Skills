"""
Analytics 埋点工具

记录使用行为，JSONL 格式。
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any


class AnalyticsLogger:
    """
    Analytics 日志记录器
    
    记录事件到 JSONL 文件（每行一个 JSON 对象）。
    
    用法:
        logger = AnalyticsLogger(Path("/path/to/memory/autodream"))
        logger.log("autodream_started", {"trigger": "auto"})
        logger.log("autodream_completed", {"duration_seconds": 123})
    """
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_file = log_dir / ".autodream_analytics.jsonl"
        
        # 确保目录存在
        log_dir.mkdir(parents=True, exist_ok=True)
    
    def log(self, event: str, data: Dict[str, Any] = None, version: str = "1.0.0") -> None:
        """
        记录事件
        
        参数:
            event: 事件名称
            data: 附加数据
            version: 版本号
        """
        entry = {
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": version,
        }
        
        if data:
            entry.update(data)
        
        # 追加到 JSONL 文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def read_all(self) -> List[Dict]:
        """
        读取所有事件
        
        返回:
            事件列表
        """
        if not self.log_file.exists():
            return []
        
        events = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return events
    
    def get_events(self, event_type: str) -> List[Dict]:
        """
        获取特定类型的事件
        
        参数:
            event_type: 事件类型
            
        返回:
            事件列表
        """
        all_events = self.read_all()
        return [e for e in all_events if e.get("event") == event_type]
    
    def get_stats(self) -> Dict:
        """
        获取统计信息
        
        返回:
            {"total_runs": int, "avg_duration": float, "failures": int}
        """
        events = self.read_all()
        
        started = [e for e in events if e.get("event") == "autodream_started"]
        completed = [e for e in events if e.get("event") == "autodream_completed"]
        failed = [e for e in events if e.get("event") == "autodream_failed"]
        
        # 计算平均耗时
        durations = [e.get("duration_seconds", 0) for e in completed if "duration_seconds" in e]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_runs": len(started),
            "successful_runs": len(completed),
            "failures": len(failed),
            "avg_duration_seconds": avg_duration,
            "total_entries_processed": sum(e.get("entries_processed", 0) for e in completed),
        }
