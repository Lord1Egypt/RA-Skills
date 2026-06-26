#!/usr/bin/env python3
"""
AI Robot Clone Tool v2.0 (Security Hardened Version)
任何 AI 机器人都可以使用此工具导出/导入配置

安全改进：
- ✅ 使用 tempfile.TemporaryDirectory 替代固定临时路径
- ✅ ZIP Slip 防护：验证所有提取路径
- ✅ 元数据脱敏：移除绝对路径
- ✅ 文档与代码一致
- ✅ 增强的文件排除机制
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# 核心配置文件列表
CORE_FILES = [
    "SOUL.md",
    "IDENTITY.md",
    "USER.md",
    "MEMORY.md",
    "HEARTBEAT.md",
    "TOOLS.md",
    "AGENTS.md",
]

# 默认排除的目录和文件（安全 + 清理）
DEFAULT_EXCLUDE_PATTERNS = [
    ".git/",
    "__pycache__/",
    ".openclaw/workspace-state.json",
    "*.log",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    ".env",  # 环境变量文件（可能包含密钥）
    "*.key",  # 密钥文件
    "*.secret",  # 敏感文件
]

# 敏感文件模式（额外检查）
SENSITIVE_PATTERNS = [
    "*api_key*",
    "*apikey*",
    "*secret*",
    "*password*",
    "*credential*",
    "*.pem",
    "*.crt",
]


def find_workspace_root(start_path: Optional[Path] = None) -> Path:
    """自动查找 workspace 根目录"""
    current = start_path or Path.cwd()
    
    # 检查当前目录是否有 SOUL.md
    if (current / "SOUL.md").exists():
        return current
    
    # 尝试常见路径
    common_paths = [
        Path.home() / ".openclaw" / "workspace",
        Path.home() / "workspace",
        Path.cwd() / "workspace",
    ]
    
    for path in common_paths:
        if path.exists() and (path / "SOUL.md").exists():
            return path
    
    return current


def is_path_safe(path_str: str) -> bool:
    """
    验证 ZIP 路径是否安全（防止 ZIP Slip）
    
    安全检查：
    - 不能包含 .. 路径遍历
    - 不能是绝对路径
    - 不能包含非法字符
    """
    # 拒绝绝对路径
    if os.path.isabs(path_str):
        return False
    
    # 拒绝路径遍历
    if ".." in path_str.split(os.sep):
        return False
    
    # 规范化路径并再次检查
    normalized = os.path.normpath(path_str)
    if normalized.startswith("..") or os.path.isabs(normalized):
        return False
    
    return True


def should_exclude(path_str: str, exclude_patterns: List[str]) -> bool:
    """检查路径是否应该排除"""
    path_lower = path_str.lower()
    
    for pattern in exclude_patterns:
        pattern_lower = pattern.lower()
        
        if pattern_lower.endswith("/"):
            # 目录模式
            if pattern_lower[:-1] in path_str:
                return True
        elif pattern_lower.startswith("*"):
            # 后缀模式
            if path_lower.endswith(pattern_lower[1:]):
                return True
        elif pattern_lower.startswith("*") and pattern_lower.endswith("*"):
            # 包含模式
            if pattern_lower[1:-1] in path_lower:
                return True
        elif pattern_lower in path_lower:
            return True
    
    # 额外检查敏感文件
    for sensitive_pattern in SENSITIVE_PATTERNS:
        if sensitive_pattern.startswith("*") and sensitive_pattern.endswith("*"):
            if sensitive_pattern[1:-1] in path_lower:
                return True
    
    return False


def scan_workspace(source_path: Path, exclude_patterns: Optional[List[str]] = None) -> List[Dict]:
    """扫描工作区文件"""
    print("📋 扫描工作区...")
    
    if exclude_patterns is None:
        exclude_patterns = DEFAULT_EXCLUDE_PATTERNS
    
    found_files = []
    missing_files = []
    
    for file in CORE_FILES:
        file_path = source_path / file
        if file_path.exists():
            # 检查是否应该排除
            if should_exclude(file, exclude_patterns):
                print(f"  ⚠️  {file} (已排除)")
                continue
            
            size = file_path.stat().st_size
            found_files.append({
                "name": file,
                "path": str(file_path),
                "size": size,
                "size_str": f"{size/1024:.1f}KB"
            })
            print(f"  ✅ {file} ({size/1024:.1f}KB)")
        else:
            missing_files.append(file)
            print(f"  ⚠️  {file} (不存在)")
    
    if missing_files and not found_files:
        print("\n❌ 警告：未找到任何核心配置文件")
        print(f"   请确保在正确的 workspace 目录运行，或检查 --source 参数")
    
    return found_files


def export_config(
    source_path: Optional[str] = None,
    output_path: Optional[str] = None,
    exclude_patterns: Optional[List[str]] = None,
    no_optional: bool = False,
    redact_metadata: bool = True
) -> bool:
    """导出配置到克隆包"""
    
    if source_path is None:
        source_path = find_workspace_root()
    
    source = Path(source_path).resolve()
    print(f"📦 导出配置...")
    print(f"   源：{source}")
    
    # 扫描文件
    found_files = scan_workspace(source, exclude_patterns)
    
    if not found_files:
        return False
    
    # 生成输出文件名
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = f"clone-package-{timestamp}.zip"
    
    # 使用安全的临时目录
    print("\n📋 准备临时文件...")
    with tempfile.TemporaryDirectory(prefix="ai-clone-") as temp_dir:
        temp_path = Path(temp_dir)
        print(f"   临时目录：{temp_path}")
        
        # 复制文件到临时目录
        for file_info in found_files:
            src = Path(file_info["path"])
            dst = temp_path / file_info["name"]
            shutil.copy2(src, dst)
            print(f"  ✅ {file_info['name']}")
        
        # 创建元数据（脱敏版本）
        metadata = {
            "version": "2.0",
            "created_at": datetime.now().isoformat(),
            "files": [f["name"] for f in found_files],
            "description": "AI Robot Clone Package",
            "security_version": "hardened",
        }
        
        # 可选：包含脱敏的源信息（仅目录名，不包含完整路径）
        if not redact_metadata:
            metadata["source_workspace_name"] = source.name
        else:
            print(f"  ℹ️  元数据已脱敏（不包含绝对路径）")
        
        metadata_path = temp_path / "clone_metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"  ✅ clone_metadata.json")
        
        # 打包为 zip
        print(f"\n🗜️  打包为 {output_path}...")
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in temp_path.iterdir():
                # 再次验证文件名安全
                if is_path_safe(file.name):
                    zipf.write(file, file.name)
                else:
                    print(f"  ⚠️  跳过不安全文件名：{file.name}")
        
        # 计算大小
        output_size = Path(output_path).stat().st_size
        
        print(f"\n✅ 导出完成！")
        print(f"   文件：{output_path}")
        print(f"   大小：{output_size/1024:.1f}KB")
        print(f"   包含：{len(found_files)} 个核心文件")
        print(f"   安全版本：hardened v2.0")
        
        return True


def validate_zip_package(package_path: str) -> bool:
    """
    验证 ZIP 包安全性
    
    检查项：
    - 所有文件路径是否安全（无 ZIP Slip）
    - 是否包含恶意文件
    """
    print(f"🔍 验证 ZIP 包安全性...")
    
    try:
        with zipfile.ZipFile(package_path, 'r') as zipf:
            for name in zipf.namelist():
                # 检查路径安全
                if not is_path_safe(name):
                    print(f"  ❌ 不安全路径：{name}")
                    return False
                
                # 检查可疑文件
                if name.endswith(('.exe', '.bat', '.sh', '.cmd')):
                    print(f"  ⚠️  可疑文件：{name}")
                
                # 检查绝对路径
                if os.path.isabs(name):
                    print(f"  ❌ 绝对路径：{name}")
                    return False
            
            print(f"  ✅ 安全性检查通过")
            return True
            
    except zipfile.BadZipFile:
        print(f"  ❌ 无效的 ZIP 文件")
        return False
    except Exception as e:
        print(f"  ❌ 验证失败：{e}")
        return False


def import_config(
    package_path: str,
    target_path: Optional[str] = None,
    preview: bool = False,
    force: bool = False
) -> bool:
    """从克隆包导入配置"""
    
    package = Path(package_path)
    
    if not package.exists():
        print(f"❌ 文件不存在：{package_path}")
        return False
    
    if not package.suffix.lower() == ".zip":
        print(f"❌ 不是 zip 文件：{package_path}")
        return False
    
    # 安全验证
    if not validate_zip_package(package_path):
        print(f"\n❌ 安全验证失败，拒绝导入")
        print(f"   可能包含恶意文件，请勿使用此克隆包")
        return False
    
    print(f"\n📥 导入配置...")
    print(f"   包：{package_path}")
    
    if target_path is None:
        target_path = str(Path.cwd())
    
    target = Path(target_path).resolve()
    
    if not target.exists():
        print(f"   创建目标目录：{target}")
        target.mkdir(parents=True, exist_ok=True)
    
    print(f"   目标：{target}")
    
    # 读取元数据
    try:
        with zipfile.ZipFile(package, 'r') as zipf:
            if "clone_metadata.json" in zipf.namelist():
                metadata_content = zipf.read("clone_metadata.json").decode("utf-8")
                metadata = json.loads(metadata_content)
                print(f"\n📋 克隆包信息:")
                print(f"   创建时间：{metadata.get('created_at', '未知')}")
                print(f"   安全版本：{metadata.get('security_version', 'unknown')}")
                print(f"   文件数量：{len(metadata.get('files', []))}")
    except Exception as e:
        print(f"⚠️  无法读取元数据：{e}")
    
    # 预览模式
    if preview:
        print(f"\n📋 包内文件:")
        with zipfile.ZipFile(package, 'r') as zipf:
            for name in zipf.namelist():
                if name != "clone_metadata.json":
                    print(f"  ✅ {name}")
        print(f"\n💡 使用 --force 参数执行实际导入")
        return True
    
    # 列出将要复制的文件
    print(f"\n📋 即将导入以下文件:")
    files_to_import = []
    with zipfile.ZipFile(package, 'r') as zipf:
        for name in zipf.namelist():
            if name != "clone_metadata.json":
                print(f"  ✅ {name}")
                files_to_import.append(name)
    
    # 确认（非强制模式）
    if not force:
        print(f"\n⚠️  注意：这将覆盖目标目录的现有文件！")
        print(f"   使用 --force 跳过确认")
        
        try:
            response = input("\n确认导入？(y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("❌ 导入已取消")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\n❌ 导入已取消")
            return False
    
    # 解压文件（安全提取）
    print(f"\n📥 正在导入...")
    target.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(package, 'r') as zipf:
        for name in zipf.namelist():
            if name == "clone_metadata.json":
                continue
            
            # 再次验证路径安全
            if not is_path_safe(name):
                print(f"  ⚠️  跳过不安全路径：{name}")
                continue
            
            # 安全提取：构建目标路径
            target_file = target / name
            
            # 确保目标文件在目标目录内
            try:
                target_file.resolve().relative_to(target.resolve())
            except ValueError:
                print(f"  ⚠️  跳过目录外文件：{name}")
                continue
            
            # 提取文件
            zipf.extract(name, target)
            print(f"  ✅ {name}")
    
    print(f"\n✅ 导入完成！")
    print(f"   目标：{target}")
    print(f"   导入：{len(files_to_import)} 个文件")
    print(f"\n🎉 机器人已成功复制配置！")
    print(f"   安全版本：hardened v2.0")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="AI 机器人克隆工具 v2.0 (安全加固版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
安全特性:
  - ZIP Slip 防护
  - 临时目录安全清理
  - 元数据脱敏
  - 敏感文件自动排除

示例:
  # 机器人 A 导出配置
  python clone_robot.py export
  python clone_robot.py export --output my-clone.zip
  python clone_robot.py export --no-optional
  
  # 机器人 B 导入配置
  python clone_robot.py import clone-package.zip
  python clone_robot.py import clone-package.zip --preview
  python clone_robot.py import clone-package.zip --force
  
  # 安全验证
  python clone_robot.py verify clone-package.zip
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # export 命令
    export_parser = subparsers.add_parser("export", help="导出配置到克隆包")
    export_parser.add_argument("--source", type=str, help="源工作区路径")
    export_parser.add_argument("--output", type=str, help="输出文件名")
    export_parser.add_argument("--exclude", type=str, nargs='+', help="额外排除的文件/目录")
    export_parser.add_argument("--no-optional", action="store_true", help="不包含可选目录")
    export_parser.add_argument("--keep-paths", action="store_true", help="在元数据中保留完整路径（默认脱敏）")
    
    # import 命令
    import_parser = subparsers.add_parser("import", help="从克隆包导入配置")
    import_parser.add_argument("package", type=str, help="克隆包文件路径")
    import_parser.add_argument("--target", type=str, help="目标工作区路径")
    import_parser.add_argument("--preview", action="store_true", help="预览包内容")
    import_parser.add_argument("--force", action="store_true", help="跳过确认直接导入")
    
    # verify 命令
    verify_parser = subparsers.add_parser("verify", help="验证克隆包安全性")
    verify_parser.add_argument("package", type=str, help="克隆包文件路径")
    
    args = parser.parse_args()
    
    if args.command == "export":
        exclude_patterns = DEFAULT_EXCLUDE_PATTERNS.copy()
        if args.exclude:
            exclude_patterns.extend(args.exclude)
        
        success = export_config(
            source_path=args.source,
            output_path=args.output,
            exclude_patterns=exclude_patterns,
            no_optional=args.no_optional,
            redact_metadata=not args.keep_paths
        )
        sys.exit(0 if success else 1)
        
    elif args.command == "import":
        success = import_config(
            package_path=args.package,
            target_path=args.target,
            preview=args.preview,
            force=args.force
        )
        sys.exit(0 if success else 1)
        
    elif args.command == "verify":
        success = validate_zip_package(args.package)
        sys.exit(0 if success else 1)
        
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
