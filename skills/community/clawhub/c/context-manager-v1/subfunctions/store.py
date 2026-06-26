#!/usr/bin/env python3
"""
Store Function - 存储功能

存储到知识库，自动建立双链连接
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple
from collections import defaultdict


class StoreFunction:
    """存储功能实现"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/kb")).expanduser()
        self.index_path = self.base_path / "_index.json"
        self.log_path = self.base_path / "_log.md"
        
        # 加载或创建索引
        self.note_index = self._load_index()
    
    def _load_index(self) -> dict:
        """加载笔记索引"""
        if self.index_path.exists():
            return json.loads(self.index_path.read_text())
        return {
            "notes": {},  # {note_id: {title, path, tags, themes, created_at}}
            "links": {},  # {note_id: [linked_by_notes]}
            "keywords": {}  # {keyword: [note_ids]}
        }
    
    def _save_index(self):
        """保存索引"""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self.note_index, indent=2, ensure_ascii=False))
    
    def _append_log(self, operation: str, details: str):
        """追加操作日志"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.log_path.exists():
            self.log_path.write_text("# 操作日志\n\n")
        
        log_entry = f"- {datetime.now().strftime('%Y-%m-%d %H:%M')} - {operation}: {details}\n"
        self.log_path.write_text(self.log_path.read_text() + log_entry)
    
    def execute(self, note_id: str, content: str, tags: dict) -> Dict[str, Any]:
        """
        执行存储功能
        
        Args:
            note_id: 笔记 ID
            content: 带标签的笔记内容
            tags: 标签信息
        
        Returns:
            存储结果
        """
        # 根据主题标签确定存储路径
        theme = tags["themes"][0] if tags["themes"] else "其他"
        folder = self._theme_to_folder(theme)
        
        storage_path = self.base_path / folder
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # 提取标题
        title = self._extract_title(content)
        
        # 移动笔记到对应文件夹
        note_path = storage_path / f"{note_id}.md"
        note_path.write_text(content)
        
        # 更新索引
        self._update_index(note_id, title, note_path, tags, content)
        
        # 自动建立双链连接
        suggested_links = self._suggest_links(note_id, content, tags)
        
        # 在笔记中添加双链
        updated_content = self._add_wikilinks(content, suggested_links)
        if updated_content != content:
            note_path.write_text(updated_content)
        
        # 更新反向链接
        self._update_backlinks(note_id, suggested_links)
        
        # 记录日志
        self._append_log("store", f"{note_id} -> {folder}/{note_id}.md, links: {len(suggested_links)}")
        
        # 保存索引
        self._save_index()
        
        return {
            "note_id": note_id,
            "storage_path": str(note_path),
            "folder": folder,
            "suggested_links": suggested_links,
            "status": "stored",
            "stored_at": datetime.now().isoformat(),
            "links_count": len(suggested_links)
        }
    
    def _extract_title(self, content: str) -> str:
        """提取笔记标题"""
        # 尝试从 Front Matter 提取
        if content.startswith("---"):
            match = re.search(r'title:\s*(.+?)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        # 尝试从第一个标题提取
        match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # 默认使用内容前 50 字
        return content[:50].split('\n')[0]
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        # 从标签提取
        tag_matches = re.findall(r'themes:\s*\[(.*?)\]', content)
        if tag_matches:
            themes = [t.strip() for t in tag_matches[0].split(',')]
            return themes
        
        # 从内容提取（简化版：提取高频词）
        words = re.findall(r'[\u4e00-\u9fa5a-zA-Z]{2,}', content)
        word_count = defaultdict(int)
        for word in words:
            word_count[word] += 1
        
        # 返回出现频率最高的 5 个词
        sorted_words = sorted(word_count.items(), key=lambda x: -x[1])
        return [word for word, count in sorted_words[:5]]
    
    def _update_index(self, note_id: str, title: str, note_path: Path, tags: dict, content: str):
        """更新笔记索引"""
        keywords = self._extract_keywords(content)
        
        self.note_index["notes"][note_id] = {
            "title": title,
            "path": str(note_path),
            "tags": tags,
            "themes": tags.get("themes", []),
            "keywords": keywords,
            "created_at": datetime.now().isoformat()
        }
        
        # 更新关键词索引
        for keyword in keywords:
            if keyword not in self.note_index["keywords"]:
                self.note_index["keywords"][keyword] = []
            if note_id not in self.note_index["keywords"][keyword]:
                self.note_index["keywords"][keyword].append(note_id)
    
    def _suggest_links(self, note_id: str, content: str, tags: dict) -> List[dict]:
        """
        自动建议双链连接
        
        匹配策略：
        1. 同主题笔记（优先级最高）
        2. 关键词匹配
        3. 标签重叠
        """
        suggestions = []
        current_themes = tags.get("themes", [])
        current_keywords = self._extract_keywords(content)
        
        # 策略 1：同主题笔记
        for other_id, other_info in self.note_index["notes"].items():
            if other_id == note_id:
                continue
            
            other_themes = other_info.get("themes", [])
            
            # 检查主题重叠
            theme_overlap = set(current_themes) & set(other_themes)
            if theme_overlap:
                score = len(theme_overlap) * 10  # 每个重叠主题 10 分
                suggestions.append({
                    "note_id": other_id,
                    "title": other_info["title"],
                    "wikilink": f"[[{other_info['title']}]]",
                    "reason": f"同主题：{', '.join(theme_overlap)}",
                    "score": score,
                    "type": "theme"
                })
        
        # 策略 2：关键词匹配
        for keyword in current_keywords:
            if keyword in self.note_index["keywords"]:
                for other_id in self.note_index["keywords"][keyword]:
                    if other_id == note_id:
                        continue
                    
                    other_info = self.note_index["notes"][other_id]
                    
                    # 检查是否已添加
                    if any(s["note_id"] == other_id for s in suggestions):
                        continue
                    
                    suggestions.append({
                        "note_id": other_id,
                        "title": other_info["title"],
                        "wikilink": f"[[{other_info['title']}]]",
                        "reason": f"关键词：{keyword}",
                        "score": 5,  # 关键词匹配 5 分
                        "type": "keyword"
                    })
        
        # 策略 3：标签重叠（场景、行动）
        for other_id, other_info in self.note_index["notes"].items():
            if other_id == note_id:
                continue
            
            other_scenes = other_info.get("tags", {}).get("scenes", [])
            other_actions = other_info.get("tags", {}).get("actions", [])
            
            scene_overlap = set(tags.get("scenes", [])) & set(other_scenes)
            action_overlap = set(tags.get("actions", [])) & set(other_actions)
            
            if scene_overlap or action_overlap:
                reasons = []
                score = 0
                if scene_overlap:
                    reasons.append(f"同场景：{', '.join(scene_overlap)}")
                    score += 3
                if action_overlap:
                    reasons.append(f"同行动：{', '.join(action_overlap)}")
                    score += 3
                
                # 检查是否已添加
                if any(s["note_id"] == other_id for s in suggestions):
                    continue
                
                suggestions.append({
                    "note_id": other_id,
                    "title": other_info["title"],
                    "wikilink": f"[[{other_info['title']}]]",
                    "reason": "; ".join(reasons),
                    "score": score,
                    "type": "tag"
                })
        
        # 按分数排序，取前 5 个
        suggestions.sort(key=lambda x: -x["score"])
        return suggestions[:5]
    
    def _add_wikilinks(self, content: str, suggested_links: List[dict]) -> str:
        """
        在笔记末尾添加双链
        
        格式：
        ## 🔗 相关笔记
        - [[笔记 A]] - 理由
        - [[笔记 B]] - 理由
        """
        if not suggested_links:
            return content
        
        # 检查是否已有相关笔记部分
        if "## 🔗 相关笔记" in content:
            return content  # 已有，不重复添加
        
        # 添加相关笔记部分
        links_section = "\n\n---\n\n## 🔗 相关笔记\n\n"
        for link in suggested_links[:3]:  # 最多添加 3 个
            links_section += f"- {link['wikilink']} - {link['reason']}\n"
        
        return content + links_section
    
    def _update_backlinks(self, note_id: str, suggested_links: List[dict]):
        """更新反向链接索引"""
        for link in suggested_links:
            linked_note_id = link["note_id"]
            
            if linked_note_id not in self.note_index["links"]:
                self.note_index["links"][linked_note_id] = []
            
            if note_id not in self.note_index["links"][linked_note_id]:
                self.note_index["links"][linked_note_id].append(note_id)
    
    def _theme_to_folder(self, theme: str) -> str:
        """将主题映射到文件夹"""
        mapping = {
            "投资/基金": "10-投资/基金",
            "投资/股票": "10-投资/股票",
            "投资/资产配置": "10-投资",
            "产品/设计": "20-产品",
            "技术/AI": "30-技术",
            "知识管理": "40-管理",
            "个人/健康": "50-个人",
        }
        return mapping.get(theme, "90-归档")
