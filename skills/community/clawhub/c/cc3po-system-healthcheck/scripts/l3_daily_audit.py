#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
L3 Daily Audit - 日级深度审计 (<60s)

功能:
1. 包含 L2 所有检查
2. 系统更新检查
3. 磁盘清理建议
4. 进程监控
5. 日志轮转检查
6. 生成日报摘要

使用方式:
    python scripts/l3_daily_audit.py
    python scripts/l3_daily_audit.py --json
    python scripts/l3_daily_audit.py --report  # 生成详细报告
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from i18n import get_i18n

# 导入 L2 检查函数
from l2_hourly_check import (
    load_config, check_disk_usage, check_memory_usage,
    check_cron_service, check_openclaw_gateway, check_log_files
)

# ============== 配置 ==============

DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"
DEFAULT_CONFIG = Path.home() / ".openclaw" / "skills" / "system-healthcheck" / "config" / "default_config.yaml"

# L3 特定阈值
MAX_LOG_AGE_DAYS = 7
MAX_PROCESSES = 500
SWAP_WARNING_PERCENT = 50


def check_system_updates() -> dict:
    """检查系统更新"""
    try:
        if sys.platform.startswith("linux"):
            # Debian/Ubuntu
            if Path("/etc/debian_version").exists():
                result = subprocess.run(
                    ["apt-get", "-s", "upgrade"],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    output = result.stdout
                    if " upgraded" in output:
                        # 提取更新数量
                        import re
                        match = re.search(r"(\d+) upgraded", output)
                        count = int(match.group(1)) if match else 0
                        return {
                            "check": "updates",
                            "ok": count == 0,
                            "status": "warning" if count > 0 else "ok",
                            "pending_updates": count,
                            "platform": "Debian/Ubuntu"
                        }
            
            # RHEL/CentOS
            elif Path("/etc/redhat-release").exists():
                result = subprocess.run(
                    ["yum", "check-update"],
                    capture_output=True, text=True, timeout=30
                )
                # yum check-update 返回 100 表示有更新
                if result.returncode == 100:
                    lines = [l for l in result.stdout.split('\n') if l.strip() and not l.startswith('(')]
                    count = len(lines) - 2  # 减去标题行
                    return {
                        "check": "updates",
                        "ok": False,
                        "status": "warning",
                        "pending_updates": max(0, count),
                        "platform": "RHEL/CentOS"
                    }
        
        return {
            "check": "updates",
            "ok": True,
            "status": "ok",
            "pending_updates": 0,
            "note": "Platform not supported or no updates"
        }
    except Exception as e:
        return {
            "check": "updates",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_swap_usage() -> dict:
    """检查 Swap 使用情况"""
    try:
        if sys.platform.startswith("linux"):
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            
            mem_info = {}
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = int(parts[1].strip().split()[0])
                    mem_info[key] = value
            
            total_swap = mem_info.get("SwapTotal", 0)
            if total_swap == 0:
                return {
                    "check": "swap",
                    "ok": True,
                    "status": "ok",
                    "note": "No swap configured"
                }
            
            used_swap = total_swap - mem_info.get("SwapFree", 0)
            usage_percent = int(used_swap / total_swap * 100)
            
            ok = usage_percent < SWAP_WARNING_PERCENT
            status = "ok" if ok else "warning"
            
            return {
                "check": "swap",
                "ok": ok,
                "status": status,
                "total_mb": total_swap // 1024,
                "used_mb": used_swap // 1024,
                "usage_percent": usage_percent
            }
        
        return {
            "check": "swap",
            "ok": True,
            "status": "ok",
            "note": "Platform check skipped"
        }
    except Exception as e:
        return {
            "check": "swap",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_process_count(max_processes: int) -> dict:
    """检查进程数量"""
    try:
        if sys.platform.startswith("linux"):
            result = subprocess.run(
                ["ps", "-e", "--no-headers"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                count = len(result.stdout.strip().split('\n'))
                ok = count < max_processes
                status = "ok" if ok else "warning"
                
                return {
                    "check": "processes",
                    "ok": ok,
                    "status": status,
                    "count": count,
                    "threshold": max_processes
                }
        
        return {
            "check": "processes",
            "ok": True,
            "status": "ok",
            "note": "Platform check skipped"
        }
    except Exception as e:
        return {
            "check": "processes",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_old_logs(workspace: Path, max_age_days: int) -> dict:
    """检查旧日志文件"""
    try:
        logs_dir = workspace / "logs"
        
        if not logs_dir.exists():
            return {
                "check": "old_logs",
                "ok": True,
                "status": "ok",
                "note": "Logs directory not found"
            }
        
        old_logs = []
        cutoff = datetime.now() - timedelta(days=max_age_days)
        
        for log_file in logs_dir.glob("*.log"):
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime < cutoff:
                old_logs.append({
                    "file": log_file.name,
                    "age_days": (datetime.now() - mtime).days,
                    "size_kb": log_file.stat().st_size // 1024
                })
        
        ok = len(old_logs) == 0
        status = "ok" if ok else "warning"
        
        return {
            "check": "old_logs",
            "ok": ok,
            "status": status,
            "count": len(old_logs),
            "threshold_days": max_age_days,
            "files": old_logs[:5]  # 只返回前 5 个
        }
    except Exception as e:
        return {
            "check": "old_logs",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def check_disk_cleanup_needs() -> dict:
    """检查磁盘清理需求"""
    try:
        # 检查常见临时目录
        temp_dirs = ["/tmp", "/var/tmp", Path.home() / ".cache"]
        total_temp_size = 0
        
        for temp_dir in temp_dirs:
            temp_path = Path(temp_dir)
            if temp_path.exists():
                try:
                    for item in temp_path.rglob("*"):
                        if item.is_file():
                            total_temp_size += item.stat().st_size
                except:
                    pass  # 权限问题跳过
        
        total_temp_mb = total_temp_size / (1024 * 1024)
        needs_cleanup = total_temp_mb > 500  # 500MB 阈值
        
        return {
            "check": "disk_cleanup",
            "ok": not needs_cleanup,
            "status": "warning" if needs_cleanup else "ok",
            "temp_size_mb": round(total_temp_mb, 1),
            "threshold_mb": 500
        }
    except Exception as e:
        return {
            "check": "disk_cleanup",
            "ok": False,
            "status": "error",
            "error": str(e)
        }


def run_l3_audit(config: dict) -> dict:
    """执行 L3 审计"""
    workspace = Path(config.get("workspace", DEFAULT_WORKSPACE))
    
    # L2 检查
    l2_checks = [
        check_disk_usage(config["disk_warning"], config["disk_critical"]),
        check_memory_usage(config["memory_warning_mb"]),
        check_cron_service(),
        check_openclaw_gateway(),
        check_log_files(workspace, config["log_size_mb"]),
    ]
    
    # L3 特有检查
    l3_checks = [
        check_system_updates(),
        check_swap_usage(),
        check_process_count(500),
        check_old_logs(workspace, 7),
        check_disk_cleanup_needs()
    ]
    
    all_checks = l2_checks + l3_checks
    
    results = {
        "checks": all_checks,
        "l2_checks": l2_checks,
        "l3_checks": l3_checks
    }
    
    results["success"] = all(c["ok"] for c in all_checks)
    results["warning_count"] = sum(1 for c in all_checks if c.get("status") == "warning")
    results["error_count"] = sum(1 for c in all_checks if c.get("status") in ["error", "critical"])
    
    return results


def generate_report(results: dict, duration_s: float) -> str:
    """生成详细报告"""
    i18n = get_i18n()
    
    lines = []
    lines.append("=" * 60)
    lines.append(f"L3 Daily Audit Report")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Duration: {duration_s:.1f}s")
    lines.append("=" * 60)
    lines.append("")
    
    # 摘要
    lines.append("## Summary")
    lines.append("")
    if results["success"]:
        lines.append("✅ All checks passed")
    else:
        lines.append(f"⚠️ {results['error_count']} errors, {results['warning_count']} warnings")
    lines.append("")
    
    # L2 检查详情
    lines.append("## L2 Health Checks")
    lines.append("")
    for check in results["l2_checks"]:
        check_name = check.get("check", "unknown")
        status = check.get("status", "ok")
        icon = "✅" if status == "ok" else "⚠️" if status == "warning" else "❌"
        lines.append(f"{icon} {check_name}: {status}")
    lines.append("")
    
    # L3 检查详情
    lines.append("## L3 Additional Checks")
    lines.append("")
    for check in results["l3_checks"]:
        check_name = check.get("check", "unknown")
        status = check.get("status", "ok")
        icon = "✅" if status == "ok" else "⚠️" if status == "warning" else "❌"
        
        # 添加详细信息
        details = []
        if check_name == "updates":
            details.append(f"Pending: {check.get('pending_updates', 0)}")
        elif check_name == "swap":
            if "usage_percent" in check:
                details.append(f"Usage: {check['usage_percent']}%")
        elif check_name == "processes":
            details.append(f"Count: {check.get('count', 0)}")
        elif check_name == "old_logs":
            details.append(f"Old files: {check.get('count', 0)}")
        elif check_name == "disk_cleanup":
            details.append(f"Temp size: {check.get('temp_size_mb', 0)}MB")
        
        detail_str = " · ".join(details) if details else ""
        lines.append(f"{icon} {check_name}: {status} {detail_str}")
    lines.append("")
    
    # 建议
    if results["warning_count"] > 0 or results["error_count"] > 0:
        lines.append("## Recommendations")
        lines.append("")
        for check in results["checks"]:
            if check.get("status") in ["warning", "error", "critical"]:
                if check["check"] == "updates":
                    lines.append("- Run system updates: `sudo apt update && sudo apt upgrade`")
                elif check["check"] == "old_logs":
                    lines.append("- Clean old log files in workspace/logs/")
                elif check["check"] == "disk_cleanup":
                    lines.append("- Clean temporary directories: /tmp, ~/.cache")
                elif check["check"] == "swap":
                    lines.append("- Investigate high swap usage")
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def format_output(results: dict, duration_s: float) -> str:
    """格式化控制台输出"""
    i18n = get_i18n()
    
    lines = []
    lines.append(f"L3 Daily Audit · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # 显示所有检查
    for check in results["checks"]:
        check_name = check.get("check", "unknown")
        status = check.get("status", "ok")
        
        if status == "ok":
            icon = "[OK]"
        elif status == "warning":
            icon = "[WARN]"
        else:
            icon = "[ERR]"
        
        # 简要详情
        details = []
        if check_name == "updates":
            details.append(f"{check.get('pending_updates', 0)} pending")
        elif check_name == "swap":
            if "usage_percent" in check:
                details.append(f"{check['usage_percent']}% used")
        elif check_name == "processes":
            details.append(f"{check.get('count', 0)} processes")
        
        detail_str = " · ".join(details) if details else ""
        lines.append(f"{icon} {check_name}: {detail_str}")
    
    lines.append("")
    lines.append("━" * 40)
    
    # 总结
    if results["success"]:
        lines.append("✅ All checks passed")
    elif results["error_count"] > 0:
        lines.append(f"❌ {results['error_count']} error(s), {results['warning_count']} warning(s)")
    else:
        lines.append(f"⚠️ {results['warning_count']} warning(s)")
    
    lines.append(f"Duration: {duration_s:.1f}s")
    
    return "\n".join(lines)


def main():
    """主函数"""
    start = time.time()
    
    # 加载配置
    config = load_config()
    
    # 解析命令行参数
    json_output = "--json" in sys.argv
    report = "--report" in sys.argv
    quiet = "--quiet" in sys.argv
    
    # 执行审计
    results = run_l3_audit(config)
    
    duration_s = time.time() - start
    
    # 输出
    if json_output:
        results["duration_s"] = duration_s
        print(json.dumps(results, indent=2))
    elif report:
        print(generate_report(results, duration_s))
    elif quiet:
        sys.exit(0 if results["success"] else 1)
    else:
        print(format_output(results, duration_s))
        sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    main()
