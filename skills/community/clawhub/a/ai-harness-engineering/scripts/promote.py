#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 自动提升脚本
将重要学习提升到workspace文件
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
LEARNINGS_FILE = DATA_DIR / "learnings_ledger.jsonl"


def load_learnings() -> list:
    """加载所有学习记录"""
    learnings = []
    if LEARNINGS_FILE.exists():
        with open(LEARNINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        learnings.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return learnings


def update_learning_status(learning_id: str, status: str, promoted_to: str = "") -> dict:
    """更新学习记录状态"""
    learnings = load_learnings()
    updated = False
    
    for i, learning in enumerate(learnings):
        if learning.get('learning_id') == learning_id:
            learnings[i]['status'] = status
            if promoted_to:
                learnings[i]['promoted_to'] = promoted_to
            updated = True
            break
    
    if updated:
        with open(LEARNINGS_FILE, 'w', encoding='utf-8') as f:
            for learning in learnings:
                f.write(json.dumps(learning, ensure_ascii=False) + '\n')
        
        return {"status": "ok", "message": f"学习 {learning_id} 已更新为 {status}"}
    
    return {"status": "error", "message": f"未找到学习记录 {learning_id}"}


def check_promote_candidates() -> list:
    """检查可提升的候选学习"""
    learnings = load_learnings()
    candidates = []
    
    for learning in learnings:
        # 满足提升条件
        should_promote = False
        target = ""
        
        # 条件1: recurrence_count >= 3
        if learning.get('recurrence_count', 1) >= 3:
            should_promote = True
            target = "AGENTS.md"  # 重复多次应该提升到工作流程
        
        # 条件2: 高优先级
        elif learning.get('priority') in ['high', 'critical']:
            should_promote = True
            target = "SOUL.md" if learning.get('category') == 'correction' else "AGENTS.md"
        
        # 条件3: 用户明确要求
        if learning.get('source') == 'user_feedback':
            should_promote = True
            target = "MEMORY.md"
        
        if should_promote and learning.get('status') == 'pending':
            learning['suggested_target'] = target
            candidates.append(learning)
    
    return candidates


def promote_to_workspace(learning_id: str, target_file: str, dry_run: bool = False) -> dict:
    """将学习提升到workspace文件"""
    workspace = Path.home() / ".qclaw" / "workspace"
    
    # 目标文件路径
    target_path = workspace / target_file
    
    # 加载学习内容
    learnings = load_learnings()
    learning = None
    for l in learnings:
        if l.get('learning_id') == learning_id:
            learning = l
            break
    
    if not learning:
        return {"status": "error", "message": f"未找到学习记录 {learning_id}"}
    
    # 如果是 dry_run，直接返回模拟结果
    if dry_run:
        return {
            "status": "ok",
            "message": f"模拟提升 {learning_id} 到 {target_file}",
            "target": str(target_path),
            "dry_run": True
        }
    
    # 蒸馏为简洁规则
    summary = learning.get('summary', '')
    details = learning.get('details', '')
    category = learning.get('category', '')
    
    # 根据类别确定section
    if category == 'correction':
        section = "## 行为纠正\n"
    elif category == 'best_practice':
        section = "## 最佳实践\n"
    elif category == 'knowledge_gap':
        section = "## 知识更新\n"
    else:
        section = "## 学习\n"
    
    entry = f"\n### {learning_id}\n"
    entry += f"**时间**: {learning.get('timestamp', '')}\n"
    entry += f"**摘要**: {summary}\n"
    entry += f"**详情**: {details}\n\n"
    
    # 写入目标文件（追加）
    try:
        # 确保目录存在
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 读取现有内容
        existing = ""
        if target_path.exists():
            existing = target_path.read_text(encoding='utf-8')
        
        # 追加新内容
        if existing and not existing.endswith('\n'):
            existing += '\n'
        
        # 检查是否已存在section
        if section not in existing:
            existing += f"\n{section}"
        
        existing += entry
        
        target_path.write_text(existing, encoding='utf-8')
        
        # 更新状态
        update_learning_status(learning_id, "promoted", target_file)
        
        return {
            "status": "ok",
            "message": f"已提升到 {target_file}",
            "target": str(target_path)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"提升失败: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(description='自动提升学习到workspace')
    parser.add_argument('--action', required=True,
                       choices=['check_candidates', 'promote', 'auto_promote'],
                       help='操作类型')
    parser.add_argument('--learning-id', help='学习ID（promote操作需要）')
    parser.add_argument('--target', 
                       choices=['SOUL.md', 'AGENTS.md', 'TOOLS.md', 'MEMORY.md'],
                       help='目标workspace文件')
    parser.add_argument('--dry-run', action='store_true',
                       help='模拟运行，不实际写入')
    
    args = parser.parse_args()
    
    if args.action == 'check_candidates':
        candidates = check_promote_candidates()
        print(json.dumps({
            "status": "ok",
            "candidates_count": len(candidates),
            "candidates": candidates
        }, ensure_ascii=False, indent=2))
    
    elif args.action == 'promote':
        if not args.learning_id or not args.target:
            print(json.dumps({
                "status": "error",
                "message": "promote操作需要 --learning-id 和 --target 参数"
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        result = promote_to_workspace(args.learning_id, args.target, args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'auto_promote':
        # 自动提升：检查所有 recurrence_count >= 3 的学习
        candidates = check_promote_candidates()
        
        if not candidates:
            print(json.dumps({
                "status": "ok",
                "message": "暂无可自动提升的学习",
                "promoted_count": 0
            }, ensure_ascii=False, indent=2))
            return
        
        # 自动提升每个候选
        promoted = []
        for candidate in candidates:
            learning_id = candidate.get('learning_id')
            suggested_target = candidate.get('suggested_target', 'AGENTS.md')
            
            if args.dry_run:
                promoted.append({
                    "learning_id": learning_id,
                    "target": suggested_target,
                    "dry_run": True
                })
            else:
                result = promote_to_workspace(learning_id, suggested_target)
                if result.get('status') == 'ok':
                    promoted.append({
                        "learning_id": learning_id,
                        "target": suggested_target
                    })
        
        print(json.dumps({
            "status": "ok",
            "message": f"自动提升完成，共 {len(promoted)} 项",
            "promoted": promoted
        }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()