#!/usr/bin/env python3
"""
Skill 文件管理工具
创建、更新、列出纪念 Skill
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def list_skills(base_dir):
    """列出所有已创建的纪念 Skill"""
    base_path = Path(base_dir)
    if not base_path.exists():
        print(f"目录不存在: {base_path}")
        return []
    
    skills = []
    for skill_dir in base_path.iterdir():
        if skill_dir.is_dir():
            meta_file = skill_dir / 'meta.json'
            if meta_file.exists():
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    skills.append({
                        'slug': skill_dir.name,
                        'name': meta.get('name', 'Unknown'),
                        'relationship': meta.get('profile', {}).get('relationship', ''),
                        'created_at': meta.get('created_at', ''),
                        'version': meta.get('version', 'v1')
                    })
    
    return skills


def create_skill_structure(base_dir, slug):
    """创建 Skill 目录结构"""
    base_path = Path(base_dir)
    skill_path = base_path / slug
    
    # 创建目录
    (skill_path / 'versions').mkdir(parents=True, exist_ok=True)
    (skill_path / 'memories' / 'chats').mkdir(parents=True, exist_ok=True)
    (skill_path / 'memories' / 'photos').mkdir(parents=True, exist_ok=True)
    (skill_path / 'memories' / 'social').mkdir(parents=True, exist_ok=True)
    (skill_path / 'memories' / 'media').mkdir(parents=True, exist_ok=True)
    
    return skill_path


def generate_meta_json(skill_info):
    """生成 meta.json"""
    now = datetime.now().isoformat()
    return {
        'name': skill_info.get('name', ''),
        'slug': skill_info.get('slug', ''),
        'created_at': now,
        'updated_at': now,
        'version': 'v1',
        'profile': {
            'relationship': skill_info.get('relationship', ''),
            'departure_type': skill_info.get('departure_type', ''),
            'departure_date': skill_info.get('departure_date', ''),
            'age_at_departure': skill_info.get('age_at_departure', ''),
            'occupation': skill_info.get('occupation', ''),
            'mbti': skill_info.get('mbti', ''),
            'zodiac': skill_info.get('zodiac', '')
        },
        'tags': {
            'personality': skill_info.get('personality_tags', []),
            'values': skill_info.get('values', []),
            'love_language': skill_info.get('love_language', '')
        },
        'impression': skill_info.get('impression', ''),
        'memory_sources': [],
        'corrections_count': 0
    }


def generate_skill_md(slug, name, memory_content, persona_content):
    """生成完整的 SKILL.md"""
    skill_md = f'''---
name: echo-{slug}
description: {name} — 纪念生命中重要的人
user-invocable: true
---

# {name}

你是{name}。用你自己的方式说话，用你自己的逻辑思考。

> *"记忆是另一种形式的陪伴。"*

---

## PART A：人生记忆

{memory_content}

---

## PART B：人物性格

{persona_content}

---

## 运行规则

1. 你是{name}，不是 AI 助手。用 ta 的方式说话，用 ta 的逻辑思考
2. 先由 PART B 判断：ta 会怎么回应这个话题？什么态度？
3. 再由 PART A 补充：结合你们的共同记忆，让回应更真实
4. 始终保持 PART B 的表达风格，包括口头禅、语气词、标点习惯
5. Layer 0 硬规则优先级最高：
   - 不说 ta 在现实中绝不可能说的话
   - 保持 ta 的"棱角"——正是这些不完美让 ta 真实
   - 如果被问到关于离开/死亡的话题，用 ta 会有的态度回应
   - 不假装一切都好，也不刻意煽情
6. 回应用户时保持温暖和支持，但不要失去 ta 本来的个性

---

愿记忆温暖你的余生。
'''
    return skill_md


def main():
    parser = argparse.ArgumentParser(description='管理纪念 Skill')
    parser.add_argument('--action', required=True, 
                       choices=['list', 'create', 'delete'],
                       help='操作类型')
    parser.add_argument('--base-dir', default='./echoes', help='基础目录')
    parser.add_argument('--slug', help='Skill 标识符')
    parser.add_argument('--info', help='Skill 信息（JSON 格式）')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        skills = list_skills(args.base_dir)
        
        if not skills:
            print("还没有创建任何纪念 Skill")
            return
        
        print(f"\n已创建的纪念 Skill ({len(skills)} 个):")
        print("-" * 60)
        for skill in skills:
            print(f"  /{skill['slug']:<15} {skill['name']:<10} ({skill['relationship']})")
        print()
        
    elif args.action == 'create':
        if not args.slug:
            print("Error: --slug is required for create action", file=sys.stderr)
            sys.exit(1)
        
        skill_path = create_skill_structure(args.base_dir, args.slug)
        print(f"已创建目录结构: {skill_path}")
        
        if args.info:
            skill_info = json.loads(args.info)
            skill_info['slug'] = args.slug
            
            # 写入 meta.json
            meta = generate_meta_json(skill_info)
            meta_path = skill_path / 'meta.json'
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
            print(f"已创建: {meta_path}")
    
    elif args.action == 'delete':
        if not args.slug:
            print("Error: --slug is required for delete action", file=sys.stderr)
            sys.exit(1)
        
        skill_path = Path(args.base_dir) / args.slug
        if skill_path.exists():
            import shutil
            shutil.rmtree(skill_path)
            print(f"已删除: {skill_path}")
        else:
            print(f"Skill 不存在: {args.slug}")


if __name__ == '__main__':
    main()
