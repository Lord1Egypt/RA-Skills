#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄小说发布模块 - 封装 fanqie-publisher 技能

通过调用外部 fanqie-publisher 实现章节发布
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict


class Chapter:
    """章节对象"""
    
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
    
    def __repr__(self):
        return f"Chapter(title='{self.title}', content_len={len(self.content)})"


class FanQiePublisher:
    """
    番茄小说发布器
    
    封装 fanqie-publisher 技能的发布功能。
    """
    
    def __init__(self, scripts_dir: str = None):
        """
        初始化发布器
        
        Args:
            scripts_dir: fanqie-publisher 脚本目录
                        默认 ~/.openclaw/skills/fanqie-publisher/scripts
        """
        if scripts_dir:
            self.scripts_dir = Path(scripts_dir)
        else:
            self.scripts_dir = Path.home() / ".openclaw/skills/fanqie-publisher/scripts"
        
        # 确保依赖的模块可用
        self._setup_path()
        
    def _setup_path(self):
        """将 publisher 脚本目录添加到 import 路径"""
        if str(self.scripts_dir) not in sys.path:
            sys.path.insert(0, str(self.scripts_dir))
    
    def check_login(self) -> Dict:
        """
        检查登录状态
        
        Returns:
            {"logged_in": bool, "message": str}
        """
        try:
            from main import check_login
            result = check_login()
            return result
        except Exception as e:
            return {"logged_in": False, "message": str(e)}
    
    def get_works(self) -> Dict:
        """
        获取作品列表
        
        Returns:
            {"success": bool, "works": [...], "message": str}
        """
        try:
            from main import get_works as _get_works
            result = _get_works()
            return result
        except Exception as e:
            return {"success": False, "works": [], "message": str(e)}
    
    def find_work(self, title: str) -> Optional[Dict]:
        """
        根据标题查找作品
        
        Args:
            title: 作品标题（支持模糊匹配）
            
        Returns:
            作品信息 dict 或 None
        """
        result = self.get_works()
        if not result["success"]:
            return None
        
        for work in result["works"]:
            if title in work["title"]:
                return work
        return None
    
    def publish_chapter(self, work_title: str, chapter: Chapter, 
                       interval: int = 5) -> Dict:
        """
        发布单个章节
        
        Args:
            work_title: 作品标题
            chapter: Chapter 对象
            interval: 发布间隔（秒）
            
        Returns:
            {"success": bool, "message": str, "chapter_title": str}
        """
        try:
            from main import publish_batch, load_chapters_from_file
            
            chapters = [{"title": chapter.title, "content": chapter.content}]
            results = publish_batch(work_title, chapters, interval=interval)
            
            if results:
                return results[0]
            return {"success": False, "message": "发布无返回结果", "chapter_title": chapter.title}
        except Exception as e:
            return {"success": False, "message": str(e), "chapter_title": chapter.title}
    
    def publish_file(self, work_title: str, file_path: str,
                    interval: int = 5) -> List[Dict]:
        """
        发布文件中的章节
        
        Args:
            work_title: 作品标题
            file_path: .md 文件路径
            interval: 发布间隔（秒）
            
        Returns:
            [{"success": bool, ...}, ...]
        """
        try:
            from main import publish_batch, load_chapters_from_file
            
            chapters = load_chapters_from_file(file_path)
            results = publish_batch(work_title, chapters, interval=interval)
            return results
        except Exception as e:
            return [{"success": False, "message": str(e), "chapter_title": "未知"}]
    
    def publish_batch(self, work_title: str, chapters: List[Chapter],
                      interval: int = 5) -> List[Dict]:
        """
        批量发布章节
        
        Args:
            work_title: 作品标题
            chapters: Chapter 对象列表
            interval: 发布间隔（秒）
            
        Returns:
            [{"success": bool, ...}, ...]
        """
        try:
            from main import publish_batch as _publish_batch
            
            chapters_data = [{"title": c.title, "content": c.content} for c in chapters]
            results = _publish_batch(work_title, chapters_data, interval=interval)
            return results
        except Exception as e:
            return [{"success": False, "message": str(e), "chapter_title": c.title}
                    for c in chapters]


def create_chapter(title: str, content: str) -> Chapter:
    """工厂函数：创建 Chapter 对象"""
    return Chapter(title, content)


def extract_chapter_from_file(filepath: str) -> Optional[Chapter]:
    """
    从 .md 文件提取章节信息
    
    Args:
        filepath: .md 文件路径
        
    Returns:
        Chapter 对象 或 None
    """
    path = Path(filepath)
    if not path.exists():
        return None
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    title = None
    body_start = 0
    
    # 找标题
    for i, line in enumerate(lines):
        if line.startswith('# 第'):
            title = line.lstrip('# ').strip()
            body_start = i + 1
            break
    
    if not title:
        return None
    
    # 找分隔符
    sep_idx = None
    for i in range(body_start, len(lines)):
        if lines[i].strip() == '---':
            sep_idx = i
            break
    
    content_start = sep_idx + 1 if sep_idx else body_start
    
    # 提取正文（到章末钩子前）
    body_lines = []
    for line in lines[content_start:]:
        if line.startswith('>'):
            break
        body_lines.append(line)
    
    pure_content = '\n'.join(body_lines).strip()
    
    return Chapter(title=title, content=pure_content)
