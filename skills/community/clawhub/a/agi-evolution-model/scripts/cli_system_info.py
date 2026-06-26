#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 系统信息工具 - 工具化封装
获取 CPU、内存、磁盘、网络等系统资源信息
"""

import os
import sys
import json
import platform
import argparse
import subprocess
import shutil
from typing import Dict, Any
import datetime


def json_output(status: str, data: Any = None, error: str = None, metadata: Dict = None) -> str:
    """统一 JSON 输出格式"""
    result = {
        "status": status,
        "data": data,
        "error": error,
        "metadata": metadata or {},
        "timestamp": datetime.datetime.now().isoformat()
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def action_system() -> str:
    """获取系统基本信息"""
    try:
        system = platform.system()
        return json_output(
            "success",
            data={
                "system": system,
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "architecture": platform.architecture(),
                "python_version": platform.python_version(),
                "hostname": os.uname().nodename if hasattr(os, 'uname') else None
            },
            metadata={"os_type": system.lower()}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_cpu() -> str:
    """获取 CPU 信息"""
    try:
        # 尝试获取 CPU 核心数和使用率
        cpu_count = os.cpu_count() or 0

        # 尝试获取 CPU 使用率（Unix/Linux）
        cpu_usage = None
        if platform.system() == "Linux":
            try:
                with open('/proc/stat', 'r') as f:
                    lines = f.readlines()
                    cpu_line = lines[0].split()
                    if len(cpu_line) >= 5:
                        user = int(cpu_line[1])
                        nice = int(cpu_line[2])
                        system = int(cpu_line[3])
                        idle = int(cpu_line[4])
                        total = user + nice + system + idle
                        usage = ((total - idle) / total * 100) if total > 0 else 0
                        cpu_usage = round(usage, 2)
            except:
                pass

        return json_output(
            "success",
            data={
                "cpu_count": cpu_count,
                "cpu_usage_percent": cpu_usage,
                "cpu_count_physical": cpu_count // 2 if cpu_count > 1 else cpu_count
            }
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_memory() -> str:
    """获取内存信息"""
    try:
        system = platform.system()
        mem_info = {}

        if system == "Linux":
            try:
                with open('/proc/meminfo', 'r') as f:
                    mem_data = {}
                    for line in f:
                        key, value = line.split(':')
                        mem_data[key.strip()] = value.strip().split()[0]

                    total = int(mem_data.get('MemTotal', 0))
                    free = int(mem_data.get('MemFree', 0))
                    available = int(mem_data.get('MemAvailable', free))
                    buffers = int(mem_data.get('Buffers', 0))
                    cached = int(mem_data.get('Cached', 0))

                    used = total - available

                    mem_info = {
                        "total_mb": round(total / 1024, 2),
                        "used_mb": round(used / 1024, 2),
                        "free_mb": round(free / 1024, 2),
                        "available_mb": round(available / 1024, 2),
                        "buffers_mb": round(buffers / 1024, 2),
                        "cached_mb": round(cached / 1024, 2),
                        "usage_percent": round((used / total * 100), 2) if total > 0 else 0
                    }
            except Exception as e:
                mem_info = {"error": f"无法读取内存信息: {str(e)}"}

        elif system == "Darwin":  # macOS
            try:
                result = subprocess.run(['vm_stat'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    page_size = 4096

                    free_pages = 0
                    for line in lines:
                        if 'Pages free' in line:
                            free_pages = int(line.split(':')[1].strip().rstrip('.'))
                        elif 'Pages active' in line:
                            active_pages = int(line.split(':')[1].strip().rstrip('.'))
                        elif 'Pages inactive' in line:
                            inactive_pages = int(line.split(':')[1].strip().rstrip('.'))
                        elif 'Pages speculative' in line:
                            speculative_pages = int(line.split(':')[1].strip().rstrip('.'))

                    free_mb = round(free_pages * page_size / 1024 / 1024, 2)
                    active_mb = round(active_pages * page_size / 1024 / 1024, 2)
                    inactive_mb = round(inactive_pages * page_size / 1024 / 1024, 2)

                    mem_info = {
                        "free_mb": free_mb,
                        "active_mb": active_mb,
                        "inactive_mb": inactive_mb,
                        "usage_estimate_mb": active_mb + inactive_mb
                    }
            except:
                mem_info = {"error": "无法读取 macOS 内存信息"}

        elif system == "Windows":
            try:
                import psutil
                mem = psutil.virtual_memory()
                mem_info = {
                    "total_mb": round(mem.total / 1024 / 1024, 2),
                    "available_mb": round(mem.available / 1024 / 1024, 2),
                    "used_mb": round(mem.used / 1024 / 1024, 2),
                    "usage_percent": mem.percent
                }
            except ImportError:
                mem_info = {"error": "需要安装 psutil 库"}

        return json_output(
            "success",
            data=mem_info,
            metadata={"os_type": system}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_disk(path: str = None) -> str:
    """获取磁盘信息"""
    try:
        if path is None:
            path = os.getcwd()

        disk_usage = shutil.disk_usage(path)

        return json_output(
            "success",
            data={
                "path": path,
                "total_gb": round(disk_usage.total / 1024 / 1024 / 1024, 2),
                "used_gb": round(disk_usage.used / 1024 / 1024 / 1024, 2),
                "free_gb": round(disk_usage.free / 1024 / 1024 / 1024, 2),
                "usage_percent": round((disk_usage.used / disk_usage.total * 100), 2)
            }
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_network() -> str:
    """获取网络信息"""
    try:
        system = platform.system()
        network_info = {"interfaces": []}

        if system == "Linux":
            try:
                # 读取网络接口信息
                net_dev_path = '/proc/net/dev'
                if os.path.exists(net_dev_path):
                    with open(net_dev_path, 'r') as f:
                        lines = f.readlines()[2:]  # 跳过前两行
                        for line in lines:
                            if ':' in line:
                                parts = line.split(':')
                                iface = parts[0].strip()
                                stats = parts[1].split()
                                network_info["interfaces"].append({
                                    "interface": iface,
                                    "rx_bytes": int(stats[0]) if len(stats) > 0 else 0,
                                    "rx_packets": int(stats[1]) if len(stats) > 1 else 0,
                                    "tx_bytes": int(stats[8]) if len(stats) > 8 else 0,
                                    "tx_packets": int(stats[9]) if len(stats) > 9 else 0
                                })
            except:
                network_info["error"] = "无法读取网络接口信息"

        elif system == "Darwin":
            try:
                result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                if result.returncode == 0:
                    # 解析 ifconfig 输出（简化版）
                    interfaces = []
                    current_iface = None
                    for line in result.stdout.split('\n'):
                        if line and not line.startswith('\t'):
                            if current_iface:
                                interfaces.append(current_iface)
                            parts = line.split(':')
                            if len(parts) >= 2:
                                current_iface = {"interface": parts[0].strip()}
                    if current_iface:
                        interfaces.append(current_iface)
                    network_info["interfaces"] = interfaces
            except:
                network_info["error"] = "无法读取 macOS 网络信息"

        return json_output(
            "success",
            data=network_info,
            metadata={"os_type": system}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_uptime() -> str:
    """获取系统运行时间"""
    try:
        uptime_seconds = 0
        system = platform.system()

        if system == "Linux":
            try:
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.read().split()[0])
            except:
                pass

        elif system == "Darwin":
            try:
                result = subprocess.run(['sysctl', '-n', 'kern.boottime'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    boot_time = int(result.stdout.strip().split()[1].replace(',', ''))
                    uptime_seconds = datetime.datetime.now().timestamp() - boot_time
            except:
                pass

        elif system == "Windows":
            try:
                import psutil
                uptime_seconds = (datetime.datetime.now() -
                                datetime.datetime.fromtimestamp(psutil.boot_time())).total_seconds()
            except ImportError:
                uptime_seconds = 0

        uptime_hours = uptime_seconds / 3600
        uptime_days = uptime_hours / 24

        return json_output(
            "success",
            data={
                "uptime_seconds": round(uptime_seconds, 2),
                "uptime_minutes": round(uptime_seconds / 60, 2),
                "uptime_hours": round(uptime_hours, 2),
                "uptime_days": round(uptime_days, 2)
            }
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_env() -> str:
    """获取环境变量"""
    try:
        env_vars = dict(os.environ)
        # 过滤敏感信息
        sensitive_keys = ['PASSWORD', 'TOKEN', 'SECRET', 'KEY', 'AUTH']
        for key in list(env_vars.keys()):
            if any(sensitive in key.upper() for sensitive in sensitive_keys):
                env_vars[key] = "***REDACTED***"

        return json_output(
            "success",
            data={
                "count": len(env_vars),
                "variables": env_vars
            },
            metadata={"sensitive_filtered": True}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_all() -> str:
    """获取所有系统信息"""
    try:
        results = {
            "system": json.loads(action_system()),
            "cpu": json.loads(action_cpu()),
            "memory": json.loads(action_memory()),
            "disk": json.loads(action_disk()),
            "network": json.loads(action_network()),
            "uptime": json.loads(action_uptime())
        }

        return json_output(
            "success",
            data=results,
            metadata={"comprehensive": True}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def main():
    parser = argparse.ArgumentParser(description="CLI 系统信息工具")
    parser.add_argument("--action", required=True, choices=[
        "system", "cpu", "memory", "disk", "network", "uptime", "env", "all"
    ], help="信息类型")

    parser.add_argument("--path", help="磁盘路径（仅用于 disk 操作）")

    args = parser.parse_args()

    # 路由到对应操作
    if args.action == "system":
        result = action_system()
    elif args.action == "cpu":
        result = action_cpu()
    elif args.action == "memory":
        result = action_memory()
    elif args.action == "disk":
        result = action_disk(args.path)
    elif args.action == "network":
        result = action_network()
    elif args.action == "uptime":
        result = action_uptime()
    elif args.action == "env":
        result = action_env()
    elif args.action == "all":
        result = action_all()
    else:
        result = json_output("error", error=f"未知操作: {args.action}")

    print(result)


if __name__ == "__main__":
    main()
