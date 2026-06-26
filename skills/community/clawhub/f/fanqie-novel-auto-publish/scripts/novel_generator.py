#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说生成模块 - 封装 novel-generator 技能

通过调用外部 AI 生成小说章节内容
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime


class NovelChapter:
    """小说章节对象"""
    
    def __init__(self, title: str, content: str, word_count: int = 0):
        self.title = title          # 章节标题，如 "第3章 午夜电梯"
        self.content = content      # 正文内容（不含标题）
        self.word_count = word_count or len(content)
        self.file_path = None       # 生成后保存的路径


class NovelPipeline:
    """
    小说生成流水线
    
    整合 novel-generator 技能，按流程生成小说章节：
    1. 想法 → 2. 设定 → 3. 大纲 → 4. 生成章节 → 5. 评审修订
    """
    
    def __init__(self, work_dir: str = None):
        """
        初始化生成流水线
        
        Args:
            work_dir: 工作目录，默认 ~/.openclaw/skills/novel-generator
        """
        self.work_dir = Path(work_dir) if work_dir else Path.home() / ".openclaw/skills/novel-generator"
        self.output_dir = self.work_dir / "output"
        self.learnings_dir = self.work_dir / ".learnings"
        
        # 状态
        self.current_chapter = None
        self.generated_chapters = []
        
    def load_learning(self, filename: str) -> str:
        """加载学习文件内容"""
        path = self.learnings_dir / filename
        if path.exists():
            return path.read_text(encoding='utf-8')
        return ""
    
    def get_story_bible(self) -> str:
        """获取故事圣经"""
        return self.load_learning("STORY_BIBLE.md")
    
    def get_characters(self) -> str:
        """获取角色设定"""
        return self.load_learning("CHARACTERS.md")
    
    def get_plot_points(self) -> str:
        """获取情节点"""
        return self.load_learning("PLOT_POINTS.md")
    
    def get_locations(self) -> str:
        """获取场景设定"""
        return self.load_learning("LOCATIONS.md")
    
    def save_chapter(self, chapter: NovelChapter, chapter_num: int = None) -> Path:
        """
        保存章节到文件
        
        Args:
            chapter: 章节对象
            chapter_num: 章节序号
            
        Returns:
            保存的文件路径
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名：第XX章_标题.md
        if chapter_num is not None:
            chapter_marker = f"第{chapter_num:02d}章"
        else:
            # 从标题提取章节号
            match = re.search(r'第(\d+)章', chapter.title)
            chapter_marker = f"第{match.group(1) if match else '?'}章"
        
        # 清理标题中的章节号（避免重复）
        clean_title = re.sub(r'^第\d+章\s*', '', chapter.title)
        filename = f"{chapter_marker}_{clean_title}.md"
        filepath = self.output_dir / filename
        
        # 写入文件（UTF-8）
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {chapter.title}\n")
            f.write("---\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"字数: {chapter.word_count}\n")
            f.write("---\n")
            f.write(f"\n{chapter.content}\n")
        
        chapter.file_path = filepath
        return filepath
    
    def extract_content_from_file(self, filepath: str) -> dict:
        """
        从 Markdown 文件提取章节信息
        
        Args:
            filepath: .md 文件路径
            
        Returns:
            {"title": str, "content": str, "pure_title": str}
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        title = None
        body_start = 0
        
        # 找标题（# 开头）
        for i, line in enumerate(lines):
            if line.startswith('# 第'):
                title = line.lstrip('# ').strip()
                body_start = i + 1
                break
        
        # 找分隔符 ---
        sep_idx = None
        for i in range(body_start, len(lines)):
            if lines[i].strip() == '---':
                sep_idx = i
                break
        
        # 正文从分隔符后开始
        content_start = sep_idx + 1 if sep_idx else body_start
        
        # 提取正文（到章末钩子 > 之前）
        body_lines = []
        for line in lines[content_start:]:
            if line.startswith('>'):
                break
            body_lines.append(line)
        
        pure_content = '\n'.join(body_lines).strip()
        
        return {
            "title": title or "未命名章节",
            "content": pure_content,
            "pure_title": title or "未命名章节"
        }
    
    def generate_chapter_content(self, prompt: str) -> str:
        """
        生成章节内容（需要外部 AI 调用）
        
        这个方法是占位符，实际内容生成由调用者通过 AI 完成。
        返回生成的 Markdown 文件路径列表。
        
        Args:
            prompt: 生成提示词
            
        Returns:
            生成的章节内容
        """
        # 实际生成依赖外部 AI，这里只是记录日志
        raise NotImplementedError(
            "内容生成需要通过 AI 对话实现。"
            "请使用 AI 对话生成章节内容，然后调用 save_chapter 保存。"
        )


def get_recent_chapters(count: int = 5) -> list:
    """
    获取最近生成的章节列表
    
    Args:
        count: 返回数量
        
    Returns:
        [{"filename": str, "path": str, "time": datetime}, ...]
    """
    output = Path.home() / ".openclaw/skills/novel-generator/output"
    if not output.exists():
        return []
    
    files = []
    for f in output.glob("*.md"):
        files.append({
            "filename": f.name,
            "path": str(f),
            "time": datetime.fromtimestamp(f.stat().st_mtime)
        })
    
    # 按时间倒序
    files.sort(key=lambda x: x["time"], reverse=True)
    return files[:count]
