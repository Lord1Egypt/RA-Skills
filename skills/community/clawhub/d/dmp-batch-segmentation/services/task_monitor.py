#!/usr/bin/env python3
"""
DMP 任务监控服务
功能：后台定期检查任务状态，完成后发送通知

使用方式：
    作为 systemd 服务运行，或手动启动：
    python3 task_monitor.py

配置：
    通过 monitor_config.json 管理待监控的任务列表
"""

import json
import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# 配置文件路径
CONFIG_FILE = Path(__file__).parent / "monitor_config.json"
LOG_FILE = Path(__file__).parent / "monitor.log"

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + "\n")

def load_config():
    """加载待监控的任务列表"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"tasks": [], "notifications": []}

def save_config(config):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def find_auth_skill_path():
    """查找鉴权技能的API脚本路径"""
    possible_paths = [
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    return None

def query_task_status(audience_ids):
    """查询任务状态"""
    auth_path = find_auth_skill_path()
    if not auth_path:
        return {"error": "找不到鉴权技能"}
    
    try:
        import subprocess
        
        # 使用 subprocess 调用 API，避免模块导入冲突
        request_body = json.dumps({"audienceIds": audience_ids})
        
        # 重试机制
        max_retries = 3
        for attempt in range(max_retries):
            result = subprocess.run(
                ["python3", str(auth_path), "POST", "/audience/manage/taskList", request_body],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                try:
                    response = json.loads(result.stdout)
                    # 检查是否是鉴权错误
                    if response.get("code") == "1001" or "AUTH_FAILED" in result.stdout:
                        if attempt < max_retries - 1:
                            time.sleep(1)  # 等待1秒后重试
                            continue
                    return response
                except json.JSONDecodeError:
                    pass
            
            # 如果有错误输出，记录日志
            if result.stderr:
                log(f"API调用错误 (尝试 {attempt + 1}/{max_retries}): {result.stderr}")
            
            if attempt < max_retries - 1:
                time.sleep(1)  # 等待1秒后重试
        
        # 所有重试都失败
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except:
                return {"error": f"API调用失败: {result.stdout}"}
        return {"error": f"API调用失败: {result.stderr}"}
    except Exception as e:
        return {"error": str(e)}

def send_notification(message, task_info=None):
    """发送通知（使用通用通知模块）"""
    # 1. 记录到配置文件
    config = load_config()
    notification = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
        "task_info": task_info,
        "read": False
    }
    config["notifications"].append(notification)
    save_config(config)
    log(f"📢 通知已记录: {message}")
    
    # 2. 使用通用通知模块发送
    try:
        notify_script = Path(__file__).parent / "notify.py"
        if notify_script.exists():
            result = subprocess.run(
                ["python3", str(notify_script), "test", message],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                log(f"📢 通知已发送: {result.stdout.strip()}")
            else:
                log(f"⚠️ 通知发送失败: {result.stderr}")
        else:
            log(f"⚠️ 通知模块不存在: {notify_script}")
    except Exception as e:
        log(f"⚠️ 通知发送异常: {e}")

def check_tasks():
    """检查所有待监控的任务"""
    config = load_config()
    
    if not config.get("tasks"):
        return
    
    # 筛选正在监控的任务
    monitoring_tasks = [t for t in config["tasks"] if t.get("status") == "monitoring"]
    
    if not monitoring_tasks:
        return
    
    # 批量查询任务状态
    audience_ids = [t["task_id"] for t in monitoring_tasks]
    result = query_task_status(audience_ids)
    
    if "error" in result:
        log(f"❌ 查询失败: {result['error']}")
        return
    
    if result.get("code") == "0" and "data" in result:
        tasks = result["data"]
        
        for task_data in tasks:
            task_id = task_data.get("audienceId")
            status = task_data.get("audienceStatus")
            name = task_data.get("audienceName", "未知")
            amount = task_data.get("audienceAmount", "未知")
            
            # 状态: 0=失败, 1=成功, 2=等待中, 3=计算中
            status_map = {0: "failed", 1: "success", 2: "waiting", 3: "computing"}
            new_status = status_map.get(status, "unknown")
            
            # 找到对应的任务
            for task in monitoring_tasks:
                if task["task_id"] == task_id:
                    old_status = task.get("api_status")
                    
                    if old_status != new_status:
                        task["api_status"] = new_status
                        log(f"📊 任务 {task_id} ({name}) 状态变更: {old_status} -> {new_status}")
                        
                        if new_status == "success":
                            task["status"] = "completed"
                            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            task["audience_amount"] = amount
                            
                            send_notification(
                                f"✅ 任务完成！任务ID: {task_id}, 名称: {name}, 人群规模: {amount}",
                                task_info=task
                            )
                            
                        elif new_status == "failed":
                            task["status"] = "failed"
                            task["failed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            send_notification(
                                f"❌ 任务失败！任务ID: {task_id}, 名称: {name}",
                                task_info=task
                            )
                    
                    break
    
    save_config(config)

def add_task(task_id, task_name, project_id=None):
    """添加待监控的任务"""
    config = load_config()
    
    # 检查是否已存在
    for task in config["tasks"]:
        if task["task_id"] == task_id:
            log(f"⚠️ 任务 {task_id} 已存在")
            return
    
    task = {
        "task_id": task_id,
        "task_name": task_name,
        "project_id": project_id,
        "status": "monitoring",
        "api_status": "unknown",
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    config["tasks"].append(task)
    save_config(config)
    log(f"✅ 添加监控任务: {task_id} ({task_name})")

def remove_task(task_id):
    """移除监控任务"""
    config = load_config()
    config["tasks"] = [t for t in config["tasks"] if t["task_id"] != task_id]
    save_config(config)
    log(f"✅ 移除监控任务: {task_id}")

def get_notifications():
    """获取未读通知"""
    config = load_config()
    unread = [n for n in config.get("notifications", []) if not n.get("read")]
    return unread

def mark_notifications_read():
    """标记所有通知为已读"""
    config = load_config()
    for notification in config.get("notifications", []):
        notification["read"] = True
    save_config(config)

def main():
    """主函数"""
    log("=" * 50)
    log("🚀 DMP 任务监控服务启动")
    log("=" * 50)
    
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "add" and len(sys.argv) >= 4:
            task_id = int(sys.argv[2])
            task_name = sys.argv[3]
            project_id = sys.argv[4] if len(sys.argv) > 4 else None
            add_task(task_id, task_name, project_id)
            return
        
        elif action == "remove" and len(sys.argv) >= 3:
            task_id = int(sys.argv[2])
            remove_task(task_id)
            return
        
        elif action == "status":
            config = load_config()
            print(json.dumps(config, indent=2, ensure_ascii=False))
            return
        
        elif action == "notifications":
            notifications = get_notifications()
            if notifications:
                for n in notifications:
                    print(f"[{n['timestamp']}] {n['message']}")
                mark_notifications_read()
            else:
                print("没有未读通知")
            return
    
    # 启动定时任务
    try:
        while True:
            check_tasks()
            time.sleep(60)  # 每60秒检查一次
    except KeyboardInterrupt:
        log("🛑 服务停止")
    except Exception as e:
        log(f"❌ 服务异常: {e}")
        raise

if __name__ == "__main__":
    main()
