#!/usr/bin/env python3
"""
OpenClaw Bridge Caller
调用 openclaw-bridge CLI 来操作 Revit
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

# 配置 - 从环境变量读取，支持自定义
REVIT_MCP_URL = os.environ.get("REVIT_MCP_URL", "http://localhost:18181")
BRIDGE_DIR = Path(os.environ.get("OPENCLAW_BRIDGE_DIR", Path.home() / "repos" / "openclaw-bridge"))


def run_bridge_command(command: str, args: dict | None = None) -> dict:
    """
    运行 bridge CLI 命令
    
    Args:
        command: 命令类型，如 "health", "tools list", "tools call <name>"
        args: 工具参数（仅用于 tools call）
    
    Returns:
        dict: 命令结果
    """
    # 构建 uv run 命令
    cmd_parts = [
        "uv", "run",
        "--with", "httpx",
        "--with", "click",
        "python", "-m", "openclaw_bridge.cli"
    ]
    
    # 添加子命令
    cmd_parts.extend(command.split())
    
    # 如果是 tools call，添加参数
    if "tools call" in command and args:
        cmd_parts.extend(["--args", json.dumps(args)])
    
    try:
        result = subprocess.run(
            cmd_parts,
            cwd=BRIDGE_DIR,
            capture_output=True,
            text=True,
            timeout=60,
            env={**subprocess.os.environ, "REVIT_MCP_URL": REVIT_MCP_URL}
        )
        
        # 尝试解析 JSON 输出（可能跨多行）
        stdout = result.stdout.strip()
        
        # 找到第一个 { 和最后一个 }
        start_idx = stdout.find('{')
        end_idx = stdout.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = stdout[start_idx:end_idx + 1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                return {
                    "error": True,
                    "message": f"Failed to parse JSON: {e}",
                    "raw": json_str
                }
        else:
            return {
                "error": True,
                "message": f"No JSON object found in output: {stdout}",
                "stderr": result.stderr
            }
            
    except subprocess.TimeoutExpired:
        return {"error": True, "message": "Command timed out"}
    except Exception as e:
        return {"error": True, "message": str(e)}


def health() -> dict:
    """检查 Revit 状态"""
    return run_bridge_command("health")


def tools_list() -> dict:
    """列出所有可用工具"""
    return run_bridge_command("tools list")


def tools_call(name: str, arguments: dict | None = None) -> dict:
    """调用指定工具"""
    return run_bridge_command(f"tools call {name}", arguments)


def main():
    """CLI 入口"""
    if len(sys.argv) < 2:
        print("Usage: revit_call.py <command> [args]")
        print("Commands: health, tools-list, tools-call")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "health":
        result = health()
    elif command == "tools-list":
        result = tools_list()
    elif command == "tools-call":
        if len(sys.argv) < 3:
            print("Usage: revit_call.py tools-call <tool-name> [json-args]")
            sys.exit(1)
        tool_name = sys.argv[2]
        tool_args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        result = tools_call(tool_name, tool_args)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()