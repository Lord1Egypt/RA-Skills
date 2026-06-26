#!/usr/bin/env python3
"""
Tag Function - 打标功能

给笔记自动打标（主题 + 场景 + 行动）
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class TagFunction:
    """打标功能实现"""
    
    def __init__(self, config: dict):
        self.config = config
        self.taxonomy = self._load_taxonomy()
    
    def _load_taxonomy(self) -> dict:
        """加载标签体系"""
        return {
            "themes": [
                "投资/基金", "投资/股票", "投资/资产配置",
                "产品/设计", "产品/需求", "产品/评审",
                "技术/AI", "技术/架构", "技术/工具",
                "管理/决策", "管理/团队", "管理/流程",
                "个人/健康", "个人/学习", "个人/关系",
                "知识管理", "个人成长"
            ],
            "scenes": [
                "场景/晨会", "场景/周会", "场景/月会",
                "场景/决策前", "场景/复盘时", "场景/写作时",
                "场景/沟通时", "场景/学习时", "场景/带娃时"
            ],
            "actions": [
                "行动/立即执行", "行动/本周内", "行动/本月内",
                "行动/调研", "行动/对比", "行动/实验",
                "行动/分享", "行动/存档", "行动/删除"
            ]
        }
    
    def execute(self, note_id: str, content: str) -> Dict[str, Any]:
        """
        执行打标功能
        
        Args:
            note_id: 笔记 ID
            content: 笔记内容
        
        Returns:
            打标结果
        """
        # 分析内容，匹配标签
        tags = self._auto_tag(content)
        
        # 生成带 Front Matter 的笔记
        frontmatter = self._generate_frontmatter(tags)
        new_content = frontmatter + self._remove_existing_frontmatter(content)
        
        return {
            "note_id": note_id,
            "content": new_content,
            "tags": tags,
            "confidence": 0.8,
            "status": "tagged",
            "tagged_at": datetime.now().isoformat()
        }
    
    def _auto_tag(self, content: str) -> dict:
        """自动打标（规则匹配）"""
        themes = []
        scenes = []
        actions = []
        
        content_lower = content.lower()
        
        # 主题匹配
        if any(kw in content_lower for kw in ["基金", "定投", "投顾", "资产配置"]):
            themes.append("投资/基金")
        if any(kw in content_lower for kw in ["股票", "个股", "选股"]):
            themes.append("投资/股票")
        if any(kw in content_lower for kw in ["产品", "需求", "设计", "评审"]):
            themes.append("产品/设计")
        if any(kw in content_lower for kw in ["ai", "大模型", "agent", "知识管理"]):
            themes.append("知识管理")
        if any(kw in content_lower for kw in ["健康", "运动", "睡眠"]):
            themes.append("个人/健康")
        
        # 场景匹配
        if any(kw in content_lower for kw in ["晨会", "早上", "每日"]):
            scenes.append("场景/晨会")
        if any(kw in content_lower for kw in ["决策", "选择", "要不要"]):
            scenes.append("场景/决策前")
        if any(kw in content_lower for kw in ["写作", "文章", "公众号"]):
            scenes.append("场景/写作时")
        
        # 行动匹配
        if any(kw in content_lower for kw in ["立即", "马上", "今天"]):
            actions.append("行动/立即执行")
        if any(kw in content_lower for kw in ["调研", "研究", "深入了解"]):
            actions.append("行动/调研")
        if any(kw in content_lower for kw in ["分享", "输出", "文章"]):
            actions.append("行动/分享")
        
        # 默认标签
        if not themes:
            themes.append("知识管理")
        if not scenes:
            scenes.append("场景/学习时")
        if not actions:
            actions.append("行动/存档")
        
        return {
            "themes": themes[:3],
            "scenes": scenes[:2],
            "actions": actions[:2]
        }
    
    def _generate_frontmatter(self, tags: dict) -> str:
        """生成 Front Matter"""
        all_tags = tags["themes"] + tags["scenes"] + tags["actions"]
        
        return f"""---
tags: [{", ".join(all_tags)}]
themes: [{", ".join(tags["themes"])}]
scenes: [{", ".join(tags["scenes"])}]
actions: [{", ".join(tags["actions"])}]
tagged_at: {datetime.now().isoformat()}
confidence: 0.8
---

"""
    
    def _remove_existing_frontmatter(self, content: str) -> str:
        """移除现有 Front Matter"""
        if content.startswith("---"):
            lines = content.split("\n")
            end_idx = 1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    end_idx = i + 1
                    break
            return "\n".join(lines[end_idx:])
        return content
