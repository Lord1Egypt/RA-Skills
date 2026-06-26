#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Gateway Watchdog v4.0
实时监控 gateway 后台异常，双通道冗余通知（WebChat + 飞书）
"""

import time
import logging
import logging.handlers
import os
import sys
import json
import random
import subprocess
import threading
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Tuple

# ============================================================
# 配置
# ============================================================

WATCHDOG_INTERVAL_SECONDS = 60
CONSECUTIVE_FAILURE_WARN = 2
CONSECUTIVE_FAILURE_ALERT = 3
CONSECUTIVE_FAILURE_CRITICAL = 5
CONSECUTIVE_FAILURE_RECOVER = 3
LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3

HOME_DIR = Path.home()
OPENCLAW_DIR = HOME_DIR / ".openclaw"
WORKSPACE_DIR = OPENCLAW_DIR / "workspace" / "skills" / "autofix" / "scripts"
STATE_FILE = WORKSPACE_DIR / "watchdog_state.json"
LOG_FILE = WORKSPACE_DIR / "gateway_watchdog.log"
PID_FILE = WORKSPACE_DIR / "watchdog.pid"
FEISHU_USER_ID = os.environ.get("WATCHDOG_FEISHU_USER_ID", "ou_your_feishu_user_id")
FEISHU_CHANNEL = "feishu"
OPENCLAW_CMD = str(HOME_DIR / "AppData/Roaming/npm/openclaw.cmd")
OPENCLAW_CONFIG_PATH = OPENCLAW_DIR / "openclaw.json"

_config_cache = {}
_config_mtime = 0
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 日志（轮转）
# ============================================================

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.handlers.RotatingFileHandler(
    str(LOG_FILE), maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT, encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(fh)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(ch)

# 自动修复库（延迟导入，避免启动时依赖）
_repair_module = None
def _get_repair():
    global _repair_module
    if _repair_module is None:
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location('auto_repair', str(WORKSPACE_DIR / 'auto_repair.py'))
            _repair_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(_repair_module)
        except Exception as e:
            logger.warning(f'修复库加载失败: {e}')
    return _repair_module

# ============================================================
# 防双开（Windows 互斥量）
# ============================================================

def acquire_single_instance() -> bool:
    # Clean up orphaned watchdog processes first
    _cleanup_stale_watchdog_processes()
    try:
        import win32event, win32api, winerror
        mutex = win32event.CreateMutex(None, False, "Global\\OpenClawWatchdog_v4")
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            print("Watchdog 实例已在运行，退出")
            return False
        return True
    except ImportError:
        return _pidfile_lock()
    except Exception:
        return _pidfile_lock()

def _cleanup_stale_watchdog_processes():
    """查杀残留的 watchdog 子进程（--status 等）"""
    try:
        import psutil
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline') or []
                if not cmdline:
                    continue
                cmd_str = ' '.join(cmdline).lower()
                if 'watchdog_monitor' not in cmd_str:
                    continue
                pid = proc.info['pid']
                if pid == current_pid:
                    continue
                # Kill any watchdog process that isn't the main daemon
                # (e.g., --status calls that may have hung)
                if '--status' in cmd_str:
                    logger.warning(f"清理残留 watchdog 进程 PID {pid}: {' '.join(cmdline)}")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except ImportError:
        # psutil not available, try wmic fallback
        try:
            current_pid = os.getpid()
            result = subprocess.run(
                ['powershell', '-Command',
                 'Get-WmiObject Win32_Process -Filter "Name like \'python%\'" | '
                 'Where-Object { $_.CommandLine -match \'watchdog_monitor\' } | '
                 'Format-Table ProcessId,CommandLine -AutoSize'],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split('\n')[1:]:  # skip header
                parts = line.strip().split(None, 1)
                if len(parts) >= 2:
                    try:
                        pid = int(parts[0])
                        cmd = parts[1].lower() if len(parts) > 1 else ''
                        if pid != current_pid and '--status' in cmd:
                            logger.warning(f"清理残留 watchdog PID {pid} (wmic)")
                            subprocess.run(['taskkill', '/F', '/PID', str(pid)],
                                         capture_output=True, timeout=5)
                    except (ValueError, subprocess.TimeoutExpired):
                        pass
        except Exception:
            pass

def _pidfile_lock() -> bool:
    try:
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            try:
                os.kill(pid, 0)
                print(f"PID 文件 {pid} 存活，退出")
                return False
            except OSError:
                pass
        PID_FILE.write_text(str(os.getpid()))
        return True
    except Exception:
        return True

def release_instance():
    try:
        if PID_FILE.exists() and PID_FILE.read_text().strip() == str(os.getpid()):
            PID_FILE.unlink()
    except Exception:
        pass

# ============================================================
# 配置热加载
# ============================================================

def load_gateway_config(force: bool = False) -> Dict:
    global _config_cache, _config_mtime
    defaults = {"host": "127.0.0.1", "port": 18788, "token": None, "session_key": "agent:main:main"}
    try:
        mtime = OPENCLAW_CONFIG_PATH.stat().st_mtime
        if force or mtime > _config_mtime:
            with open(OPENCLAW_CONFIG_PATH, encoding="utf-8") as f:
                raw = json.load(f)
            g = raw.get("gateway", {})
            host = g.get("bind", "127.0.0.1")
            defaults["host"] = "127.0.0.1" if host in ("loopback", "localhost") else host
            defaults["port"] = int(g.get("port", 18788))
            defaults["token"] = g.get("auth", {}).get("token")
            defaults["session_key"] = raw.get("session", {}).get("mainKey", "agent:main:main")
            if mtime > _config_mtime:
                logger.info(f"配置热加载 (mtime: {mtime})")
                _config_cache = dict(defaults)
                _config_mtime = mtime
    except Exception as e:
        logger.warning(f"配置加载: {e}")
        if _config_cache:
            return dict(_config_cache)
    # 优先使用缓存（修复：缓存命中时不应返回重新初始化的 defaults）
    if _config_cache:
        return dict(_config_cache)
    return dict(defaults)

# ============================================================
# 健康检查
# ============================================================

def _run_cli(args: list) -> Tuple[int, str, str]:
    cmd = [OPENCLAW_CMD] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError:
        raise FileNotFoundError(f"CLI 未找到: {OPENCLAW_CMD}")
    except subprocess.TimeoutExpired:
        return -1, "", "超时"

def check_health() -> Tuple[bool, str, Dict]:
    try:
        rc, stdout, stderr = _run_cli(["gateway", "status", "--json"])
        if rc == 0 and stdout.strip():
            data = json.loads(stdout)
            s = data.get("service", {}).get("runtime", {}).get("status", "unknown")
            ok = s in ("running", "healthy", "ok")
            rpc = data.get("rpc", {}).get("ok", False)
            return (ok, f"Gateway: {s} | RPC: {'OK' if rpc else 'FAIL'}", {
                "status": s, "rpc_ok": rpc,
                "pid": data.get("service", {}).get("runtime", {}).get("pid"),
                "version": data.get("rpc", {}).get("server", {}).get("version"),
                "source": "cli"})
        elif rc == 0:
            return (False, "Gateway 无输出", {"status": "empty", "source": "cli"})
        return (False, f"CLI: {stderr.strip()[:80]}", {"status": "cli_err", "source": "cli"})
    except FileNotFoundError:
        logger.warning("CLI 不可用，回退 HTTP")
    except Exception as e:
        logger.warning(f"CLI 异常: {e}，回退 HTTP")
    return _check_http()

def _check_http() -> Tuple[bool, str, Dict]:
    cfg = load_gateway_config()
    token = cfg.get("token")
    if not token:
        return _simulate()
    url = f"http://{cfg['host']}:{cfg['port']}/v1/models"
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            ok = resp.status == 200
            return (ok, f"HTTP {'OK' if ok else resp.status}", {"status": "healthy" if ok else "http_err", "source": "http"})
    except urllib.error.URLError as e:
        return (False, f"HTTP 不可达: {e.reason}", {"status": "unreachable", "source": "http"})
    except Exception as e:
        return (False, f"HTTP: {e}", {"status": "exception", "source": "http"})

def _simulate() -> Tuple[bool, str, Dict]:
    r = random.uniform(0.1, 90.0)
    ok = r < 75
    return (ok, f"模拟 {'OK' if ok else 'FAILED'}", {"error_rate": round(r, 1), "source": "sim"})

# ============================================================
# 等级 & 状态
# ============================================================

def severity(failures: int, status: str) -> Dict:
    if status == "stopped" or failures >= CONSECUTIVE_FAILURE_CRITICAL:
        return {"level": 4, "label": "严重", "emoji": "\U0001f534"}
    if failures >= CONSECUTIVE_FAILURE_ALERT:
        return {"level": 3, "label": "警告", "emoji": "\U0001f7e0"}
    if failures >= CONSECUTIVE_FAILURE_WARN:
        return {"level": 2, "label": "注意", "emoji": "\U0001f7e1"}
    return {"level": 1, "label": "正常", "emoji": "\U0001f7e2"}

def load_state() -> Dict:
    d = {"last_alert_time": 0, "last_status": "unknown", "alert_count": 0,
         "consecutive_failures": 0, "consecutive_success": 0, "severity_level": 1, "check_history": [], "auto_repairs": 0, "auto_fixes_applied": []}
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, encoding="utf-8") as f:
                d.update(json.load(f))
    except Exception as e:
        logger.warning(f"状态: {e}")
    return d

def save_state(state: Dict):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"保存: {e}")

# ============================================================
# 通知
# ============================================================

def send_webchat(msg: str, timeout: int = 60) -> bool:
    """
    通过 Gateway HTTP API 发送 WebChat 通知（后台模型推理可能需要30-60秒）
    
    Args:
        msg: 要发送的消息内容
        timeout: 超时秒数（默认60s，模型首次加载约需40s）
        
    Returns:
        bool: True=成功，False=失败（会记录详细错误）
    """
    cfg = load_gateway_config()
    token, sk = cfg.get("token"), cfg.get("session_key", "agent:main:main")
    if not token:
        logger.warning("WebChat 通道：Gateway 未配置 API Token")
        return False
    body = json.dumps({
        "model": "openclaw",
        "messages": [{"role": "user", "content": f"[WD]\n\n{msg}"}],
        "max_tokens": 50
    }).encode("utf-8")
    url = f"http://{cfg['host']}:{cfg['port']}/v1/chat/completions"
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json",
        "X-OpenClaw-Session-Key": sk, "X-OpenClaw-Message-Channel": "webchat"
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                logger.info(f"WebChat 发送成功 (HTTP {resp.status}, 约{timeout}秒超时)")
                return True
            else:
                logger.warning(f"WebChat 返回非 200: HTTP {resp.status}")
                return False
    except TimeoutError:
        logger.error(f"WebChat 连接超时（{timeout}s），模型可能未加载，降级到飞书通道")
        return False
    except urllib.error.HTTPError as e:
        logger.error(f"WebChat API 错误：HTTP {e.code} - {e.reason}")
        logger.error(f" 请求 URL: {url}")
        logger.error(f" 消息内容预览：{msg[:200]}...")
        return False
    except urllib.error.URLError as e:
        logger.error(f"WebChat 网络连接失败：{type(e.reason).__name__}: {e.reason}")
        if hasattr(e, 'reason') and e.reason:
            logger.error(f" 目标地址：{url}")
        return False
    except Exception as e:
        logger.error(f"WebChat 发送失败（未知异常）：{type(e).__name__}: {e}", exc_info=True)
        return False

def send_feishu(msg: str) -> bool:
    """
    通过飞书 CLI 发送通知
    
    Args:
        msg: 要发送的消息内容
        
    Returns:
        bool: True=成功，False=失败
    """
    clean = msg.replace("**", "").replace("*", "")
    text = f"Watchdog\n\n{clean}\n\n---\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    try:
        _run_cli(["message", "send", "--channel", FEISHU_CHANNEL,
                  "--target", FEISHU_USER_ID, "--message", text])
        logger.info(f"飞书发送成功")
        return True
    except Exception as e:
        logger.error(f"飞书发送失败：{type(e).__name__}: {e}", exc_info=True)
        return False

def send_alerts(msg: str):
    """
    发送 watchdog 告警通知（双通道冗余）
    
    1. 飞书通道：即时发送（CLI 方式，零延迟）
    2. WebChat 通道：后台线程发送（HTTP API，模型加载约需40s，不阻塞主循环）
    """
    # 通道1：飞书即时通知（主要通道）
    feishu_ok = send_feishu(msg)
    if feishu_ok:
        logger.info(f"✅ 飞书通知已送达（即时通道）")
    else:
        logger.warning(f"⚠️ 飞书通知发送失败，请检查日志")
    
    # 通道2：WebChat 后台通知（模型推理慢，不阻塞主循环）
    def _webchat_worker():
        try:
            logger.info(f"WebChat 后台线程启动（可能需要30-60秒模型加载时间）...")
            ok = send_webchat(msg, timeout=60)
            if ok:
                logger.info(f"✅ WebChat 通知已送达（后台通道）")
            else:
                logger.warning(f"⚠️ WebChat 通知发送失败（后台通道）")
        except Exception as e:
            logger.error(f"WebChat 后台线程异常：{type(e).__name__}: {e}")
    
    t = threading.Thread(target=_webchat_worker, daemon=True, name="wd-webchat")
    t.start()
    
    # 记录告警状态
    s = load_state()
    s["last_alert_time"] = time.time()
    s["last_alert_ts"] = datetime.now().isoformat()
    s["alert_count"] = s.get("alert_count", 0) + 1
    save_state(s)
    logger.info(f"📊 [状态] 告警计数：{s['alert_count']}, 飞书: {'ok' if feishu_ok else 'fail'}, WebChat: 后台处理中")

def send_startup():
    msg = (
        "**Watchdog v4.0 已启动**\n\n"
        f"**PID:** {os.getpid()}\n"
        f"**时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"**通道:** 飞书(即时) + WebChat(后台)\n"
        f"**降噪:** \u26a0\ufe0f>={CONSECUTIVE_FAILURE_WARN} "
        f"\U0001f7e0>={CONSECUTIVE_FAILURE_ALERT} \U0001f534>={CONSECUTIVE_FAILURE_CRITICAL}\n\n"
        "守护进程后台持续监控中"
    )
    # 使用 send_alerts 统一发送（飞书即时 + WebChat后台线程）
    send_alerts(msg)
    logger.info("启动确认已发送")

# ============================================================
# 精准调度
# ============================================================

def sleep_until(interval: int = 60):
    now = time.time()
    target = ((now // interval) + 1) * interval
    d = target - now
    if d > 0:
        time.sleep(d)

# ============================================================
# 开机自启
# ============================================================

def install_autostart():
    py = Path(sys.executable).resolve()
    script = WORKSPACE_DIR / "watchdog_monitor.py"
    reg = r"HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    cmd = ['powershell', '-Command',
           f'Set-ItemProperty -Path "{reg}" -Name "OpenClawWatchdog" -Value \'{py} {script}\'']
    subprocess.run(cmd, check=True)
    logger.info("开机自启已安装")

def uninstall_autostart():
    reg = r"HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    cmd = ['powershell', '-Command',
           f'Remove-ItemProperty -Path "{reg}" -Name "OpenClawWatchdog" -ErrorAction SilentlyContinue']
    subprocess.run(cmd, check=True)
    logger.info("开机自启已移除")

# ============================================================
# 主循环
# ============================================================

def run():
    logger.info("=" * 60)
    logger.info(f"Gateway Watchdog v4.0  PID: {os.getpid()}")
    logger.info(f"  间隔: {WATCHDOG_INTERVAL_SECONDS}s | 日志轮转: {LOG_MAX_BYTES//1024}KB")
    logger.info("=" * 60)

    load_gateway_config(force=True)
    logger.info(f"  Gateway: {_config_cache['host']}:{_config_cache['port']}")

    send_startup()
    logger.info("启动确认已发送")

    while True:
        try:
            # 健康检查
            ok, status_msg, detail = check_health()
            # 热加载
            load_gateway_config()
            # 状态
            state = load_state()
            prev_level = state.get("severity_level", 1)
            cf = state.get("consecutive_failures", 0)
            cs = state.get("consecutive_success", 0)
            # 计数
            if not ok:
                cf += 1; cs = 0
            else:
                cs += 1
                cf = 0 if cs >= CONSECUTIVE_FAILURE_RECOVER else max(0, cf - 1)
            # 等级
            sev = severity(cf, detail.get("status", ""))
            # 是否通知
            alert = False
            reason = ""
            if not ok:
                if sev["level"] > prev_level:
                    alert, reason = True, f"升级 {prev_level}>{sev['level']}"
                elif cf == CONSECUTIVE_FAILURE_ALERT and sev["level"] >= 3:
                    alert, reason = True, f"达阈值 ({cf}次)"
                elif sev["level"] >= 3 and cf % CONSECUTIVE_FAILURE_CRITICAL == 0:
                    alert, reason = True, f"持续 (第{cf}次)"
            elif ok and prev_level >= 3 and cs == CONSECUTIVE_FAILURE_RECOVER:
                alert, reason = True, "已恢复"
                sev = {"level": 1, "label": "已恢复", "emoji": "\u2705"}
            # 发通知
            if alert:
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if sev["level"] == 1 and "恢复" in sev["label"]:
                    msg = (
                        "**\u2705 [已恢复] Gateway 运行正常**\n\n"
                        f"**时间:** {now_str}\n"
                        f"**连续正常:** {cs} 次\n"
                        f"**状态:** {status_msg}"
                    )
                else:
                    ctx = json.dumps({
                        "type": f"{sev['label']}-Gateway", "time": now_str,
                        "consecutive": cf, "severity": f"L{sev['level']}/4",
                        "status": status_msg, "detail": detail.get("status", "?"),
                        "source": detail.get("source", "?"),
                        "pid": detail.get("pid"), "version": detail.get("version"),
                    }, ensure_ascii=False)
                    msg = (
                        f"**{sev['emoji']} [{sev['label']}] 系统异常 \u2014 请执行自检**\n\n"
                        f"**时间:** {now_str}\n"
                        f"**异常原因:** {reason}\n"
                        f"**等级:** {sev['emoji']} Level {sev['level']}/4 (连续 {cf} 次)\n"
                        f"**状态:** {status_msg}\n\n"
                        "\u2501\u2501\u2501 自动诊断指引 \u2501\u2501\u2501\n\n"
                        "检测到系统异常。请直接告诉我以下任一指令：\n\n"
                        "\U0001f449 **`请运行 autofix 自检`**\n"
                        "\U0001f449 **`帮我看看 Gateway 出了什么问题`**\n"
                        "\U0001f449 **直接说 `自动修复`**\n\n"
                        "---\n"
                        f"`{ctx}`"
                    )
                send_alerts(msg)
                # 自动修复：检查是否有可用的低风险修复方案
                repair = _get_repair()
                if repair:
                    actions = repair.match_repair({
                        "status": detail.get("status", "?"),
                        "rpc_ok": detail.get("rpc_ok"),
                        "source": detail.get("source", "?")
                    })
                    if actions:
                        auto_actions = [a for a in actions if a.auto_approve]
                        if auto_actions:
                            logger.info(f"尝试自动修复: {len(auto_actions)} 个步骤")
                            for action in auto_actions:
                                ok_repair = action.execute()
                                if ok_repair:
                                    state["auto_repairs"] = state.get("auto_repairs", 0) + 1
                                    if "auto_fixes_applied" not in state:
                                        state["auto_fixes_applied"] = []
                                    state["auto_fixes_applied"].append({
                                        "ts": datetime.now().isoformat(),
                                        "issue": action.issue
                                    })
                                    # 修复后验证 (v1.1 — 轮询模式)
                                    logger.info("修复后验证 (轮询 30s)...")
                                    try:
                                        rep = _get_repair()
                                        if rep and hasattr(rep, 'verify_repair'):
                                            v_ok, v_msg = rep.verify_repair(max_wait=30, interval=5)
                                        else:
                                            # 降级: 单次检查
                                            time.sleep(5)
                                            _, v_msg, _ = check_health()
                                            v_ok = 'running' in v_msg
                                    except Exception:
                                        time.sleep(5)
                                        _, v_msg, _ = check_health()
                                        v_ok = 'running' in v_msg
                                    if v_ok:
                                        logger.info(f"修复验证通过: {v_msg}")
                                        send_webchat(f"**✅ 自动修复成功**\n{action.description}\n验证: {v_msg}")
                                    else:
                                        logger.warning(f"修复验证失败: {v_msg}")
                                        send_webchat(f"**⚠️ 自动修复未完全生效**\n{action.description}\n仍需人工诊断: {v_msg}")
            # 日志
            if ok:
                logger.info(f"{sev['emoji']} 正常 | {status_msg} | 成功: {cs}")
            else:
                logger.info(f"{sev['emoji']} {sev['label']} | {status_msg} | 失败: {cf}/{CONSECUTIVE_FAILURE_CRITICAL}")
            # 持久化
            state.update({
                "last_check_time": time.time(),
                "last_check_ts": datetime.now().isoformat(),
                "last_status": "healthy" if ok else sev["label"],
                "consecutive_failures": cf, "consecutive_success": cs,
                "severity_level": sev["level"], "severity_label": sev["label"],
                "last_detail": detail, "last_status_msg": status_msg,
            })
            # 趋势记录：保留最近 1440 次检查（24小时）
            if "check_history" not in state:
                state["check_history"] = []
            state["check_history"].append({
                "ts": datetime.now().isoformat(),
                "ok": ok,
                "severity": sev["level"],
                "status": detail.get("status", "?"),
                "source": detail.get("source", "?")
            })
            # 只保留最近 1440 条
            if len(state["check_history"]) > 1440:
                state["check_history"] = state["check_history"][-1440:]
            # 紧凑存储：不再存全量时间戳到磁盘
            save_state(state)
            sleep_until(WATCHDOG_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            logger.info("退出"); break
        except Exception as e:
            logger.error(f"循环: {e}", exc_info=True); time.sleep(5)

# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    if "--install" in sys.argv:
        install_autostart(); sys.exit(0)
    if "--uninstall" in sys.argv:
        uninstall_autostart(); sys.exit(0)
    if "--status" in sys.argv:
        # 显示当前状态并退出，不启动新实例
        state = load_state()
        print(f"Watchdog v4.0")
        print(f"  PID: {os.getpid()}")
        print(f"  状态: {state.get('last_status', 'unknown')}")
        print(f"  等级: {state.get('severity_label', 'N/A')} (L{state.get('severity_level', '?')})")
        print(f"  连续失败: {state.get('consecutive_failures', 0)}")
        print(f"  连续成功: {state.get('consecutive_success', 0)}")
        print(f"  最后检查: {state.get('last_status_msg', 'N/A')}")
        print(f"  告警次数: {state.get('alert_count', 0)}")
        print(f"  自动修复: {state.get('auto_repairs', 0)}")
        print(f"  最后检查时间: {state.get('last_check_ts', 'N/A')}")
        sys.exit(0)
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Watchdog v4.0\n  --install   安装开机自启\n  --uninstall 移除\n  --status    查看当前状态\n  --help      帮助")
        sys.exit(0)
    if not acquire_single_instance():
        sys.exit(1)
    try:
        run()
    finally:
        release_instance()

