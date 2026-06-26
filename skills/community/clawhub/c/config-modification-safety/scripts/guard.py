#!/usr/bin/env python3
"""
Config Guard — 第一层守护核心
原理：监听配置文件变更，校验 JSON 语法，错误则立即回滚
由 launchd WatchPaths 触发（每次配置文件写入都会运行）
"""
import json
import shutil
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

BACKUP_DIR = Path.home() / ".openclaw" / "config-backups"
WORK_DIR = Path.home() / ".openclaw" / "workspace" / ".lib" / "config-safety"
LOG_FILE = WORK_DIR / "guard.log"

# 要监控的配置文件
CONFIG_FILE = Path.home() / ".openclaw" / "workspace" / "config" / "agent.json"
MAIN_CONFIG = Path.home() / ".openclaw" / "config.json"


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def create_backup():
    """创建配置快照"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = None
    
    if CONFIG_FILE.exists():
        backup_path = BACKUP_DIR / f"agent-{ts}.json"
        shutil.copy2(CONFIG_FILE, backup_path)
        log(f"备份已创建: {backup_path.name}")
    
    if MAIN_CONFIG.exists():
        main_backup = BACKUP_DIR / f"main-{ts}.json"
        shutil.copy2(MAIN_CONFIG, main_backup)
        log(f"主配置已备份: {main_backup.name}")
    
    # 最多保留 10 个备份
    backups = sorted(BACKUP_DIR.glob("agent-*.json"))
    for old in backups[:-10]:
        old.unlink()
        log(f"清理旧备份: {old.name}")
    
    return backup_path


def restore_latest():
    """恢复到最后一次正常配置"""
    backups = sorted(BACKUP_DIR.glob("agent-*.json"))
    if not backups:
        log("没有找到备份文件！")
        return False
    
    latest = backups[-1]
    log(f"恢复到: {latest.name}")
    shutil.copy2(latest, CONFIG_FILE)
    
    # 尝试恢复主配置
    main_backups = sorted(BACKUP_DIR.glob("main-*.json"))
    if main_backups:
        shutil.copy2(main_backups[-1], MAIN_CONFIG)
        log(f"主配置已恢复: {main_backups[-1].name}")
    
    return True


def validate_json(path):
    """验证 JSON 语法"""
    try:
        with open(path) as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        log(f"JSON 语法错误: {e}")
        return False


def restart_gateway():
    """重启 Gateway"""
    log("重启 Gateway...")
    result = subprocess.run(
        ["openclaw", "gateway", "restart"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        log("Gateway 重启成功 ✅")
    else:
        log(f"Gateway 重启失败: {result.stderr}")


def rollback():
    """执行回滚"""
    log("=== 开始回滚 ===")
    if restore_latest():
        restart_gateway()
        log("回滚完成 ✅")
    else:
        log("回滚失败 ❌")


def check_and_guard():
    """检查配置并执行守卫逻辑（由 launchd 触发）"""
    log("--- 收到配置变更通知 ---")
    
    if not CONFIG_FILE.exists():
        log("配置文件不存在，跳过")
        return
    
    # 短暂延迟确保文件写入完成
    import time
    time.sleep(0.2)
    
    # 校验 JSON
    if validate_json(CONFIG_FILE):
        log("配置校验通过 ✅")
        create_backup()  # 每次成功修改都备份
    else:
        log("检测到 JSON 语法错误！触发回滚...")
        rollback()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    
    if cmd == "rollback":
        rollback()
    elif cmd == "backup":
        path = create_backup()
        if path:
            print(f"备份已创建: {path}")
        else:
            print("没有配置可以备份")
    elif cmd == "check":
        check_and_guard()
    else:
        print(f"未知命令: {cmd}")
        print("用法: guard.py [rollback|backup|check]")
