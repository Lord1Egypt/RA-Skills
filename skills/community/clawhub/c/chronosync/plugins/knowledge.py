"""
知识沉淀插件

功能：
- 提取关键决策、结论
- 自动分类到 PARA 结构
- 生成 topic 笔记
"""

import os
import re
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# 从 plugin_base 导入 Plugin 基类
sys.path.insert(0, str(Path(__file__).parent.parent))
from plugin_base import Plugin


class KnowledgePlugin(Plugin):
    """知识沉淀插件"""
    
    name = "knowledge"
    enabled = True
    
    # 决策关键词
    DECISION_PATTERNS = [
        r"决定.*",
        r"确定.*",
        r"选择.*",
        r"方案.*",
        r"结论是.*",
        r"最终.*",
    ]
    
    # 技术知识点
    TECH_PATTERNS = [
        r".*原理.*",
        r".*方法.*",
        r".*步骤.*",
        r".*配置.*",
        r".*优化.*",
    ]
    
    def __init__(self):
        # 从环境变量或默认位置获取
        openclaw_dir = Path(os.environ.get("OPENCLAW_STATE_DIR", Path.home() / ".openclaw"))
        self.output_dir = openclaw_dir / "workspace" / "memory" / "sync" / "decisions"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def on_sync(self, messages: List[Dict]) -> Dict[str, Any]:
        """处理消息，提取知识"""
        decisions = []
        tech_notes = []
        
        for msg in messages:
            content = msg.get("content", "")
            role = msg.get("role", "")
            
            # 提取决策
            if self._is_decision(content):
                decisions.append({
                    "content": content,
                    "role": role,
                    "timestamp": msg.get("timestamp", ""),
                    "type": "decision"
                })
            
            # 提取技术知识点
            if self._is_tech_note(content):
                tech_notes.append({
                    "content": content,
                    "role": role,
                    "timestamp": msg.get("timestamp", ""),
                    "type": "tech_note"
                })
        
        # 保存到文件
        if decisions:
            self._save_decisions(decisions)
        
        if tech_notes:
            self._save_tech_notes(tech_notes)
        
        return {
            "decisions_extracted": len(decisions),
            "tech_notes_extracted": len(tech_notes)
        }
    
    def _is_decision(self, content: str) -> bool:
        """判断是否为决策内容"""
        for pattern in self.DECISION_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _is_tech_note(self, content: str) -> bool:
        """判断是否为技术知识点"""
        for pattern in self.TECH_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        # 代码块也是技术内容
        if "```" in content:
            return True
        return False
    
    def _save_decisions(self, decisions: List[Dict]):
        """保存决策记录"""
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = self.output_dir / f"decisions_{today}.md"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            for d in decisions:
                f.write(f"\n## {d['timestamp']}\n\n")
                f.write(f"**来源:** {d['role']}\n\n")
                f.write(f"{d['content']}\n\n")
                f.write("---\n")
    
    def _save_tech_notes(self, notes: List[Dict]):
        """保存技术笔记"""
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = self.output_dir / f"tech_notes_{today}.md"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            for n in notes:
                f.write(f"\n## {n['timestamp']}\n\n")
                f.write(f"**来源:** {n['role']}\n\n")
                f.write(f"{n['content']}\n\n")
                f.write("---\n")


# 实例化
plugin = KnowledgePlugin()
