#!/usr/bin/env python3
"""
runtime_health_check.py — Autofix v6.0 M1: Runtime Health Detection

Checks OpenClaw runtime status beyond static config:
  1. Gateway process & RPC connectivity
  2. Model endpoint connectivity (lightweight)
  3. Recent log error/warning pattern analysis
  4. Session file backlog health

Output: structured JSON with severity levels (🔴/🟠/🟡/🟢)

Usage:
    python scripts/runtime_health_check.py [--json] [--verbose]

Integration:
    This script is called by the autofix workflow after `openclaw doctor`
    to add runtime-level diagnostics.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
import signal

# ── Configuration ──────────────────────────────────────────────────────────

HOME_DIR = Path.home()
OPENCLAW_DIR = HOME_DIR / ".openclaw"
AGENTS_DIR = OPENCLAW_DIR / "agents"
LOGS_DIR = OPENCLAW_DIR / "logs"
TEMP_LOG_DIR = Path(os.environ.get("TEMP", "/tmp")) / "openclaw"
WORKSPACE_DIR = OPENCLAW_DIR / "workspace"

THRESHOLDS = {
    "disk_warn_mb": 1000,       # 🟡 warn at 1GB
    "disk_crit_mb": 5000,       # 🔴 crit at 5GB
    "session_count_warn": 100,  # 🟡 warn at 100 session files
    "log_size_warn_mb": 50,     # 🟠 warn at 50MB log
    "log_error_window_m": 60,   # scan errors in last 60 min
    "rpc_timeout_s": 5,         # RPC check timeout
}


# ── Helpers ────────────────────────────────────────────────────────────────

def run_cmd(cmd: list, timeout_s: int = 15) -> dict:
    """Run a command and return {ok, stdout, stderr, returncode}.
    Uses CREATE_NEW_PROCESS_GROUP + taskkill to ensure children die on timeout.
    """
    import subprocess as _sp
    proc = None
    try:
        proc = _sp.Popen(
            cmd,
            stdout=_sp.PIPE,
            stderr=_sp.PIPE,
            text=True,
            shell=True,
            creationflags=_sp.CREATE_NEW_PROCESS_GROUP if hasattr(_sp, 'CREATE_NEW_PROCESS_GROUP') else 0,
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout_s)
            return {
                "ok": proc.returncode == 0,
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
                "returncode": proc.returncode,
            }
        except _sp.TimeoutExpired:
            # Kill the entire process tree
            try:
                _sp.run(['taskkill', '/F', '/T', '/PID', str(proc.pid)],
                       capture_output=True, timeout=5)
            except Exception:
                proc.kill()
                proc.wait(5)
            return {"ok": False, "stdout": "", "stderr": "TIMEOUT", "returncode": -1}
    except FileNotFoundError:
        return {"ok": False, "stdout": "", "stderr": "command not found", "returncode": -2}


def sev(s: str) -> str:
    """Normalize severity string."""
    return s.strip("🔴🟠🟡🟢").strip()


def result(status: str, title: str, detail: str = "", suggestion: str = "") -> dict:
    return {
        "severity": status,
        "title": title,
        "detail": detail,
        "suggestion": suggestion,
    }


# ── Checks ─────────────────────────────────────────────────────────────────

def check_gateway_status() -> dict:
    """Check Gateway process and RPC status via `openclaw gateway status --json`."""
    r = run_cmd(["openclaw", "gateway", "status", "--json"], timeout_s=15)
    if not r["ok"]:
        return result("🔴", "Gateway 状态检测失败",
                      detail=f"命令执行错误: {r['stderr'] or r['stdout']}",
                      suggestion="检查 openclaw CLI 是否可用，或运行 openclaw gateway restart")

    try:
        data = json.loads(r["stdout"])
    except json.JSONDecodeError as e:
        return result("🔴", "Gateway 状态解析失败",
                      detail=f"JSON 解析错误: {e}",
                      suggestion="手动运行 openclaw gateway status --json 诊断")

    issues = []

    # ── service status ──
    svc = data.get("service", {})
    runtime = svc.get("runtime", {})
    status = runtime.get("status", "unknown")
    pid = runtime.get("pid")

    if status != "running":
        issues.append(result("🔴", f"Gateway 状态: {status}（应为 running）",
                             detail=f"PID: {pid}",
                             suggestion="运行 openclaw gateway restart"))
    elif not pid:
        issues.append(result("🟠", "Gateway 进程 PID 为空",
                             detail="status=running 但无 PID",
                             suggestion="可能存在僵尸进程，建议重启"))
    else:
        issues.append(result("🟢", f"Gateway 运行中",
                             detail=f"PID: {pid}, 端口: {data.get('gateway', {}).get('port', '?')}"))

    # ── RPC connectivity ──
    rpc = data.get("rpc", {})
    rpc_ok = rpc.get("ok", False)
    if rpc_ok:
        auth = rpc.get("auth", {})
        issues.append(result("🟢", "RPC 连接正常",
                             detail=f"角色: {auth.get('role', '?')}, "
                                    f"版本: {rpc.get('server', {}).get('version', '?')}"))
    else:
        issues.append(result("🔴", "RPC 连接异常",
                             detail=f"kind={rpc.get('kind', '?')}",
                             suggestion="重启 Gateway 通常可修复 RPC 断开"))

    # ── config audit ──
    config_audit = svc.get("configAudit", {})
    if not config_audit.get("ok", True):
        cfg_issues = config_audit.get("issues", [])
        issues.append(result("🟠", f"配置审计发现 {len(cfg_issues)} 个问题",
                             detail="; ".join(str(i) for i in cfg_issues[:5]),
                             suggestion="运行 openclaw doctor --fix 修复配置问题"))

    return {
        "severity": max(i["severity"] for i in issues),
        "title": "Gateway 运行状态",
        "checks": issues,
        "raw": data,
    }


def check_disk_usage() -> dict:
    """Check .openclaw directory disk usage.
    Uses os.scandir for faster traversal; skips large subdirs like sessions/archive."""
    SKIP_DIRS = {"archive", "sessions", "__pycache__", "node_modules", ".git"}
    try:
        total_bytes = 0
        for root, dirs, files in os.walk(str(OPENCLAW_DIR)):
            # Skip large/non-critical directories for speed
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            # Limit to at most 5000 files
            for f in files[:5000]:
                try:
                    fp = os.path.join(root, f)
                    total_bytes += os.path.getsize(fp)
                except OSError:
                    continue
        total_mb = total_bytes / (1024 * 1024)
    except Exception as e:
        return result("🟡", "磁盘用量检查失败", detail=str(e))

    if total_mb >= THRESHOLDS["disk_crit_mb"]:
        sev = "🔴"
        suggestion = "清理 logs/ 和 sessions/ 目录中的旧文件"
    elif total_mb >= THRESHOLDS["disk_warn_mb"]:
        sev = "🟠"
        suggestion = "考虑清理旧 session 记录和日志"
    else:
        sev = "🟢"
        suggestion = ""

    return result(sev, f".openclaw 目录用量: {total_mb:.0f} MB",
                  detail=f"阈值: ⚠️ {THRESHOLDS['disk_warn_mb']}MB / 🔴 {THRESHOLDS['disk_crit_mb']}MB",
                  suggestion=suggestion)


def check_session_backlog() -> dict:
    """Check session file count in agents/main/sessions (active only, not archive)."""
    sessions_dir = AGENTS_DIR / "main" / "sessions"
    total_files = 0
    if sessions_dir.exists():
        total_files = len(list(sessions_dir.glob("*.jsonl")))

    if total_files >= THRESHOLDS["session_count_warn"]:
        return result("🟡", f"Session 文件积压: {total_files} 个",
                      detail=f"阈值: {THRESHOLDS['session_count_warn']} 个",
                      suggestion="运行 openclaw doctor --fix 自动归档孤立文件")
    return result("🟢", f"Session 文件状态正常: {total_files} 个")


def check_log_errors() -> dict:
    """Scan recent logs for error/warning patterns."""
    log_files = []
    if TEMP_LOG_DIR.exists():
        log_files.extend(sorted(TEMP_LOG_DIR.glob("openclaw-*.log"), key=os.path.getmtime, reverse=True)[:3])
    if LOGS_DIR.exists():
        log_files.extend(
            f for f in LOGS_DIR.iterdir() if f.suffix in (".log", ".jsonl")
        )

    if not log_files:
        return result("🟡", "日志文件未找到", detail=f"扫描路径: {TEMP_LOG_DIR}, {LOGS_DIR}")

    error_patterns = [
        (re.compile(r'"logLevelName":"ERROR"', re.I), "ERROR"),
        (re.compile(r'"logLevelName":"WARN"', re.I), "WARN"),
        (re.compile(r'(\[31m|\x1b\[38;2;226;61;45m)', re.I), "VISIBLE_ERROR"),
        (re.compile(r'tool.*failed|tool.*error|tool.*exception', re.I), "TOOL_ERROR"),
        (re.compile(r'ECONNREFUSED|ETIMEDOUT|ENOTFOUND', re.I), "NETWORK_ERROR"),
        (re.compile(r'RateLimitError|429|rate limit', re.I), "RATE_LIMIT"),
    ]

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=THRESHOLDS["log_error_window_m"])
    counts = {"ERROR": 0, "WARN": 0, "VISIBLE_ERROR": 0, "TOOL_ERROR": 0, "NETWORK_ERROR": 0, "RATE_LIMIT": 0}
    recent_errors = []

    for lf in log_files:
        try:
            size_mb = lf.stat().st_size / (1024 * 1024)
            if size_mb > THRESHOLDS["log_size_warn_mb"]:
                counts.setdefault("LOG_TOO_LARGE", 0)
                counts["LOG_TOO_LARGE"] += 1

            with open(lf, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Try to parse timestamp from JSONL
                    try:
                        rec = json.loads(line)
                        ts_str = rec.get("time") or rec.get("timestamp") or rec.get("_meta", {}).get("time", "")
                        if ts_str:
                            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                            if ts < cutoff:
                                continue
                    except (json.JSONDecodeError, ValueError):
                        pass

                    for pattern, label in error_patterns:
                        if pattern.search(line):
                            counts[label] = counts.get(label, 0) + 1
                            if label in ("ERROR", "VISIBLE_ERROR", "TOOL_ERROR", "NETWORK_ERROR"):
                                if len(recent_errors) < 5:
                                    # Truncate long lines
                                    truncated = line[:200] + "..." if len(line) > 200 else line
                                    recent_errors.append(f"[{label}] {truncated}")
                            break
        except Exception:
            continue

    total_errors = sum(counts.get(k, 0) for k in ("ERROR", "VISIBLE_ERROR", "TOOL_ERROR", "NETWORK_ERROR"))

    if total_errors > 20:
        sev = "🔴"
        suggestion = "日志中出现大量错误，建议手动检查最新日志文件"
    elif total_errors > 5:
        sev = "🟠"
        suggestion = f"近期有 {total_errors} 个错误/异常，建议关注"
    elif total_errors > 0:
        sev = "🟡"
        suggestion = ""
    else:
        sev = "🟢"
        suggestion = ""

    detail_parts = [f"{k}: {v}" for k, v in counts.items() if v > 0]
    if recent_errors:
        detail_parts.append("最近错误:")
        detail_parts.extend(f"  {e}" for e in recent_errors)

    return result(sev, f"日志异常扫描（最近 {THRESHOLDS['log_error_window_m']} 分钟）",
                  detail=" | ".join(detail_parts) if detail_parts else "无异常",
                  suggestion=suggestion)


def check_model_connectivity() -> dict:
    """
    Lightweight model endpoint connectivity check.
    Reads configured providers from openclaw.json and tests endpoints.
    Only tests up to MAX_PROVIDERS_TO_TEST providers to avoid hanging.
    """
    MAX_PROVIDERS_TO_TEST = 3
    config_path = OPENCLAW_DIR / "openclaw.json"
    if not config_path.exists():
        return result("🟡", "模型连通性检查跳过", detail="openclaw.json 未找到")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return result("🟡", "模型配置解析失败", detail=str(e))

    # Extract provider endpoints from config
    providers = config.get("providers", {})
    if not providers:
        return result("🟡", "模型连通性检查跳过", detail="配置中未定义 providers")

    checks = []
    # Only test first MAX_PROVIDERS_TO_TEST providers with a baseUrl
    testable = [(name, p) for name, p in providers.items()
                if p.get("baseUrl", "") or p.get("baseURL", "")]
    
    if not testable:
        return result("🟡", "模型连通性检查跳过",
                      detail=f"扫描了 {len(providers)} 个 provider，但未找到可测试的 baseUrl")

    total = len(testable)
    for name, p_cfg in testable[:MAX_PROVIDERS_TO_TEST]:
        base_url = p_cfg.get("baseUrl", "") or p_cfg.get("baseURL", "") or ""
        api_key = p_cfg.get("apiKey", "") or p_cfg.get("key", "") or ""

        # Strip trailing slash and standardize
        base_url = base_url.rstrip("/")

        # Determine which endpoint to hit
        if "/v1/" not in base_url:
            test_url = f"{base_url}/v1/models"
        else:
            test_url = f"{base_url}/models" if "models" not in base_url else base_url

        try:
            req = urllib.request.Request(test_url, method="GET")
            if api_key:
                req.add_header("Authorization", f"Bearer {api_key[:8]}...")
            req.add_header("User-Agent", "OpenClaw-Autofix/6.0")
            req.add_header("Connection", "close")  # Force close to avoid keep-alive hangs

            start = time.time()
            with urllib.request.urlopen(req, timeout=4) as resp:
                elapsed = (time.time() - start) * 1000
                if resp.status == 200:
                    checks.append(result("🟢", f" provider [{name}] 可达",
                                         detail=f"响应 {elapsed:.0f}ms"))
                else:
                    checks.append(result("🟠", f" provider [{name}] 返回异常",
                                         detail=f"HTTP {resp.status} ({elapsed:.0f}ms)"))
        except urllib.error.HTTPError as e:
            if e.code == 401:
                checks.append(result("🟠", f" provider [{name}] 认证失败",
                                     detail="HTTP 401，API Key 可能无效"))
            elif e.code == 404:
                checks.append(result("🟡", f" provider [{name}] 端点异常",
                                     detail=f"HTTP {e.code}，可能端点路径不同"))
            else:
                checks.append(result("🟠", f" provider [{name}] 不可达",
                                     detail=f"HTTP {e.code}: {e.reason}"))
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            checks.append(result("🟡", f" provider [{name}] 连接超时/失败",
                                 detail=str(e)[:80],
                                 suggestion="检查网络连接或 baseUrl 配置"))

    if total > MAX_PROVIDERS_TO_TEST:
        checks.append(result("🟡", f"模型连通性检查",
                             detail=f"已测试 {MAX_PROVIDERS_TO_TEST}/{total} 个 provider"))

    combined_sev = "🟢"
    if checks:
        sev_order = {"🔴": 0, "🟠": 1, "🟡": 2, "🟢": 3}
        combined_sev = min(checks, key=lambda c: sev_order.get(c.get("severity", "🟢"), 99))["severity"]

    return {
        "severity": combined_sev,
        "title": "模型端点连通性",
        "checks": checks,
    }


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv

    if not as_json:
        print(f"🔍 OpenClaw Runtime Health Check v6.0-M1")
        print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   工作目录: {OPENCLAW_DIR}")
        print()

    # Run all checks
    checks = {
        "gateway": check_gateway_status(),
        "disk": check_disk_usage(),
        "sessions": check_session_backlog(),
        "logs": check_log_errors(),
        "models": check_model_connectivity(),
    }

    # Determine overall severity
    sev_order = {"🔴": 0, "🟠": 1, "🟡": 2, "🟢": 3}
    overall = "🟢"
    for name, c in checks.items():
        if isinstance(c, dict):
            cs = c.get("severity", "🟢")
            if cs in sev_order and sev_order.get(cs, 3) < sev_order.get(overall, 3):
                overall = cs

    # Summary header
    summary_counts = {"🔴": 0, "🟠": 0, "🟡": 0, "🟢": 0}
    for name, c in checks.items():
        if isinstance(c, dict):
            cs = c.get("severity", "🟢")
            if cs in summary_counts:
                summary_counts[cs] += 1

    if as_json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "tool": "runtime_health_check",
            "version": "6.0-M1",
            "overall_severity": overall,
            "summary": {f"{k}": v for k, v in summary_counts.items()},
            "checks": checks,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
        return

    # ── Human-readable output ──
    print(f"{'='*60}")
    print(f"  整体健康等级: {overall}")
    print(f"  🔴 阻断: {summary_counts['🔴']}  🟠 高风险: {summary_counts['🟠']}"
          f"  🟡 可优化: {summary_counts['🟡']}  🟢 正常: {summary_counts['🟢']}")
    print(f"{'='*60}")
    print()

    for name, c in checks.items():
        if not isinstance(c, dict):
            continue
        label_map = {
            "gateway": "🌐 Gateway 状态",
            "disk": "💾 磁盘用量",
            "sessions": "📋 Session 积压",
            "logs": "📜 日志异常",
            "models": "🔌 模型连通性",
        }
        label = label_map.get(name, name)
        sev_icon = c.get("severity", "🟢")
        title = c.get("title", "")
        detail = c.get("detail", "")
        suggestion = c.get("suggestion", "")

        print(f"  {sev_icon} {label}")
        if title:
            print(f"       {title}")
        if detail:
            print(f"       详情: {detail}")
        if suggestion:
            print(f"       建议: {suggestion}")

        # Sub-checks
        sub_checks = c.get("checks", [])
        if sub_checks:
            for sc in sub_checks:
                if isinstance(sc, dict):
                    sc_sev = sc.get("severity", "  ")
                    sc_title = sc.get("title", "")
                    sc_detail = sc.get("detail", "")
                    print(f"     {sc_sev} {sc_title}")
                    if verbose and sc_detail:
                        print(f"            {sc_detail}")
        print()

    # ── Action items ──
    action_items = []
    for name, c in checks.items():
        if isinstance(c, dict) and c.get("severity") in ("🔴", "🟠"):
            suggestion = c.get("suggestion", "")
            if suggestion:
                action_items.append(f"  {c['severity']} [{name}] {suggestion}")
        sub_checks = c.get("checks", [])
        for sc in sub_checks:
            if isinstance(sc, dict) and sc.get("suggestion"):
                action_items.append(f"  {sc['severity']} {sc['suggestion']}")

    if action_items:
        print(f"{'='*60}")
        print("  📋 建议操作")
        print(f"{'='*60}")
        for item in action_items:
            print(item)
        print()

    print(f"{'='*60}")
    print(f"  耗时: {time.process_time():.1f}s  |  运行: python scripts/runtime_health_check.py")
    print()


if __name__ == "__main__":
    main()
