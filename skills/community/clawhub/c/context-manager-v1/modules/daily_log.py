#!/usr/bin/env python3
"""
Daily Log Manager - 认知日志管理器
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class DailyLogManager:
    """认知日志管理器"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/context")).expanduser()
    
    def create(self, items: List[Dict]) -> Dict[str, Any]:
        """创建每日认知日志"""
        log = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "items": [],
            "summary": "",
            "created_at": datetime.now().isoformat()
        }
        
        for item in items:
            log["items"].append({
                "content": item.get("content", ""),
                "judgment": item.get("judgment", ""),
                "tags": self._extract_tags(item.get("content", ""))
            })
        
        # 保存到 logs 目录
        log_id = f"log-{log['date']}"
        log_path = self.base_path / "logs" / f"{log_id}.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False))
        
        log["id"] = log_id
        log["path"] = str(log_path)
        
        return log
    
    def _extract_tags(self, content: str) -> List[str]:
        """提取标签（简化版）"""
        meaning_tags = {
            "成长痛点": ["痛点", "困难", "挑战"],
            "关系锚点": ["朋友", "争论", "关系"],
            "灵感触发": ["洞察", "顿悟", "灵光"],
        }
        
        tags = []
        for tag, keywords in meaning_tags.items():
            if any(kw in content for kw in keywords):
                tags.append(f"#{tag}#")
        
        return tags
