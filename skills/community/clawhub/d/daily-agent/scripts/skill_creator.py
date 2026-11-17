#!/usr/bin/env python3
"""
Skill 自动创建辅助脚本
当对话中出现可复用的模式时，辅助创建 SKILL.md。

触发词：保存为skill / 创建技能 / 记住这个流程
冷静期：同一模式需≥3次独立会话才建议创建

Usage:
    python skill_creator.py --name=my-skill --description="..." --content="..."
    python skill_creator.py --suggest  # 检查是否有待创建的技能建议
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


SKILL_TEMPLATE = """---
name: {name}
version: 1.0.0
description: "{description}"
---

# {title}

{content}
"""

SUGGESTIONS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    '..', '..', 'memory', 'skill_suggestions.json'
)


def create_skill(name, description, content, output_dir=None):
    """创建新的 skill 目录和 SKILL.md"""
    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            '..', '..', 'skills'
        )
    
    skill_dir = os.path.join(output_dir, name)
    os.makedirs(skill_dir, exist_ok=True)
    
    title = name.replace('-', ' ').title()
    skill_content = SKILL_TEMPLATE.format(
        name=name,
        description=description,
        title=title,
        content=content
    )
    
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    with open(skill_md, 'w', encoding='utf-8') as f:
        f.write(skill_content)
    
    return {
        'status': 'created',
        'path': skill_dir,
        'skill_md': skill_md,
    }


def add_suggestion(pattern, context, session_id):
    """添加技能建议（用于冷静期机制）"""
    suggestions = load_suggestions()
    
    # 检查是否已有相同模式的建议
    for s in suggestions:
        if s['pattern'] == pattern:
            s['count'] += 1
            s['last_seen'] = datetime.now().isoformat()
            s['sessions'] = list(set(s.get('sessions', []) + [session_id]))
            save_suggestions(suggestions)
            return {'status': 'updated', 'count': s['count'], 'ready': s['count'] >= 3}
    
    suggestions.append({
        'pattern': pattern,
        'context': context,
        'session_id': session_id,
        'sessions': [session_id],
        'count': 1,
        'created': datetime.now().isoformat(),
        'last_seen': datetime.now().isoformat(),
    })
    save_suggestions(suggestions)
    return {'status': 'added', 'count': 1, 'ready': False}


def load_suggestions():
    if os.path.exists(SUGGESTIONS_FILE):
        with open(SUGGESTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_suggestions(suggestions):
    os.makedirs(os.path.dirname(SUGGESTIONS_FILE), exist_ok=True)
    with open(SUGGESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(suggestions, f, ensure_ascii=False, indent=2)


def check_ready_suggestions():
    """检查哪些建议已达到冷静期要求"""
    suggestions = load_suggestions()
    ready = [s for s in suggestions if s['count'] >= 3]
    return {'ready_count': len(ready), 'suggestions': ready}


def main():
    parser = argparse.ArgumentParser(description='Skill 自动创建辅助')
    parser.add_argument('--name', help='Skill 名称')
    parser.add_argument('--description', help='Skill 描述')
    parser.add_argument('--content', help='Skill 内容')
    parser.add_argument('--output-dir', help='输出目录')
    parser.add_argument('--suggest', action='store_true', help='添加/检查建议')
    parser.add_argument('--pattern', help='建议的模式')
    parser.add_argument('--context', help='建议的上下文')
    parser.add_argument('--session-id', help='当前会话ID')
    
    args = parser.parse_args()
    
    if args.suggest:
        if args.pattern and args.session_id:
            result = add_suggestion(args.pattern, args.context or '', args.session_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            result = check_ready_suggestions()
            print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.name and args.description:
        result = create_skill(
            args.name, args.description,
            args.content or 'TODO: Add skill content',
            args.output_dir
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
