#!/usr/bin/env python3
"""
章节写作辅助脚本 - 整合大纲、前文回顾、角色信息，生成写作提示
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Optional

# 导入 novel_manager 的功能
sys.path.insert(0, str(Path(__file__).parent))
from novel_manager import (
    get_novels_dir, format_backlog, get_recent_summaries,
    get_chapter_dir, create_chapter, parse_meta
)


class ChapterWriter:
    """章节写作助手"""
    
    def __init__(self, novel_name: str):
        self.novel_name = novel_name
        self.novel_dir = get_novels_dir() / novel_name
        
        if not self.novel_dir.exists():
            raise FileNotFoundError(f"小说 '{novel_name}' 不存在")
    
    def read_file(self, relative_path: str) -> str:
        """读取小说目录下的文件"""
        file_path = self.novel_dir / relative_path
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return ""
    
    def get_context_for_writing(self, volume: int, chapter: int) -> Dict:
        """
        获取写作第X章所需的全部上下文
        
        Returns:
            包含所有上下文信息的字典
        """
        context = {
            "novel_name": self.novel_name,
            "volume": volume,
            "chapter": chapter,
        }
        
        # 1. 元数据
        context["meta"] = self.read_file("meta.md")
        
        # 2. 大纲
        context["outline"] = self.read_file("outline.md")
        
        # 3. 前文回顾（最近10章）
        context["backlog"] = format_backlog(self.novel_name, 10)
        
        # 4. 角色信息
        context["characters"] = self.read_file("characters/index.md")
        
        # 5. 设定信息
        context["settings"] = {
            "world": self.read_file("settings/world.md"),
            "system": self.read_file("settings/system.md"),
            "cultivation": self.read_file("settings/cultivation.md"),
            "items": self.read_file("settings/items.md"),
            "skills": self.read_file("settings/skills.md"),
        }
        
        # 6. 上一章的笔记（获取最新信息）
        if chapter > 1:
            prev_chapter_dir = get_chapter_dir(self.novel_name, volume, chapter - 1)
            if prev_chapter_dir.exists():
                context["prev_note"] = self.read_file(
                    f"chapters/{prev_chapter_dir.name}/note.md"
                )
            else:
                # 尝试找上一卷的最后一章
                prev_volume_last = self._find_last_chapter_of_volume(volume - 1)
                if prev_volume_last:
                    context["prev_note"] = self.read_file(
                        f"chapters/{prev_volume_last}/note.md"
                    )
        
        return context
    
    def _find_last_chapter_of_volume(self, volume: int) -> Optional[str]:
        """找到指定卷的最后一章目录名"""
        chapters_dir = self.novel_dir / "chapters"
        if not chapters_dir.exists():
            return None
        
        chapters = []
        for item in chapters_dir.iterdir():
            if item.is_dir():
                match = re.match(r'(\d{2})-(\d{3})', item.name)
                if match and int(match.group(1)) == volume:
                    chapters.append((int(match.group(2)), item.name))
        
        if chapters:
            chapters.sort()
            return chapters[-1][1]
        return None
    
    def generate_writing_prompt(self, volume: int, chapter: int, 
                                title_hint: str = "") -> str:
        """
        生成写作提示
        
        Args:
            volume: 卷号
            chapter: 章节号
            title_hint: 标题提示（可选）
        
        Returns:
            完整的写作提示文本
        """
        context = self.get_context_for_writing(volume, chapter)
        
        prompt_lines = []
        prompt_lines.append("=" * 70)
        prompt_lines.append(f"【写作任务】第{chapter}章")
        if title_hint:
            prompt_lines.append(f"【建议标题】{title_hint}")
        prompt_lines.append("=" * 70)
        
        # 前文回顾
        prompt_lines.append("\n" + context["backlog"])
        
        # 大纲中的本章规划
        prompt_lines.append("\n【本章规划】")
        chapter_plan = self._extract_chapter_plan(context["outline"], chapter)
        prompt_lines.append(chapter_plan if chapter_plan else "请根据整体大纲规划本章内容")
        
        # 角色信息
        prompt_lines.append("\n【角色参考】")
        prompt_lines.append(context["characters"][:1000] if context["characters"] else "暂无角色信息")
        prompt_lines.append("...")
        
        # 设定参考
        prompt_lines.append("\n【设定参考】")
        if context["settings"]["system"]:
            prompt_lines.append("【系统设定】")
            prompt_lines.append(context["settings"]["system"][:500])
        if context["settings"]["cultivation"]:
            prompt_lines.append("\n【修炼体系】")
            prompt_lines.append(context["settings"]["cultivation"][:500])
        
        # 上一章笔记中的新信息
        if context.get("prev_note"):
            prompt_lines.append("\n【上一章新信息】")
            prompt_lines.append(context["prev_note"][:800])
        
        # 写作要求
        prompt_lines.append("\n" + "=" * 70)
        prompt_lines.append("【写作要求】")
        prompt_lines.append("=" * 70)
        prompt_lines.append("""
1. 字数要求：3000-5000字
2. 风格要求：参考《斗破苍穹》，节奏快、爽点密集
3. 避免AI味词汇：不要使用"值得一提的是"、"不难发现"等表达
4. 对话简洁有力，避免长篇说教
5. 章末必须留悬念或爽点
6. 保持与设定的一致性

【输出格式】
请直接输出章节正文，格式如下：

# 第X章 章节标题

正文内容...

（本章完）
""")
        
        return '\n'.join(prompt_lines)
    
    def _extract_chapter_plan(self, outline: str, chapter: int) -> str:
        """从大纲中提取指定章节的规划"""
        # 查找章节规划表格中的对应行
        lines = outline.split('\n')
        for line in lines:
            # 匹配 | 001 | 或 |第001章| 等格式
            if re.search(rf'\|\s*{chapter:03d}\s*\|', line) or \
               re.search(rf'\|\s*第?{chapter}\s*章?\s*\|', line):
                return line.strip()
        
        # 尝试查找章节标题
        for line in lines:
            if re.search(rf'第{chapter}章[：:\s]', line) or \
               re.search(rf'^{chapter}\.', line):
                return line.strip()
        
        return ""
    
    def generate_summary_template(self, content: str) -> str:
        """
        根据章节内容生成摘要模板
        
        Args:
            content: 章节正文
        
        Returns:
            摘要模板
        """
        # 提取章节号
        chapter_match = re.search(r'第(\d+)章', content)
        chapter = chapter_match.group(1) if chapter_match else "X"
        
        # 提取标题
        title_match = re.search(r'第\d+章\s*(.+?)[\n\r]', content)
        title = title_match.group(1) if title_match else ""
        
        template = f"""# 第{chapter}章{title} - 摘要

## 情节概要
【请用200字概括本章主要情节】

## 关键对话
【记录本章重要的对话片段】
- 

## 爽点/高潮
【描述本章的爽点或高潮部分】
- 

## 伏笔/悬念
【记录本章埋下的伏笔或结尾悬念】
- 

## 战力/等级变化
【如有升级或战力变化，记录于此】
- 
"""
        return template
    
    def generate_note_template(self, content: str) -> str:
        """
        根据章节内容生成笔记模板
        
        Args:
            content: 章节正文
        
        Returns:
            笔记模板
        """
        chapter_match = re.search(r'第(\d+)章', content)
        chapter = chapter_match.group(1) if chapter_match else "X"
        
        template = f"""# 第{chapter}章笔记

## 新角色
【记录本章新出场的角色】
- 角色名：简介/身份

## 新地点
【记录本章新出现的地点】
- 地点名：描述

## 新技能/道具
【记录本章出现的新技能、道具】
- 名称：描述

## 系统信息
【记录系统提示、奖励等】
- 

## 势力关系变化
【如有势力关系变化，记录于此】
- 

## 待跟进事项
【需要在后续章节跟进的内容】
- 
"""
        return template


def main():
    """命令行入口"""
    if len(sys.argv) < 4:
        print("Usage: chapter_writer.py <novel_name> <volume> <chapter> [title_hint]")
        print("")
        print("Commands:")
        print("  prompt <novel_name> <volume> <chapter> [title] - 生成写作提示")
        print("  summary <content_file> - 根据内容生成摘要模板")
        print("  note <content_file> - 根据内容生成笔记模板")
        return
    
    command = sys.argv[1]
    
    if command == "prompt":
        if len(sys.argv) < 5:
            print("Usage: chapter_writer.py prompt <novel_name> <volume> <chapter> [title]")
            return
        
        novel_name = sys.argv[2]
        volume = int(sys.argv[3])
        chapter = int(sys.argv[4])
        title_hint = sys.argv[5] if len(sys.argv) > 5 else ""
        
        try:
            writer = ChapterWriter(novel_name)
            prompt = writer.generate_writing_prompt(volume, chapter, title_hint)
            print(prompt)
        except FileNotFoundError as e:
            print(f"错误：{e}")
    
    elif command == "summary":
        if len(sys.argv) < 3:
            print("Usage: chapter_writer.py summary <content_file>")
            return
        
        content_path = Path(sys.argv[2])
        if not content_path.exists():
            print(f"错误：文件不存在 {content_path}")
            return
        
        content = content_path.read_text(encoding='utf-8')
        # 创建一个临时writer来获取模板
        writer = ChapterWriter("temp")
        print(writer.generate_summary_template(content))
    
    elif command == "note":
        if len(sys.argv) < 3:
            print("Usage: chapter_writer.py note <content_file>")
            return
        
        content_path = Path(sys.argv[2])
        if not content_path.exists():
            print(f"错误：文件不存在 {content_path}")
            return
        
        content = content_path.read_text(encoding='utf-8')
        writer = ChapterWriter("temp")
        print(writer.generate_note_template(content))
    
    else:
        # 向后兼容：直接生成写作提示
        novel_name = sys.argv[1]
        volume = int(sys.argv[2])
        chapter = int(sys.argv[3])
        title_hint = sys.argv[4] if len(sys.argv) > 4 else ""
        
        try:
            writer = ChapterWriter(novel_name)
            prompt = writer.generate_writing_prompt(volume, chapter, title_hint)
            print(prompt)
        except FileNotFoundError as e:
            print(f"错误：{e}")


if __name__ == "__main__":
    main()
