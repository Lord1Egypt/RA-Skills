#!/usr/bin/env python3
"""
检查项目目录结构是否符合 agent-project-structure 规范
"""

import os
import sys
from pathlib import Path


def check_structure(project_path):
    """检查项目目录结构"""
    project_path = Path(project_path)
    
    required_dirs = [
        'projects',
        'log',
        'temp',
        'config',
        'data',
        'scripts',
        'docs'
    ]
    
    issues = []
    
    # 检查必需目录是否存在
    for dir_name in required_dirs:
        dir_path = project_path / dir_name
        if not dir_path.exists():
            issues.append(f"缺失目录: {dir_name}/")
        elif not dir_path.is_dir():
            issues.append(f"不是目录: {dir_name}/")
    
    # 检查 temp 目录的子目录
    temp_dir = project_path / 'temp'
    if temp_dir.exists() and temp_dir.is_dir():
        temp_subdirs = ['screenshots', 'cache']
        for subdir in temp_subdirs:
            subdir_path = temp_dir / subdir
            if not subdir_path.exists():
                issues.append(f"temp/ 缺少子目录: {subdir}/")
    
    return issues


def main():
    if len(sys.argv) < 2:
        print("用法: python check_structure.py <项目路径>")
        print("示例: python check_structure.py /home/user/my-project")
        sys.exit(1)
    
    project_path = Path(sys.argv[1])
    
    if not project_path.exists():
        print(f"错误: 路径不存在: {project_path}")
        sys.exit(1)
    
    issues = check_structure(project_path)
    
    if issues:
        print(f"发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("✓ 目录结构符合规范")
        sys.exit(0)


if __name__ == '__main__':
    main()
