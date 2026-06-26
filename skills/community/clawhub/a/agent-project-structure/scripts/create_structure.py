#!/usr/bin/env python3
"""
创建符合 agent-project-structure 规范的目录结构
"""

import os
import sys
from pathlib import Path


def create_structure(project_path):
    """创建标准目录结构"""
    project_path = Path(project_path)
    
    # 创建主目录
    main_dirs = [
        'projects',
        'log',
        'temp',
        'config',
        'data',
        'scripts',
        'docs'
    ]
    
    # 创建子目录
    sub_dirs = {
        'temp': ['screenshots', 'cache'],
        'projects': [],
        'data': ['input', 'output'],
        'config': [],
        'scripts': [],
        'docs': [],
        'log': []
    }
    
    # 创建主目录
    for dir_name in main_dirs:
        dir_path = project_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {dir_name}/")
    
    # 创建子目录
    for parent, children in sub_dirs.items():
        for child in children:
            dir_path = project_path / parent / child
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {parent}/{child}/")
    
    # 创建示例文件
    example_files = {
        'config/settings.json': '{}',
        'config/.gitkeep': '',
        'data/input/.gitkeep': '',
        'data/output/.gitkeep': '',
        'log/.gitkeep': '',
        'projects/.gitkeep': '',
        'scripts/.gitkeep': '',
        'docs/.gitkeep': '',
        'temp/.gitkeep': '',
        'temp/screenshots/.gitkeep': '',
        'temp/cache/.gitkeep': ''
    }
    
    for file_path, content in example_files.items():
        full_path = project_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"创建文件: {file_path}")
    
    print(f"\n✓ 已创建标准目录结构: {project_path}")


def main():
    if len(sys.argv) < 2:
        print("用法: python create_structure.py <项目路径>")
        print("示例: python create_structure.py /home/user/my-project")
        sys.exit(1)
    
    project_path = Path(sys.argv[1])
    
    # 检查路径是否已存在
    if project_path.exists():
        print(f"警告: 路径已存在: {project_path}")
        response = input("是否继续? (y/N): ")
        if response.lower() != 'y':
            print("已取消")
            sys.exit(0)
    
    create_structure(project_path)


if __name__ == '__main__':
    main()
