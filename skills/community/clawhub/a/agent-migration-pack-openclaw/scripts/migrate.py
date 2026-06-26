#!/usr/bin/env python3
"""
Agent 迁移包管理脚本
v1.0.4

功能：
- python migrate.py validate    # 校验所有JSON格式
- python migrate.py checksum   # 计算SHA256校验码
- python migrate.py pack       # 打包成ZIP
- python migrate.py bootstrap  # 初始化迁移包结构

依赖：标准库（hashlib, zipfile, json, os, pathlib）
"""

import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime


def get_project_root():
    """获取项目根目录（脚本所在目录的父目录）"""
    return Path(__file__).parent.parent


def validate_json_files(root_dir=None):
    """校验所有JSON文件格式"""
    if root_dir is None:
        root_dir = get_project_root()
    
    json_files = list(root_dir.glob("**/*.json"))
    # 排除 node_modules, .git 等目录
    json_files = [f for f in json_files if not any(
        part.startswith('.') or part == 'node_modules' 
        for part in f.parts
    )]
    
    print(f"\n{'='*50}")
    print("🔍 JSON 格式校验")
    print(f"{'='*50}")
    
    errors = []
    valid_count = 0
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"✅ {json_file.relative_to(root_dir)}")
            valid_count += 1
        except json.JSONDecodeError as e:
            print(f"❌ {json_file.relative_to(root_dir)}: {e}")
            errors.append((json_file, str(e)))
        except Exception as e:
            print(f"⚠️ {json_file.relative_to(root_dir)}: {e}")
            errors.append((json_file, str(e)))
    
    print(f"\n📊 校验结果: {valid_count}/{len(json_files)} 个文件通过")
    
    if errors:
        print(f"\n❌ 发现 {len(errors)} 个错误:")
        for path, error in errors:
            print(f"  - {path}: {error}")
        return False
    
    print("✅ 所有JSON文件格式正确!")
    return True


def calculate_checksum(file_path=None, root_dir=None):
    """计算SHA256校验码"""
    if file_path:
        # 计算单个文件
        return calculate_file_checksum(file_path)
    
    if root_dir is None:
        root_dir = get_project_root()
    
    print(f"\n{'='*50}")
    print("🔐 SHA256 校验码计算")
    print(f"{'='*50}")
    
    # 查找ZIP文件
    zip_files = list(root_dir.glob("*.zip"))
    
    if not zip_files:
        print("⚠️ 未找到ZIP文件，请先执行 pack 命令")
        return None
    
    # 使用最新的ZIP文件
    latest_zip = max(zip_files, key=lambda p: p.stat().st_mtime)
    checksum = calculate_file_checksum(latest_zip)
    
    print(f"\n📦 文件: {latest_zip.name}")
    print(f"🔑 SHA256: {checksum}")
    
    return checksum


def calculate_file_checksum(file_path):
    """计算单个文件的SHA256校验码"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def pack_zip(output_name=None, root_dir=None):
    """打包成ZIP"""
    if root_dir is None:
        root_dir = get_project_root()
    
    print(f"\n{'='*50}")
    print("📦 打包迁移包")
    print(f"{'='*50}")
    
    if output_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"agent-migration-pack_{timestamp}.zip"
    
    output_path = root_dir / output_name
    
    # 定义要打包的目录和文件
    include_patterns = [
        "README.md",
        "MIGRATION-GUIDE.md",
        "manifest.toml",
        "TEMPLATE/",
        "EXAMPLES/",
        "scripts/"
    ]
    
    # 排除 generate-pack.py（如果存在但不在templates中）
    exclude_files = []
    
    print(f"\n📁 源目录: {root_dir}")
    print(f"📦 输出文件: {output_name}")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pattern in include_patterns:
            full_path = root_dir / pattern
            if full_path.exists():
                if full_path.is_file():
                    arcname = full_path.name
                    zipf.write(full_path, arcname)
                    print(f"  + {arcname}")
                else:
                    for file_path in full_path.rglob("*"):
                        if file_path.is_file():
                            arcname = str(file_path.relative_to(root_dir))
                            # 检查是否在排除列表中
                            if file_path.name not in exclude_files:
                                zipf.write(file_path, arcname)
                                print(f"  + {arcname}")
            else:
                print(f"  ⚠️ 跳过: {pattern} (不存在)")
    
    # 计算校验码
    checksum = calculate_file_checksum(output_path)
    
    print(f"\n✅ 打包完成!")
    print(f"📦 文件: {output_path.name}")
    print(f"🔑 SHA256: {checksum}")
    print(f"📏 大小: {output_path.stat().st_size / 1024:.2f} KB")
    
    return str(output_path), checksum


def bootstrap(structure_type="full"):
    """初始化迁移包结构"""
    root_dir = get_project_root()
    
    print(f"\n{'='*50}")
    print("🚀 Bootstrap 初始化迁移包结构")
    print(f"{'='*50}")
    
    # 创建必要目录
    dirs = [
        root_dir / "TEMPLATE",
        root_dir / "EXAMPLES" / "my-agent",
        root_dir / "scripts"
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"📁 创建目录: {d.relative_to(root_dir)}")
    
    # 检查必要文件
    required_files = [
        "README.md",
        "MIGRATION-GUIDE.md",
        "manifest.toml",
        "TEMPLATE/identity.template.json"
    ]
    
    print("\n📋 必要文件检查:")
    all_exist = True
    for f in required_files:
        path = root_dir / f
        if path.exists():
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} (缺失)")
            all_exist = False
    
    if all_exist:
        print("\n✅ 迁移包结构完整!")
    else:
        print("\n⚠️ 部分必要文件缺失，请检查模板包完整性")
    
    return all_exist


def show_help():
    """显示帮助信息"""
    print("""
╔══════════════════════════════════════════════════════════╗
║           Agent 迁移包管理脚本 v1.0.4                    ║
╚══════════════════════════════════════════════════════════╝

用法: python migrate.py <command>

命令:
  validate    校验所有JSON文件格式是否正确
  checksum    计算SHA256校验码（需要先pack）
  pack        打包成ZIP文件
  bootstrap   初始化/检查迁移包结构

示例:
  python migrate.py validate    # 检查JSON格式
  python migrate.py pack        # 打包迁移包
  python migrate.py checksum    # 计算校验码
  python migrate.py bootstrap   # 检查结构完整性

提示:
  - validate 会在 pack 之前自动运行
  - pack 会自动计算 SHA256 校验码
  - bootstrap 用于快速检查包结构完整性
""")


def main():
    """主入口"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    commands = {
        'validate': validate_json_files,
        'checksum': lambda: calculate_checksum(),
        'pack': lambda: pack_zip(),
        'bootstrap': bootstrap
    }
    
    if command in commands:
        result = commands[command]()
        if result is False:
            sys.exit(1)
    else:
        print(f"❌ 未知命令: {command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
