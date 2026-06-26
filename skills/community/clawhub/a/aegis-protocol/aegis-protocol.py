#!/usr/bin/env python3
"""Aegis Protocol - Dream 稳定性守护协议

版本：0.12.0
功能：核心三问题检测 + 白名单 + 精准恢复
"""

import json
import subprocess
import ssl
import socket
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import time

WORKSPACE = Path("/root/.openclaw/workspace")
CONFIG_FILE = WORKSPACE / ".watchdog-config.json"
HEALING_MEMORY = WORKSPACE / ".healing-memory.json"
LOOP_HISTORY_FILE = WORKSPACE / ".loop-history.json"
LOG_FILE = Path("/var/log/aegis-protocol.log")
CACHE_FILE = WORKSPACE / ".aegis-cache.json"

# 缓存配置
CACHE_TTL_SECONDS = 300  # 5 分钟缓存有效期


class ResultCache:
    """检查结果缓存"""
    
    def __init__(self, ttl: int = CACHE_TTL_SECONDS):
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
        self._load()
    
    def _load(self) -> None:
        """加载缓存"""
        if CACHE_FILE.exists():
            try:
                data = json.loads(CACHE_FILE.read_text())
                now = time.time()
                self.cache = {
                    k: v for k, v in data.items()
                    if now - v.get("timestamp", 0) < self.ttl
                }
            except Exception:
                self.cache = {}
    
    def _save(self) -> None:
        """保存缓存"""
        try:
            CACHE_FILE.write_text(json.dumps(self.cache, indent=2))
        except Exception:
            pass
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """获取缓存结果"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry.get("timestamp", 0) < self.ttl:
                return entry.get("result")
            del self.cache[key]
        return None
    
    def set(self, key: str, result: Dict[str, Any]) -> None:
        """设置缓存结果"""
        self.cache[key] = {"result": result, "timestamp": time.time()}
        self._save()
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache = {}
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()


cache = ResultCache()


# ============ 异常类 ============

class AegisError(Exception):
    """Aegis 基础异常"""
    pass


class ConfigError(AegisError):
    """配置错误"""
    pass


class CheckError(AegisError):
    """检查执行错误"""
    pass


class RecoveryError(AegisError):
    """恢复执行错误"""
    pass


class ExternalCommandError(AegisError):
    """外部命令执行错误"""
    
    def __init__(self, command: str, returncode: int, stderr: str):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        message = f"命令 '{command}' 执行失败 (code={returncode}): {stderr}"
        super().__init__(message)


# ============ 配置 ============

def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text())
            if "thresholds" not in config:
                raise ConfigError("配置文件缺少 'thresholds' 字段")
            return config
        except json.JSONDecodeError as e:
            raise ConfigError(f"配置文件 JSON 格式错误：{e}")
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> bool:
    """保存配置文件"""
    try:
        CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False))
        return True
    except Exception:
        return False


DEFAULT_CONFIG = {
    "version": 1,
    "thresholds": {
        "sessionTimeoutMinutes": 60,
        "pm2RestartAlert": 50,
        "diskUsagePercent": 90,
        "memoryUsagePercent": 95,
        "contextUsagePercent": 80,
        "loopDetectionWindow": 10,
        "loopDetectionThreshold": 0.6
    },
    "cooldowns": {
        "sessionKill": 300,
        "serviceRestart": 600,
        "contextCompact": 300
    },
    "actions": {
        "onSessionTimeout": "kill",
        "onPm2Offline": "restart",
        "onDiskFull": "alert",
        "onLoopDetected": "abort"
    },
    "notifications": {
        "enabled": False,
        "channel": "telegram",
        "note": "Disabled to avoid security false positives"
    },
    "whitelist": {
        "sessions": [],
        "services": []
    }
}


# ============ 工具函数 ============

def exec_cmd(cmd: str, timeout: int = 30, raise_on_error: bool = False) -> Tuple[int, str, str]:
    """执行 shell 命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        if raise_on_error and result.returncode != 0:
            raise ExternalCommandError(cmd, result.returncode, result.stderr)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        if raise_on_error:
            raise ExternalCommandError(cmd, -1, "Command timed out")
        return -1, "", "Command timed out"
    except Exception as e:
        if raise_on_error:
            raise ExternalCommandError(cmd, -1, str(e))
        return -1, "", str(e)


def log(message: str) -> None:
    """记录日志"""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry + "\n")
    except Exception:
        pass


# ============ 检查函数 ============

def check_sessions() -> Dict[str, Any]:
    """检查卡住的会话"""
    config = load_config()
    whitelist = config.get("whitelist", {}).get("sessions", [])
    
    code, out, err = exec_cmd("openclaw sessions list --limit 100")
    
    if code != 0:
        return {"status": "ok", "stuck_count": 0, "sessions": [], "note": "会话检查需要 API 支持"}
    
    stuck_sessions: List[str] = []
    try:
        sessions = re.findall(r'"key":"([^"]*)".*?"status":"([^"]*)"', out)
        for key, status in sessions:
            if status == "running" and key not in whitelist:
                stuck_sessions.append(key)
    except Exception:
        pass
    
    return {
        "status": "ok",
        "stuck_count": len(stuck_sessions),
        "sessions": stuck_sessions
    }


def check_pm2() -> Dict[str, Any]:
    """检查 PM2 服务状态"""
    config = load_config()
    alert_threshold = config["thresholds"]["pm2RestartAlert"]
    whitelist = config.get("whitelist", {}).get("services", [])
    
    code, out, err = exec_cmd("pm2 status")
    if code != 0:
        return {"status": "error", "message": "PM2 不可用"}
    
    lines = out.strip().split('\n')[3:]
    services = []
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 9:
            name = parts[1]
            status = parts[3]
            restarts = int(parts[7]) if parts[7].isdigit() else 0
            
            if name not in whitelist:
                services.append({
                    "name": name,
                    "status": status,
                    "restarts": restarts,
                    "alert": restarts > alert_threshold
                })
    
    return {
        "status": "ok",
        "services": services,
        "alerts": [s for s in services if s["alert"]]
    }


def check_nginx() -> Dict[str, Any]:
    """检查 Nginx 状态"""
    code, out, err = exec_cmd("systemctl is-active nginx")
    active = code == 0 and out.strip() == "active"
    
    code2, out2, err2 = exec_cmd("nginx -t 2>&1")
    config_ok = "syntax is ok" in out2
    
    return {
        "status": "ok" if active else "error",
        "active": active,
        "config_ok": config_ok
    }


def check_disk() -> Dict[str, Any]:
    """检查磁盘使用率"""
    cache_key = "disk"
    
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    config = load_config()
    threshold = config["thresholds"]["diskUsagePercent"]
    
    code, out, err = exec_cmd("df / | tail -1")
    if code != 0:
        result = {"status": "error", "message": err}
    else:
        parts = out.split()
        usage_percent = int(parts[4].replace('%', ''))
        result = {
            "status": "warning" if usage_percent > threshold else "ok",
            "usage_percent": usage_percent,
            "threshold": threshold,
            "available": parts[3]
        }
    
    cache.set(cache_key, result)
    return result


def check_memory() -> Dict[str, Any]:
    """检查内存使用率"""
    config = load_config()
    threshold = config["thresholds"]["memoryUsagePercent"]
    
    code, out, err = exec_cmd("free | grep Mem")
    if code != 0:
        return {"status": "error", "message": err}
    
    parts = out.split()
    total = int(parts[1])
    used = int(parts[2])
    usage_percent = int(used / total * 100)
    
    return {
        "status": "warning" if usage_percent > threshold else "ok",
        "usage_percent": usage_percent,
        "threshold": threshold,
        "available_gb": (total - used) / 1024 / 1024
    }


def check_context_usage() -> Dict[str, Any]:
    """检查上下文使用率"""
    config = load_config()
    threshold = config["thresholds"]["contextUsagePercent"]
    
    code, out, err = exec_cmd("openclaw session_status 2>&1 || echo 'contextTokens:0'")
    
    match = re.search(r'contextTokens[:\s]+(\d+)', out)
    if match:
        tokens = int(match.group(1))
        max_tokens = 1000000
        usage_percent = int(tokens / max_tokens * 100)
        
        return {
            "status": "warning" if usage_percent > threshold else "ok",
            "usage_percent": usage_percent,
            "threshold": threshold,
            "tokens_used": tokens,
            "tokens_max": max_tokens
        }
    
    return {
        "status": "ok",
        "usage_percent": 0,
        "note": "无法获取上下文使用率"
    }


def check_task_stall() -> Dict[str, Any]:
    """检查任务停滞"""
    task_state_file = WORKSPACE / ".task-state.json"
    
    if not task_state_file.exists():
        return {"status": "ok", "stalled_tasks": []}
    
    try:
        state = json.loads(task_state_file.read_text())
        stalled = []
        now = datetime.now()
        stall_threshold = timedelta(minutes=30)
        
        for task_id, task in state.get("tasks", {}).items():
            if task.get("status") == "doing":
                updated_at = task.get("updated_at")
                if updated_at:
                    last_update = datetime.fromisoformat(updated_at)
                    if now - last_update > stall_threshold:
                        stalled.append({
                            "task_id": task_id,
                            "stalled_minutes": int((now - last_update).total_seconds() / 60)
                        })
        
        return {
            "status": "warning" if stalled else "ok",
            "stalled_tasks": stalled
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_loop_history() -> Dict[str, Any]:
    """检测工具调用循环"""
    config = load_config()
    window_size = config["thresholds"]["loopDetectionWindow"]
    threshold = config["thresholds"]["loopDetectionThreshold"]
    
    if not LOOP_HISTORY_FILE.exists():
        return {"status": "ok", "loop_detected": False}
    
    history = json.loads(LOOP_HISTORY_FILE.read_text())
    recent = history.get("calls", [])[-window_size:]
    
    if len(recent) < 5:
        return {"status": "ok", "loop_detected": False}
    
    unique = len(set(recent))
    duplication = 1 - (unique / len(recent))
    
    return {
        "status": "warning" if duplication > threshold else "ok",
        "loop_detected": duplication > threshold,
        "duplication_rate": duplication,
        "window_size": len(recent)
    }


def check_cron_tasks() -> Dict[str, Any]:
    """检查 cron 任务状态"""
    code, out, err = exec_cmd("crontab -l 2>&1")
    
    if code != 0 or 'no crontab' in out.lower():
        return {"status": "ok", "tasks": [], "note": "无 cron 任务"}
    
    tasks = [line for line in out.strip().split('\n') if line and not line.startswith('#')]
    
    return {
        "status": "ok",
        "task_count": len(tasks),
        "tasks": tasks[:5]
    }


def get_health_score(checks: Dict[str, Dict[str, Any]]) -> int:
    """计算健康度评分 (0-100)"""
    if not checks:
        return 0
    
    score_map = {"ok": 100, "info": 80, "warning": 50, "error": 0}
    
    total = 0
    count = 0
    for result in checks.values():
        status = result.get("status", "ok")
        total += score_map.get(status, 50)
        count += 1
    
    return int(total / count) if count > 0 else 0


# ============ 核心三问题分类 ============

class IssueType:
    """核心问题类型"""
    SESSION_STUCK = "session_stuck"
    LLM_TIMEOUT = "llm_timeout"
    SERVICE_DOWN = "service_down"


RECOVERY_STRATEGIES = {
    IssueType.SESSION_STUCK: {
        "action": "kill",
        "priority": "critical",
        "cooldown": 300,
        "description": "Kill stuck session"
    },
    IssueType.LLM_TIMEOUT: {
        "action": "alert",
        "priority": "warning",
        "cooldown": 600,
        "description": "Alert - LLM/model issue"
    },
    IssueType.SERVICE_DOWN: {
        "action": "restart",
        "priority": "critical",
        "cooldown": 300,
        "description": "Restart service"
    },
}


def classify_issue(check_name: str, check_result: Dict[str, Any]) -> Optional[str]:
    """核心三问题分类"""
    if check_result.get("status") == "ok":
        return None
    
    if check_name == "sessions" and check_result.get("stuck_count", 0) > 0:
        return IssueType.SESSION_STUCK
    
    if check_name == "context" and check_result.get("status") == "warning":
        return IssueType.LLM_TIMEOUT
    
    if check_name == "nginx" and not check_result.get("active"):
        return IssueType.SERVICE_DOWN
    
    if check_name == "cron" and check_result.get("task_count", 0) == 0:
        return IssueType.SERVICE_DOWN
    
    if check_name == "pm2" and len(check_result.get("alerts", [])) > 0:
        return IssueType.SERVICE_DOWN
    
    return None


def get_recovery_action(issue_type: str) -> Dict[str, Any]:
    """获取恢复策略"""
    return RECOVERY_STRATEGIES.get(issue_type, {
        "action": "alert",
        "priority": "info",
        "cooldown": 600,
        "description": "Unknown issue"
    })


# ============ 恢复函数 ============

def record_incident(incident_type: str, action: str, success: bool, recovery_time: float, details: Optional[Dict[str, Any]] = None) -> None:
    """记录事件到 Healing Memory"""
    memory = {"incidents": [], "strategyStats": {}}
    
    if HEALING_MEMORY.exists():
        memory = json.loads(HEALING_MEMORY.read_text())
    
    incident = {
        "id": f"inc-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "type": incident_type,
        "action": action,
        "success": success,
        "recoveryTimeSeconds": recovery_time,
        "details": details or {}
    }
    
    memory["incidents"].append(incident)
    
    if action not in memory["strategyStats"]:
        memory["strategyStats"][action] = {"attempts": 0, "successes": 0}
    
    memory["strategyStats"][action]["attempts"] += 1
    if success:
        memory["strategyStats"][action]["successes"] += 1
    
    HEALING_MEMORY.write_text(json.dumps(memory, indent=2, ensure_ascii=False))
    log(f"Healing Memory 已更新：{incident['id']}")


def kill_session(session_key: str) -> bool:
    """终止会话"""
    start = datetime.now()
    code, out, err = exec_cmd(f"openclaw sessions kill {session_key}")
    duration = (datetime.now() - start).total_seconds()
    
    success = code == 0
    record_incident("session_timeout", "session_kill", success, duration, {"session_key": session_key})
    
    return success


def restart_service(service_name: str) -> bool:
    """重启服务"""
    start = datetime.now()
    
    if service_name == "pm2":
        code, out, err = exec_cmd("pm2 restart all")
    elif service_name == "nginx":
        code, out, err = exec_cmd("systemctl restart nginx")
    else:
        code, out, err = -1, "", f"未知服务：{service_name}"
    
    duration = (datetime.now() - start).total_seconds()
    success = code == 0
    
    record_incident("service_offline", "service_restart", success, duration, {"service": service_name})
    
    return success


def compact_context() -> bool:
    """压缩上下文"""
    start = datetime.now()
    code, out, err = exec_cmd("openclaw memory compact")
    duration = (datetime.now() - start).total_seconds()
    
    success = code == 0
    record_incident("context_overload", "context_compact", success, duration)
    
    return success


# ============ 主函数 ============

def heal() -> Dict[str, Any]:
    """执行核心三问题检查 + 恢复
    
    只关注:
    1. Session 是否卡死 → kill
    2. LLM 响应是否超时 → alert
    3. Gateway/Cron 是否存活 → restart
    """
    log("执行核心三问题检查...")
    log("=" * 50)
    
    actions_taken: List[str] = []
    errors: List[str] = []
    issues: List[str] = []
    
    # 核心 5 项检查
    core_checks = {
        "sessions": check_sessions(),
        "context": check_context_usage(),
        "nginx": check_nginx(),
        "cron": check_cron_tasks(),
        "pm2": check_pm2(),
    }
    
    # 分类 + 恢复
    for check_name, result in core_checks.items():
        issue_type = classify_issue(check_name, result)
        
        if issue_type is None:
            continue
        
        issues.append(issue_type)
        strategy = get_recovery_action(issue_type)
        
        log(f"[{strategy['priority'].upper()}] {issue_type}: {strategy['description']}")
        
        try:
            if issue_type == IssueType.SESSION_STUCK:
                for session in result.get("sessions", []):
                    log(f"→ Killing: {session}")
                    if kill_session(session):
                        actions_taken.append(f"kill:{session}")
                    else:
                        errors.append(f"kill_failed:{session}")
            
            elif issue_type == IssueType.LLM_TIMEOUT:
                log(f"→ Alert: LLM/model may have issues")
                actions_taken.append("alert:llm_timeout")
            
            elif issue_type == IssueType.SERVICE_DOWN:
                if check_name == "nginx":
                    log(f"→ Restarting: Nginx")
                    if restart_service("nginx"):
                        actions_taken.append("restart:nginx")
                    else:
                        errors.append("nginx_restart_failed")
                
                elif check_name == "pm2":
                    log(f"→ Restarting: PM2")
                    if restart_service("pm2"):
                        actions_taken.append("restart:pm2")
                    else:
                        errors.append("pm2_restart_failed")
                
                elif check_name == "cron":
                    log(f"→ Alert: Cron tasks missing")
                    actions_taken.append("alert:cron_missing")
        
        except Exception as e:
            errors.append(f"error:{check_name}:{str(e)}")
    
    # 总结
    log("=" * 50)
    log(f"Issues: {len(issues)}")
    log(f"Actions: {len(actions_taken)}")
    log(f"Errors: {len(errors)}")
    
    result = {
        "issues": issues,
        "actions": actions_taken,
        "errors": errors,
        "success": len(errors) == 0
    }
    
    # 输出汇总报告
    send_heal_report(result)
    
    return result


def send_heal_report(result: Dict[str, Any]) -> None:
    """输出 heal 汇总报告到日志
    
    Args:
        result: heal() 的返回结果
    """
    issues = result.get("issues", [])
    actions = result.get("actions", [])
    errors = result.get("errors", [])
    success = result.get("success", False)
    
    if not issues:
        log("[HEAL REPORT] ✅ No issues detected")
        return
    
    log("[HEAL REPORT] " + "=" * 40)
    log("[HEAL REPORT] **Aegis Recovery Report**")
    log("[HEAL REPORT] " + "=" * 40)
    
    log(f"[HEAL REPORT] Issues Detected: {len(issues)}")
    for issue in issues:
        log(f"[HEAL REPORT]   • {issue}")
    
    log(f"[HEAL REPORT] Actions Taken: {len(actions)}")
    for action in actions:
        log(f"[HEAL REPORT]   • {action}")
    
    if errors:
        log(f"[HEAL REPORT] Errors: {len(errors)}")
        for error in errors:
            log(f"[HEAL REPORT]   • {error}")
    
    status = "✅ Success" if success else "❌ Failed"
    log(f"[HEAL REPORT] Status: {status}")
    log("[HEAL REPORT] " + "=" * 40)


def status(mode: str = "standard") -> Dict[str, Any]:
    """显示状态摘要"""
    log("=" * 60)
    log("Aegis Protocol 状态检查")
    log("=" * 60)
    
    checks = {
        "sessions": check_sessions(),
        "pm2": check_pm2(),
        "nginx": check_nginx(),
        "disk": check_disk(),
        "memory": check_memory(),
        "context": check_context_usage(),
        "task_stall": check_task_stall(),
        "loop": check_loop_history()
    }
    
    if mode in ["full", "extended"]:
        checks["ssl_cert"] = check_ssl_cert()
        checks["docker"] = check_docker_containers()
        checks["network"] = check_network_connectivity()
        checks["cron"] = check_cron_tasks()
        checks["git"] = check_git_status()
        checks["security"] = check_security_updates()
        checks["disk_cleanup"] = check_disk_cleanup_suggestions()
        checks["cpu_load"] = check_cpu_load()
        checks["zombies"] = check_zombie_processes()
        checks["open_files"] = check_open_files()
        checks["connections"] = check_connections()
        checks["backup"] = check_backup_status()
    
    ok_count = sum(1 for r in checks.values() if r.get("status") == "ok")
    warning_count = sum(1 for r in checks.values() if r.get("status") == "warning")
    error_count = sum(1 for r in checks.values() if r.get("status") == "error")
    info_count = sum(1 for r in checks.values() if r.get("status") == "info")
    
    health_score = get_health_score(checks)
    
    for name, result in checks.items():
        status_icon = "✅" if result.get("status") == "ok" else "⚠️" if result.get("status") == "warning" else "❌" if result.get("status") == "error" else "ℹ️"
        log(f"{status_icon} {name}: {json.dumps(result, ensure_ascii=False, default=str)}")
    
    log("-" * 60)
    log(f"总览：{ok_count} 正常 / {warning_count} 警告 / {error_count} 错误 / {info_count} 信息")
    log(f"健康度评分：{health_score}/100")
    
    return {"results": checks, "summary": {"ok": ok_count, "warning": warning_count, "error": error_count, "info": info_count, "health_score": health_score}}


def check() -> Dict[str, Any]:
    """执行完整检查"""
    log("执行完整健康检查...")
    return status()


def init_config() -> bool:
    """初始化配置文件"""
    if CONFIG_FILE.exists():
        log(f"⚠️  配置文件已存在：{CONFIG_FILE}")
        log("如需重置，请先删除该文件")
        return False
    
    try:
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False))
        log(f"✅ 配置文件已创建：{CONFIG_FILE}")
        log("可使用 'aegis-protocol config' 查看配置")
        return True
    except Exception as e:
        log(f"❌ 创建配置失败：{e}")
        return False


def config_cmd() -> None:
    """查看配置"""
    config = load_config()
    print(json.dumps(config, indent=2, ensure_ascii=False))


def cmd_help() -> None:
    """帮助信息"""
    print("""Aegis Protocol - Dream 稳定性守护协议

用法：python3 aegis-protocol.py [命令]

命令:
  init    初始化配置文件
  status  显示系统健康状态
  check   执行完整健康检查
  heal    执行自动恢复
  config  查看配置
  help    显示帮助

核心三问题:
  1. Session 卡死 → kill
  2. LLM 超时 → alert
  3. Service Down → restart
""")


def main() -> None:
    """CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(1)
    
    command = sys.argv[1]
    mode = "full" if "--full" in sys.argv else "standard"
    
    if command == "init":
        init_config()
    elif command in ["status", "check"]:
        status(mode=mode)
    elif command == "heal":
        heal()
        # send_heal_report 已在 heal() 内部调用
    elif command == "config":
        config_cmd()
    elif command == "help":
        cmd_help()
    else:
        print(f"未知命令：{command}")
        print("使用 'python3 aegis-protocol.py help' 查看帮助")
        sys.exit(1)


# ============ 扩展检查函数 (full mode) ============

def check_ssl_cert(domain: str = "nevmatrix.com", port: int = 443, days_threshold: int = 30) -> Dict[str, Any]:
    """检查 SSL 证书有效期"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                days_left = (expiry - datetime.now()).days
                
                return {
                    "status": "warning" if days_left < days_threshold else "ok",
                    "domain": domain,
                    "expiry": expiry.isoformat(),
                    "days_left": days_left,
                    "threshold": days_threshold
                }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_docker_containers() -> Dict[str, Any]:
    """检查 Docker 容器健康状态"""
    code, out, err = exec_cmd("docker ps --format '{{.Names}}:{{.Status}}' 2>&1")
    
    if code != 0 or not out.strip():
        return {"status": "ok", "containers": [], "note": "无运行中的容器"}
    
    containers = []
    unhealthy = []
    
    for line in out.strip().split('\n'):
        if ':' in line:
            name, status = line.split(':', 1)
            is_healthy = 'healthy' in status.lower() or 'up' in status.lower()
            containers.append({"name": name, "status": status})
            if not is_healthy:
                unhealthy.append(name)
    
    return {"status": "warning" if unhealthy else "ok", "containers": containers, "unhealthy": unhealthy}


def check_network_connectivity(hosts: Optional[List[str]] = None) -> Dict[str, Any]:
    """检查网络连通性"""
    if hosts is None:
        hosts = ["8.8.8.8", "1.1.1.1", "baidu.com"]
    
    results = []
    for host in hosts:
        code, out, err = exec_cmd(f"ping -c 1 -W 2 {host} 2>&1 | grep 'time=' || echo 'failed'")
        reachable = 'time=' in out
        results.append({"host": host, "reachable": reachable})
    
    unreachable = [r["host"] for r in results if not r["reachable"]]
    
    return {"status": "warning" if unreachable else "ok", "hosts": results, "unreachable": unreachable}


def check_git_status() -> Dict[str, Any]:
    """检查 Git 仓库状态"""
    code, out, err = exec_cmd("cd /root/.openclaw/workspace && git status --short 2>&1")
    
    if code != 0:
        return {"status": "error", "message": "不是 git 仓库"}
    
    changes = [line for line in out.strip().split('\n') if line]
    
    return {"status": "warning" if changes else "ok", "has_changes": len(changes) > 0, "change_count": len(changes), "changes": changes[:10]}


def check_security_updates() -> Dict[str, Any]:
    """检查安全更新"""
    code, out, err = exec_cmd("apt list --upgradable 2>/dev/null | grep -v '^Listing' | head -20")
    
    if code != 0 or not out.strip():
        return {"status": "ok", "updates": [], "note": "无可用更新或 apt 不可用"}
    
    updates = [line for line in out.strip().split('\n') if line]
    
    return {"status": "info" if updates else "ok", "update_count": len(updates), "updates": updates[:10]}


def check_disk_cleanup_suggestions() -> Dict[str, Any]:
    """检查磁盘清理建议"""
    suggestions = []
    
    code, out, err = exec_cmd("find /var/log -name '*.log' -size +100M 2>/dev/null")
    large_logs = [f for f in out.strip().split('\n') if f]
    if large_logs:
        suggestions.append({"type": "large_logs", "files": large_logs[:5], "action": "考虑轮转或删除"})
    
    code, out, err = exec_cmd("du -sh /tmp 2>/dev/null | awk '{print $1}'")
    if out.strip():
        suggestions.append({"type": "tmp_size", "size": out.strip(), "action": "定期清理"})
    
    return {"status": "info" if suggestions else "ok", "suggestions": suggestions}


def check_cpu_load() -> Dict[str, Any]:
    """检查 CPU 负载"""
    code, out, err = exec_cmd("cat /proc/loadavg")
    if code != 0:
        return {"status": "error", "message": err}
    
    parts = out.strip().split()
    load_1m, load_5m, load_15m = float(parts[0]), float(parts[1]), float(parts[2])
    
    code2, out2, err2 = exec_cmd("nproc")
    cpu_count = int(out2.strip()) if out2.strip().isdigit() else 1
    
    threshold = cpu_count * 2
    
    return {"status": "warning" if load_1m > threshold else "ok", "load_1m": load_1m, "load_5m": load_5m, "load_15m": load_15m, "cpu_count": cpu_count, "threshold": threshold}


def check_zombie_processes() -> Dict[str, Any]:
    """检查僵尸进程"""
    code, out, err = exec_cmd("ps aux | awk '$8 ~ /Z/ {print $2}' | wc -l")
    zombie_count = int(out.strip()) if out.strip().isdigit() else 0
    
    return {"status": "warning" if zombie_count > 0 else "ok", "zombie_count": zombie_count}


def check_open_files() -> Dict[str, Any]:
    """检查打开的文件数"""
    code, out, err = exec_cmd("lsof 2>/dev/null | wc -l")
    open_files = int(out.strip()) if out.strip().isdigit() else 0
    
    code2, out2, err2 = exec_cmd("cat /proc/sys/fs/file-nr")
    if code2 == 0:
        parts = out2.strip().split()
        allocated = int(parts[0]) if parts[0].isdigit() else 0
        max_files = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        usage_percent = int(allocated / max_files * 100) if max_files > 0 else 0
        
        return {"status": "warning" if usage_percent > 80 else "ok", "open_files": allocated, "max_files": max_files, "usage_percent": usage_percent}
    
    return {"status": "ok", "open_files": open_files, "note": "无法获取系统限制"}


def check_connections() -> Dict[str, Any]:
    """检查网络连接数"""
    code, out, err = exec_cmd("ss -tun 2>/dev/null | wc -l")
    conn_count = int(out.strip()) if out.strip().isdigit() else 0
    
    code2, out2, err2 = exec_cmd("ss -tun state time-wait 2>/dev/null | wc -l")
    time_wait = int(out2.strip()) if out2.strip().isdigit() else 0
    
    return {"status": "warning" if time_wait > 1000 else "ok", "total_connections": conn_count, "time_wait": time_wait}


def check_backup_status() -> Dict[str, Any]:
    """检查备份状态"""
    backup_dir = WORKSPACE.parent / "backups"
    
    if not backup_dir.exists():
        return {"status": "info", "message": "备份目录不存在", "path": str(backup_dir)}
    
    code, out, err = exec_cmd(f"find {backup_dir} -name '*.tar.gz' -mtime -7 2>/dev/null | head -5")
    recent_backups = [f for f in out.strip().split('\n') if f]
    
    return {"status": "ok" if recent_backups else "warning", "backup_dir": str(backup_dir), "recent_count": len(recent_backups), "recent_backups": recent_backups}


if __name__ == "__main__":
    main()
