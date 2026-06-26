#!/usr/bin/env python3
"""
Claude Code 远程执行器 — 三通道 + 重试机制

支持三种通道（按优先级）:
  1. fastapi  — 远程 FastAPI，HTTP POST/GET，最稳定
  2. redis    — Redis Worker，监听 Redis 队列
  3. screen   — SSH Screen 模式，fallback

重试机制:
  - 每个通道失败最多3次
  - 失败后等待 5~7秒（随机）再试
  - 三通道全失败 → 报错

⚠️ 首次使用前：修改顶部配置区的 IP 和路径
"""

import requests
import redis
import json
import uuid
import time
import random
import sys
import argparse
import subprocess
from typing import Optional

# ========== 配置（修改这里） ==========
# 远程机器的 IP 或域名
REMOTE_HOST = "192.168.0.128"      # 👈 改成你的远程机器 IP
REMOTE_API_PORT = 18900            # FastAPI 端口

# Redis 配置（队列服务地址）
REDIS_HOST = "192.168.0.107"       # 👈 改成你的 Redis 地址
REDIS_PORT = 11980                 # Redis 端口

# SSH 配置
SSH_HOST = f"m1-meng@{REMOTE_HOST}"  # 👈 改成你的 SSH 用户名
SSH_KEY = "~/.ssh/id_rsa"

# 远程机器上的项目路径
PROJECT_DIR = "/Users/m1-meng/workspace/soulwriter-api"  # 👈 改成你的项目路径
CLAUDE_BIN = "/Users/m1-meng/.npm-global/bin/claude"      # Claude Code 路径

# ========== 常量（一般不改） ==========
QUEUE = "claude_tasks"
RESULT_PREFIX = "claude_result:"
STATUS_PREFIX = "claude_status:"
LOG_FILE = "/tmp/cc_exec.log"

MAX_RETRIES = 3
RETRY_WAIT_MIN = 5
RETRY_WAIT_MAX = 7
TASK_TIMEOUT = 300

# ========== 日志 ==========
def log(msg, level="INFO"):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

# ========== 通道1: FastAPI ==========
class FastAPIChannel:
    name = "fastapi"
    priority = 1
    
    def __init__(self):
        self.base_url = f"http://{REMOTE_HOST}:{REMOTE_API_PORT}"
    
    def health(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=5)
            return r.status_code == 200
        except Exception:
            return False
    
    def submit(self, task_id: str, prompt: str) -> bool:
        try:
            r = requests.post(f"{self.base_url}/task",
                json={"prompt": prompt, "task_id": task_id},
                timeout=10)
            return r.status_code == 200
        except Exception:
            return False
    
    def result(self, task_id: str) -> Optional[dict]:
        try:
            r = requests.get(f"{self.base_url}/result/{task_id}", timeout=5)
            if r.status_code == 200:
                return r.json()
            return None
        except Exception:
            return None
    
    def status(self, task_id: str) -> str:
        try:
            r = requests.get(f"{self.base_url}/status/{task_id}", timeout=5)
            if r.status_code == 200:
                return r.json().get("status", "unknown")
        except Exception:
            pass
        return "unknown"


# ========== 通道2: Redis ==========
class RedisChannel:
    name = "redis"
    priority = 2
    
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    
    def health(self) -> bool:
        try:
            return self.r.ping()
        except Exception:
            return False
    
    def submit(self, task_id: str, prompt: str) -> bool:
        try:
            task = {
                "task_id": task_id,
                "prompt": prompt,
                "exec_mode": "claude"
            }
            self.r.lpush(QUEUE, json.dumps(task))
            return True
        except Exception:
            return False
    
    def result(self, task_id: str) -> Optional[dict]:
        try:
            data = self.r.get(f"{RESULT_PREFIX}{task_id}")
            if data:
                return json.loads(data)
            return None
        except Exception:
            return None
    
    def status(self, task_id: str) -> str:
        try:
            return self.r.get(f"{STATUS_PREFIX}{task_id}") or "unknown"
        except Exception:
            return "unknown"


# ========== 通道3: SSH Screen ==========
class ScreenChannel:
    name = "screen"
    priority = 3
    
    def health(self) -> bool:
        try:
            r = subprocess.run(
                ["ssh", "-o", "ServerAliveInterval=10", "-o", "StrictHostKeyChecking=no",
                 SSH_HOST, "screen -ls"],
                capture_output=True, timeout=10)
            return r.returncode == 0
        except Exception:
            return False
    
    def submit(self, task_id: str, prompt: str) -> bool:
        try:
            escaped_prompt = prompt.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
            screen_name = f"cc_{task_id[:8]}"
            
            ssh_cmd = (
                f"ssh -o ServerAliveInterval=30 -o StrictHostKeyChecking=no {SSH_HOST} "
                f"'screen -dmS {screen_name} /bin/zsh -c \"{escaped_prompt}\"'"
            )
            r = subprocess.run(ssh_cmd, shell=True, capture_output=True, timeout=15)
            return r.returncode == 0
        except Exception:
            return False
    
    def result(self, task_id: str) -> Optional[dict]:
        try:
            r = subprocess.run(
                ["ssh", "-o", "ServerAliveInterval=10", SSH_HOST,
                 f"cat /tmp/cc_result_{task_id}.json 2>/dev/null || echo NOT_FOUND"],
                capture_output=True, text=True, timeout=10)
            out = r.stdout.strip()
            if out and out != "NOT_FOUND":
                return json.loads(out)
        except Exception:
            pass
        return None
    
    def status(self, task_id: str) -> str:
        try:
            r = subprocess.run(
                ["ssh", "-o", "ServerAliveInterval=10", SSH_HOST,
                 f"grep -q 'END:{task_id}' /tmp/cc_screen.log && echo done || echo running"],
                capture_output=True, text=True, timeout=10)
            return "done" if "done" in r.stdout else "running"
        except Exception:
            return "unknown"


# ========== 执行器 ==========
CHANNELS = [FastAPIChannel(), RedisChannel(), ScreenChannel()]

def wait_with_jitter():
    t = random.uniform(RETRY_WAIT_MIN, RETRY_WAIT_MAX)
    time.sleep(t)

def exec_with_retry(prompt: str, task_id: str = None, timeout: int = TASK_TIMEOUT) -> dict:
    task_id = task_id or str(uuid.uuid4())[:8]
    start = time.time()
    last_error = ""
    
    for channel in sorted(CHANNELS, key=lambda c: c.priority):
        attempts = 0
        
        while attempts < MAX_RETRIES:
            attempts += 1
            log(f"[{channel.name}] attempt {attempts}/{MAX_RETRIES}")
            
            if not channel.health():
                log(f"[{channel.name}] health check failed")
                last_error = f"{channel.name} health check failed"
                if attempts < MAX_RETRIES:
                    wait_with_jitter()
                continue
            
            if not channel.submit(task_id, prompt):
                log(f"[{channel.name}] submit failed")
                last_error = f"{channel.name} submit failed"
                if attempts < MAX_RETRIES:
                    wait_with_jitter()
                continue
            
            log(f"[{channel.name}] task {task_id} submitted, waiting result...")
            
            while time.time() - start < timeout:
                result = channel.result(task_id)
                if result:
                    result["channel"] = channel.name
                    log(f"[{channel.name}] success!")
                    return result
                
                status = channel.status(task_id)
                time.sleep(3 if status != "unknown" else 2)
                
                if time.time() - start >= timeout:
                    last_error = f"{channel.name} timeout"
                    break
            
            if time.time() - start >= timeout:
                last_error = f"{channel.name} timeout after {timeout}s"
                break
            
            last_error = f"{channel.name} no result"
            if attempts < MAX_RETRIES:
                wait_with_jitter()
        
        log(f"[{channel.name}] all attempts failed, trying next channel...")
    
    return {
        "task_id": task_id,
        "status": "all_channels_failed",
        "error": last_error,
        "output": ""
    }


def main():
    parser = argparse.ArgumentParser(description="Claude Code 远程执行器")
    parser.add_argument("prompt", help="要执行的指令")
    parser.add_argument("--task-id", help="指定任务ID")
    parser.add_argument("--timeout", type=int, default=TASK_TIMEOUT)
    parser.add_argument("--channel", choices=["fastapi", "redis", "screen"],
                        help="强制使用指定通道")
    args = parser.parse_args()
    
    if args.channel:
        global CHANNELS
        if args.channel == "fastapi":
            CHANNELS = [FastAPIChannel()]
        elif args.channel == "redis":
            CHANNELS = [RedisChannel()]
        elif args.channel == "screen":
            CHANNELS = [ScreenChannel()]
    
    result = exec_with_retry(args.prompt, args.task_id, args.timeout)
    
    print(f"\n{'='*50}")
    print(f"Task: {result['task_id']}")
    print(f"Status: {result['status']}")
    print(f"Channel: {result.get('channel', 'N/A')}")
    if result.get("output"):
        print(f"\nOutput:\n{result['output'][:2000]}")
    if result.get("error"):
        print(f"\nError:\n{result['error'][:500]}")
    
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
