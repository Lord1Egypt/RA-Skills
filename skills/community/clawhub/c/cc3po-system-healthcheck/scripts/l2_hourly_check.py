#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
L2 Hourly Health Check - 小时级系统检查 (<5s)

功能:
1. 系统资源监控（CPU/内存/磁盘）
2. 关键服务状态（Cron/OpenClaw Gateway）
3. 日志文件大小检查
4. Python 环境检查

使用方式:
    python scripts/l2_hourly_check.py
    python scripts/l2_hourly_check.py --json
    python scripts/l2_hourly_check.py --quiet
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# 添加父目录到路径（用于导入 i18n）
sys.path.insert(0, str(Path(__file__).parent))
from i18n import get_i18n

# ============== 配置 ==============

DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"
DEFAULT_CONFIG = Path.home() / ".openclaw" / "skills" / "system-healthcheck" / "config" / "default_config.yaml"

# 阈值默认值
DISK_WARNING = 80
DISK_CRITICAL = 95
MEMORY_WARNING_MB = 500
LOG_SIZE_WARNING_MB = 100


def load_config() -> dict:
    """加载配置文件"""
    config = {
        "workspace": DEFAULT_WORKSPACE,
        "disk_warning": DISK_WARNING,
        "disk_critical": DISK_CRITICAL,
        "memory_warning_mb": MEMORY_WARNING_MB,
        "log_size_mb": LOG_SIZE_WARNING_MB,
    }
    
    config_file = Path(DEFAULT_CONFIG)
    if config_file.exists():
        try:
            import yaml
            with open(config_file, "r", encoding="utf-8") as f:
                full_config = yaml.safe_load(f) or {}
                thresholds = full_config.get("thresholds", {})
                if thresholds:
                    config["disk_warning"] = thresholds.get("disk_warning", DISK_WARNING)
                    config["disk_critical"] = thresholds.get("disk_critical", DISK_CRITICAL)
                    config["memory_warning_mb"] = thresholds.get("memory_warning_mb", MEMORY_WARNING_MB)
                    config["log_size_mb"] = thresholds.get("log_size_mb", LOG_SIZE_WARNING_MB)
        except:
            pass
    
    return config


def check_disk_usage(threshold_warning: int, threshold_critical: int) -> dict:
    """检查磁盘使用率"""
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        usage = int(used / total * 100)
        
        if usage >= threshold_critical:
            status = "critical"
            ok = False
        elif usage >= threshold_warning:
            status = "warning"
            ok = False
        else:
            status = "ok"
            ok = True
        
        return {
            "check": "disk",
            "ok": ok,
            "status": status,
            "usage_percent": usage,
            "total_gb": round(total / (1024**3), 1),
            "used_gb": round(used / (1024**3), 1),
            "free_gb": round(free / (1024**3), 1)
        }
    except Exception as e:
        return {
            "check": "disk",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_memory_usage(threshold_mb: int) -> dict:
    """检查内存使用"""
    try:
        # Linux: 读取 /proc/meminfo
        if sys.platform.startswith("linux"):
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            
            mem_info = {}
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = int(parts[1].strip().split()[0])  # kB
                    mem_info[key] = value
            
            total_kb = mem_info.get("MemTotal", 0)
            available_kb = mem_info.get("MemAvailable", mem_info.get("MemFree", 0))
            used_kb = total_kb - available_kb
            
            total_mb = total_kb / 1024
            available_mb = available_kb / 1024
            used_mb = used_kb / 1024
            
            ok = available_mb >= threshold_mb
            status = "ok" if ok else "warning"
            
            return {
                "check": "memory",
                "ok": ok,
                "status": status,
                "total_mb": round(total_mb, 0),
                "used_mb": round(used_mb, 0),
                "available_mb": round(available_mb, 0)
            }
        
        # macOS
        elif sys.platform == "darwin":
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                total_bytes = int(result.stdout.strip())
                total_mb = total_bytes / (1024 * 1024)
                
                # macOS 可用内存估算
                result = subprocess.run(
                    ["vm_stat"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    # 简化处理，返回总量
                    return {
                        "check": "memory",
                        "ok": True,
                        "status": "ok",
                        "total_mb": round(total_mb, 0),
                        "used_mb": 0,
                        "available_mb": total_mb
                    }
        
        return {
            "check": "memory",
            "ok": False,
            "status": "error",
            "error": "Unsupported platform"
        }
    except Exception as e:
        return {
            "check": "memory",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_cron_service() -> dict:
    """检查 Cron 服务状态"""
    try:
        if sys.platform.startswith("linux"):
            # 尝试多种方式检测 Cron
            # 方式 1: systemctl (Debian/Ubuntu)
            result = subprocess.Popen(
                ["systemctl", "is-active", "cron"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=5)
            if result.returncode == 0 and stdout.strip() == "active":
                return {
                    "check": "cron",
                    "ok": True,
                    "status": "ok",
                    "running": True
                }
            
            # 方式 2: systemctl (RHEL/CentOS - crond)
            result = subprocess.Popen(
                ["systemctl", "is-active", "crond"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=5)
            if result.returncode == 0 and stdout.strip() == "active":
                return {
                    "check": "cron",
                    "ok": True,
                    "status": "ok",
                    "running": True
                }
            
            # 方式 3: 检查进程
            result = subprocess.Popen(
                ["pgrep", "-x", "crond"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=5)
            if result.returncode == 0 and stdout.strip():
                return {
                    "check": "cron",
                    "ok": True,
                    "status": "ok",
                    "running": True
                }
            
            # 方式 4: 检查 cron 进程（兼容模式）
            result = subprocess.Popen(
                ["pgrep", "-f", "cron"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=5)
            ok = result.returncode == 0 and stdout.strip()
            
            return {
                "check": "cron",
                "ok": ok,
                "status": "ok" if ok else "warning",
                "running": ok,
                "note": "Process-based detection" if ok else "Cron service not found"
            }
        
        elif sys.platform == "darwin":
            result = subprocess.Popen(
                ["launchctl", "list", "com.vix.cron"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=5)
            ok = result.returncode == 0
            
            return {
                "check": "cron",
                "ok": ok,
                "status": "ok" if ok else "error",
                "running": ok
            }
        
        return {
            "check": "cron",
            "ok": True,
            "status": "ok",
            "running": True,
            "note": "Platform check skipped"
        }
    except Exception as e:
        return {
            "check": "cron",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_openclaw_gateway() -> dict:
    """检查 OpenClaw Gateway 状态"""
    try:
        # 检查 gateway 进程（更精确的匹配）
        result = subprocess.Popen(
            ["pgrep", "-f", "openclaw-gateway"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = result.communicate(timeout=5)
        ok = result.returncode == 0 and bool(stdout.strip())
        
        # 如果没找到，尝试检查端口
        if not ok:
            result = subprocess.Popen(
                ["lsof", "-i", ":17514"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=5)
            ok = result.returncode == 0 and bool(stdout.strip())
        
        return {
            "check": "gateway",
            "ok": ok,
            "status": "ok" if ok else "warning",
            "running": ok,
            "note": "Port 17514 check" if ok else None
        }
    except Exception as e:
        return {
            "check": "gateway",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_log_files(workspace: Path, threshold_mb: int) -> dict:
    """检查日志文件大小"""
    try:
        logs_dir = workspace / "logs"
        
        if not logs_dir.exists():
            return {
                "check": "logs",
                "ok": True,
                "status": "ok",
                "size_mb": 0,
                "note": "Logs directory not found"
            }
        
        total_size = sum(f.stat().st_size for f in logs_dir.glob("*.log") if f.is_file())
        total_size_mb = total_size / (1024 * 1024)
        
        ok = total_size_mb < threshold_mb
        status = "ok" if ok else "warning"
        
        return {
            "check": "logs",
            "ok": ok,
            "status": status,
            "size_mb": round(total_size_mb, 1),
            "file_count": len(list(logs_dir.glob("*.log")))
        }
    except Exception as e:
        return {
            "check": "logs",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_python_environment() -> dict:
    """检查 Python 环境"""
    try:
        version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        return {
            "check": "python",
            "ok": True,
            "status": "ok",
            "version": version,
            "executable": sys.executable
        }
    except Exception as e:
        return {
            "check": "python",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def run_l2_check(config: dict) -> dict:
    """执行 L2 检查"""
    workspace = Path(config.get("workspace", DEFAULT_WORKSPACE))
    
    results = {
        "checks": [
            check_disk_usage(config["disk_warning"], config["disk_critical"]),
            check_memory_usage(config["memory_warning_mb"]),
            check_cron_service(),
            check_openclaw_gateway(),
            check_log_files(workspace, config["log_size_mb"]),
            check_python_environment()
        ]
    }
    
    results["success"] = all(c["ok"] for c in results["checks"])
    results["warning_count"] = sum(1 for c in results["checks"] if c.get("status") == "warning")
    results["error_count"] = sum(1 for c in results["checks"] if c.get("status") in ["error", "critical"])
    
    return results


def format_output(results: dict, duration_s: float) -> str:
    """格式化输出"""
    i18n = get_i18n()
    
    lines = []
    
    # 标题
    lines.append(f"{i18n.t('l2.title')} · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # 各项检查
    for check in results["checks"]:
        check_name = i18n.t(f"checks.{check['check']}")
        status = check.get("status", "ok")
        
        if status == "ok":
            icon = i18n.t("status.ok")
        elif status == "warning":
            icon = i18n.t("status.warning")
        elif status == "critical":
            icon = i18n.t("status.critical")
        else:
            icon = i18n.t("status.error")
        
        # 构建详情
        details = []
        if check["check"] == "disk":
            details.append(f"{check.get('usage_percent', 0)}%")
        elif check["check"] == "memory":
            used_gb = check.get('used_mb', 0) / 1024
            total_gb = check.get('total_mb', 0) / 1024
            details.append(f"{used_gb:.1f}GB / {total_gb:.1f}GB")
        elif check["check"] == "logs":
            details.append(f"{check.get('size_mb', 0)}MB")
        elif check["check"] == "python":
            details.append(f"Python {check.get('version', '?')}")
        elif check["check"] in ["cron", "gateway"]:
            details.append(i18n.t("status.running") if check.get("running") else i18n.t("status.not_running"))
        
        detail_str = " · ".join(details) if details else ""
        lines.append(f"{icon} {check_name}: {detail_str}")
    
    lines.append("")
    lines.append("━" * 40)
    
    # 总结
    if results["success"]:
        lines.append(f"{i18n.t('summary.all_ok')}")
    elif results["error_count"] > 0:
        lines.append(i18n.t("summary.has_errors", count=results["error_count"]))
    else:
        lines.append(i18n.t("summary.has_warnings", count=results["warning_count"]))
    
    lines.append(f"{i18n.t('meta.duration', seconds=f'{duration_s:.1f}s')}")
    
    return "\n".join(lines)


def main():
    """主函数"""
    start = time.time()
    
    # 加载配置
    config = load_config()
    
    # 解析命令行参数
    json_output = "--json" in sys.argv
    quiet = "--quiet" in sys.argv
    
    # 执行检查
    results = run_l2_check(config)
    
    duration_s = time.time() - start
    
    # 输出
    if json_output:
        results["duration_s"] = duration_s
        print(json.dumps(results, indent=2))
    elif quiet:
        sys.exit(0 if results["success"] else 1)
    else:
        print(format_output(results, duration_s))
        sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    main()
