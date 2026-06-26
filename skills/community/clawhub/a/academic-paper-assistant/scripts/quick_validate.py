#!/usr/bin/env python3
"""
学术论文助手技能验证脚本
验证 SKILL.md 结构和 frontmatter 规范性
"""

import os
import re
import sys
from pathlib import Path


def validate_skill_structure(skill_path: str) -> tuple[bool, list[str]]:
    """验证技能结构完整性"""
    errors = []
    skill_path = Path(skill_path)

    # 检查必要文件
    required_files = ['SKILL.md', '_meta.json']
    for file in required_files:
        file_path = skill_path / file
        if not file_path.exists():
            errors.append(f"缺少必要文件: {file}")

    return len(errors) == 0, errors


def validate_frontmatter(skill_path: str) -> tuple[bool, list[str]]:
    """验证 SKILL.md frontmatter 规范性"""
    errors = []
    skill_path = Path(skill_path) / 'SKILL.md'

    if not skill_path.exists():
        errors.append("SKILL.md 文件不存在")
        return False, errors

    content = skill_path.read_text(encoding='utf-8')

    # 检查是否以 frontmatter 开头（不能以 # 开头）
    first_line = content.strip().split('\n')[0]
    if first_line.startswith('#'):
        errors.append("错误: SKILL.md 不能以 # 标题开头，必须以 --- frontmatter 开始")

    # 提取 frontmatter
    if not content.startswith('---'):
        errors.append("错误: SKILL.md 必须以 --- 开头定义 frontmatter")
        return False, errors

    # 解析 frontmatter
    frontmatter_pattern = r'^---\s*\n(.*?)\n---'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        errors.append("错误: 无法解析 frontmatter，请检查格式")
        return False, errors

    frontmatter_content = match.group(1)

    # 检查必填字段
    required_fields = ['name', 'description']
    for field in required_fields:
        if not re.search(rf'^{field}:\s*.+', frontmatter_content, re.MULTILINE):
            errors.append(f"缺少必填字段: {field}")

    # 验证 name 格式（连字符，小写）
    name_match = re.search(r'^name:\s*(.+)', frontmatter_content, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip()
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"name 格式错误: '{name}'，应使用小写字母、数字和连字符")
        if len(name) > 64:
            errors.append(f"name 长度超过64字符限制")

    # 验证 description 包含触发短语
    desc_match = re.search(r'^description:\s*(.+)', frontmatter_content, re.MULTILINE)
    if desc_match:
        description = desc_match.group(1).strip()
        if len(description) < 20:
            errors.append("description 过短，应包含详细的触发短语描述")
        # 检查是否包含中文
        if not re.search(r'[\u4e00-\u9fff]', description):
            errors.append("description 应包含中文描述")

    return len(errors) == 0, errors


def validate_meta_json(skill_path: str) -> tuple[bool, list[str]]:
    """验证 _meta.json 规范性"""
    import json
    errors = []
    meta_path = Path(skill_path) / '_meta.json'

    if not meta_path.exists():
        errors.append("_meta.json 文件不存在")
        return False, errors

    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"_meta.json 格式错误: {e}")
        return False, errors

    # 检查必填字段
    required_fields = ['id', 'version']
    for field in required_fields:
        if field not in meta:
            errors.append(f"缺少必填字段: {field}")

    # 验证 id 是整数
    if 'id' in meta:
        if not isinstance(meta['id'], (int, str)):
            errors.append("id 应为数字或字符串")
        elif isinstance(meta['id'], str) and not meta['id'].isdigit():
            errors.append("id 应为纯数字字符串")

    # 验证 version 格式
    if 'version' in meta:
        if not re.match(r'^\d+\.\d+\.\d+$', meta['version']):
            errors.append("version 格式应为 x.y.z (如 1.0.0)")

    return len(errors) == 0, errors


def main():
    """主验证流程"""
    skill_path = sys.argv[1] if len(sys.argv) > 1 else '.'

    print(f"正在验证技能: {skill_path}")
    print("=" * 50)

    all_passed = True

    # 1. 结构验证
    print("\n[1] 技能结构验证...")
    passed, errors = validate_skill_structure(skill_path)
    if passed:
        print("   ✓ 通过")
    else:
        for err in errors:
            print(f"   ✗ {err}")
        all_passed = False

    # 2. Frontmatter 验证
    print("\n[2] Frontmatter 验证...")
    passed, errors = validate_frontmatter(skill_path)
    if passed:
        print("   ✓ 通过")
    else:
        for err in errors:
            print(f"   ✗ {err}")
        all_passed = False

    # 3. Meta JSON 验证
    print("\n[3] _meta.json 验证...")
    passed, errors = validate_meta_json(skill_path)
    if passed:
        print("   ✓ 通过")
    else:
        for err in errors:
            print(f"   ✗ {err}")
        all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("✓ 所有验证通过！")
        return 0
    else:
        print("✗ 存在错误，请修复后重试")
        return 1


if __name__ == '__main__':
    sys.exit(main())
