#!/usr/bin/env python3
"""
Zeelin Deep Research - 完全异步任务处理器
- 提交任务后立即返回
- 后台进程持续监控
- 自动确认大纲
- 任务完成后通知
"""

import argparse
import json
import os
import sys
import time
import requests
import subprocess
import signal
from datetime import datetime

API_BASE_URL = "https://desearch.zeelin.cn"
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
REPORTS_DIR = os.path.join(SKILL_DIR, "reports")

STATUS_FILE = os.path.join(REPORTS_DIR, "zeelin-research-status.json")
NOTIFIED_FILE = os.path.join(REPORTS_DIR, "zeelin-last-notified.json")
PID_FILE = os.path.join(REPORTS_DIR, "zeelin-research.pid")
LOG_FILE = os.path.join(REPORTS_DIR, "zeelin-research.log")
CONFIG_FILE = os.path.expanduser("~/.openclaw/zeelin-config.json")

STATUS_MAP = {1: "进行中", 2: "已完成"}
CRON_JOB_NAME = "zeelin-check"

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{ts}] {msg}")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def add_cron_job():
    """创建定时任务"""
    try:
        # 先删除可能存在的旧任务
        subprocess.run(["openclaw", "cron", "rm", CRON_JOB_NAME], capture_output=True)
        # 创建新任务：每1分钟检查一次
        result = subprocess.run([
            "openclaw", "cron", "add",
            "--name", CRON_JOB_NAME,
            "--every", "1m",
            "--message", "python3 ~/.openclaw/workspace/skills/zeelin-deep-research/scripts/check_zeelin_complete.py",
            "--timeout-seconds", "60",
            "--channel", "dingtalk",
            "--to", "0211560138072828"
        ], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            log("定时任务已创建")
        else:
            log(f"创建定时任务失败: {result.stderr}")
    except Exception as e:
        log(f"创建定时任务错误: {e}")

def remove_cron_job():
    """删除定时任务"""
    try:
        # 先获取任务ID
        result = subprocess.run(["openclaw", "cron", "list"], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            # 查找zeelin-check任务的ID
            for line in result.stdout.split('\n'):
                if CRON_JOB_NAME in line:
                    parts = line.split()
                    if parts:
                        job_id = parts[0]
                        subprocess.run(["openclaw", "cron", "rm", job_id], capture_output=True, text=True, timeout=30)
                        log("定时任务已删除")
                        return
        log("未找到定时任务")
    except Exception as e:
        log(f"删除定时任务错误: {e}")

def get_api_key():
    """从配置文件读取API Key"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return config.get("api_key")
    return None

def check_status(session_id, api_key):
    url = f"{API_BASE_URL}/api/conversation/status"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    params = {"sessionId": session_id}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    return r.json()

def confirm_outline(session_id, question_id, api_key):
    url = f"{API_BASE_URL}/api/conversation/re_chat"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {"sessionId": session_id, "questionId": str(question_id), "confirmOutline": True}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        return r.json()
    except:
        return {"code": -1}

def get_history(session_id, api_key):
    url = f"{API_BASE_URL}/api/conversation/history"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    params = {"sessionId": session_id, "pageSize": "50", "pageNo": "1"}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    return r.json()

def has_content(history):
    for item in history.get("data", []):
        for ans in item.get("answers", []):
            if ans.get("contentType") == "text" and len(ans.get("content", "")) > 1000:
                return True
    return False

def save_result(session_id, query):
    api_key = get_api_key()
    history = get_history(session_id, api_key)
    safe_q = "".join(c for c in query if c.isalnum() or c in " -_")[:20]
    out_file = f"{REPORTS_DIR}/zeelin_{safe_q}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    md = f"# {query}\n\n> 生成时间: {datetime.now()}\n\n---\n\n"
    for item in history.get("data", []):
        for ans in item.get("answers", []):
            if ans.get("contentType") == "text":
                md += ans.get("content", "") + "\n\n"
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(md)
    return out_file

def save_status(session_id, query, status, progress):
    with open(STATUS_FILE, "w") as f:
        json.dump({
            "session_id": session_id,
            "query": query,
            "status": status,
            "progress": progress,
            "last_check": datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)

def monitor(session_id, question_id, query, interval=30, timeout=3600):
    """后台监控主循环"""
    # 保存PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    
    api_key = get_api_key()
    if not api_key:
        log("错误: 没有API Key")
        return
    
    log(f"开始监控: {session_id}")
    start = time.time()
    outline_confirmed = False
    
    while True:
        # 超时检查
        if time.time() - start > timeout:
            log("超时退出")
            save_status(session_id, query, -1, "超时")
            break
        
        try:
            # 检查状态
            result = check_status(session_id, api_key)
            data = result.get("data", {})
            status = data.get("status", 1)
            msg = data.get("message", "")
            md_url = data.get("mdUrl", "")
            
            # 检查历史内容
            history = get_history(session_id, api_key)
            has_c = has_content(history)
            
            log(f"状态: {status} - {msg}")
            
            # 自动确认大纲
            if not outline_confirmed and status == 1:
                cr = confirm_outline(session_id, question_id, api_key)
                if cr.get("code") == 200:
                    log("大纲已确认")
                    outline_confirmed = True
            
            # 检查完成
            if (md_url and has_c) or (status == 2 and has_c):
                log("任务完成!")
                out_file = save_result(session_id, query)
                log(f"文件: {out_file}")
                # 保存状态
                with open(STATUS_FILE, "w") as f:
                    json.dump({
                        "session_id": session_id,
                        "query": query,
                        "status": 2,
                        "progress": f"完成: {out_file}",
                        "last_check": datetime.now().isoformat()
                    }, f, ensure_ascii=False, indent=2)
                
                # 等待90秒让cron有机会检测并发送通知
                log("等待cron发送通知...")
                time.sleep(90)
                
                # 删除定时任务
                remove_cron_job()
                break
            
            time.sleep(interval)
            
        except Exception as e:
            log(f"错误: {e}")
            time.sleep(5)
    
    # 清理PID
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", "-q")
    p.add_argument("--thinking", "-t", default="deep")
    p.add_argument("--search-range", "-sr", default="web")
    p.add_argument("--monitor", action="store_true")
    p.add_argument("--session-id", "-s")
    p.add_argument("--question-id", "-qid")
    p.add_argument("--interval", "-i", type=int, default=30)
    p.add_argument("--timeout", "-o", type=int, default=3600)
    p.add_argument("--status", action="store_true")
    p.add_argument("--check-key", action="store_true")
    p.add_argument("--set-key")
    args = p.parse_args()
    
    # 设置Key
    if args.set_key:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"api_key": args.set_key}, f)
        print("API Key已保存")
        return
    
    # 检查Key
    if args.check_key:
        key = get_api_key()
        if key:
            print("✅ API Key有效")
        else:
            print("❌ 没有API Key")
        return
    
    # 查状态
    if args.status:
        if os.path.exists(STATUS_FILE):
            print(json.dumps(json.load(open(STATUS_FILE)), indent=2))
        else:
            print("无状态")
        return
    
    # 后台监控
    if args.monitor and args.session_id:
        monitor(args.session_id, args.question_id, args.query, args.interval, args.timeout)
        return
    
    # 提交任务
    if args.query:
        api_key = get_api_key()
        if not api_key:
            print("请先设置API Key: --set-key YOUR_KEY")
            return
        
        # 提交
        url = f"{API_BASE_URL}/api/conversation/anew"
        headers = {"x-api-key": api_key, "Content-Type": "application/json"}
        payload = {"content": args.query, "thinking": args.thinking, "workflow": "", "moreSettings": {"search_range": args.search_range}}
        
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        result = r.json()
        
        if result.get("code") != 200:
            print(f"提交失败: {result.get('msg')}")
            return
        
        data = result.get("data", {})
        session_id = data.get("sessionId")
        question_id = data.get("questionId")
        
        print(f"✅ 任务提交成功!")
        print(f"Session: {session_id}")
        
        # 清除上次通知标记
        if os.path.exists(NOTIFIED_FILE):
            os.remove(NOTIFIED_FILE)
        
        # 创建定时任务监控
        add_cron_job()
        
        # 更新状态文件
        save_status(session_id, args.query, 1, "已提交")
        
        # 启动后台监控 - 使用nohup确保持续运行
        script = os.path.abspath(__file__)
        import subprocess
        subprocess.Popen(
            [sys.executable, script, "--monitor", "-s", session_id, "-qid", str(question_id), "-q", args.query],
            stdout=open("/tmp/zeelin-monitor.log", "a"),
            stderr=open("/tmp/zeelin-monitor.log", "a"),
            start_new_session=True
        )
        
        print("后台监控已启动")
        return
    
    p.print_help()

if __name__ == "__main__":
    main()
