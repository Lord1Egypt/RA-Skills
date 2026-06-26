#!/usr/bin/env python3
"""
Context Collector - 上下文收集器

支持来源：
- 飞书文档
- 微信读书
- 小红书笔记
- 内心认知
- 手动笔记
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


class ContextCollector:
    """上下文收集器"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/context")).expanduser()
        self.inbox_path = self.base_path / "inbox"
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        
        # 意义标签关键词
        self.meaning_tags = {
            "成长痛点": ["痛点", "困难", "挑战", "挣扎", "困惑"],
            "关系锚点": ["朋友", "争论", "关系", "理解", "家人", "同事"],
            "灵感触发": ["洞察", "顿悟", "灵光", "想到", "启发"],
            "认知冲突": ["冲突", "矛盾", "困惑", "犹豫", "纠结"],
            "决策背景": ["决定", "选择", "决策", "犹豫", "权衡"]
        }
    
    def collect(self, 
                source_type: str, 
                content: str,
                metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        收集上下文
        
        Args:
            source_type: 来源类型 (feishu|wechat|xiaohongshu|inner_cognition|manual)
            content: 内容
            metadata: 可选元数据
        
        Returns:
            收集结果
        """
        if source_type == "feishu":
            return self._collect_feishu(content, metadata)
        elif source_type == "wechat":
            return self._collect_wechat(content, metadata)
        elif source_type == "xiaohongshu":
            return self._collect_xiaohongshu(content, metadata)
        elif source_type == "inner_cognition":
            return self._collect_inner_cognition(content, metadata)
        elif source_type == "manual":
            return self._collect_manual(content, metadata)
        else:
            raise ValueError(f"不支持的来源类型：{source_type}")
    
    def _collect_feishu(self, doc_token: str, metadata: Optional[Dict] = None) -> Dict:
        """从飞书文档收集"""
        context_id = f"ctx-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        title = metadata.get("title", f"飞书文档 - {doc_token}") if metadata else f"飞书文档 - {doc_token}"
        
        context = {
            "id": context_id,
            "type": "external",
            "source": "feishu",
            "title": title,
            "content": f"（待从飞书 API 获取实际内容）",
            "source_url": f"https://my.feishu.cn/docx/{doc_token}",
            "created_at": datetime.now().isoformat(),
            "tags": []
        }
        
        # 保存到 inbox
        context_path = self.inbox_path / f"{context_id}.json"
        context_path.write_text(json.dumps(context, indent=2, ensure_ascii=False))
        
        return {
            "id": context_id,
            "title": title,
            "content": context["content"],
            "source": "feishu",
            "created_at": context["created_at"],
            "status": "collected",
            "path": str(context_path)
        }
    
    def _collect_wechat(self, export_text: str, metadata: Optional[Dict] = None) -> Dict:
        """从微信读书导出收集"""
        context_id = f"ctx-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        context = {
            "id": context_id,
            "type": "external",
            "source": "wechat",
            "title": metadata.get("title", "微信读书"),
            "content": export_text,
            "created_at": datetime.now().isoformat(),
            "tags": []
        }
        
        context_path = self.inbox_path / f"{context_id}.json"
        context_path.write_text(json.dumps(context, indent=2, ensure_ascii=False))
        
        return {
            "id": context_id,
            "title": context["title"],
            "content": export_text,
            "source": "wechat",
            "created_at": context["created_at"],
            "status": "collected",
            "path": str(context_path)
        }
    
    def _collect_xiaohongshu(self, note_content: str, metadata: Optional[Dict] = None) -> Dict:
        """从小红书笔记收集"""
        context_id = f"ctx-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        context = {
            "id": context_id,
            "type": "external",
            "source": "xiaohongshu",
            "title": metadata.get("title", "小红书笔记"),
            "content": note_content,
            "created_at": datetime.now().isoformat(),
            "tags": []
        }
        
        context_path = self.inbox_path / f"{context_id}.json"
        context_path.write_text(json.dumps(context, indent=2, ensure_ascii=False))
        
        return context
    
    def _collect_inner_cognition(self, 
                                  content: str,
                                  metadata: Optional[Dict] = None) -> Dict:
        """收集内心认知"""
        context_id = f"ctx-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 提取意义标签
        tags = self.extract_meaning_tags(content)
        
        # 情绪分析（简化版）
        emotion = self._analyze_emotion(content)
        
        context = {
            "id": context_id,
            "type": "inner_cognition",
            "source": "inner",
            "title": f"内心认知 - {datetime.now().strftime('%Y-%m-%d')}",
            "content": content,
            "emotion": emotion,
            "created_at": datetime.now().isoformat(),
            "tags": tags
        }
        
        context_path = self.inbox_path / f"{context_id}.json"
        context_path.write_text(json.dumps(context, indent=2, ensure_ascii=False))
        
        return {
            "id": context_id,
            "title": context["title"],
            "content": content,
            "emotion": emotion,
            "tags": tags,
            "source": "inner_cognition",
            "created_at": context["created_at"],
            "status": "collected",
            "path": str(context_path)
        }
    
    def _collect_manual(self, content: str, metadata: Optional[Dict] = None) -> Dict:
        """收集手动笔记"""
        context_id = f"ctx-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        title = metadata.get("title", f"手动笔记 - {datetime.now().strftime('%Y-%m-%d')}")
        
        context = {
            "id": context_id,
            "type": "manual",
            "source": "manual",
            "title": title,
            "content": content,
            "created_at": datetime.now().isoformat(),
            "tags": []
        }
        
        context_path = self.inbox_path / f"{context_id}.json"
        context_path.write_text(json.dumps(context, indent=2, ensure_ascii=False))
        
        return {
            "id": context_id,
            "title": title,
            "content": content,
            "source": "manual",
            "created_at": context["created_at"],
            "status": "collected",
            "path": str(context_path)
        }
    
    def extract_meaning_tags(self, content: str) -> List[str]:
        """提取意义标签"""
        tags = []
        
        for tag, keywords in self.meaning_tags.items():
            if any(kw in content for kw in keywords):
                tags.append(f"#{tag}#")
        
        return tags
    
    def _analyze_emotion(self, content: str) -> str:
        """情绪分析（简化版）"""
        positive_words = ["开心", "高兴", "兴奋", "满意", "感动"]
        negative_words = ["难过", "生气", "失望", "焦虑", "痛苦"]
        
        pos_count = sum(1 for word in positive_words if word in content)
        neg_count = sum(1 for word in negative_words if word in content)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
