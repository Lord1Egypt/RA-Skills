#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
toolnode - 统一工具节点（PerceptionNode 能力层 · Python 原型）

设计目标（见 tool-node-redesign-proposal.md）：
- 单二进制 + 子命令（仿 BusyBox）：fs / sys / proc / exec
- 零/最小依赖：仅用标准库 + ctypes；不依赖 psutil 等第三方库
- 统一契约：所有操作返回  {status, data, error, metadata{trace_id,duration_seconds}, trace_id, timestamp}
- trace_id 贯穿：优先使用调用方传入的 trace_id，否则自生成
- 防静默失败：
    * 写入类 → 回读磁盘确认，返回 真实绝对路径 + 字节数 + sha256 + 摘要（取自磁盘，非内存 len）
    * 检索类 → 返回 来源文件 mtime（来源时间戳，非响应时刻）

本文件是被 PerceptionNode 经 subprocess/FFI 调用的能力节点；未来由 Rust 静态二进制
替换时，仅替换二进制、保持子命令与契约不变即可。

契约参考：references/tool-node-redesign-proposal.md §5
"""

import sys
import os
import io
import json
import time
import uuid
import hashlib
import argparse
import subprocess
import datetime
import re
from typing import Any, Dict, Optional
import locale

# 让同目录的 interfaces 可导入（trace_id 生成统一走这里，避免死代码）
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
try:
    from interfaces import create_trace_context
except Exception:
    create_trace_context = None


# ==================== 参数 Schema（自描述，供本节点与 PerceptionNode 共用） ====================

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


# ==================== 危险命令网关（受控执行） ====================

# 原型级黑名单：覆盖典型破坏性/逃逸模式。注意：黑名单是下限而非银弹，
# 真实强隔离应结合沙箱/权限；此处仅作"明显危险"拦截。
DANGER_PATTERNS = [
    r"\brm\s+-rf\s+~", r"\brm\s+-rf\s+/\b", r"\bsudo\s+rm\b", r"\bmkfs\b",
    r"\bdd\b.*\bif=/dev/", r":\(\)\s*\{", r">\s*/dev/sd", r"\bshutdown\b",
    r"\breboot\b", r"\bformat\b", r"\bchkdsk\b", r"\bcurl\b.*\|", r"\bwget\b.*\|",
    r"\bpython\b.*-c\b.*import\s+os", r"\bpowershell\b.*-enc",
]

_danger_re = [re.compile(p, re.IGNORECASE) for p in DANGER_PATTERNS]


def _is_dangerous(cmd: str) -> Optional[str]:
    for pat, rx in zip(DANGER_PATTERNS, _danger_re):
        if rx.search(cmd):
            return pat
    return None


# ==================== 契约构造 ====================

class ToolNodeError(Exception):
    """工具执行期错误，由 dispatch 统一转成契约 error。"""
    def __init__(self, code: str, message: str, retryable: bool = False):
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


def _decode(b: Any) -> str:
    """容错解码子进程输出：依次尝试 utf-8 → 系统编码 → GBK → latin-1。

    避免 Windows 下 cmd/powershell 以 GBK 输出、而进程以 UTF-8 模式运行时
    单猜一种编码导致的中文乱码。
    """
    if not isinstance(b, bytes):
        return b
    for enc in ("utf-8", locale.getpreferredencoding(False), "gbk", "cp936", "latin-1"):
        try:
            return b.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return b.decode("utf-8", errors="replace")


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _mk_trace(trace_id: Optional[str]) -> str:
    if trace_id:
        return trace_id
    if create_trace_context is not None:
        return create_trace_context().trace_id
    return f"trace_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:12]}"


def _ok(data: Any, trace_id: str, duration: float) -> Dict[str, Any]:
    return {
        "status": "success",
        "data": data,
        "error": None,
        "metadata": {"trace_id": trace_id, "duration_seconds": round(duration, 4)},
        "trace_id": trace_id,
        "timestamp": _now_iso(),
    }


def _err(code: str, message: str, trace_id: str, duration: float, retryable: bool = False) -> Dict[str, Any]:
    return {
        "status": "error",
        "data": None,
        "error": {"code": code, "message": message, "retryable": retryable},
        "metadata": {"trace_id": trace_id, "duration_seconds": round(duration, 4)},
        "trace_id": trace_id,
        "timestamp": _now_iso(),
    }


# ==================== 参数校验 ====================

def validate_params(group: str, op: str, params: Dict[str, Any]) -> Optional[str]:
    """返回错误信息字符串；None 表示通过。"""
    schema = SCHEMAS.get(group, {}).get(op)
    if schema is None:
        return f"unknown operation: {group}.{op}"
    missing = [r for r in schema["required"] if r not in params]
    if missing:
        return f"missing required params: {', '.join(missing)}"
    return None


# ==================== fs 组 ====================

def _op_fs(op: str, params: Dict[str, Any]) -> Any:
    if op == "read":
        path = params["path"]
        encoding = params.get("encoding", "utf-8")
        max_bytes = params.get("max_bytes", 5 * 1024 * 1024)
        with open(path, "rb") as f:
            raw = f.read(max_bytes)
        mtime = os.path.getmtime(path)
        src_ts = datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            content = raw.decode(encoding)
        except UnicodeDecodeError:
            content = None
        return {
            "path": os.path.abspath(path),
            "size_bytes": len(raw),
            "encoding": encoding,
            "source_timestamp": src_ts,   # 防静默失败：用来源 mtime，非响应时刻
            "content": content,
            "binary": content is None,
        }

    if op == "write":
        path = params["path"]
        content = params["content"]
        mode = params.get("mode", "w")
        encoding = params.get("encoding", "utf-8")
        # 二进制写入：避免 Windows 文本模式把 \n 翻成 \r\n，保证回读字节与入参逐字节一致
        # （否则 readback 会出现“内容看似一样、实则换行符被改写”的静默差异，违背 Q4 防静默失败）
        write_mode = mode if "b" in mode else mode + "b"
        with open(path, write_mode) as f:
            f.write(content.encode(encoding))
        # 防静默失败：回读磁盘确认，报告磁盘真实状态
        with open(path, "rb") as f:
            raw = f.read()
        sha = hashlib.sha256(raw).hexdigest()
        snippet = content[:120].replace("\n", " ")
        return {
            "path": os.path.abspath(path),
            "exists": os.path.exists(path),
            "bytes_written": len(raw),            # 取自磁盘，非内存 len
            "encoding": encoding,
            "sha256": sha,
            "summary": snippet,
            "verified_on_disk": True,
        }

    if op == "list":
        path = params["path"]
        pattern = params.get("pattern")
        recursive = params.get("recursive", False)
        entries = []
        walker = os.walk(path) if recursive else [(path, [], [f for f in os.listdir(path)])]
        for root, _dirs, files in walker if recursive else [(path, [], [f for f in os.listdir(path)])]:
            for name in files:
                full = os.path.join(root, name)
                if pattern and pattern not in name:
                    continue
                try:
                    st = os.stat(full)
                    entries.append({"name": name, "path": full, "size": st.st_size, "mtime": st.st_mtime})
                except OSError:
                    continue
        return {"path": os.path.abspath(path), "count": len(entries), "entries": entries}

    if op == "copy":
        import shutil
        shutil.copy2(params["src"], params["dst"])
        return {"src": os.path.abspath(params["src"]), "dst": os.path.abspath(params["dst"]), "done": True}

    if op == "move":
        import shutil
        shutil.move(params["src"], params["dst"])
        return {"src": os.path.abspath(params["src"]), "dst": os.path.abspath(params["dst"]), "done": True}

    if op == "delete":
        p = params["path"]
        if os.path.isdir(p):
            import shutil
            shutil.rmtree(p)
        else:
            os.remove(p)
        return {"path": os.path.abspath(p), "deleted": True}

    if op == "mkdir":
        p = params["path"]
        if params.get("parents", True):
            os.makedirs(p, exist_ok=True)
        else:
            os.mkdir(p)
        return {"path": os.path.abspath(p), "created": True}

    if op == "stat":
        p = params["path"]
        st = os.stat(p)
        return {
            "path": os.path.abspath(p),
            "size": st.st_size,
            "is_dir": os.path.isdir(p),
            "mtime": datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "ctime": datetime.datetime.fromtimestamp(st.st_ctime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    if op == "search":
        import fnmatch
        root = params["path"]
        pat = params["pattern"]
        max_depth = params.get("max_depth", 5)
        hits = []
        for dirpath, _dirs, files in os.walk(root):
            depth = dirpath[len(root):].count(os.sep)
            if depth > max_depth:
                continue
            for name in files:
                if fnmatch.fnmatch(name, pat):
                    hits.append(os.path.join(dirpath, name))
        return {"root": os.path.abspath(root), "pattern": pat, "count": len(hits), "matches": hits}

    raise ValueError(f"unimplemented fs op: {op}")


# ==================== sys 组（零第三方依赖） ====================

def _sys_mem() -> Dict[str, Any]:
    if sys.platform.startswith("win"):
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            ms = MEMORYSTATUSEX()
            ms.dwLength = ctypes.sizeof(ms)
            kernel.GlobalMemoryStatusEx(ctypes.byref(ms))
            total = ms.ullTotalPhys
            avail = ms.ullAvailPhys
            return {"total_bytes": total, "available_bytes": avail,
                    "used_bytes": total - avail, "percent_used": round((total - avail) / total * 100, 1)}
        except Exception as e:
            return {"error": str(e)}
    else:
        try:
            with open("/proc/meminfo") as f:
                info = {}
                for line in f:
                    k, v = line.split(":", 1)
                    info[k.strip()] = int(v.strip().split()[0]) * 1024
            total = info.get("MemTotal", 0)
            avail = info.get("MemAvailable", info.get("MemFree", 0))
            return {"total_bytes": total, "available_bytes": avail,
                    "used_bytes": total - avail, "percent_used": round((total - avail) / total * 100, 1)}
        except Exception as e:
            return {"error": str(e)}


def _sys_cpu() -> Dict[str, Any]:
    if sys.platform.startswith("win"):
        try:
            out = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_Processor).LoadPercentage"],
                capture_output=True, timeout=15)
            val = _decode(out.stdout).strip()
            return {"load_percent": int(val) if val.isdigit() else None, "platform": "windows"}
        except Exception:
            return {"note": "cpu load unavailable on windows without psutil", "platform": "windows"}
    else:
        try:
            with open("/proc/loadavg") as f:
                avg = f.read().split()
            with open("/proc/cpuinfo") as f:
                ncpu = sum(1 for l in f if l.startswith("processor"))
            return {"load_1m": float(avg[0]), "load_5m": float(avg[1]),
                    "load_15m": float(avg[2]), "cores": ncpu, "platform": "linux"}
        except Exception as e:
            return {"error": str(e), "platform": "linux"}


def _sys_disk(path: str = None) -> Dict[str, Any]:
    import shutil
    p = path or ("C:\\" if sys.platform.startswith("win") else "/")
    try:
        usage = shutil.disk_usage(p)
        return {"path": p, "total_bytes": usage.total, "used_bytes": usage.used,
                "free_bytes": usage.free, "percent_used": round(usage.used / usage.total * 100, 1)}
    except Exception as e:
        return {"path": p, "error": str(e)}


def _sys_net() -> Dict[str, Any]:
    try:
        import socket
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            ip = None
        return {"hostname": hostname, "ip": ip}
    except Exception as e:
        return {"error": str(e)}


def _sys_uptime() -> Dict[str, Any]:
    if sys.platform.startswith("win"):
        try:
            out = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime"],
                capture_output=True, timeout=15)
            boot = _decode(out.stdout).strip()
            if boot:
                try:
                    bt = datetime.datetime.fromisoformat(boot)
                    secs = (datetime.datetime.now() - bt).total_seconds()
                    return {"boot_time": boot, "seconds": secs, "days": round(secs / 86400, 2)}
                except Exception:
                    return {"boot_time": boot}
            return {"note": "uptime unavailable"}
        except Exception:
            return {"note": "uptime unavailable on windows"}
    else:
        try:
            with open("/proc/uptime") as f:
                secs = float(f.read().split()[0])
            return {"seconds": secs, "days": round(secs / 86400, 2)}
        except Exception as e:
            return {"error": str(e)}


def _op_sys(op: str, params: Dict[str, Any]) -> Any:
    if op == "cpu":
        return _sys_cpu()
    if op == "mem":
        return _sys_mem()
    if op == "disk":
        return _sys_disk(params.get("path"))
    if op == "net":
        return _sys_net()
    if op == "uptime":
        return _sys_uptime()
    if op == "env":
        key = params.get("key")
        if key:
            return {"key": key, "value": os.environ.get(key)}
        return {"count": len(os.environ), "sample_keys": list(os.environ.keys())[:20]}
    if op == "all":
        return {
            "cpu": _sys_cpu(),
            "mem": _sys_mem(),
            "disk": _sys_disk(),
            "net": _sys_net(),
            "uptime": _sys_uptime(),
            "platform": sys.platform,
            "python": sys.version.split()[0],
        }
    raise ValueError(f"unimplemented sys op: {op}")


# ==================== proc 组 ====================

def _proc_list(pattern: str = None) -> Dict[str, Any]:
    procs = []
    if sys.platform.startswith("win"):
        try:
            out = subprocess.run(["tasklist", "/fo", "csv", "/nh"],
                                  capture_output=True, text=True, timeout=15)
            for line in out.stdout.splitlines():
                parts = line.strip().strip('"').split('","')
                if len(parts) >= 2:
                    name, pid = parts[0], parts[1]
                    if pattern and pattern.lower() not in name.lower():
                        continue
                    procs.append({"pid": int(pid), "name": name})
        except Exception as e:
            return {"error": str(e)}
    else:
        for pid in os.listdir("/proc"):
            if not pid.isdigit():
                continue
            try:
                with open(f"/proc/{pid}/comm") as f:
                    name = f.read().strip()
                if pattern and pattern not in name:
                    continue
                procs.append({"pid": int(pid), "name": name})
            except OSError:
                continue
    return {"count": len(procs), "processes": procs[:200]}


def _op_proc(op: str, params: Dict[str, Any]) -> Any:
    if op == "list":
        return _proc_list(params.get("pattern"))
    if op == "search":
        return _proc_list(params["pattern"])
    if op == "detail":
        pid = params["pid"]
        if sys.platform.startswith("win"):
            try:
                out = subprocess.run(["tasklist", "/fo", "list", "/fi", f"PID eq {pid}"],
                                      capture_output=True, text=True, timeout=10)
                return {"pid": pid, "raw": out.stdout[:1000]}
            except Exception as e:
                return {"error": str(e)}
        try:
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                cmdline = f.read().replace(b"\x00", b" ").decode(errors="replace").strip()
            with open(f"/proc/{pid}/status") as f:
                status = f.read()[:800]
            return {"pid": pid, "cmdline": cmdline, "status": status}
        except OSError as e:
            return {"error": str(e)}
    if op == "kill":
        pid = params["pid"]
        sig = params.get("signal", 15)
        try:
            if sys.platform.startswith("win"):
                subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True, timeout=10)
            else:
                os.kill(pid, sig)
            return {"pid": pid, "killed": True}
        except Exception as e:
            return {"error": str(e)}
    if op == "tree":
        return _proc_list()
    if op == "stats":
        data = _proc_list()
        return {"count": data.get("count", 0), "note": "process count summary"}
    raise ValueError(f"unimplemented proc op: {op}")


# ==================== exec 组（受控） ====================

def _op_exec(op: str, params: Dict[str, Any]) -> Any:
    if op == "run":
        cmd = params["command"]
        danger = _is_dangerous(cmd)
        if danger:
            raise ToolNodeError("DANGEROUS_COMMAND_BLOCKED",
                                f"command matches danger pattern: {danger}", retryable=False)
        timeout = params.get("timeout", 60)
        cwd = params.get("cwd")
        try:
            proc = subprocess.run(cmd, shell=True, capture_output=True,
                                   timeout=timeout, cwd=cwd)
            stdout = _decode(proc.stdout)
            stderr = _decode(proc.stderr)
            return {
                "command": cmd,
                "returncode": proc.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "timeout": timeout,
            }
        except subprocess.TimeoutExpired:
            raise ToolNodeError("COMMAND_TIMEOUT", f"command exceeded {timeout}s", retryable=False)
        except Exception as e:
            raise ToolNodeError("COMMAND_FAILED", str(e), retryable=False)
    raise ValueError(f"unimplemented exec op: {op}")


# ==================== 统一分发 ====================

_DISPATCH = {
    "fs": _op_fs,
    "sys": _op_sys,
    "proc": _op_proc,
    "exec": _op_exec,
}


def dispatch(group: str, op: str, params: Dict[str, Any], trace_id: Optional[str] = None) -> Dict[str, Any]:
    """核心分发：返回统一契约 dict。供 PerceptionNode 经 subprocess 调用，或本文件直接调用测试。"""
    tid = _mk_trace(trace_id)
    start = time.time()
    if group not in SCHEMAS:
        return _err("UNKNOWN_GROUP", f"unknown group: {group}", tid, time.time() - start)
    if op not in SCHEMAS[group]:
        return _err("UNKNOWN_OP", f"unknown op: {group}.{op}", tid, time.time() - start)
    verr = validate_params(group, op, params)
    if verr:
        return _err("INVALID_PARAMS", verr, tid, time.time() - start, retryable=False)
    try:
        data = _DISPATCH[group](op, params)
        return _ok(data, tid, time.time() - start)
    except FileNotFoundError as e:
        return _err("PATH_NOT_FOUND", str(e), tid, time.time() - start, retryable=False)
    except PermissionError as e:
        return _err("PERMISSION_DENIED", str(e), tid, time.time() - start, retryable=False)
    except ToolNodeError as e:
        return _err(e.code, e.message, tid, time.time() - start, retryable=e.retryable)
    except Exception as e:
        return _err("EXECUTION_ERROR", f"{type(e).__name__}: {e}", tid, time.time() - start, retryable=True)


# ==================== CLI 入口 ====================

def main():
    parser = argparse.ArgumentParser(description="toolnode - 统一工具节点（fs/sys/proc/exec）")
    parser.add_argument("group", choices=["fs", "sys", "proc", "exec"])
    parser.add_argument("op")
    parser.add_argument("--params", default="{}", help="JSON string of parameters")
    parser.add_argument("--trace-id", default=None, help="trace_id from caller (PerceptionNode)")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError as e:
        print(json.dumps(_err("BAD_PARAMS_JSON", str(e), args.trace_id or "", 0.0),
                         ensure_ascii=False))
        sys.exit(2)

    # exec 的 timeout 透传
    if args.group == "exec" and "timeout" not in params:
        params["timeout"] = args.timeout

    result = dispatch(args.group, args.op, params, args.trace_id)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
