#!/usr/bin/env python3
"""
Chat History - 主脚本 (v3.0)
支持多种命令和触发关键词

v3.0 更新：
- 移除所有系统命令（os.popen, os.system）
- 使用 OpenClaw cron 替代系统 crontab
- 完全跨平台兼容（macOS/Windows/Linux）
- 归档时间改为 23:59
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime, timedelta

# 配置（自动检测路径）
OPENCLAW_DIR = os.path.expanduser(os.environ.get("OPENCLAW_DIR", "~/.openclaw"))
WORKSPACE_DIR = os.path.expanduser(os.environ.get("OPENCLAW_WORKSPACE", os.path.join(OPENCLAW_DIR, "workspace")))
ARCHIVE_DIR = os.path.join(WORKSPACE_DIR, "conversation-archives")
CHANNEL_DIR = os.path.join(ARCHIVE_DIR, "channel-side")
WEBUI_DIR = os.path.join(ARCHIVE_DIR, "webui-side")
SEARCH_INDEX = os.path.join(ARCHIVE_DIR, "search-index.json")
EVALUATIONS_INDEX = os.path.join(ARCHIVE_DIR, "evaluations-index.json")
STATUS_FILE = os.path.join(ARCHIVE_DIR, "status.json")
LOG_FILE = os.path.join(ARCHIVE_DIR, "chat-archive.log")

def ensure_directories():
    """确保所有目录存在"""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    os.makedirs(CHANNEL_DIR, exist_ok=True)
    os.makedirs(WEBUI_DIR, exist_ok=True)

def load_status():
    """加载状态"""
    if not os.path.exists(STATUS_FILE):
        return {
            "enabled": False,
            "first_run": True,
            "last_archive": None,
            "archive_time": "23:59",
            "total_sessions": 0,
            "total_files": 0,
            "channels": []
        }
    with open(STATUS_FILE, "r") as f:
        return json.load(f)

def save_status(status):
    """保存状态"""
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

def log_message(message):
    """写入日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

def check_cron_setup():
    """检查 OpenClaw 定时任务是否已设置"""
    try:
        result = subprocess.run(
            ["openclaw", "cron", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "chat-history" in result.stdout
    except Exception as e:
        log_message(f"检查cron失败: {e}")
        return False

def setup_cron():
    """设置 OpenClaw 定时任务"""
    try:
        skill_dir = os.path.dirname(os.path.abspath(__file__))
        main_py_path = os.path.join(skill_dir, "main_v3.py")
        
        if check_cron_setup():
            return True, "定时任务已存在"
        
        result = subprocess.run(
            [
                "openclaw", "cron", "add",
                "--name", "chat-history-archive",
                "--cron", "59 23 * * *",
                "--system-event", f"Chat History: 请运行 python3 {main_py_path} --archive",
                "--session", "main"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            log_message("成功设置 OpenClaw cron 任务")
            return True, "success"
        else:
            log_message(f"设置 cron 失败: {result.stderr}")
            return False, f"设置失败: {result.stderr}"
            
    except Exception as e:
        log_message(f"设置 cron 异常: {e}")
        return False, str(e)

def remove_cron():
    """移除 OpenClaw 定时任务"""
    try:
        result = subprocess.run(
            ["openclaw", "cron", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        for line in result.stdout.split("\n"):
            if "chat-history" in line:
                parts = line.split()
                if parts:
                    task_id = parts[0]
                    subprocess.run(
                        ["openclaw", "cron", "remove", task_id],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    log_message(f"已移除 cron 任务: {task_id}")
        
        return True
        
    except Exception as e:
        log_message(f"移除 cron 失败: {e}")
        return False

def set_archive_time(new_time):
    """设置自动归档时间"""
    if not re.match(r"^\d{2}:\d{2}$", new_time):
        return False, "时间格式错误，请使用 HH:MM 格式（例如：23:59）"
    
    hour, minute = map(int, new_time.split(":"))
    
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return False, "时间超出范围，小时必须为 0-23，分钟必须为 0-59"
    
    remove_cron()
    
    try:
        skill_dir = os.path.dirname(os.path.abspath(__file__))
        main_py_path = os.path.join(skill_dir, "main_v3.py")
        
        result = subprocess.run(
            [
                "openclaw", "cron", "add",
                "--name", "chat-history-archive",
                "--cron", f"{minute} {hour} * * *",
                "--system-event", f"Chat History: 请运行 python3 {main_py_path} --archive",
                "--session", "main"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            status = load_status()
            status["archive_time"] = new_time
            save_status(status)
            log_message(f"归档时间已更新为 {new_time}")
            return True, f"归档时间已设置为 {new_time}"
        else:
            return False, f"设置失败: {result.stderr}"
            
    except Exception as e:
        return False, str(e)

# 保持原有的其他功能（评估、搜索、归档等）
# 这里省略了所有其他函数，实际文件中应该保留...
# 包括: initialize_evaluations_index, add_evaluation, list_evaluations, etc.

def show_help():
    """显示帮助信息"""
    help_text = """
📚 Chat History v3.0 指令列表

基础命令：
• --help / -h - 显示帮助
• --archive - 执行归档
• --status - 查看归档状态
• --start - 启动自动归档（23:59）
• --stop - 停止自动归档
• --timing - 查看或设置归档时间
• --keyword - 列出触发关键词

v3.0 更新：
• 使用 OpenClaw cron（跨平台）
• 归档时间改为 23:59
• 无需系统权限
"""
    return help_text

def main():
    """主函数"""
    ensure_directories()
    status = load_status()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command in ["--help", "-h"]:
            print(show_help())
            return

        elif command == "--archive":
            print("📦 开始归档...")
            
            # 导入归档模块
            skill_dir = os.path.dirname(os.path.abspath(__file__))
            archive_module_path = os.path.join(skill_dir, "archive_from_jsonl.py")
            
            import importlib.util
            spec = importlib.util.spec_from_file_location("archive_from_jsonl", archive_module_path)
            archive_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(archive_module)
            
            count = archive_module.archive_all_sessions()
            
            status["last_archive"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status["total_sessions"] = status.get("total_sessions", 0) + count
            save_status(status)
            
            log_message(f"归档完成: {count} 条消息")
            print(f"✅ 归档完成: {count} 条消息")
            return

        elif command == "--status":
            enabled = "✅ 已启用" if status.get('enabled', False) else "❌ 已禁用"
            archive_time = status.get('archive_time', '23:59')
            print(f"📊 归档状态")
            print(f"自动归档: {enabled}")
            print(f"定时任务: 每天 {archive_time}")
            print(f"使用 OpenClaw cron 跨平台支持 ✅")
            return

        elif command == "--start":
            print("🎉 Chat History v3.0 启动")
            print("使用 OpenClaw cron（无系统依赖）")
            
            if check_cron_setup():
                print("⚠️ 定时任务已存在")
                return
            
            result, message = setup_cron()
            if result:
                status["enabled"] = True
                status["first_run"] = False
                save_status(status)
                print("✅ 已设置定时任务（每天 23:59）")
                print(f"✅ 自动归档已启动\n")
                log_message("启动自动归档")
            else:
                print(f"❌ 设置失败: {message}\n")
            return

        elif command == "--stop":
            print("⏹️ 停止自动归档...")
            result = remove_cron()
            if result:
                status["enabled"] = False
                save_status(status)
                print("✅ 已停止自动归档\n")
                log_message("停止自动归档")
            else:
                print("❌ 停止失败\n")
            return

        elif command == "--timing":
            if len(sys.argv) < 3:
                print(f"当前归档时间: {status.get('archive_time', '23:59')}")
                print("用法: --timing <时间> 例如: --timing 23:59")
                return
            
            new_time = sys.argv[2]
            result, message = set_archive_time(new_time)
            print(message)
            return

        elif command == "--keyword":
            print("🔑 触发关键词:")
            print("• 我想不起来了 • 查记录 • 搜索聊天")
            print("• chat history • conversation log • find chat")
            return

    print(show_help())

if __name__ == "__main__":
    main()
