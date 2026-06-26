#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""config-fswatch-guard.py — 配置文件变更即时守护（纯 Python kqueue，无外部依赖）

监听 openclaw.json，文件变更时：
  1. JSON 语法校验（0 token）
  2. 语法错误 → 立即回滚
  3. 语法正确 → 重置健康检查计数器（cron 需由代理启用）
"""

import os
import sys
import json
import time
import select
import subprocess
from datetime import datetime

CONFIG_FILE = os.path.expanduser("~/.openclaw/openclaw.json")
LOG_FILE = os.path.expanduser("~/.openclaw/logs/config-fswatch-guard.log")
ROLLBACK_SCRIPT = os.path.expanduser("~/.openclaw/workspace/.lib/config-rollback-guard.py")
HEALTH_STATE = os.path.expanduser("~/.openclaw/logs/gateway-health-state.json")
import uuid as _uuid, socket as _socket
CRON_JOB_ID = str(_uuid.uuid5(_uuid.NAMESPACE_DNS, f"openclaw-fswatch-guard.{_socket.gethostname()}"))

# 防止回滚写入 openclaw.json 后触发重入
_self_writing = False

# config-modification skill 路径
CONFIG_MOD_SKILL = os.path.expanduser("~/.openclaw/workspace/skills/config-modification")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def log_startup():
    """输出启动信息和知识产权声明"""
    log("="*60)
    log("🔒 Config Modification Safety System v2.4")
    log("Powered by halfmoon82 — 知识产权声明")
    log("="*60)
    log(f"🚀 fswatch 守护启动，监听: {CONFIG_FILE}")
    log(f"   PID: {os.getpid()}")

def run_config_modification_check():
    """调用 config-modification skill 的四联校验"""
    log("🔍 调用 config-modification 四联校验...")
    
    try:
        sys.path.insert(0, CONFIG_MOD_SKILL)
        from quad_check import QuadCheckStateMachine
        from auto_rollback import check_and_rollback
        
        qc = QuadCheckStateMachine(CONFIG_FILE)
        results = qc.run_all()
        
        all_passed = all(r.passed for r in results)
        
        for r in results:
            status = "✅" if r.passed else "❌"
            log(f"  {status} {r.phase}: {r.message}")
        
        if not all_passed:
            log("⚠️ 四联校验未通过，执行自动回滚...")
            global _self_writing
            _self_writing = True
            try:
                success = check_and_rollback(results, CONFIG_FILE)
            finally:
                _self_writing = False
            if success:
                log("✅ 自动回滚完成")
            else:
                log("❌ 自动回滚失败，需要人工介入")
            return False
        
        log("✅ 四联校验全部通过")
        return True
        
    except Exception as e:
        log(f"⚠️ config-modification 调用失败: {e}")
        log("  回退到简单 JSON 校验...")
        return True  # 让原逻辑继续

def on_change():
    global _self_writing
    if _self_writing:
        log("⏭️ 忽略自身回滚写入触发的事件，跳过")
        return
    log("🔔 检测到 openclaw.json 变更")

    # JSON 语法校验（Level 1）
    try:
        with open(CONFIG_FILE) as f:
            json.load(f)
        
        log("✅ JSON 语法有效")
        
        # Level 2: config-modification 四联校验
        if not run_config_modification_check():
            return  # 校验失败，已回滚，不再继续
        
        log("📌 fswatch 触发 → 重置健康检查计数器")
        
        # 重置健康计数器
        state = {
            "consecutive_healthy": 0,
            "threshold": 3,
            "cron_job_id": CRON_JOB_ID,
            "last_check": None
        }
        with open(HEALTH_STATE, "w") as f:
            json.dump(state, f, indent=2)
        log("🔄 已重置健康检查计数器")

    except json.JSONDecodeError as e:
        log(f"❌ JSON 语法无效: {e}")
        log("📌 fswatch 触发 → 直接回滚（语法错误）")
        
        # 立即回滚
        _self_writing = True
        try:
            result = subprocess.run(
                ["python3", ROLLBACK_SCRIPT, "rollback"],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.strip().split("\n"):
                if line:
                    log(f"  回滚: {line}")
            if result.returncode == 0:
                log("✅ 回滚完成")
            else:
                log(f"⚠️ 回滚返回码: {result.returncode}")
                if result.stderr:
                    log(f"  stderr: {result.stderr.strip()}")
        except Exception as ex:
            log(f"❌ 回滚失败: {ex}")
            return
        finally:
            _self_writing = False
        
        # 重启 Gateway
        log("🔄 尝试重启 Gateway...")
        import shutil as _shutil
        openclaw_bin = (
            _shutil.which("openclaw") or
            os.path.expanduser("~/.local/share/fnm/node-versions/v24.13.0/installation/bin/openclaw")
        )
        try:
            result = subprocess.run(
                [openclaw_bin, "gateway", "restart"],
                capture_output=True, text=True, timeout=30
            )
            log(f"  重启结果: returncode={result.returncode}")
        except Exception as ex:
            log(f"⚠️ 重启异常: {ex}")

def watch_with_kqueue():
    """使用 macOS kqueue 监听文件变更（事件驱动，非轮询）"""
    log_startup()
    
    kq = select.kqueue()
    
    while True:
        try:
            fd = os.open(CONFIG_FILE, os.O_RDONLY)
            ev = select.kevent(
                fd,
                filter=select.KQ_FILTER_VNODE,
                flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
                fflags=select.KQ_NOTE_WRITE | select.KQ_NOTE_RENAME | select.KQ_NOTE_DELETE
            )
            
            while True:
                events = kq.control([ev], 1, None)  # 阻塞等待
                for event in events:
                    if event.fflags & (select.KQ_NOTE_WRITE | select.KQ_NOTE_RENAME):
                        time.sleep(0.1)  # 等写入完成
                        on_change()
                    if event.fflags & (select.KQ_NOTE_DELETE | select.KQ_NOTE_RENAME):
                        # 文件被删除/重命名，重新打开
                        os.close(fd)
                        time.sleep(0.5)
                        break
                else:
                    continue
                break  # 重新打开文件
                
        except FileNotFoundError:
            log("⚠️ 配置文件不存在，等待创建...")
            time.sleep(2)
        except Exception as e:
            log(f"⚠️ 监听异常: {e}，5秒后重试")
            time.sleep(5)
        finally:
            try:
                os.close(fd)
            except:
                pass

def watch_with_polling():
    """回退方案：轮询 mtime"""
    log_startup()
    log("[polling mode]")
    
    last_mtime = os.path.getmtime(CONFIG_FILE)
    
    while True:
        time.sleep(1)
        try:
            current_mtime = os.path.getmtime(CONFIG_FILE)
            if current_mtime != last_mtime:
                last_mtime = current_mtime
                time.sleep(0.1)
                on_change()
        except FileNotFoundError:
            log("⚠️ 配置文件不存在")
            time.sleep(2)
        except Exception as e:
            log(f"⚠️ 轮询异常: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # macOS 支持 kqueue
    if hasattr(select, "kqueue"):
        watch_with_kqueue()
    else:
        watch_with_polling()
