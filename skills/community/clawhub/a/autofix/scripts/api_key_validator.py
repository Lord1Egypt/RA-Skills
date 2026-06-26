#!/usr/bin/env python3
"""
api_key_validator.py — Autofix v6.0-M2: API Key Health Validator

Validates all configured API keys in the OpenClaw environment:
  1. Key format validation (pattern matching)
  2. Lightweight endpoint ping (minimal request)
  3. Severity-graded output

Usage:
    python scripts/api_key_validator.py [--json] [--verbose]

Integration:
    Called by runtime_health_check.py as part of the unified health report.
    Also runnable standalone for targeted key diagnostics.
"""

import json
import os
import re
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────

HOME_DIR = Path.home()
OPENCLAW_DIR = HOME_DIR / ".openclaw"
WORKSPACE_DIR = OPENCLAW_DIR / "workspace"
CONFIG_PATH = OPENCLAW_DIR / "openclaw.json"

REQUEST_TIMEOUT = 3  # seconds per key test (reduced to avoid pipeline hangs)

# ── Key format patterns ───────────────────────────────────────────────────

KEY_PATTERNS = {
    "OpenAI": r"^sk-(proj-)?[A-Za-z0-9_-]{30,}$",
    "Tavily": r"^tvly-[A-Za-z0-9-]{20,}$",
    "Notion": r"^ntn_[A-Za-z0-9]{20,}$",
    "GitHub": r"^gh[pousr]_[A-Za-z0-9]{20,}$",
    "DeepSeek": r"^sk-[A-Za-z0-9_-]{20,}$",
    "Feishu": r"^[A-Za-z0-9]{24,}$",    # appSecret 通常 32 位，16 位会误判模型名
    "Generic": r"^[A-Za-z0-9_-]{16,}$",
}


def detect_key_type(key: str) -> dict:
    """Detect the service type based on key prefix/pattern.
    Returns dict with key_type and optional warning."""
    if not key:
        return {"key_type": "Unknown"}
    
    cleaned = key.strip()
    
    # Try exact match first
    for ktype, pattern in KEY_PATTERNS.items():
        if re.match(pattern, cleaned):
            return {"key_type": ktype}
    
    # Check for corrupted keys (embedded whitespace is a common copy-paste error)
    # Only flag if the text looks like a real key (starts with known prefix)
    known_prefixes = ["sk-", "tvly-", "ntn_", "ghp_", "ghu_", "gho_", "ghs_", "ghr_", "utK", "cli_"]
    has_prefix = any(cleaned.startswith(p) for p in known_prefixes)
    if any(c.isspace() for c in cleaned) and has_prefix:
        stripped = re.sub(r"\s+", "", cleaned)
        for ktype, pattern in KEY_PATTERNS.items():
            if re.match(pattern, stripped):
                return {"key_type": f"{ktype}_CORRUPTED"}
    
    return {"key_type": "Unknown"}


def mask_key(key: str) -> str:
    """Mask key for display: show first 12 and last 4 chars."""
    if len(key) <= 16:
        return key[:4] + "..." + key[-4:] if len(key) > 8 else "****"
    return key[:12] + "..." + key[-4:]


# ── Result builder ────────────────────────────────────────────────────────

def result(severity: str, title: str, detail: str = "", suggestion: str = "") -> dict:
    return {"severity": severity, "title": title, "detail": detail, "suggestion": suggestion}


# ── Individual key validators ─────────────────────────────────────────────

def validate_openai_key(key: str, label: str = "OpenAI") -> dict:
    """Test OpenAI API key by listing models (cheapest endpoint)."""
    url = "https://api.openai.com/v1/models"
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", f"Bearer {key}")
        req.add_header("User-Agent", "OpenClaw-Autofix/6.0")
        start = time.time()
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            elapsed = (time.time() - start) * 1000
            return result("🟢", f"✅ [{label}] 有效",
                          detail=f"HTTP {resp.status} ({elapsed:.0f}ms)")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return result("🔴", f"❌ [{label}] 认证失败",
                          detail="HTTP 401 — Key 无效或已撤销",
                          suggestion="检查 API Key 是否正确，或在 OpenAI 控制台重新生成")
        elif e.code == 429:
            return result("🟠", f"⚠️ [{label}] 限流",
                          detail="HTTP 429 Rate Limited",
                          suggestion="额度可能已用尽，请在 OpenAI 控制台检查用量")
        return result("🟠", f"⚠️ [{label}] 返回异常",
                      detail=f"HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return result("🔴", f"❌ [{label}] 网络不可达",
                      detail=str(e.reason),
                      suggestion="检查网络连接")
    except OSError as e:
        return result("🔴", f"❌ [{label}] 连接超时",
                      detail=str(e),
                      suggestion="检查网络连接或 API 端点")


def validate_tavily_key(key: str, label: str = "Tavily") -> dict:
    """Test Tavily API key with a minimal search."""
    url = "https://api.tavily.com/search"
    payload = json.dumps({
        "api_key": key,
        "query": "test",
        "search_depth": "basic",
        "max_results": 1,
    }).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "OpenClaw-Autofix/6.0")
        start = time.time()
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            elapsed = (time.time() - start) * 1000
            body = json.loads(resp.read().decode("utf-8"))
            # Tavily returns a results object — if we got here, key is valid
            return result("🟢", f"✅ [{label}] 有效",
                          detail=f"HTTP {resp.status} ({elapsed:.0f}ms)")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 401 or e.code == 403:
            return result("🔴", f"❌ [{label}] 认证失败",
                          detail=f"HTTP {e.code}",
                          suggestion="Key 无效，请在 Tavily 控制台检查")
        elif e.code == 429:
            return result("🟠", f"⚠️ [{label}] 达到速率限制",
                          detail="HTTP 429",
                          suggestion="请稍后再试或升级套餐")
        return result("🟠", f"⚠️ [{label}] 返回异常",
                      detail=f"HTTP {e.code}: {body[:100]}")
    except urllib.error.URLError as e:
        return result("🔴", f"❌ [{label}] 网络不可达", detail=str(e.reason))
    except OSError as e:
        return result("🔴", f"❌ [{label}] 连接超时", detail=str(e))


def validate_notion_key(key: str, label: str = "Notion") -> dict:
    """Test Notion API key by listing users."""
    url = "https://api.notion.com/v1/users"
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", f"Bearer {key}")
        req.add_header("Notion-Version", "2022-06-28")
        req.add_header("User-Agent", "OpenClaw-Autofix/6.0")
        start = time.time()
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            elapsed = (time.time() - start) * 1000
            return result("🟢", f"✅ [{label}] 有效",
                          detail=f"HTTP {resp.status} ({elapsed:.0f}ms)")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return result("🔴", f"❌ [{label}] 认证失败",
                          detail="HTTP 401",
                          suggestion="Integration token 可能已失效，请在 Notion 重新生成")
        return result("🟠", f"⚠️ [{label}] 返回异常", detail=f"HTTP {e.code}")
    except (urllib.error.URLError, OSError) as e:
        return result("🔴", f"❌ [{label}] 网络不可达", detail=str(e))


def validate_github_key(key: str, label: str = "GitHub") -> dict:
    """Test GitHub API key."""
    url = "https://api.github.com/user"
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", f"Bearer {key}")
        req.add_header("User-Agent", "OpenClaw-Autofix/6.0")
        req.add_header("Accept", "application/vnd.github.v3+json")
        start = time.time()
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            elapsed = (time.time() - start) * 1000
            body = json.loads(resp.read().decode("utf-8"))
            login = body.get("login", "?")
            return result("🟢", f"✅ [{label}] 有效 (用户: {login})",
                          detail=f"HTTP {resp.status} ({elapsed:.0f}ms)")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return result("🔴", f"❌ [{label}] 认证失败",
                          detail="HTTP 401",
                          suggestion="Token 可能已过期，请在 GitHub Settings > Tokens 重新生成")
        return result("🟠", f"⚠️ [{label}] 返回异常", detail=f"HTTP {e.code}")
    except (urllib.error.URLError, OSError) as e:
        return result("🔴", f"❌ [{label}] 网络不可达", detail=str(e))


def validate_generic_endpoint(url: str, key: str, label: str = "Generic") -> dict:
    """Generic endpoint validation: try a GET request with Bearer auth."""
    try:
        req = urllib.request.Request(url, method="GET")
        if key:
            req.add_header("Authorization", f"Bearer {key}")
        req.add_header("User-Agent", "OpenClaw-Autofix/6.0")
        start = time.time()
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            elapsed = (time.time() - start) * 1000
            return result("🟢", f"✅ [{label}] 端点可达",
                          detail=f"HTTP {resp.status} ({elapsed:.0f}ms)")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return result("🟠", f"⚠️ [{label}] 端点需认证",
                          detail="HTTP 401（如有 Key 则 Key 可能无效）")
        return result("🟡", f"ℹ️ [{label}] 端点返回 {e.code}",
                      detail=f"HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return result("🔴", f"❌ [{label}] 端点不可达", detail=str(e.reason))
    except OSError as e:
        return result("🔴", f"❌ [{label}] 连接超时", detail=str(e))


# ── Scanner ───────────────────────────────────────────────────────────────

def scan_configured_keys() -> list:
    """Scan openclaw.json and TOOLS.md for API keys and validate them."""
    keys = []  # list of {source, key_type, key_value, label}

    # ── Scan openclaw.json ──
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            keys.append({"source": "config", "error": str(e)})
            return keys

        def crawl(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    full = f"{path}.{k}" if path else k
                    if isinstance(v, str) and len(v) >= 16 and not v.startswith("http"):
                        kt_info = detect_key_type(v)
                        kt = kt_info["key_type"]
                        if kt != "Unknown" and "Generic" not in kt:
                            # Create a meaningful label based on source path
                            path_parts = full.split(".")
                            key_name = path_parts[-1] if len(path_parts) > 1 else full
                            # Special handling: gateway token vs feishu
                            if "gateway" in full and "token" in full:
                                label_name = "Gateway auth"
                                kt = "Gateway"
                            elif "feishu" in full and "secret" in full:
                                label_name = "Feishu"
                            elif "feishu" in full and "token" in full:
                                label_name = "Feishu"
                            else:
                                label_name = f"{kt} (配置)"
                            entry = {
                                "source": f"config:{full}",
                                "key_type": kt,
                                "key": v,
                                "label": label_name,
                                "key_name": key_name,
                            }
                            # Preserve corruption info if detected
                            if "CORRUPTED" in kt:
                                entry["corrupted"] = True
                            keys.append(entry)
                    crawl(v, full)
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    crawl(v, f"{path}[{i}]")

        crawl(cfg)

    # ── Scan TOOLS.md for endpoint URLs and keys ──
    tools_path = WORKSPACE_DIR / "TOOLS.md"
    if tools_path.exists():
        try:
            content = tools_path.read_text(encoding="utf-8")
            # Find API Base URLs
            for m in re.finditer(r'\*\*API Base\*\*:\s*(\S+)', content):
                url = m.group(1).strip()
                if url and url.startswith("http"):
                    keys.append({
                        "source": "tools.md:API Base",
                        "key_type": "Endpoint",
                        "key": "",
                        "label": f"Endpoint ({url[:40]}...)",
                        "url": url,
                    })
            # Find SearXNG secret_key
            for m in re.finditer(r'\*\*secret_key\*\*:\s*(\S+)', content):
                sk = m.group(1).strip()
                if sk and sk not in ("your-secret-key-here", ""):
                    st = detect_key_type(sk)["key_type"]
                    keys.append({
                        "source": "tools.md:secret_key",
                        "key_type": st,
                        "key": sk,
                        "label": f"SearXNG secret",
                    })
        except OSError:
            pass

    return keys


def validate_key(entry: dict) -> dict:
    """Dispatch key validation based on type."""
    kt = entry.get("key_type", "Unknown")
    key = entry.get("key", "")
    label = entry.get("label", kt)
    url = entry.get("url", "")

    corrupted = entry.get("corrupted", False)

    # Handle corrupted keys (embedded whitespace = copy-paste error)
    if corrupted:
        clean = re.sub(r"\s+", "", key)
        orig_type = kt.replace("_CORRUPTED", "")
        return result("🔴", f"❌ [{label}] Key 格式异常 (含空格)",
                      detail=f"推测为 {orig_type} Key，但存储时嵌入了空格字符",
                      suggestion=f"请重新复制完整 Key，确保不包含换行或空格。\n"
                                f"       修正后的 Key 预览: {mask_key(clean)}")

    if kt == "OpenAI":
        return validate_openai_key(key, label)
    elif kt == "Tavily":
        return validate_tavily_key(key, label)
    elif kt == "Notion":
        return validate_notion_key(key, label)
    elif kt == "GitHub":
        return validate_github_key(key, label)
    elif kt == "Endpoint" and url:
        return validate_generic_endpoint(url, key, label)
    elif kt == "Feishu":
        return result("🟡", f"🔑 [{label}] 格式有效 (Feishu appSecret)",
                      detail="需配合 appId 使用，无法单独端点验证")
    elif kt == "Gateway":
        return result("🟡", f"🔑 [{label}] 内部令牌，跳过在线验证",
                      detail="用于 Gateway RPC 认证")
    else:
        return result("🟡", f"🔑 [{label}] 格式有效，跳过在线验证",
                      detail=f"类型: {kt}")


# ── Resource Monitoring (P2) ──────────────────────────────────────────────

def check_resource_health() -> dict:
    """
    Enhanced resource monitoring (P2).
    Extends the disk/session checks from M1 with memory and log file metrics.
    """
    import psutil  # optional, fallback to WMI

    results = []

    # ── 1. Log file sizes ──
    log_dirs = [
        Path(os.environ.get("TEMP", "/tmp")) / "openclaw",
        OPENCLAW_DIR / "logs",
    ]
    total_log_mb = 0
    for ld in log_dirs:
        if ld.exists():
            for f in ld.iterdir():
                if f.is_file() and f.suffix in (".log", ".jsonl"):
                    total_log_mb += f.stat().st_size / (1024 * 1024)

    if total_log_mb > 50:
        results.append(result("🟠", f"📦 日志文件总大小: {total_log_mb:.0f} MB",
                              detail="超过 50MB 建议清理或配置日志轮转",
                              suggestion="清理旧日志或配置日志自动轮转"))
    elif total_log_mb > 20:
        results.append(result("🟡", f"📦 日志文件总大小: {total_log_mb:.0f} MB"))
    else:
        results.append(result("🟢", f"📦 日志文件总大小: {total_log_mb:.0f} MB"))

    # ── 2. Process memory (psutil or fallback via tasklist) ──
    try:
        import psutil
        gateway_pids = []
        for proc in psutil.process_iter(["pid", "name", "memory_info", "create_time"]):
            try:
                if proc.info["name"] and "node" in proc.info["name"].lower():
                    cmdline = proc.cmdline()
                    if any("openclaw" in p for p in cmdline):
                        mem_mb = proc.memory_info().rss / (1024 * 1024)
                        gateway_pids.append((proc.pid, mem_mb))
            except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                continue

        if gateway_pids:
            total_mem = sum(m for _, m in gateway_pids)
            if total_mem > 500:
                results.append(result("🟠", f"🧠 Gateway 进程内存: {total_mem:.0f} MB",
                                      detail=f"PID(s): {', '.join(str(p) for p,_ in gateway_pids)}",
                                      suggestion="超过 500MB，建议检查是否有内存泄漏"))
            else:
                results.append(result("🟢", f"🧠 Gateway 进程内存: {total_mem:.0f} MB",
                                      detail=f"PID(s): {', '.join(str(p) for p,_ in gateway_pids)}"))
        else:
            # Fallback to tasklist
            results.append(result("🟡", "🧠 Gateway 进程内存: 无法获取（psutil 未安装）",
                                  detail="可通过 pip install psutil 安装"))
    except ImportError:
        # Fallback — try tasklist
        try:
            import subprocess
            r = subprocess.run(
                'tasklist /FI "IMAGENAME eq node.exe" /FO CSV /NH',
                capture_output=True, text=True, timeout=5, shell=True
            )
            if r.returncode == 0:
                lines = [l.strip() for l in r.stdout.split("\n") if l.strip()]
                total_mem = 0
                for line in lines:
                    parts = line.split(",")
                    if len(parts) >= 5:
                        try:
                            mem_str = parts[4].strip().strip('"').replace(",", "").replace(" K", "")
                            total_mem += int(mem_str) / 1024
                        except (ValueError, IndexError):
                            pass
                if total_mem > 0:
                    results.append(result("🟡", f"🧠 node.exe 进程总内存: {total_mem:.0f} MB (tasklist)",
                                          detail="psutil 未安装，精度有限"))
                else:
                    results.append(result("🟡", "🧠 Gateway 进程内存: 无法获取",
                                          detail="可 pip install psutil 获得精确信息"))
        except Exception:
            results.append(result("🟡", "🧠 Gateway 进程内存: 无法获取",
                                  detail="tasklist 也无法获取"))

    # ── 3. Session directory depth ──
    session_dir = OPENCLAW_DIR / "agents" / "main" / "sessions"
    if session_dir.exists():
        session_count = len(list(session_dir.glob("*.jsonl")))
        if session_count > 100:
            results.append(result("🟡", f"📋 Session 文件: {session_count} 个",
                                  detail="超过 100 个建议归档",
                                  suggestion="运行 openclaw doctor --fix 自动归档"))
        else:
            results.append(result("🟢", f"📋 Session 文件: {session_count} 个"))

    # Combine results
    sev_order = {"🔴": 0, "🟠": 1, "🟡": 2, "🟢": 3}
    combined_sev = min(results, key=lambda r: sev_order.get(r["severity"], 3))["severity"]

    return {
        "severity": combined_sev,
        "title": "资源监控",
        "checks": results,
    }


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv

    if not as_json:
        print(f"🔑 OpenClaw API Key Validator v6.0-M2")
        print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   配置文件: {CONFIG_PATH}")
        print()

    # ── Step 1: Scan keys ──
    keys = scan_configured_keys()
    if not keys:
        print("  ❌ 未找到任何 API Key")
        return

    # Deduplicate by key value
    seen_keys = set()
    unique_keys = []
    for k in keys:
        if k.get("key", "") not in seen_keys:
            seen_keys.add(k.get("key", ""))
            unique_keys.append(k)

    print(f"  发现 {len(unique_keys)} 个 API Key/Endpoint")
    print(f"  正在验证网络连通性...")
    print()

    # ── Step 2: Validate each key ──
    key_results = []
    for entry in unique_keys:
        key_type = entry.get("key_type", "Unknown")
        source = entry.get("source", "")
        label = entry.get("label", source.split(".")[-1] if "." in source else source)
        key = entry.get("key", "")
        error = entry.get("error", "")

        print(f"  🔍 测试: {label}", end="")

        if error:
            r = result("🔴", f"❌ [{label}] 无法读取", detail=error)
        elif key_type == "Unknown" and not key:
            r = result("🟡", f"🔑 [{source}] 无密钥，跳过验证", detail="仅作为信息记录")
        else:
            r = validate_key(entry)

        key_results.append(r)
        print(f"\r  {'✅' if r['severity']=='🟢' else '⚠️' if r['severity']=='🟡' else '❌'}  {label}: {r['title']}")

    print()

    # ── Step 3: Resource monitoring (P2) ──
    print(f"📊 资源监控检查 (P2)")
    print()
    resource_result = check_resource_health()
    sub_checks = resource_result.get("checks", [])
    for sc in sub_checks:
        print(f"  {sc['severity']} {sc['title']}")
        if verbose and sc.get("detail"):
            print(f"     {sc['detail']}")
        if sc.get("suggestion"):
            print(f"     建议: {sc['suggestion']}")
    print()

    # ── Summary ──
    all_results = key_results + sub_checks
    counts = {"🔴": 0, "🟠": 0, "🟡": 0, "🟢": 0}
    for r in all_results:
        s = r.get("severity", "🟢")
        if s in counts:
            counts[s] += 1

    sev_order = {"🔴": 0, "🟠": 1, "🟡": 2, "🟢": 3}
    overall = min(all_results, key=lambda r: sev_order.get(r.get("severity", "🟢"), 3))["severity"]

    print(f"{'='*60}")
    print(f"  整体健康等级: {overall}")
    print(f"  🔴 阻断: {counts['🔴']}  🟠 高风险: {counts['🟠']}"
          f"  🟡 可优化: {counts['🟡']}  🟢 正常: {counts['🟢']}")
    print(f"{'='*60}")
    print()

    # Action items
    has_suggestions = [r for r in all_results if r.get("suggestion")]
    if has_suggestions:
        print(f"  📋 建议操作")
        for r in has_suggestions:
            print(f"    {r['severity']} {r['suggestion']}")
        print()

    if as_json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "tool": "api_key_validator",
            "version": "6.0-M2",
            "overall_severity": overall,
            "summary": {k: v for k, v in counts.items()},
            "key_results": key_results,
            "resource_checks": sub_checks,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    import sys
    main()
