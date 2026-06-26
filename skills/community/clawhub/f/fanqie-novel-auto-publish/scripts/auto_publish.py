#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键发布工作流 - 整合小说生成和番茄发布

完整流程：
1. 加载故事设定（从 .learnings 目录）
2. 生成/读取章节内容
3. 发布到番茄小说平台
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List

# 导入封装模块（包内引用）
from novel_generator import NovelPipeline, NovelChapter, get_recent_chapters
from fanqie_publisher import FanQiePublisher, Chapter, extract_chapter_from_file


class AutoPublishWorkflow:
    """
    自动发布工作流
    
    整合 novel-generator 和 fanqie-publisher，
    实现从生成到发布的一键完成。
    """
    
    def __init__(self):
        self.novel_gen = NovelPipeline()
        self.publisher = FanQiePublisher()
        
    def check_status(self) -> dict:
        """
        检查各模块状态
        
        Returns:
            {"novel_generator": bool, "fanqie_publisher": bool, "logged_in": bool}
        """
        status = {
            "novel_generator": True,  # 本地文件存在即正常
            "fanqie_publisher": self.novel_gen.work_dir.exists(),
            "logged_in": False,
            "works": []
        }
        
        # 检查登录
        login_result = self.publisher.check_login()
        status["logged_in"] = login_result.get("logged_in", False)
        
        # 获取作品列表
        if status["logged_in"]:
            works_result = self.publisher.get_works()
            if works_result.get("success"):
                status["works"] = works_result["works"]
        
        return status
    
    def get_work(self, title: str) -> Optional[dict]:
        """获取指定作品信息"""
        return self.publisher.find_work(title)
    
    def publish_chapter(self, work_title: str, chapter_file: str,
                       interval: int = 5) -> dict:
        """
        发布单个章节
        
        Args:
            work_title: 作品标题
            chapter_file: 章节 .md 文件路径
            interval: 发布间隔（秒）
            
        Returns:
            {"success": bool, "message": str}
        """
        # 提取章节
        chapter = extract_chapter_from_file(chapter_file)
        if not chapter:
            return {
                "success": False,
                "message": f"无法从文件提取章节: {chapter_file}"
            }
        
        # 发布
        result = self.publisher.publish_chapter(
            work_title=work_title,
            chapter=chapter,
            interval=interval
        )
        
        return result
    
    def publish_all_in_output(self, work_title: str,
                              interval: int = 5) -> List[dict]:
        """
        发布 output 目录下所有章节
        
        Args:
            work_title: 作品标题
            interval: 发布间隔（秒）
            
        Returns:
            [result_dict, ...]
        """
        output_dir = self.novel_gen.output_dir
        if not output_dir.exists():
            return [{"success": False, "message": f"目录不存在: {output_dir}"}]
        
        md_files = list(output_dir.glob("*.md"))
        if not md_files:
            return [{"success": False, "message": "没有找到章节文件"}]
        
        results = []
        for f in sorted(md_files):
            print(f"  正在发布: {f.name}")
            result = self.publish_chapter(work_title, str(f), interval)
            results.append(result)
            if result.get("success"):
                print(f"    ✓ 成功")
            else:
                print(f"    ✗ 失败: {result.get('message')}")
        
        return results


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="番茄小说一键发布工具")
    parser.add_argument("--work", "-w", type=str, help="作品标题")
    parser.add_argument("--file", "-f", type=str, help="章节文件路径")
    parser.add_argument("--check", "-c", action="store_true", help="仅检查状态")
    parser.add_argument("--works", action="store_true", help="列出所有作品")
    parser.add_argument("--interval", "-i", type=int, default=5, help="发布间隔(秒)")
    
    args = parser.parse_args()
    
    workflow = AutoPublishWorkflow()
    
    # 检查状态
    if args.check:
        print("=" * 60)
        print("状态检查")
        print("=" * 60)
        status = workflow.check_status()
        print(f"小说生成模块: {'✓' if status['novel_generator'] else '✗'}")
        print(f"番茄发布模块: {'✓' if status['fanqie_publisher'] else '✗'}")
        print(f"登录状态: {'✓' if status['logged_in'] else '✗'}")
        if status["works"]:
            print(f"\n作品列表 ({len(status['works'])} 部):")
            for w in status["works"]:
                print(f"  - {w['title']} ({w['chapter_count']}章)")
        return
    
    # 列出作品
    if args.works:
        status = workflow.check_status()
        if not status["works"]:
            print("未登录或无作品")
            return
        print("=" * 60)
        print("作品列表")
        print("=" * 60)
        for i, w in enumerate(status["works"], 1):
            print(f"{i}. {w['title']}")
            print(f"   章节: {w['chapter_count']} | 状态: {w.get('status', 'unknown')}")
        return
    
    # 发布单个章节
    if args.work and args.file:
        print(f"正在发布到: {args.work}")
        print(f"文件: {args.file}")
        result = workflow.publish_chapter(args.work, args.file, args.interval)
        if result["success"]:
            print(f"\n✓ 发布成功: {result.get('message', '')}")
        else:
            print(f"\n✗ 发布失败: {result.get('message', '')}")
            sys.exit(1)
        return
    
    # 无参数时显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
