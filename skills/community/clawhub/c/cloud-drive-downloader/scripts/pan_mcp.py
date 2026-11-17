#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cloud-drive-downloader 的最小 stdio MCP 服务器（纯 Python，无第三方依赖）。

暴露给 Agent 的工具：
  - pan_doctor    : 环境检查（JSON）
  - pan_route     : 一次链接路由与预检（JSON）
  - pan_auth      : 秒级登录/授权检查（JSON）
  - pan_engines   : 零客户端引擎桥目录（JSON）
  - pan_detect    : 识别网盘（JSON）
  - pan_dirs      : 默认下载目录（JSON）
  - pan_get_plan  : 生成 dry-run 下载计划（JSON，不打码省略凭据）

注册到 Codex（<codex-home>/config.toml）示例：
  [mcp_servers.pan-cloud-drive]
  command = "<pan-root>/scripts/pan_mcp.py"
  enabled = true

协议遵循 MCP stdio JSON-RPC：initialize / notifications/initialized / tools/list / tools/call / ping。
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

SCRIPT_DIR = Path(__file__).resolve().parent
PAN_PY = SCRIPT_DIR / "pan.py"
SERVER_NAME = "pan-cloud-drive"
SERVER_VERSION = "0.6.1-r3"

TOOLS: Dict[str, Dict[str, Any]] = {
    "pan_doctor": {
        "description": "检查网盘下载环境（Python、curl、系统凭据库、共享引擎、默认目录），返回 JSON。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "pan_detect": {
        "description": "识别分享链接属于哪个网盘，返回 drive/key、显示名与推荐引擎。",
        "inputSchema": {
            "type": "object",
            "properties": {"url": {"type": "string", "description": "网盘分享链接或直链"}},
            "required": ["url"],
        },
    },
    "pan_get": {
        "description": "实际下载（默认 dry_run=true 只出计划）。设 dry_run=false 才真正下载；--json 输出。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "to": {"type": "string", "description": "保存目录（默认配置目录）"},
                "pwd": {"type": "string"},
                "engine": {"type": "string"},
                "tier": {"type": "string", "enum": ["free", "vip", "auto"]},
                "path": {"type": "string"},
                "dry_run": {"type": "boolean", "default": True},
            },
            "required": ["url"],
        },
    },
    "pan_task": {
        "description": "任务控制：list（默认）或 pause/resume/delete/retry + id。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["list", "pause", "resume", "delete", "retry"], "default": "list"},
                "id": {"type": "string"},
                "state": {"type": "string", "description": "list 过滤：running/done/failed/paused/cancelled"},
            },
        },
    },
    "pan_dirs": {
        "description": "返回默认下载根目录与示例任务目录。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "pan_get_plan": {
        "description": "为一条下载链接生成 dry-run 计划（JSON），只读不下发文件；可带提取码/路径/tier。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "pwd": {"type": "string", "description": "分享提取码（非账号密码）"},
                "path": {"type": "string", "description": "AList 中已挂载路径"},
                "tier": {"type": "string", "enum": ["free", "vip", "auto"]},
            },
            "required": ["url"],
        },
    },
    "pan_route": {
        "description": "链接一次路由：识别、登录门禁、预检、零客户端桥和下一步动作；纯本地，不联网。默认返回省 token 的简要 JSON。",
        "inputSchema": {"type":"object","properties":{"url":{"type":"string"},"pwd":{"type":"string"},"path":{"type":"string"},"tier":{"type":"string","enum":["free","vip","auto"]},"brief":{"type":"boolean","default":True}},"required":["url"]},
    },
    "pan_auth": {
        "description": "收到链接后立即做纯本地登录/授权检查；返回 login_required、blocking 和统一登录页。",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]},
    },
    "pan_engines": {
        "description": "查看零客户端引擎桥、适用范围和本地兼容回退；可选传 url。",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}}},
    },
    "pan_test": {
        "description": "测试一条下载链接是否就绪（只读，不下载）：识别网盘、检查依赖/提码、目标目录可写性，返回 JSON。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "pwd": {"type": "string", "description": "分享提取码（非账号密码）"},
                "path": {"type": "string", "description": "AList/WebDAV 已挂载路径"},
                "tier": {"type": "string", "enum": ["free", "vip", "auto"]},
            },
            "required": ["url"],
        },
    },
}


def _env() -> Dict[str, str]:
    env = dict(os.environ)
    env.setdefault("PYTHONPYCACHEPREFIX", "/tmp/pan-mcp-pycache")
    return env


def run_cli(args, timeout=60):
    cmd = [sys.executable or "python3", str(PAN_PY)] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=_env())
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "{\"ok\": false, \"error\": \"%s\"}" % str(exc), True
    text = (proc.stdout or "").strip() or (proc.stderr or "").strip()
    try:
        json.loads(text)
        return text, proc.returncode != 0
    except json.JSONDecodeError:
        return json.dumps({"ok": proc.returncode == 0, "text": text}, ensure_ascii=False), proc.returncode != 0


def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    args = arguments or {}
    if name == "pan_doctor":
        text, is_err = run_cli(["doctor", "--json"])
    elif name == "pan_route":
        cmd = ["route", str(args.get("url", "")), "--json"]
        if args.get("pwd"):
            cmd += ["--pwd", str(args["pwd"])]
        if args.get("path"):
            cmd += ["--path", str(args["path"])]
        if args.get("tier"):
            cmd += ["--tier", str(args["tier"])]
        if args.get("brief", True):
            cmd += ["--brief"]
        text, is_err = run_cli(cmd)
    elif name == "pan_auth":
        text, is_err = run_cli(["auth", str(args.get("url", "")), "--json"])
    elif name == "pan_engines":
        cmd = ["engines", "--json"]
        if args.get("url"):
            cmd = ["engines", str(args.get("url")), "--json"]
        text, is_err = run_cli(cmd)
    elif name == "pan_detect":
        text, is_err = run_cli(["detect", str(args.get("url", ""))])
    elif name == "pan_dirs":
        text, is_err = run_cli(["dirs", "--json"])
    elif name == "pan_get_plan":
        cmd = ["get", str(args.get("url", "")), "--dry-run", "--json"]
        if args.get("pwd"):
            cmd += ["--pwd", str(args["pwd"])]
        if args.get("path"):
            cmd += ["--path", str(args["path"])]
        if args.get("tier"):
            cmd += ["--tier", str(args["tier"])]
        text, is_err = run_cli(cmd)
    elif name == "pan_get":
        cmd = ["get", str(args.get("url", "")), "--json"]
        if args.get("to"):
            cmd += ["--to", str(args["to"])]
        if args.get("pwd"):
            cmd += ["--pwd", str(args["pwd"])]
        if args.get("engine"):
            cmd += ["--engine", str(args["engine"])]
        if args.get("tier"):
            cmd += ["--tier", str(args["tier"])]
        if args.get("path"):
            cmd += ["--path", str(args["path"])]
        if not bool(args.get("dry_run", True)):
            pass  # 真下载：不加 --dry-run
        else:
            cmd += ["--dry-run"]
        text, is_err = run_cli(cmd)
    elif name == "pan_task":
        action = str(args.get("action") or "list")
        if action == "list":
            cmd = ["task", "--json", "list"]
            if args.get("state"):
                cmd += ["--state", str(args["state"])]
        else:
            cmd = ["task", action, str(args.get("id", ""))]
        text, is_err = run_cli(cmd)
    elif name == "pan_test":
        cmd = ["test", str(args.get("url", "")), "--json"]
        if args.get("pwd"):
            cmd += ["--pwd", str(args["pwd"])]
        if args.get("path"):
            cmd += ["--path", str(args["path"])]
        if args.get("tier"):
            cmd += ["--tier", str(args["tier"])]
        text, is_err = run_cli(cmd)
    else:
        return {"content": [{"type": "text", "text": "未知工具：%s" % name}], "isError": True}
    return {"content": [{"type": "text", "text": text}], "isError": is_err}


def handle(msg: Dict[str, Any]) -> Dict[str, Any]:
    method = msg.get("method", "")
    params = msg.get("params") or {}
    if method == "initialize":
        return {
            "protocolVersion": params.get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            "instructions": "该 MCP 服务器用于统一网盘下载：识别、目录规划与 dry-run 计划。凭据一律不出口、不打码参数全部隐藏；实际下载请调用本机 pan.py（CLI）。",
        }
    if method == "tools/list":
        return {"tools": [{"name": k, "description": v["description"], "inputSchema": v["inputSchema"]} for k, v in TOOLS.items()]}
    if method == "tools/call":
        name = str(params.get("name", ""))
        return call_tool(name, params.get("arguments") or {})
    if method == "ping":
        return {}
    raise ValueError("unknown method: %s" % method)


def main() -> int:
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("method") == "notifications/initialized":
            continue
        try:
            result = handle(msg)
        except Exception as exc:  # noqa: BLE001
            response = {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32601, "message": str(exc)}}
        else:
            response = {"jsonrpc": "2.0", "id": msg.get("id"), "result": result}
        if msg.get("id") is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
