#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package.py - Skill打包脚本
将Skill目录打包为 .skill 文件
"""

import zipfile
import os
import sys

def package_skill(skill_dir, output_path):
    """
    打包Skill
    
    Args:
        skill_dir: Skill目录路径
        output_path: 输出文件路径 (.skill)
    """
    print(f"开始打包 Skill: {skill_dir}")
    print(f"输出文件: {output_path}")
    
    # 创建ZIP文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历Skill目录
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # 计算相对路径
                arcname = os.path.relpath(file_path, skill_dir)
                
                print(f"  添加: {arcname}")
                zipf.write(file_path, arcname)
    
    print(f"✓ Skill打包完成: {output_path}")
    print(f"  文件大小: {os.path.getsize(output_path)} 字节")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python package.py <skill_dir> <output.skill>")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_path = sys.argv[2]
    
    package_skill(skill_dir, output_path)
