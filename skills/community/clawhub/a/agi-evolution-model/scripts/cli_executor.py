#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 通用命令执行器 - 工具化封装
支持 bash、cmd、powershell 命令执行
"""

import os
import sys
import json
import argparse
import subprocess
import shlex
import shutil
import platform
import re
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


# 危险命令黑名单
DANGEROUS_COMMANDS = [
    r'rm\s+-rf\s+/',
    r'dd\s+if=/dev/zero',
    r':\(\)\{\s*:\|:&\s*\};:',
    r'mkfs\.',
    r'chmod\s+-R\s+777\s+/',
    r'chown\s+-R\s+.*\s+/',
    r'shutdown',
    r'reboot',
    r'poweroff',
    r'init\s+0',
    r'sudo\s+rm',
    r'>\s*/dev/sd',
    r'wget.*\|.*sh',
    r'curl.*\|.*sh',
]


def check_dangerous_command(command: str) -> tuple[bool, str]:
    """检查是否为危险命令"""
    cmd_lower = command.lower()
    for pattern in DANGEROUS_COMMANDS:
        if re.search(pattern, cmd_lower, re.IGNORECASE):
            return True, f"检测到危险命令模式: {pattern}"
    if re.search(r'(rm|chmod|chown).*\s+(\/etc|\/usr|\/var|\/bin|\/sbin|\/boot)\b', cmd_lower):
        return True, "禁止修改系统关键目录"
    return False, ""


def get_shell_info(system: str, shell_type: str = None) -> tuple[str, str]:
    """获取 shell 类型和可执行文件"""
    if shell_type:
        return shell_type.lower(), shell_type.lower()

    if system == "windows":
        if shutil.which("powershell"):
            return "powershell", "powershell"
        return "cmd", "cmd"
    return "bash", "bash"


def execute_command(
    command: str,
    work_dir: str = None,
    timeout: int = 60,
    env_vars: Dict[str, str] = None,
    capture_output: bool = True,
    shell_type: str = None
) -> str:
    """执行命令并返回结果"""
    is_dangerous, reason = check_dangerous_command(command)
    if is_dangerous:
        return json_output("error", error=f"命令执行被阻止: {reason}",
                         metadata={"blocked": True, "reason": reason})

    system = platform.system().lower()
    detected_shell_type, shell_executable = get_shell_info(system, shell_type)

    cwd = work_dir if work_dir else os.getcwd()
    try:
        cwd = os.path.abspath(cwd)
        if not os.path.exists(cwd):
            return json_output("error", error=f"工作目录不存在: {cwd}")
    except Exception as e:
        return json_output("error", error=f"工作目录验证失败: {str(e)}")

    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    start_time = datetime.datetime.now()
    try:
        if detected_shell_type == "powershell":
            result = subprocess.run(
                [shell_executable, "-Command", command],
                cwd=cwd,
                env=env,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                env=env,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )

        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()

        return json_output(
            "success",
            data={
                "command": command,
                "stdout": result.stdout if capture_output else "",
                "stderr": result.stderr if capture_output else "",
                "exit_code": result.returncode,
                "success": result.returncode == 0
            },
            metadata={
                "duration_seconds": round(duration, 3),
                "timeout": timeout,
                "shell_type": detected_shell_type,
                "shell_executable": shell_executable,
                "work_dir": cwd,
                "capture_output": capture_output
            }
        )

    except subprocess.TimeoutExpired:
        return json_output("error", error=f"命令执行超时（>{timeout}秒）",
                         metadata={"timeout": timeout, "duration_seconds": timeout, "command": command})
    except FileNotFoundError as e:
        return json_output("error", error=f"命令或文件不存在: {str(e)}", metadata={"command": command})
    except PermissionError as e:
        return json_output("error", error=f"权限不足: {str(e)}", metadata={"command": command})
    except Exception as e:
        return json_output("error", error=f"命令执行失败: {str(e)}",
                         metadata={"command": command, "exception_type": type(e).__name__})


def main():
    parser = argparse.ArgumentParser(description="CLI 通用命令执行器（支持 bash/cmd/powershell）")
    parser.add_argument("--action", required=True, choices=["execute"], help="执行类型")
    parser.add_argument("--command", help="要执行的命令")
    parser.add_argument("--work-dir", help="工作目录")
    parser.add_argument("--timeout", type=int, default=60, help="超时时间（秒）")
    parser.add_argument("--no-capture", action="store_true", help="不捕获输出")
    parser.add_argument("--env", action="append", help="环境变量（格式：KEY=VALUE）")
    parser.add_argument("--shell-type", choices=["bash", "cmd", "powershell"],
                       help="指定 Shell 类型（默认自动选择）")

    args = parser.parse_args()

    if not args.command:
        print(json_output("error", error="--action execute 需要 --command 参数"))
        return

    env_vars = {}
    if args.env:
        for env_pair in args.env:
            if '=' in env_pair:
                key, value = env_pair.split('=', 1)
                env_vars[key] = value

    result = execute_command(
        command=args.command,
        work_dir=args.work_dir,
        timeout=args.timeout,
        capture_output=not args.no_capture,
        env_vars=env_vars if env_vars else None,
        shell_type=args.shell_type
    )

    print(result)


if __name__ == "__main__":
    main()
