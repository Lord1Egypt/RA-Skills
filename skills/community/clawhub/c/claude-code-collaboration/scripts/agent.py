#!/usr/bin/env python3
"""
Claude Code Interface Agent - OpenClaw 与 Claude Code 之间的桥梁
监控输入队列，调用 Claude Code 执行任务，结果写入输出队列
增强版：包含对话日志
"""

import os
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

WORK_DIR = "/Volumes/256G/mywork"
IN_DIR = f"{WORK_DIR}/.oc-cc-in"
OUT_DIR = f"{WORK_DIR}/.oc-cc-out"
LOG_FILE = f"{WORK_DIR}/.oc-cc-chat.log"
STATUS_FILE = f"{WORK_DIR}/.oc-cc-status.json"

def log(message: str):
    """写入对话日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line)
    print(line.strip())

def update_status(status: str, last_task: str = None):
    """更新状态文件"""
    data = {
        "status": status,
        "last_task": last_task,
        "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    }
    with open(STATUS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def process_task(task_file: Path):
    """处理单个任务"""
    task_id = task_file.stem
    
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            task = json.load(f)
        
        prompt = task.get("prompt", "")
        if not prompt:
            raise ValueError("任务中没有 prompt 字段")
        
        log(f"📤 OPENCLAW → CLAUDE CODE [任务: {task_id}]")
        log(f"    提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        
        update_status("processing", task_id)
        
        # 调用 Claude Code 执行任务
        # 复制当前环境并添加 Claude Code 所需的环境变量
        env = os.environ.copy()
        env["ANTHROPIC_AUTH_TOKEN"] = "sk-sp-5cec1d99ac9f4848b2dc625406bea113"
        env["ANTHROPIC_BASE_URL"] = "https://coding.dashscope.aliyuncs.com/apps/anthropic"
        env["ANTHROPIC_MODEL"] = "qwen3.5-plus"
        env["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = "qwen3.5-plus"
        env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = "qwen3.5-plus"
        env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = "qwen3.5-plus"
        env["ANTHROPIC_REASONING_MODEL"] = "qwen3.5-plus"
        env["API_TIMEOUT_MS"] = "3000000"
        env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"

        result = subprocess.run(
            ["claude", "--print", "--no-session-persistence",
             "--dangerously-skip-permissions", prompt],
            cwd=WORK_DIR,
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )
        
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        # 写入结果
        output = {
            "task_id": task_id,
            "status": "completed" if result.returncode == 0 else "failed",
            "prompt": prompt,
            "stdout": stdout,
            "stderr": stderr,
            "returncode": result.returncode,
            "completed_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        }
        
        out_file = Path(OUT_DIR) / f"{task_id}.json"
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        # 从输入队列删除
        task_file.unlink()
        
        log(f"📥 CLAUDE CODE → OPENCLAW [任务: {task_id}]")
        if stdout:
            log(f"    输出: {stdout[:200]}{'...' if len(stdout) > 200 else ''}")
        if stderr:
            log(f"    错误: {stderr[:200]}{'...' if len(stderr) > 200 else ''}")
        log(f"    状态: {'✅ 完成' if result.returncode == 0 else '❌ 失败'} (返回码: {result.returncode})")
        
        update_status("idle")
        
    except Exception as e:
        log(f"❌ 任务失败 [{task_id}]: {str(e)}")
        update_status("error", task_id)

def main():
    """主循环"""
    print(f"Claude Code Interface Agent 启动")
    print(f"监控目录: {IN_DIR}")
    print(f"对话日志: {LOG_FILE}")
    
    # 初始化目录
    Path(IN_DIR).mkdir(parents=True, exist_ok=True)
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    
    log("=" * 60)
    log("🤖 Claude Code Interface Agent 启动")
    log("=" * 60)
    
    update_status("idle")
    
    while True:
        # 检查输入队列
        for task_file in Path(IN_DIR).glob("*.json"):
            process_task(task_file)
        
        time.sleep(2)  # 每 2 秒检查一次

if __name__ == "__main__":
    main()
