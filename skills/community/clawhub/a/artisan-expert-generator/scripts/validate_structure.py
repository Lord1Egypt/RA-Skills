#!/usr/bin/env python3
"""
Skill结构验证脚本
验证生成Skill的结构完整性和规范性
"""

import argparse
import json
import re
import sys
from pathlib import Path


def validate_yaml_frontmatter(content):
    """验证YAML前言区"""
    issues = []
    required_fields = ['name', 'description']

    # 检查是否有YAML分隔符
    if not content.startswith('---'):
        issues.append("缺少YAML前言区起始标记'---'")
        return issues

    # 提取YAML内容
    yaml_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        issues.append("缺少YAML前言区结束标记'---'")
        return issues

    yaml_content = yaml_match.group(1)

    # 检查必需字段
    for field in required_fields:
        if field not in yaml_content:
            issues.append(f"YAML前言区缺少必需字段: {field}")

    # 检查name格式
    name_match = re.search(r'name:\s*(.+)', yaml_content)
    if name_match:
        name_value = name_match.group(1).strip()
        if name_value.endswith('-skill'):
            issues.append("name不应包含'-skill'后缀")

    # 检查description格式
    desc_match = re.search(r'description:\s*(.+)', yaml_content)
    if desc_match:
        desc_value = desc_match.group(1).strip().strip('"\'')
        if '\n' in desc_value:
            issues.append("description应为一行，不应包含换行符")
        # 中文字符按1个字符计算
        desc_len = len(desc_value)
        if desc_len < 100 or desc_len > 150:
            issues.append(f"description长度应为100-150字符，当前为{desc_len}字符")

    return issues


def validate_required_sections(content):
    """验证必需章节"""
    issues = []
    required_sections = [
        '## 任务目标',
        '## 操作步骤',
        '## 使用示例'
    ]

    for section in required_sections:
        if section not in content:
            issues.append(f"缺少必需章节: {section}")

    return issues


def validate_skill_directory(skill_path):
    """验证Skill目录结构"""
    issues = []
    skill_dir = Path(skill_path)

    if not skill_dir.exists():
        return [f"目录不存在: {skill_path}"]

    # 检查SKILL.md
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        issues.append("缺少SKILL.md文件")
    else:
        content = skill_md.read_text(encoding='utf-8')

        # 验证YAML前言区
        yaml_issues = validate_yaml_frontmatter(content)
        issues.extend([f"YAML前言区: {issue}" for issue in yaml_issues])

        # 验证必需章节
        section_issues = validate_required_sections(content)
        issues.extend([f"章节结构: {issue}" for issue in section_issues])

        # 检查正文长度
        yaml_match = re.search(r'---\n.*?\n---', content, re.DOTALL)
        if yaml_match:
            body_content = content[yaml_match.end():]
            body_lines = len(body_content.split('\n'))
            if body_lines > 500:
                issues.append(f"正文过长，应控制在500行以内，当前为{body_lines}行")

    # 检查目录结构规范性
    for item in skill_dir.iterdir():
        if item.is_dir():
            dir_name = item.name
            if dir_name not in ['scripts', 'references', 'assets']:
                issues.append(f"包含非标准目录: {dir_name}")
            # 检查空目录
            if not any(item.iterdir()):
                issues.append(f"存在空目录: {dir_name}")

    # 检查README.md等临时文件
    temp_files = ['README.md', '.DS_Store', '__pycache__']
    for temp_file in temp_files:
        if (skill_dir / temp_file).exists():
            issues.append(f"应移除临时文件: {temp_file}")

    return issues


def generate_suggestions(issues):
    """生成优化建议"""
    suggestions = []

    for issue in issues:
        if 'YAML前言区' in issue:
            suggestions.append("请确保YAML前言区包含name和description字段，且格式正确")
        elif '缺少必需章节' in issue:
            suggestions.append("请补充缺失的章节，确保Skill结构完整")
        elif '正文过长' in issue:
            suggestions.append("建议将详细内容移至references/目录，保持SKILL.md简洁")
        elif '临时文件' in issue:
            suggestions.append("请打包前删除所有临时文件和测试数据")
        elif '非标准目录' in issue:
            suggestions.append("仅保留scripts/、references/、assets/三个标准目录")

    if not suggestions:
        suggestions.append("Skill结构符合规范，可以进行打包")

    return suggestions


def main():
    parser = argparse.ArgumentParser(description='验证Skill结构完整性')
    parser.add_argument('--skill_path', required=True, help='Skill目录路径')

    args = parser.parse_args()

    try:
        # 验证目录结构
        issues = validate_skill_directory(args.skill_path)

        # 生成建议
        suggestions = generate_suggestions(issues)

        result = {
            "status": "pass" if not issues else "fail",
            "skill_path": str(Path(args.skill_path).absolute()),
            "validation_result": "通过" if not issues else "失败",
            "issues": issues,
            "suggestions": suggestions,
            "issue_count": len(issues)
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

        if issues:
            sys.exit(1)

    except Exception as e:
        result = {
            "status": "error",
            "message": str(e)
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
