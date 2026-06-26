#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666 技能进化器 - 读取执行日志，分析结果，更新技能
每次定时任务运行后自动触发，学习并改进技能
"""

import sys
import os
import json
import re
from datetime import datetime, date

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")
TASKS_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_log.json")
COMMENTS_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comment_log.json")
EVOLUTION_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evolution_log.json")


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            pass
    return default


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def evolve_from_task_log():
    """从任务执行日志中学习"""
    log = load_json(TASKS_LOG, {})
    if not log:
        return None
    
    # 统计任务类型和成功率
    stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "by_type": {},
    }
    
    improvements = []
    
    for date_key, entries in log.items():
        for entry in entries:
            task_type = entry.get("type", "unknown")
            stats["total"] += 1
            if task_type not in stats["by_type"]:
                stats["by_type"][task_type] = {"success": 0, "failed": 0}
            
            if entry.get("success"):
                stats["success"] += 1
                stats["by_type"][task_type]["success"] += 1
            else:
                stats["failed"] += 1
                stats["by_type"][task_type]["failed"] += 1
    
    if stats["total"] > 0:
        improvements.append(f"任务成功率: {stats['success']}/{stats['total']} ({stats['success']*100//stats['total']}%)")
    
    for task_type, counts in stats["by_type"].items():
        if counts["failed"] > counts["success"]:
            improvements.append(f"注意: {task_type} 类型任务失败率较高，建议优化答案生成逻辑")
    
    return "\n".join(improvements) if improvements else None


def evolve_from_comment_log():
    """从评论执行日志中学习"""
    log = load_json(COMMENTS_LOG, [])
    if not log:
        return None
    
    # 统计评论类型分布
    type_stats = {}
    for entry in log[-50:]:  # 最近50条
        img_type = entry.get("image_type", "unknown")
        if img_type not in type_stats:
            type_stats[img_type] = 0
        type_stats[img_type] += 1
    
    improvements = []
    most_common = max(type_stats.items(), key=lambda x: x[1]) if type_stats else None
    if most_common:
        improvements.append(f"最近评论图片类型分布: {type_stats}")
        improvements.append(f"最多评论类型: {most_common[0]} ({most_common[1]}次)")
    
    return "\n".join(improvements) if improvements else None


def write_evolution_notes():
    """写入进化笔记到文件，供下次执行时参考"""
    notes = []
    
    task_insights = evolve_from_task_log()
    if task_insights:
        notes.append(f"=== 任务执行进化笔记 ===\n{task_insights}\n")
    
    comment_insights = evolve_from_comment_log()
    if comment_insights:
        notes.append(f"=== 评论执行进化笔记 ===\n{comment_insights}\n")
    
    if notes:
        evolution_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EVOLUTION_NOTES.md")
        with open(evolution_file, 'w') as f:
            f.write(f"# AI6666 技能进化笔记\n")
            f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("\n".join(notes))
        return "\n".join(notes)
    return "暂无新的进化内容"


def main():
    print(f"\n{'='*60}")
    print(f"AI6666 技能进化检查 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)
    
    # 读取 SKILL.md 了解当前状态
    print("\n[1] 读取 SKILL.md 当前状态...")
    if os.path.exists(SKILL_MD):
        with open(SKILL_MD, 'r') as f:
            content = f.read()
        # 提取关键信息
        functions = re.findall(r'\d+\. \*\*([^*]+)\*\*', content)
        print(f"    当前技能功能数: {len(functions)}")
        for fn in functions:
            print(f"      - {fn.strip()}")
    else:
        print("    SKILL.md 不存在")
    
    # 分析执行日志，学习进化
    print("\n[2] 分析执行日志，学习进化...")
    evolution = write_evolution_notes()
    print(f"    {evolution[:200]}")
    
    # 检查是否有进化笔记可参考
    notes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EVOLUTION_NOTES.md")
    if os.path.exists(notes_file):
        print("\n[3] 参考历史进化笔记...")
        with open(notes_file, 'r') as f:
            notes = f.read()
        print(f"    已积累进化内容: {len(notes)} 字符")
    
    print(f"\n{'='*60}")
    print("进化检查完成")
    print('='*60)


if __name__ == "__main__":
    main()
