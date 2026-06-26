#!/usr/bin/env python3
"""
AI Coding Tools Full Suite - Skill Validation Script
验证AI编程工具全能套件技能包
"""

import os
import json
import re

# 配置
SKILL_DIR = "/workspace/temp-skills/ai-coding-tools-full-suite"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def check(name, condition, error_msg=""):
    """检查条件并打印结果"""
    if condition:
        print(f"  {Colors.GREEN}✓{Colors.RESET} {name}")
        return True
    else:
        print(f"  {Colors.RED}✗{Colors.RESET} {name}")
        if error_msg:
            print(f"    {Colors.YELLOW}→{Colors.RESET} {error_msg}")
        return False

def validate_frontmatter():
    """验证Frontmatter格式"""
    print(f"\n{Colors.BLUE}[1] 验证Frontmatter格式{Colors.RESET}")

    skill_path = os.path.join(SKILL_DIR, "SKILL.md")
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否以---开头
    has_start = content.startswith('---')
    check("SKILL.md以---开头", has_start, "Frontmatter必须以---开头")

    # 提取frontmatter
    if has_start:
        parts = content[2:].split('---', 1)
        if len(parts) > 1:
            frontmatter = parts[0].strip()
            lines = frontmatter.split('\n')

            # 检查必需字段
            has_name = bool(re.search(r'^name:\s*', frontmatter, re.MULTILINE))
            has_desc = bool(re.search(r'^description:\s*', frontmatter, re.MULTILINE))

            check("包含name字段", has_name, "Frontmatter必须包含name字段")
            check("包含description字段", has_desc, "Frontmatter必须包含description字段")

            # 提取name值
            name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if name_match:
                name_value = name_match.group(1).strip()
                check("name值有效", len(name_value) > 0, "name不能为空")

                # 检查name格式
                is_hyphen = re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name_value)
                check("name格式正确(连字符)", is_hyphen or len(name_value.split()) == 1, "name应使用连字符格式")

            # 检查description长度
            desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
            if desc_match:
                desc_value = desc_match.group(1).strip()
                check("description有内容", len(desc_value) > 10, "description至少需要10个字符")

            return has_name and has_desc

    return False

def validate_meta():
    """验证_meta.json"""
    print(f"\n{Colors.BLUE}[2] 验证_meta.json{Colors.RESET}")

    meta_path = os.path.join(SKILL_DIR, "_meta.json")

    if not os.path.exists(meta_path):
        print(f"  {Colors.RED}✗{Colors.RESET} _meta.json不存在")
        return False

    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)

        # 检查必需字段
        has_id = 'skill-id' in meta
        has_name = 'name' in meta
        has_version = 'version' in meta

        check("_meta.json包含skill-id", has_id, "必须包含skill-id字段")
        check("_meta.json包含name", has_name, "必须包含name字段")
        check("_meta.json包含version", has_version, "必须包含version字段")

        # 验证name一致性
        if has_name:
            skill_path = os.path.join(SKILL_DIR, "SKILL.md")
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()

            name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
            if name_match:
                frontmatter_name = name_match.group(1).strip()
                meta_name = meta['name']
                check("name与SKILL.md一致", frontmatter_name == meta_name,
                      f"SKILL.md: {frontmatter_name}, _meta.json: {meta_name}")

        return has_id and has_name and has_version

    except json.JSONDecodeError as e:
        print(f"  {Colors.RED}✗{Colors.RESET} JSON格式错误: {e}")
        return False

def validate_references():
    """验证参考文档"""
    print(f"\n{Colors.BLUE}[3] 验证参考文档{Colors.RESET}")

    refs_dir = os.path.join(SKILL_DIR, "references")

    if not os.path.exists(refs_dir):
        print(f"  {Colors.YELLOW}⚠{Colors.RESET} references目录不存在")
        return True

    ref_files = [f for f in os.listdir(refs_dir) if f.endswith('.md')]
    check("参考文档存在", len(ref_files) > 0, "references目录为空")

    # 检查参考文档命名
    for ref in ref_files:
        is_numbered = re.match(r'^\d+-', ref)
        check(f"参考文档命名规范: {ref}", is_numbered, "应使用数字前缀命名")

    return True

def validate_structure():
    """验证目录结构"""
    print(f"\n{Colors.BLUE}[4] 验证目录结构{Colors.RESET}")

    required_files = ["SKILL.md", "_meta.json"]
    for file in required_files:
        path = os.path.join(SKILL_DIR, file)
        check(f"文件存在: {file}", os.path.exists(path))

    # 检查目录
    dirs = ["references", "scripts"]
    for dir_name in dirs:
        path = os.path.join(SKILL_DIR, dir_name)
        check(f"目录存在: {dir_name}", os.path.exists(path))

    return True

def validate_content():
    """验证内容完整性"""
    print(f"\n{Colors.BLUE}[5] 验证内容完整性{Colors.RESET}")

    skill_path = os.path.join(SKILL_DIR, "SKILL.md")
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查关键内容
    checks = [
        ("包含调度指令", "智能调度" in content or "dispatch" in content.lower()),
        ("包含路由规则", "路由" in content or "route" in content.lower()),
        ("包含子技能索引", "子技能" in content or "sub-skill" in content.lower()),
        ("包含快捷指令", "/ai-tools" in content or "指令" in content),
    ]

    for name, condition in checks:
        check(name, condition)

    return all(c[1] for c in checks)

def validate_meta_content():
    """验证_meta.json内容完整性"""
    print(f"\n{Colors.BLUE}[6] 验证元数据内容{Colors.RESET}")

    meta_path = os.path.join(SKILL_DIR, "_meta.json")
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    # 检查扩展字段
    checks = [
        ("包含tags", "tags" in meta and len(meta.get("tags", [])) > 0),
        ("包含sub-skills", "sub-skills" in meta and len(meta.get("sub-skills", [])) > 0),
        ("包含commands", "commands" in meta and len(meta.get("commands", [])) > 0),
    ]

    for name, condition in checks:
        check(name, condition)

    return all(c[1] for c in checks)

def main():
    """主验证流程"""
    print(f"\n{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BLUE}AI Coding Tools Full Suite - 技能验证{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"技能目录: {SKILL_DIR}")

    results = []

    # 执行各项验证
    results.append(validate_frontmatter())
    results.append(validate_meta())
    results.append(validate_references())
    results.append(validate_structure())
    results.append(validate_content())
    results.append(validate_meta_content())

    # 汇总结果
    print(f"\n{Colors.BLUE}{'='*50}{Colors.RESET}")

    passed = sum(results)
    total = len(results)

    if all(results):
        print(f"{Colors.GREEN}✅ 验证通过! ({passed}/{total} 项检查通过){Colors.RESET}")
        return 0
    else:
        print(f"{Colors.YELLOW}⚠ 部分检查未通过 ({passed}/{total} 项检查通过){Colors.RESET}")
        return 1

if __name__ == "__main__":
    exit(main())
