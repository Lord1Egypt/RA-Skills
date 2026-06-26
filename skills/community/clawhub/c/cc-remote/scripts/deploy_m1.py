#!/usr/bin/env python3
"""
M1 Claude Code 通道部署脚本

⚠️ 首次使用前：修改以下配置
  - REMOTE_HOST: 远程机器 IP
  - REDIS_HOST: Redis 服务器 IP
  - REDIS_PORT: Redis 端口
  - SSH_HOST: SSH 登录用户
"""

import subprocess
import sys
import time
import os

# ===== 修改这里 =====
REMOTE_HOST = "192.168.0.128"     # 👈 远程机器 IP
REDIS_HOST = "192.168.0.107"     # 👈 Redis 服务器 IP
REDIS_PORT = 11980                # Redis 端口
SSH_HOST = f"m1-meng@{REMOTE_HOST}"  # 👈 SSH 用户名
# ====================

HOST = SSH_HOST

def ssh(cmd, timeout=30):
    r = subprocess.run(
        ["ssh", "-o", "ServerAliveInterval=10", HOST, f"source ~/.zshrc && {cmd}"],
        capture_output=True, text=True, timeout=timeout
    )
    return r.returncode, r.stdout, r.stderr

def scp(local, remote):
    r = subprocess.run(["scp", "-o", "ServerAliveInterval=10", local, f"{HOST}:{remote}"],
                       capture_output=True, timeout=30)
    return r.returncode

def main():
    print("=== Claude Code 通道部署 ===\n")
    
    # 1. 安装依赖
    print("1. 检查/安装 Python 依赖...")
    code, out, err = ssh("python3 -c 'import redis, uvicorn, fastapi; print(OK)' 2>&1")
    if code != 0 or "OK" not in out:
        print("   安装 redis, uvicorn, fastapi...")
        ssh("pip3 install redis uvicorn fastapi --quiet 2>&1 | tail -2")
        print("   ✅ 依赖安装完成")
    else:
        print("   ✅ 依赖已满足")
    
    # 2. 生成并上传 Worker
    print("\n2. 生成 cc_worker.py...")
    worker_code = f'''#!/usr/bin/env python3
"""Claude Code Worker - 后台执行器"""
import redis, json, subprocess, time, os

REDIS_HOST = "{REDIS_HOST}"
REDIS_PORT = {REDIS_PORT}
QUEUE = "claude_tasks"
RESULT_PREFIX = "claude_result:"
STATUS_PREFIX = "claude_status:"
CLAUDE = "/Users/m1-meng/.npm-global/bin/claude"
PROJECT = "/Users/m1-meng/workspace/soulwriter-api"

def log(msg):
    print(f"[{{time.strftime('%H:%M:%S')}}] {{msg}}", flush=True)

def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.ping()
    log(f"Worker: Redis connected, listening on {{QUEUE}}")
    
    while True:
        try:
            result = r.blpop(QUEUE, timeout=5)
            if not result:
                continue
            
            _, data = result
            task = json.loads(data)
            task_id = task["task_id"]
            prompt = task["prompt"]
            
            log(f"Processing [{{task_id}}]: {{prompt[:40]}}...")
            r.setex(f"{{STATUS_PREFIX}}{{task_id}}", 300, "running")
            
            try:
                proc = subprocess.run(
                    [CLAUDE, "--print", "--permission-mode", "bypassPermissions", "--no-session-persistence"],
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd=PROJECT,
                    env={{**os.environ, "HOME": "/Users/m1-meng", "PATH": os.environ.get("PATH","") + ":/Users/m1-meng/.npm-global/bin"}}
                )
                output, error, status = proc.stdout, proc.stderr, "success" if proc.returncode == 0 else "error"
            except subprocess.TimeoutExpired:
                output, error, status = "", "TIMEOUT", "timeout"
            except Exception as e:
                output, error, status = "", str(e), "error"
            
            result_data = {{
                "task_id": task_id, "status": status,
                "output": output[:5000], "error": error[:1000] if error else "",
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }}
            r.setex(f"{{RESULT_PREFIX}}{{task_id}}", 3600, json.dumps(result_data))
            r.setex(f"{{STATUS_PREFIX}}{{task_id}}", 3600, status)
            log(f"Done [{{task_id}}]: {{status}}")
            
        except redis.ConnectionError:
            log("Redis disconnected, reconnecting...")
            time.sleep(2)
            try:
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
                r.ping()
            except:
                pass
        except Exception as e:
            log(f"Error: {{e}}")
            time.sleep(1)

if __name__ == "__main__":
    main()
'''
    
    with open("/tmp/cc_worker_m1.py", "w") as f:
        f.write(worker_code)
    
    code = scp("/tmp/cc_worker_m1.py", "/Users/m1-meng/workspace/cc_worker.py")
    if code == 0:
        print("   ✅ cc_worker.py 上传成功")
    else:
        print(f"   ❌ 上传失败")
        return 1
    
    # 3. 生成并上传 API
    print("\n3. 生成 cc_api.py...")
    api_code = f'''#!/usr/bin/env python3
"""Claude Code API Server"""
import redis, json, uuid
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

REDIS_HOST = "{REDIS_HOST}"
REDIS_PORT = {REDIS_PORT}
QUEUE = "claude_tasks"
RESULT_PREFIX = "claude_result:"
STATUS_PREFIX = "claude_status:"
PORT = 18900

app = FastAPI()
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class TaskRequest(BaseModel):
    prompt: str
    task_id: Optional[str] = None
    exec_mode: Optional[str] = "claude"

@app.post("/task")
async def submit_task(req: TaskRequest):
    task_id = req.task_id or str(uuid.uuid4())[:8]
    r.lpush(QUEUE, json.dumps({{"task_id": task_id, "prompt": req.prompt, "exec_mode": req.exec_mode or "claude"}}))
    return {{"task_id": task_id, "status": "queued"}}

@app.get("/result/{{task_id}}")
async def get_result(task_id: str):
    result = r.get(f"{{RESULT_PREFIX}}{{task_id}}")
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return json.loads(result)

@app.get("/status/{{task_id}}")
async def get_status(task_id: str):
    return {{"status": r.get(f"{{STATUS_PREFIX}}{{task_id}}") or "not_found"}}

@app.get("/health")
async def health():
    return {{"status": "ok", "queue_len": r.llen(QUEUE)}}

uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
'''
    
    with open("/tmp/cc_api_m1.py", "w") as f:
        f.write(api_code)
    
    code = scp("/tmp/cc_api_m1.py", "/Users/m1-meng/workspace/cc_api.py")
    if code == 0:
        print("   ✅ cc_api.py 上传成功")
    else:
        print(f"   ❌ 上传失败")
        return 1
    
    # 4. 重启进程
    print("\n4. 重启 Worker...")
    ssh("pkill -f cc_worker 2>/dev/null; sleep 1; nohup python3 /Users/m1-meng/workspace/cc_worker.py > /tmp/cc_worker.log 2>&1 & echo Worker PID: $!")
    print("   ✅ Worker 重启")
    
    print("\n5. 重启 API...")
    ssh("pkill -f cc_api 2>/dev/null; sleep 1; nohup python3 /Users/m1-meng/workspace/cc_api.py > /tmp/cc_api.log 2>&1 & echo API PID: $!")
    time.sleep(2)
    print("   ✅ API 重启")
    
    # 5. 验证
    print("\n6. 健康检查...")
    code, out, err = ssh("curl -s http://localhost:18900/health")
    if code == 0 and "ok" in out:
        print(f"   ✅ API 健康: {out}")
    else:
        print(f"   ⚠️ API 未就绪")
    
    code, out, err = ssh("cat /tmp/cc_worker.log | tail -1")
    print(f"   Worker: {out.strip() if out else 'check log'}")
    
    print("\n✅ 部署完成！")
    return 0

if __name__ == "__main__":
    sys.exit(main())
