#!/usr/bin/env python3
"""
Discover Task Scripts - 自动发现任务脚本
从 cron、配置文件、常见目录中收集所有脚本

Usage:
    python3 discover-scripts.py [--output <path>]
"""

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# 配置
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
OPENCLAW_DIR = Path.home() / ".openclaw"
DEFAULT_OUTPUT = WORKSPACE_DIR / "configs" / "scripts-list.json"

# 常见脚本目录
COMMON_SCRIPT_DIRS = [
    Path.home() / "scripts",
    Path.home() / "bin",
    WORKSPACE_DIR / "scripts",
    Path("/opt/scripts"),
]

# 配置文件路径
CONFIG_FILES = [
    WORKSPACE_DIR / "TOOLS.md",
    WORKSPACE_DIR / "MEMORY.md",
    WORKSPACE_DIR / "HEARTBEAT.md",
]


def get_system_crontab_scripts():
    """从系统 crontab 提取脚本路径"""
    scripts = set()
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # 提取 .py 和 .sh 文件路径
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('#'):
                    # 匹配脚本路径
                    matches = re.findall(r'(/[^\s]+\.(py|sh))', line)
                    for match, _ in matches:
                        scripts.add(match)
    except Exception as e:
        print(f"  ⚠️ 读取系统 crontab 失败：{e}")
    return scripts


def get_gateway_cron_scripts():
    """从 Gateway cron 配置提取脚本路径"""
    scripts = set()
    config_file = OPENCLAW_DIR / "openclaw.json"
    if not config_file.exists():
        return scripts
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 提取 cron 配置中的脚本
        cron_tasks = config.get('cron', [])
        for task in cron_tasks:
            payload = task.get('payload', {})
            command = payload.get('command', '')
            if isinstance(command, str):
                matches = re.findall(r'(/[^\s]+\.(py|sh))', command)
                for match, _ in matches:
                    scripts.add(match)
    except Exception as e:
        print(f"  ⚠️ 读取 Gateway cron 配置失败：{e}")
    return scripts


def get_config_file_scripts():
    """从配置文件提取脚本路径"""
    scripts = set()
    for config_file in CONFIG_FILES:
        if not config_file.exists():
            continue
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取 .py 和 .sh 文件路径
            matches = re.findall(r'(/[^\s\`\"]+\.(py|sh))', content)
            for match, _ in matches:
                scripts.add(match)
        except Exception as e:
            print(f"  ⚠️ 读取 {config_file} 失败：{e}")
    return scripts


def scan_common_dirs():
    """扫描常见脚本目录"""
    scripts = set()
    for script_dir in COMMON_SCRIPT_DIRS:
        if not script_dir.exists():
            continue
        
        try:
            for script_file in script_dir.rglob('*'):
                if script_file.is_file() and script_file.suffix in ['.py', '.sh']:
                    scripts.add(str(script_file))
        except Exception as e:
            print(f"  ⚠️ 扫描 {script_dir} 失败：{e}")
    return scripts


def validate_scripts(scripts):
    """验证脚本是否存在"""
    valid_scripts = []
    for script in scripts:
        if os.path.isfile(script):
            valid_scripts.append(script)
        else:
            print(f"  ⚠️ 脚本不存在：{script}")
    return valid_scripts


def collect_script_info(script_path):
    """收集脚本详细信息"""
    info = {
        "path": script_path,
        "exists": os.path.isfile(script_path),
        "executable": os.access(script_path, os.X_OK) if os.path.isfile(script_path) else False,
        "size": os.path.getsize(script_path) if os.path.isfile(script_path) else 0,
        "modified": datetime.fromtimestamp(
            os.path.getmtime(script_path), tz=timezone.utc
        ).isoformat() if os.path.isfile(script_path) else None,
        "dependencies": [],
        "config_files": [],
    }
    
    # 提取脚本中的依赖
    if script_path.endswith('.py'):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取 import
            imports = re.findall(r'^(?:import|from)\s+(\w+)', content, re.MULTILINE)
            info["dependencies"] = list(set(imports))
            
            # 提取配置文件路径
            config_matches = re.findall(r'([\'"]([^\'"]+\.(json|yaml|yml|md))[\'"])', content)
            info["config_files"] = [m[1] for m in config_matches]
        except Exception as e:
            print(f"    ⚠️ 读取脚本失败：{e}")
    
    return info


def main():
    import sys
    
    output = DEFAULT_OUTPUT
    
    # 解析输出路径
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output = Path(sys.argv[i + 1])
    
    print("🔍 Discover Task Scripts")
    print("=" * 50)
    print()
    
    # 收集脚本
    print("📋 Collecting scripts from:")
    
    print("  1. System crontab...")
    crontab_scripts = get_system_crontab_scripts()
    print(f"     Found: {len(crontab_scripts)} scripts")
    
    print("  2. Gateway cron config...")
    gateway_scripts = get_gateway_cron_scripts()
    print(f"     Found: {len(gateway_scripts)} scripts")
    
    print("  3. Config files (TOOLS.md, etc)...")
    config_scripts = get_config_file_scripts()
    print(f"     Found: {len(config_scripts)} scripts")
    
    print("  4. Common directories...")
    dir_scripts = scan_common_dirs()
    print(f"     Found: {len(dir_scripts)} scripts")
    
    # 合并去重
    all_scripts = crontab_scripts | gateway_scripts | config_scripts | dir_scripts
    print()
    print(f"✅ Total unique scripts: {len(all_scripts)}")
    print()
    
    # 验证脚本
    print("✓ Validating scripts...")
    valid_scripts = validate_scripts(all_scripts)
    print(f"  Valid: {len(valid_scripts)}/{len(all_scripts)}")
    print()
    
    # 收集详细信息
    print("📝 Collecting script details...")
    script_details = []
    for script in sorted(valid_scripts):
        info = collect_script_info(script)
        script_details.append(info)
        print(f"  ✓ {script}")
    
    # 生成输出
    output_data = {
        "_meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "version": "1.0",
            "description": "Discovered task scripts for backup"
        },
        "summary": {
            "total_found": len(all_scripts),
            "total_valid": len(valid_scripts),
            "sources": {
                "crontab": len(crontab_scripts),
                "gateway_cron": len(gateway_scripts),
                "config_files": len(config_scripts),
                "common_dirs": len(dir_scripts)
            }
        },
        "scripts": script_details
    }
    
    # 确保输出目录存在
    output.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 50)
    print(f"✅ Script list saved to: {output.name}")
    print()
    
    # 生成备份清单
    print("📦 Next steps:")
    print("  1. Review scripts-list.json")
    print("  2. Run one-click-backup.sh (will include these scripts)")
    print("  3. Use restore-scripts.sh to restore after recovery")
    print()


if __name__ == "__main__":
    main()
