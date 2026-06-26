#!/usr/bin/env python3
"""
技能打包脚本
将技能文件夹打包为 .skill 文件
"""

import os
import sys
import zipfile
import json
from pathlib import Path
from datetime import datetime


def get_package_name(skill_path: str) -> str:
    """生成打包文件名"""
    skill_path = Path(skill_path)
    meta_path = skill_path / '_meta.json'

    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        version = meta.get('version', '1.0.0')
        name = skill_path.name
        return f"{name}_v{version}_{datetime.now().strftime('%Y%m%d%H%M%S')}.skill"

    return f"{skill_path.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.skill"


def is_safe_path(path: str, base_path: str) -> bool:
    """检查路径安全性，防止符号链接逃逸"""
    real_path = Path(path).resolve()
    real_base = Path(base_path).resolve()
    return str(real_path).startswith(str(real_base))


def package_skill(skill_path: str, output_dir: str = None) -> str:
    """打包技能"""
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        raise FileNotFoundError(f"技能路径不存在: {skill_path}")

    # 确定输出目录
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = skill_path.parent

    # 生成输出文件名
    package_name = get_package_name(skill_path)
    output_file = output_path / package_name

    # 打包
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            # 排除隐藏目录和临时文件
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            files = [f for f in files if not f.startswith('.') and not f.endswith('.pyc')]

            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path)

                # 安全检查
                if not is_safe_path(file_path, skill_path):
                    print(f"跳过不安全的路径: {file_path}")
                    continue

                zf.write(file_path, arcname)

    return str(output_file)


def main():
    if len(sys.argv) < 2:
        print("用法: python package_skill.py <skill_path> [output_dir]")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"正在打包技能: {skill_path}")

    try:
        output_file = package_skill(skill_path, output_dir)
        print(f"✓ 打包完成: {output_file}")
    except Exception as e:
        print(f"✗ 打包失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
