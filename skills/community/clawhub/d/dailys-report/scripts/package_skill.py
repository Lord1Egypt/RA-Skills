#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package skill for ClawHub
打包技能到 ClawHub

Usage:
    python package_skill.py                    # 打包当前技能
    python package_skill.py --validate         # 仅验证不打包
"""

import os
import sys
import json
import argparse
import zipfile
from pathlib import Path
from datetime import datetime

# Windows UTF-8 编码修复
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


def validate_skill(skill_dir):
    """验证技能目录结构"""
    skills_path = Path(skill_dir)
    errors = []
    warnings = []
    
    # 必需文件
    skill_md = skills_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("❌ 缺少必需文件: SKILL.md")
    else:
        # 检查 SKILL.md 内容
        content = skill_md.read_text(encoding='utf-8')
        
        if '---' not in content:
            warnings.append("⚠️ SKILL.md 缺少 YAML frontmatter")
        if 'name:' not in content.lower():
            warnings.append("⚠️ SKILL.md 缺少 name 字段")
        if 'description:' not in content.lower():
            warnings.append("⚠️ SKILL.md 缺少 description 字段")
    
    # 检查目录结构
    scripts_dir = skills_path / "scripts"
    if scripts_dir.exists() and not any(scripts_dir.iterdir()):
        warnings.append("⚠️ scripts 目录为空")
    
    references_dir = skills_path / "references"
    if references_dir.exists() and not any(references_dir.iterdir()):
        warnings.append("⚠️ references 目录为空")
    
    return errors, warnings


def get_skill_info(skill_dir):
    """从 SKILL.md 提取技能信息"""
    skill_md = Path(skill_dir) / "SKILL.md"
    content = skill_md.read_text(encoding='utf-8')
    
    info = {
        "name": "unknown",
        "description": "",
        "version": "1.0.0"
    }
    
    # 简单解析 YAML frontmatter
    if '---' in content:
        parts = content.split('---')
        if len(parts) >= 2:
            frontmatter = parts[1]
            for line in frontmatter.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip().strip('"').strip("'")
                    
                    if key == 'name':
                        info['name'] = value
                    elif key == 'description':
                        info['description'] = value
                    elif key == 'version':
                        info['version'] = value
    
    return info


def package_skill(skill_dir, output_dir=None):
    """打包技能为 zip 文件"""
    skills_path = Path(skill_dir)
    
    # 验证
    errors, warnings = validate_skill(skill_dir)
    
    for w in warnings:
        print(w)
    
    if errors:
        for e in errors:
            print(e)
        return None
    
    # 获取技能信息
    info = get_skill_info(skill_dir)
    skill_name = info['name']
    version = info['version']
    
    # 确定输出路径
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = skills_path.parent
    
    # 创建 zip 文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{skill_name}-v{version}-{timestamp}.zip"
    zip_path = output_path / zip_name
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            # 排除隐藏文件和 __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                arc_name = file_path.relative_to(skills_path.parent)
                zf.write(file_path, arc_name)
    
    return zip_path


def main():
    parser = argparse.ArgumentParser(description='打包技能到 ClawHub')
    parser.add_argument('--validate', action='store_true', help='仅验证不打包')
    parser.add_argument('--output', type=str, default=None, help='输出目录')
    
    args = parser.parse_args()
    
    # 当前技能目录
    skill_dir = Path(__file__).parent.parent
    
    print(f"📂 技能目录: {skill_dir}")
    print()
    
    if args.validate:
        print("🔍 验证模式")
        errors, warnings = validate_skill(skill_dir)
        
        if warnings:
            print("\n⚠️ 警告:")
            for w in warnings:
                print(f"  {w}")
        
        if errors:
            print("\n❌ 错误:")
            for e in errors:
                print(f"  {e}")
            sys.exit(1)
        else:
            print("\n✅ 验证通过")
            sys.exit(0)
    
    # 打包
    print("📦 正在打包...")
    zip_path = package_skill(skill_dir, args.output)
    
    if zip_path:
        print(f"\n✅ 打包完成: {zip_path}")
        print(f"   文件大小: {zip_path.stat().st_size / 1024:.1f} KB")
    else:
        print("\n❌ 打包失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
