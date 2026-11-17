#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BusyBox 兜底层 · PerceptionNode 能力层第三级（保命层）

设计定位（对齐 tool-node-redesign-proposal.md §3/§9 Step 4）：
    Rust 二进制(主) → Python 原型 toolnode.py(回退) → BusyBox(保命)

触发条件（由 perception_node._execute_toolnode 判定并路由）：
    1. 能力层入口全缺：既无 toolnode(.exe) 也无 toolnode.py
    2. 能力层崩溃：subprocess spawn 失败（OSError）/ 输出非合法契约（非 JSON）
    正常错误契约（exit 1 + 合法 JSON，如 COMMAND_TIMEOUT）**不**触发本层——那是业务结果，非崩溃。

实现约束（BusyBox 哲学）：
    - 纯 Python 标准库，零第三方依赖；内嵌于治理层进程，只要 PerceptionNode 活即活。
    - 仅覆盖"保命"核心子集：fs.read/write/list/stat/copy/move/delete/mkdir、proc.list、sys.all、exec.run。
    - 不支持的 op 返回 BUSYBOX_UNSUPPORTED（明确告知调用方兜底层能力边界，不静默假装成功）。
    - 返回与 toolnode 完全一致的统一契约，metadata 额外标 backend="busybox" 便于可观测区分。

防静默失败（沿用 agent-behavior-guide §2，与 Rust 层一致）：
    - 写入类 → 回读磁盘确认，返 bytes_written/sha256/verified_on_disk
    - 检索类 → 返 source_timestamp（来源 mtime）
"""

import os
import shutil
import hashlib
import socket
import platform
import subprocess
import time
import json
from datetime import datetime, timezone
from typing import Dict, Any


# ==================== 参数 Schema（与 toolnode.py 对齐，保命模式下供治理层校验复用） ====================
# 当 toolnode.py 缺失时，perception_node 回退从此处取 SCHEMAS，保证保命模式下参数校验仍生效。
SCHEMAS: Dict[str, Dict[str, Any]] = {
    "fs": {
        "read":   {"required": ["path"], "properties": {"path": "string", "encoding": "string", "max_bytes": "integer"}},
        "write":  {"required": ["path", "content"], "properties": {"path": "string", "content": "string", "mode": "string", "encoding": "string"}},
        "list":   {"required": ["path"], "properties": {"path": "string", "pattern": "string", "recursive": "boolean"}},
        "copy":   {"required": ["src", "dst"], "properties": {"src": "string", "dst": "string"}},
        "move":   {"required": ["src", "dst"], "properties": {"src": "string", "dst": "string"}},
        "delete": {"required": ["path"], "properties": {"path": "string"}},
        "mkdir":  {"required": ["path"], "properties": {"path": "string", "parents": "boolean"}},
        "stat":   {"required": ["path"], "properties": {"path": "string"}},
        "search": {"required": ["path", "pattern"], "properties": {"path": "string", "pattern": "string", "max_depth": "integer"}},
    },
    "sys": {
        "cpu":    {"required": [], "properties": {}},
        "mem":    {"required": [], "properties": {}},
        "disk":   {"required": [], "properties": {"path": "string"}},
        "net":    {"required": [], "properties": {}},
        "uptime": {"required": [], "properties": {}},
        "env":    {"required": [], "properties": {"key": "string"}},
        "all":    {"required": [], "properties": {}},
    },
    "proc": {
        "list":   {"required": [], "properties": {"pattern": "string"}},
        "search": {"required": ["pattern"], "properties": {"pattern": "string"}},
        "detail": {"required": ["pid"], "properties": {"pid": "integer"}},
        "kill":   {"required": ["pid"], "properties": {"pid": "integer", "signal": "integer"}},
        "tree":   {"required": [], "properties": {}},
        "stats":  {"required": [], "properties": {}},
    },
    "exec": {
        "run":    {"required": ["command"], "properties": {"command": "string", "timeout": "integer", "cwd": "string"}},
    },
}


# ==================== 危险命令网关（与 Rust/Python 原型保持一致） ====================

_DANGER_SUBSTR = (
    "rm -rf ~", "rm -rf /", "sudo rm", "mkfs", "dd if=/dev/",
    ":(){", ": () {", "> /dev/sd", "shutdown", "reboot", "format",
    "chkdsk", "powershell -enc",
)


def _is_dangerous(cmd: str):
    c = cmd.lower()
    for pat in _DANGER_SUBSTR:
        if pat in c:
            return "danger pattern matched"
    if ("curl" in c or "wget" in c) and "|" in c:
        return "pipe to curl/wget"
    if "python" in c and "-c" in c and "import" in c and "os" in c:
        return "python -c import os"
    return None


# ==================== 时间 / 契约工具 ====================

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _mtime_iso(path: str) -> str:
    try:
        m = os.path.getmtime(path)
        return datetime.fromtimestamp(m, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except OSError:
        return ""


def _ok(data, tid, start, op=None):
    return {
        "status": "success",
        "data": data,
        "error": None,
        "metadata": {
            "trace_id": tid,
            "duration_seconds": round(time.time() - start, 4),
            "backend": "busybox",
        },
        "trace_id": tid,
        "timestamp": _now_iso(),
    }


def _err(code, message, tid, start, retryable=False):
    return {
        "status": "error",
        "data": None,
        "error": {"code": code, "message": message, "retryable": retryable},
        "metadata": {
            "trace_id": tid,
            "duration_seconds": round(time.time() - start, 4),
            "backend": "busybox",
        },
        "trace_id": tid,
        "timestamp": _now_iso(),
    }


def _unsupported(group, op, tid, start):
    return _err(
        "BUSYBOX_UNSUPPORTED",
        f"busybox fallback does not implement {group}.{op} (保命层仅覆盖核心 fs/proc.list/sys.all/exec.run)",
        tid, start, retryable=False,
    )


# ==================== fs 组 ====================

def _fs(op, params, tid, start):
    if op == "read":
        path = params.get("path")
        if not path:
            return _err("INVALID_PARAMS", "path required", tid, start)
        try:
            with open(path, "rb") as f:
                raw = f.read()
        except FileNotFoundError:
            return _err("PATH_NOT_FOUND", f"not found: {path}", tid, start)
        except PermissionError:
            return _err("PERMISSION_DENIED", f"denied: {path}", tid, start)
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        try:
            content = raw.decode("utf-8")
            binary = False
        except UnicodeDecodeError:
            content = None
            binary = True
        return _ok({
            "path": os.path.abspath(path),
            "size_bytes": len(raw),
            "encoding": params.get("encoding", "utf-8"),
            "source_timestamp": _mtime_iso(path),
            "content": content,
            "binary": binary,
        }, tid, start)

    if op == "write":
        path = params.get("path")
        content = params.get("content")
        if not path or content is None:
            return _err("INVALID_PARAMS", "path and content required", tid, start)
        try:
            # 二进制写入：避免 Windows 文本模式 \n→\r\n 静默改写（Q4，与 Rust 层一致）
            data = content.encode("utf-8") if isinstance(content, str) else content
            with open(path, "wb") as f:
                f.write(data)
            # 防静默失败：回读磁盘确认
            with open(path, "rb") as f:
                on_disk = f.read()
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        sha = hashlib.sha256(on_disk).hexdigest()
        snippet = content.replace("\n", " ")[:120] if isinstance(content, str) else ""
        return _ok({
            "path": os.path.abspath(path),
            "exists": os.path.exists(path),
            "bytes_written": len(on_disk),
            "encoding": params.get("encoding", "utf-8"),
            "sha256": sha,
            "summary": snippet,
            "verified_on_disk": on_disk == data,
        }, tid, start)

    if op == "list":
        path = params.get("path", "")
        if not path:
            return _err("INVALID_PARAMS", "path required", tid, start)
        if not os.path.isdir(path):
            return _err("PATH_NOT_FOUND", f"not a dir: {path}", tid, start)
        entries = []
        try:
            for name in os.listdir(path):
                p = os.path.join(path, name)
                try:
                    st = os.stat(p)
                    entries.append({
                        "name": name,
                        "path": p,
                        "size": st.st_size,
                        "mtime": int(st.st_mtime),
                    })
                except OSError:
                    entries.append({"name": name, "path": p})
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        return _ok({"path": os.path.abspath(path), "count": len(entries), "entries": entries}, tid, start)

    if op == "stat":
        path = params.get("path")
        if not path:
            return _err("INVALID_PARAMS", "path required", tid, start)
        try:
            st = os.stat(path)
        except FileNotFoundError:
            return _err("PATH_NOT_FOUND", f"not found: {path}", tid, start)
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        return _ok({
            "path": os.path.abspath(path),
            "size": st.st_size,
            "is_dir": os.path.isdir(path),
            "mtime": _mtime_iso(path),
            "ctime": datetime.fromtimestamp(st.st_ctime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }, tid, start)

    if op == "copy":
        src, dst = params.get("src"), params.get("dst")
        if not src or not dst:
            return _err("INVALID_PARAMS", "src and dst required", tid, start)
        try:
            shutil.copy2(src, dst)
        except FileNotFoundError:
            return _err("PATH_NOT_FOUND", f"not found: {src}", tid, start)
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        return _ok({"src": os.path.abspath(src), "dst": dst, "done": True}, tid, start)

    if op == "move":
        src, dst = params.get("src"), params.get("dst")
        if not src or not dst:
            return _err("INVALID_PARAMS", "src and dst required", tid, start)
        try:
            shutil.move(src, dst)
        except FileNotFoundError:
            return _err("PATH_NOT_FOUND", f"not found: {src}", tid, start)
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        return _ok({"src": src, "dst": dst, "done": True}, tid, start)

    if op == "delete":
        path = params.get("path")
        if not path:
            return _err("INVALID_PARAMS", "path required", tid, start)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except FileNotFoundError:
            return _err("PATH_NOT_FOUND", f"not found: {path}", tid, start)
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        return _ok({"path": path, "deleted": True}, tid, start)

    if op == "mkdir":
        path = params.get("path")
        if not path:
            return _err("INVALID_PARAMS", "path required", tid, start)
        try:
            if params.get("parents", True):
                os.makedirs(path, exist_ok=True)
            else:
                os.mkdir(path)
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        return _ok({"path": os.path.abspath(path), "created": True}, tid, start)

    # fs.search / 其它：保命层不实现
    return _unsupported("fs", op, tid, start)


# ==================== sys 组（保命基础版） ====================

def _sys(op, params, tid, start):
    if op == "all":
        du = shutil.disk_usage(os.path.abspath(params.get("path") or (".") if os.name == "nt" else "/"))
        return _ok({
            "platform": "windows" if os.name == "nt" else "linux",
            "python": platform.python_version(),
            "hostname": socket.gethostname(),
            "cpu_count": os.cpu_count() or 0,
            "disk": {
                "path": params.get("path", ""),
                "total_bytes": du.total,
                "used_bytes": du.used,
                "free_bytes": du.free,
                "percent_used": round(du.used / du.total * 100, 1) if du.total else 0,
            },
            "backend": "busybox",
        }, tid, start)
    if op in ("cpu", "mem", "disk", "net", "uptime", "env"):
        # 保命层不细化各 sys 子项；sys.all 已给摘要，子项返 UNSUPPORTED 引导调用方用 all
        return _unsupported("sys", op, tid, start)
    return _unsupported("sys", op, tid, start)


# ==================== proc 组（保命：仅 list） ====================

def _proc(op, params, tid, start):
    if op == "list":
        procs = []
        try:
            if os.name == "nt":
                out = subprocess.run(
                    ["tasklist", "/fo", "csv", "/nh"],
                    capture_output=True, text=True, timeout=15,
                ).stdout
                for line in out.splitlines():
                    parts = line.strip().strip('"').split('","')
                    if len(parts) >= 2 and parts[1].isdigit():
                        procs.append({"pid": int(parts[1]), "name": parts[0]})
            else:
                for d in os.listdir("/proc"):
                    if d.isdigit():
                        try:
                            with open(f"/proc/{d}/comm") as f:
                                procs.append({"pid": int(d), "name": f.read().strip()})
                        except OSError:
                            continue
        except OSError as e:
            return _err("EXECUTION_ERROR", str(e), tid, start, retryable=True)
        pat = params.get("pattern", "").lower()
        if pat:
            procs = [p for p in procs if pat in (p.get("name") or "").lower()]
        procs = procs[:200]
        return _ok({"count": len(procs), "processes": procs}, tid, start)
    return _unsupported("proc", op, tid, start)


# ==================== exec 组（保命：受控执行 + 危险网关） ====================

def _exec(op, params, tid, start):
    if op != "run":
        return _unsupported("exec", op, tid, start)
    cmd = params.get("command")
    if not cmd:
        return _err("INVALID_PARAMS", "command required", tid, start)
    reason = _is_dangerous(cmd)
    if reason:
        return _err("DANGEROUS_COMMAND_BLOCKED",
                    f"command matches danger pattern: {reason}", tid, start, retryable=False)
    timeout = params.get("timeout", 60)
    shell = "cmd" if os.name == "nt" else "sh"
    flag = "/C" if os.name == "nt" else "-c"
    try:
        cp = subprocess.run(
            [shell, flag, cmd],
            capture_output=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return _err("COMMAND_TIMEOUT", f"command exceeded {timeout}s", tid, start, retryable=False)
    except OSError as e:
        return _err("COMMAND_FAILED", str(e), tid, start, retryable=False)
    return _ok({
        "command": cmd,
        "returncode": cp.returncode,
        "stdout": cp.stdout.decode("utf-8", errors="replace"),
        "stderr": cp.stderr.decode("utf-8", errors="replace"),
        "timeout": timeout,
    }, tid, start)


# ==================== 统一分发 ====================

_DISPATCH = {"fs": _fs, "sys": _sys, "proc": _proc, "exec": _exec}


def execute(group, op, params, trace_id=""):
    """BusyBox 兜底入口。返回与 toolnode 一致的统一契约（metadata.backend="busybox"）。

    参数:
        group: fs / sys / proc / exec
        op: 操作名
        params: dict 参数
        trace_id: 调用方注入的 trace_id（空则自生成）
    """
    start = time.time()
    tid = trace_id or f"trace_busybox_{int(start*1000)}"
    if not isinstance(params, dict):
        params = {}
    handler = _DISPATCH.get(group)
    if handler is None:
        return _err("UNKNOWN_GROUP", f"unknown group: {group}", tid, start)
    try:
        return handler(op, params, tid, start)
    except Exception as e:
        # 保命层自身异常绝不裸抛——兜底层崩了就没下一级了，必须包成契约
        return _err("BUSYBOX_INTERNAL_ERROR", f"{type(e).__name__}: {e}", tid, start, retryable=False)


# ==================== CLI 自测入口（便于独立验证） ====================

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) < 2:
        print(json.dumps(_err("INVALID_PARAMS",
                              "usage: busybox_fallback <group> <op> --params <json> [--trace-id <tid>]",
                              "", time.time())))
        sys.exit(2)
    g, o = args[0], args[1]
    pjson, tid = "", ""
    i = 2
    while i < len(args):
        if args[i] == "--params" and i + 1 < len(args):
            pjson = args[i + 1]; i += 2
        elif args[i] == "--trace-id" and i + 1 < len(args):
            tid = args[i + 1]; i += 2
        else:
            i += 1
    p = json.loads(pjson) if pjson else {}
    contract = execute(g, o, p, tid)
    print(json.dumps(contract, ensure_ascii=False))
    sys.exit(0 if contract["status"] == "success" else 1)
