#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 进程管理工具 - 工具化封装
查看进程列表、搜索进程、获取进程详情等
"""

import os
import sys
import json
import argparse
import subprocess
import signal
import platform
from typing import Dict, Any, List
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


def action_list(user_only: bool = False, name_filter: str = None) -> str:
    """获取进程列表"""
    try:
        system = platform.system()
        processes = []

        if system == "Linux" or system == "Darwin":
            # 使用 ps 命令获取进程列表
            cmd = ['ps', 'aux']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                lines = result.stdout.split('\n')[1:]  # 跳过标题行
                for line in lines:
                    if not line.strip():
                        continue

                    parts = line.split(None, 10)
                    if len(parts) < 11:
                        continue

                    username = parts[0]
                    pid = int(parts[1])
                    cpu = float(parts[2])
                    mem = float(parts[3])
                    command = parts[10]

                    # 过滤条件
                    if user_only and username != os.getlogin():
                        continue
                    if name_filter and name_filter.lower() not in command.lower():
                        continue

                    processes.append({
                        "pid": pid,
                        "user": username,
                        "cpu_percent": cpu,
                        "memory_percent": mem,
                        "command": command
                    })

        elif system == "Windows":
            # 使用 tasklist 命令
            cmd = ['tasklist', '/fo', 'csv']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                import csv
                lines = result.stdout.split('\n')[1:]  # 跳过标题行
                for line in lines:
                    if not line.strip():
                        continue

                    reader = csv.reader([line])
                    for row in reader:
                        if len(row) >= 5:
                            pid = int(row[1].strip('"'))
                            name = row[0].strip('"')
                            mem = row[4].strip('"')

                            # 过滤条件
                            if name_filter and name_filter.lower() not in name.lower():
                                continue

                            processes.append({
                                "pid": pid,
                                "name": name,
                                "memory": mem,
                                "command": name
                            })

        # 按 CPU 使用率排序
        if system in ["Linux", "Darwin"]:
            processes.sort(key=lambda x: x["cpu_percent"], reverse=True)

        return json_output(
            "success",
            data={
                "processes": processes[:100],  # 限制返回数量
                "count": len(processes),
                "system": system
            },
            metadata={"user_only": user_only, "name_filter": name_filter}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_search(name: str) -> str:
    """搜索进程"""
    try:
        return action_list(user_only=False, name_filter=name)
    except Exception as e:
        return json_output("error", error=str(e))


def action_detail(pid: int) -> str:
    """获取进程详细信息"""
    try:
        system = platform.system()
        detail = {"pid": pid}

        if system == "Linux":
            # 读取 /proc/[pid]/status
            status_path = f'/proc/{pid}/status'
            if os.path.exists(status_path):
                with open(status_path, 'r') as f:
                    for line in f:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            detail[key.strip()] = value.strip()

            # 读取 /proc/[pid]/cmdline
            cmdline_path = f'/proc/{pid}/cmdline'
            if os.path.exists(cmdline_path):
                with open(cmdline_path, 'r') as f:
                    cmdline = f.read().replace('\x00', ' ')
                    detail["command_line"] = cmdline

            # 读取 /proc/[pid]/stat
            stat_path = f'/proc/{pid}/stat'
            if os.path.exists(stat_path):
                with open(stat_path, 'r') as f:
                    stat_data = f.read().split()
                    if len(stat_data) > 13:
                        detail["utime"] = stat_data[13]
                        detail["stime"] = stat_data[14]

        elif system == "Darwin":
            # 使用 ps 获取详情
            result = subprocess.run(['ps', '-p', str(pid), '-o', 'pid,ppid,user,%cpu,%mem,command'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    parts = lines[1].split(None, 5)
                    if len(parts) >= 6:
                        detail.update({
                            "pid": parts[0],
                            "ppid": parts[1],
                            "user": parts[2],
                            "cpu": parts[3],
                            "memory": parts[4],
                            "command": parts[5]
                        })

        elif system == "Windows":
            # 使用 tasklist 获取详情
            result = subprocess.run(['tasklist', '/fi', f'PID eq {pid}', '/fo', 'csv', '/v'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                import csv
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    reader = csv.reader([lines[1]])
                    for row in reader:
                        if len(row) >= 8:
                            detail.update({
                                "name": row[0].strip('"'),
                                "pid": row[1].strip('"'),
                                "memory": row[4].strip('"'),
                                "status": row[7].strip('"')
                            })

        return json_output(
            "success",
            data=detail,
            metadata={"system": system}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_kill(pid: int, signal_name: str = None) -> str:
    """终止进程"""
    try:
        if signal_name is None:
            signal_name = "TERM"  # 默认使用 SIGTERM

        # 信号映射
        signal_map = {
            "TERM": signal.SIGTERM,
            "KILL": signal.SIGKILL,
            "INT": signal.SIGINT,
            "HUP": signal.SIGHUP
        }

        sig = signal_map.get(signal_name.upper(), signal.SIGTERM)

        os.kill(pid, sig)

        return json_output(
            "success",
            data={
                "pid": pid,
                "signal": signal_name.upper(),
                "message": f"已向进程 {pid} 发送 {signal_name.upper()} 信号"
            }
        )
    except ProcessLookupError:
        return json_output("error", error=f"进程 {pid} 不存在")
    except PermissionError:
        return json_output("error", error=f"权限不足，无法终止进程 {pid}")
    except Exception as e:
        return json_output("error", error=str(e))


def action_tree(pid: int = None) -> str:
    """获取进程树"""
    try:
        system = platform.system()
        tree = []

        if system == "Linux":
            # 使用 pstree 命令
            cmd = ['pstree', '-p', '-s', '-l'] if pid else ['pstree', '-p', '-A']
            if pid:
                cmd.append(str(pid))

            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    tree.append({"raw": result.stdout})
                else:
                    tree.append({"error": "pstree 命令不可用"})
            except FileNotFoundError:
                tree.append({"error": "pstree 未安装"})

            # 如果 pstree 不可用，尝试使用 ps 构建
            if not tree or "error" in tree[0]:
                result = subprocess.run(['ps', '-eo', 'pid,ppid,comm'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')[1:]
                    process_map = {}
                    root_processes = []

                    for line in lines:
                        if not line.strip():
                            continue
                        parts = line.split()
                        if len(parts) >= 3:
                            ppid = int(parts[1])
                            if ppid == 0:
                                root_processes.append({"pid": int(parts[0]), "name": parts[2]})
                            else:
                                process_map[int(parts[0])] = {
                                    "pid": int(parts[0]),
                                    "ppid": ppid,
                                    "name": parts[2]
                                }

                    tree.append({"roots": root_processes, "processes": list(process_map.values())})

        elif system == "Darwin":
            result = subprocess.run(['ps', '-axo', 'pid,ppid,comm'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')[1:]
                process_list = []
                for line in lines:
                    if not line.strip():
                        continue
                    parts = line.split(None, 2)
                    if len(parts) >= 3:
                        process_list.append({
                            "pid": int(parts[0]),
                            "ppid": int(parts[1]),
                            "name": parts[2]
                        })
                tree.append({"processes": process_list})

        elif system == "Windows":
            # Windows 不支持进程树
            tree.append({"info": "Windows 不支持进程树功能"})

        return json_output(
            "success",
            data={"tree": tree},
            metadata={"system": system, "pid": pid}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def action_stats() -> str:
    """获取进程统计信息"""
    try:
        list_result = json.loads(action_list())
        if list_result["status"] != "success":
            return list_result

        processes = list_result["data"]["processes"]

        # 计算统计信息
        total_count = len(processes)

        cpu_values = [p.get("cpu_percent", 0) for p in processes if "cpu_percent" in p]
        mem_values = [p.get("memory_percent", 0) for p in processes if "memory_percent" in p]

        top_cpu = sorted(processes, key=lambda x: x.get("cpu_percent", 0), reverse=True)[:5]
        top_mem = sorted(processes, key=lambda x: x.get("memory_percent", 0), reverse=True)[:5]

        stats = {
            "total_processes": total_count,
            "avg_cpu": round(sum(cpu_values) / len(cpu_values), 2) if cpu_values else 0,
            "avg_memory": round(sum(mem_values) / len(mem_values), 2) if mem_values else 0,
            "top_cpu_processes": top_cpu,
            "top_memory_processes": top_mem
        }

        return json_output(
            "success",
            data=stats,
            metadata={"sample_size": len(processes)}
        )
    except Exception as e:
        return json_output("error", error=str(e))


def main():
    parser = argparse.ArgumentParser(description="CLI 进程管理工具")
    parser.add_argument("--action", required=True, choices=[
        "list", "search", "detail", "kill", "tree", "stats"
    ], help="操作类型")

    # 列表参数
    parser.add_argument("--user-only", action="store_true", help="仅显示当前用户进程")
    parser.add_argument("--name-filter", help="进程名过滤")

    # 搜索参数
    parser.add_argument("--name", help="搜索进程名")

    # 详情参数
    parser.add_argument("--pid", type=int, help="进程 ID")

    # 终止参数
    parser.add_argument("--signal", choices=["TERM", "KILL", "INT", "HUP"],
                       help="信号类型（默认：TERM）")

    args = parser.parse_args()

    # 路由到对应操作
    if args.action == "list":
        result = action_list(args.user_only, args.name_filter)
    elif args.action == "search":
        result = action_search(args.name)
    elif args.action == "detail":
        result = action_detail(args.pid)
    elif args.action == "kill":
        result = action_kill(args.pid, args.signal)
    elif args.action == "tree":
        result = action_tree(args.pid)
    elif args.action == "stats":
        result = action_stats()
    else:
        result = json_output("error", error=f"未知操作: {args.action}")

    print(result)


if __name__ == "__main__":
    main()
