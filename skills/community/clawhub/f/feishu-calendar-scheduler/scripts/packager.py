#!/usr/bin/env python3
"""
飞书日历智能调度器 - 技能包打包工具
将技能打包成 ZIP 文件供分发
"""

import os
import sys
import json
import zipfile
import hashlib
from datetime import datetime
import argparse

def get_version():
    """获取版本信息"""
    version_file = os.path.join(os.path.dirname(__file__), "..", "VERSION")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            return f.read().strip()
    return "1.0.0"

def create_zip_package(output_path="feishu-calendar-scheduler.zip"):
    """创建ZIP包"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 需要包含的文件
    include_files = [
        "SKILL.md",
        "README.md", 
        "install.sh",
        "scripts/recommend.py",
        "scripts/simple_test.py",
        "scripts/packager.py",
    ]
    
    # 需要包含的目录
    include_dirs = [
        "scripts"
    ]
    
    print(f"📦 开始打包技能: 飞书日历智能调度器")
    print(f"📁 基础目录: {base_dir}")
    print(f"📄 输出文件: {output_path}")
    
    # 创建ZIP文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加文件
        for file_name in include_files:
            file_path = os.path.join(base_dir, file_name)
            if os.path.exists(file_path):
                arcname = file_name
                zipf.write(file_path, arcname)
                print(f"  ✅ 添加: {file_name}")
            else:
                print(f"  ⚠️  缺失: {file_name}")
        
        # 添加目录
        for dir_name in include_dirs:
            dir_path = os.path.join(base_dir, dir_name)
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.py') or file.endswith('.sh'):
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, base_dir)
                            zipf.write(file_path, arcname)
                            print(f"  ✅ 添加: {arcname}")
        
        # 添加版本信息
        version_info = {
            "name": "飞书日历智能调度器",
            "version": get_version(),
            "build_date": datetime.now().isoformat(),
            "files_count": len(zipf.namelist())
        }
        
        zipf.writestr("version.json", json.dumps(version_info, indent=2, ensure_ascii=False))
    
    # 计算文件哈希
    with open(output_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    # 生成包信息
    package_info = {
        "package_name": os.path.basename(output_path),
        "size_bytes": os.path.getsize(output_path),
        "sha256_hash": file_hash,
        "version": get_version(),
        "build_time": datetime.now().isoformat(),
        "files": include_files + [f"{dir}/" for dir in include_dirs]
    }
    
    print(f"\n✅ 打包完成!")
    print(f"📊 包信息:")
    print(f"   文件: {output_path}")
    print(f"   大小: {package_info['size_bytes']:,} 字节")
    print(f"   版本: {package_info['version']}")
    print(f"   SHA256: {file_hash[:16]}...")
    print(f"   文件数: {version_info['files_count']}")
    
    # 保存包信息
    info_file = output_path.replace('.zip', '.json')
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(package_info, f, indent=2, ensure_ascii=False)
    
    print(f"📝 包信息已保存到: {info_file}")
    
    return package_info

def main():
    parser = argparse.ArgumentParser(description="技能包打包工具")
    parser.add_argument("--output", "-o", default="feishu-calendar-scheduler.zip", 
                       help="输出ZIP文件名")
    parser.add_argument("--list", "-l", action="store_true",
                       help="列出将包含的文件")
    
    args = parser.parse_args()
    
    if args.list:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("将包含的文件:")
        for root, dirs, files in os.walk(base_dir):
            # 跳过隐藏目录和文件
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            
            for file in files:
                if file.endswith(('.py', '.sh', '.md', '.txt', '.json')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, base_dir)
                    print(f"  {rel_path}")
        return
    
    create_zip_package(args.output)

if __name__ == "__main__":
    main()