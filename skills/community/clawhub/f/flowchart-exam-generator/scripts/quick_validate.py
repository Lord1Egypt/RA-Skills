#!/usr/bin/env python3
"""
技能结构验证脚本
验证SKILL.md和_meta.json的格式是否正确
"""

import os
import re
import json
import sys

def validate_skill(skill_path):
    """
    验证技能结构

    Returns:
        tuple: (is_valid, errors)
    """
    errors = []

    # 检查SKILL.md是否存在
    skill_md_path = os.path.join(skill_path, 'SKILL.md')
    if not os.path.exists(skill_md_path):
        errors.append("SKILL.md 文件不存在")
        return False, errors

    # 读取SKILL.md内容
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查frontmatter格式
    if not content.startswith('---'):
        errors.append("SKILL.md 必须以 YAML frontmatter (---) 开头")

    # 提取frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("无法解析 YAML frontmatter")
    else:
        frontmatter = frontmatter_match.group(1)

        # 检查必填字段
        if 'name:' not in frontmatter:
            errors.append("frontmatter 必须包含 name 字段")
        if 'description:' not in frontmatter:
            errors.append("frontmatter 必须包含 description 字段")

    # 检查_meta.json
    meta_path = os.path.join(skill_path, '_meta.json')
    if not os.path.exists(meta_path):
        errors.append("_meta.json 文件不存在")
    else:
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)

            # 检查必填字段
            if 'id' not in meta:
                errors.append("_meta.json 必须包含 id 字段")
            if 'version' not in meta:
                errors.append("_meta.json 必须包含 version 字段")

            # 检查id类型
            if 'id' in meta and not isinstance(meta['id'], int):
                errors.append("_meta.json 的 id 必须是整数")
        except json.JSONDecodeError as e:
            errors.append(f"_meta.json JSON格式错误: {e}")

    return len(errors) == 0, errors


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python quick_validate.py <skill_path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    is_valid, errors = validate_skill(skill_path)

    if is_valid:
        print("✓ 验证通过")
        sys.exit(0)
    else:
        print("✗ 验证失败:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
