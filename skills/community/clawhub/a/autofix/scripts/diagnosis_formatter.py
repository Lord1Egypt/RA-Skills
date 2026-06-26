#!/usr/bin/env python3
"""
diagnosis_formatter.py — Autofix v6.0-M3: Unified Diagnosis Report + Regression Check

Collects results from all diagnostic sources and produces a severity-sorted,
unified health report with Before/After regression comparison.

Features:
  P3 — Unified Report with severity sorting (🔴→🟠→🟡→🟢)
  P4 — Baseline save/compare for post-fix regression verification

Usage:
    # Run full diagnosis and generate unified report
    python scripts/diagnosis_formatter.py

    # Save a baseline for later comparison
    python scripts/diagnosis_formatter.py --save-baseline

    # Compare current state against saved baseline
    python scripts/diagnosis_formatter.py --compare

    # JSON output for tooling
    python scripts/diagnosis_formatter.py --json

Integration:
    Called by autofix workflow after Steps 1-3 to summarize findings.
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────

HOME_DIR = Path.home()
SKILL_DIR = HOME_DIR / ".openclaw" / "workspace" / "skills" / "autofix"
SCRIPTS_DIR = SKILL_DIR / "scripts"
BASELINE_FILE = SCRIPTS_DIR / "diagnosis_baseline.json"

SEV_ORDER = {"🔴": 0, "🟠": 1, "🟡": 2, "🟢": 3}
CATEGORIES = {
    "gateway": "🌐 Gateway",
    "disk": "💾 存储",
    "sessions": "📋 Session",
    "logs": "📜 日志",
    "models": "🔌 模型",
    "key": "🔑 密钥",
    "resource": "📊 资源",
}

_WIN_CREATION_FLAGS = 0
if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP'):
    _WIN_CREATION_FLAGS = subprocess.CREATE_NEW_PROCESS_GROUP


def _safe_kill(proc):
    """Kill a subprocess and its entire tree on Windows."""
    try:
        import subprocess as _sp
        _sp.run(['taskkill', '/F', '/T', '/PID', str(proc.pid)],
               capture_output=True, timeout=5)
    except Exception:
        try:
            proc.kill()
            proc.wait(5)
        except Exception:
            pass


def _safe_run(cmd_args, timeout_s):
    """Run a command with safe subprocess tree cleanup on timeout.
    Uses shell=True for .cmd files (openclaw CLI) on Windows."""
    use_shell = isinstance(cmd_args, str) or (
        isinstance(cmd_args, list) and cmd_args and 'openclaw' in cmd_args[0].lower()
    )
    proc = subprocess.Popen(
        cmd_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=use_shell,
        creationflags=_WIN_CREATION_FLAGS,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout_s)
        return stdout, stderr, proc.returncode, None
    except subprocess.TimeoutExpired:
        _safe_kill(proc)
        return "", "", -1, subprocess.TimeoutExpired(cmd_args, timeout_s)


def run_script(script_name: str, args: list = None, script_timeout: int = 30) -> dict:
    """Run a Python script with --json flag and parse output.
    Uses script_timeout to limit execution time (default 30s).
    """
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return {"error": f"Script not found: {script_name}"}

    cmd = [sys.executable, str(script_path), "--json"]
    if args:
        cmd.extend(args)

    try:
        stdout, stderr, rc, exc = _safe_run(cmd, script_timeout)
        if exc:
            return {"error": f"Script timed out ({script_timeout}s)"}
        if rc != 0:
            return {"error": stderr[:500] if stderr else f"exit code {rc}"}

        # Find JSON in stdout (skip any header lines)
        json_start = stdout.find("{")
        if json_start < 0:
            return {"error": "No JSON in output"}
        return json.loads(stdout[json_start:])
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}"}
    except Exception as e:
        return {"error": str(e)}


def parse_doctor_output() -> dict:
    """Parse openclaw doctor output and extract severity-graded items.
    Uses a short timeout (12s). If doctor hangs, falls back to
    `openclaw gateway status --json` for at least some data.
    """
    try:
        stdout, stderr, rc, exc = _safe_run(["openclaw", "doctor"], 12)
        if exc:
            # Doctor hung — fall back to gateway status
            return _fallback_doctor_output()
        output = stdout + stderr
    except FileNotFoundError:
        return {"error": "openclaw CLI not found", "items": []}
    except Exception:
        return _fallback_doctor_output()

    items = []

    # Extract warning/error sections
    # Pattern: Doctor warnings --- followed by items
    sections = re.findall(
        r"\|[ \t]*[-]+\+[ \t]*\n\|[ \t]*\n((?:\|[^\n]*\n)*)",
        output,
    )

    for section in sections:
        for line in section.split("\n"):
            line = line.strip().strip("|").strip()
            if not line or line.startswith("-"):
                continue
            # Classify severity
            sev = "🟡"  # default for doctor findings
            if "error" in line.lower() or "critical" in line.lower():
                sev = "🔴"
            elif "warning" in line.lower():
                sev = "🟠"

            items.append({
                "severity": sev,
                "title": line[:120],
                "source": "doctor",
            })

    # If we found nothing structured, try to extract raw warnings
    if not items:
        # Extract anything that looks like a warning message
        for match in re.finditer(r"-\s+(.+?)(?:\n|$)", output):
            text = match.group(1).strip()
            if text and len(text) > 10 and not text.startswith("Run "):
                items.append({
                    "severity": "🟡",
                    "title": text[:120],
                    "source": "doctor",
                })

    return {"items": items}


def _fallback_doctor_output() -> dict:
    """Fallback when openclaw doctor hangs: use gateway status instead."""
    items = []
    try:
        r = subprocess.run(
            ["openclaw", "gateway", "status", "--json"],
            capture_output=True, text=True, timeout=15, shell=True,
        )
        if r.returncode == 0 and r.stdout.strip():
            data = json.loads(r.stdout)
            # Check service status
            svc = data.get("service", {})
            runtime = svc.get("runtime", {})
            status = runtime.get("status", "unknown")
            rpc_ok = data.get("rpc", {}).get("ok", False)

            cat = "🌐 Gateway"
            if status != "running":
                items.append({
                    "severity": "🔴",
                    "title": f"Gateway 状态: {status}（应为 running）",
                    "detail": f"PID: {runtime.get('pid', 'N/A')}",
                    "source": "gateway_status", "category": cat,
                })
            else:
                items.append({
                    "severity": "🟢",
                    "title": "Gateway 运行中",
                    "detail": f"PID: {runtime.get('pid', 'N/A')}, 端口: {data.get('gateway', {}).get('port', '?')}",
                    "source": "gateway_status", "category": cat,
                })

            if not rpc_ok:
                items.append({
                    "severity": "🔴",
                    "title": "RPC 连接异常",
                    "detail": f"kind: {data.get('rpc', {}).get('kind', '?')}",
                    "source": "gateway_status", "category": cat,
                })
            else:
                items.append({
                    "severity": "🟢",
                    "title": "RPC 连接正常",
                    "detail": f"版本: {data.get('rpc', {}).get('server', {}).get('version', '?')}",
                    "source": "gateway_status", "category": cat,
                })

            # Config audit
            config_audit = svc.get("configAudit", {})
            if not config_audit.get("ok", True):
                for issue in config_audit.get("issues", []):
                    items.append({
                        "severity": "🟠",
                        "title": str(issue)[:120],
                        "source": "gateway_status",
                    })

    except (Exception, json.JSONDecodeError) as e:
        return {"error": f"Fallback also failed: {e}", "items": items}

    if not items:
        items.append({
            "severity": "🟡",
            "title": "openclaw doctor 超时，仅能获取 Gateway 状态",
            "source": "gateway_status",
        })

    return {"items": items, "fallback": True}


def flatten_checks(checks: dict, category: str = "") -> list:
    """Flatten nested check results into a flat list of items."""
    items = []
    if isinstance(checks, dict):
        # If it has sub-checks, recurse
        sub = checks.get("checks", [])
        if sub:
            for s in sub:
                if isinstance(s, dict):
                    items.append({
                        "severity": s.get("severity", "🟢"),
                        "title": s.get("title", ""),
                        "detail": s.get("detail", ""),
                        "suggestion": s.get("suggestion", ""),
                        "category": category or checks.get("title", ""),
                    })
                    # Handle nested checks
                    if "checks" in s:
                        items.extend(flatten_checks(s, category))
        else:
            items.append({
                "severity": checks.get("severity", "🟢"),
                "title": checks.get("title", ""),
                "detail": checks.get("detail", ""),
                "suggestion": checks.get("suggestion", ""),
                "category": category,
            })
    return items


def collect_all_results() -> dict:
    """Run all diagnostics and collect results."""
    results = {"timestamp": datetime.now().isoformat(), "items": [], "errors": []}

    # ── 1. openclaw doctor (static config) ──
    doctor_data = parse_doctor_output()
    if "error" in doctor_data:
        results["errors"].append(f"doctor: {doctor_data['error']}")
    else:
        for item in doctor_data.get("items", []):
            if "category" not in item:
                item["category"] = "⚙️ 配置"
            results["items"].append(item)

    # ── 2. runtime_health_check.py (20s timeout — skip if slow) ──
    runtime_data = run_script("runtime_health_check.py", script_timeout=20)
    if "error" in runtime_data:
        results["errors"].append(f"runtime: {runtime_data['error']}")
    else:
        for name, check in runtime_data.get("checks", {}).items():
            cat = CATEGORIES.get(name, f"🔍 {name}")
            if "checks" in check:
                results["items"].extend(flatten_checks(check, cat))
            else:
                results["items"].append({
                    "severity": check.get("severity", "🟢"),
                    "title": check.get("title", ""),
                    "detail": check.get("detail", ""),
                    "suggestion": check.get("suggestion", ""),
                    "category": cat,
                })

    # ── 3. api_key_validator.py (20s timeout) ──
    key_data = run_script("api_key_validator.py", script_timeout=20)
    if "error" in key_data:
        results["errors"].append(f"keys: {key_data['error']}")
    else:
        for kr in key_data.get("key_results", []):
            kr["category"] = "🔑 密钥"
            results["items"].append(kr)
        for rc in key_data.get("resource_checks", []):
            rc["category"] = "📊 资源"
            if "checks" in rc:
                results["items"].extend(flatten_checks(rc, "📊 资源"))
            else:
                results["items"].append(rc)

    # Deduplicate by (title, category) — keep the most severe entry
    seen = {}
    for item in results["items"]:
        key = (item.get("title", ""), item.get("category", ""))
        if key not in seen or SEV_ORDER.get(item.get("severity", "🟢"), 99) < SEV_ORDER.get(seen[key].get("severity", "🟢"), 99):
            seen[key] = item
    results["items"] = list(seen.values())

    # Sort by severity
    results["items"].sort(key=lambda x: SEV_ORDER.get(x.get("severity", "🟢"), 99))

    # Compute summary counts
    counts = {"🔴": 0, "🟠": 0, "🟡": 0, "🟢": 0}
    for item in results["items"]:
        s = item.get("severity", "🟢")
        if s in counts:
            counts[s] += 1
    results["summary"] = counts

    # Overall severity
    overall = "🟢"
    for s in ["🔴", "🟠", "🟡"]:
        if counts.get(s, 0) > 0:
            overall = s
            break
    results["overall_severity"] = overall

    return results


# ── Baseline Management (P4) ──────────────────────────────────────────────

def save_baseline(results: dict) -> bool:
    """Save current diagnosis as baseline for later comparison."""
    baseline = {
        "timestamp": datetime.now().isoformat(),
        "items": results["items"],
        "summary": results["summary"],
        "overall_severity": results["overall_severity"],
    }
    try:
        with open(BASELINE_FILE, "w", encoding="utf-8") as f:
            json.dump(baseline, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


def load_baseline() -> dict:
    """Load saved baseline, or empty dict if not found."""
    if BASELINE_FILE.exists():
        try:
            with open(BASELINE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def compare_with_baseline(current: dict, baseline: dict) -> dict:
    """Compare current results with baseline and produce diff report."""
    baseline_items = {(i.get("title", ""), i.get("category", "")): i
                      for i in baseline.get("items", [])}
    current_items = {(i.get("title", ""), i.get("category", "")): i
                     for i in current.get("items", [])}

    diff = {
        "fixed": [],
        "new": [],
        "degraded": [],
        "improved": [],
        "unchanged": [],
    }

    # Items in baseline but not in current → fixed
    for key, item in baseline_items.items():
        if key not in current_items:
            diff["fixed"].append(item)
        else:
            cur = current_items[key]
            old_sev = item.get("severity", "🟢")
            new_sev = cur.get("severity", "🟢")
            if SEV_ORDER.get(new_sev, 3) < SEV_ORDER.get(old_sev, 3):
                diff["degraded"].append({"item": cur, "was": old_sev, "now": new_sev})
            elif SEV_ORDER.get(new_sev, 3) > SEV_ORDER.get(old_sev, 3):
                diff["improved"].append({"item": cur, "was": old_sev, "now": new_sev})
            else:
                diff["unchanged"].append(cur)

    # Items in current but not baseline → new
    for key, item in current_items.items():
        if key not in baseline_items:
            diff["new"].append(item)

    # Compute summary
    changes = {
        "fixed_count": len(diff["fixed"]),
        "new_count": len(diff["new"]),
        "degraded_count": len(diff["degraded"]),
        "improved_count": len(diff["improved"]),
        "unchanged_count": len(diff["unchanged"]),
    }

    return {"changes": changes, "diff": diff}


# ── Report Rendering ──────────────────────────────────────────────────────

def render_report(results: dict, comparison: dict = None):
    """Render a unified, severity-sorted health report."""
    items = results.get("items", [])
    counts = results.get("summary", {})
    overall = results.get("overall_severity", "🟢")
    errors = results.get("errors", [])

    # ── Regression summary (P4) ──
    if comparison:
        changes = comparison.get("changes", {})
        print(f"{'='*60}")
        print(f"  📋 回归验证报告")
        print(f"{'='*60}")
        print(f"  ✅ 已修复: {changes.get('fixed_count', 0)}")
        print(f"  🆕 新增:   {changes.get('new_count', 0)}")
        print(f"  📈 改善:   {changes.get('improved_count', 0)}")
        print(f"  📉 恶化:   {changes.get('degraded_count', 0)}")
        print(f"  ➖ 不变:   {changes.get('unchanged_count', 0)}")

        # Show fixed items
        fixed = comparison.get("diff", {}).get("fixed", [])
        if fixed:
            print()
            print(f"  ✅ 已修复问题:")
            for f in fixed:
                print(f"     🟢 {f.get('title', '')[:80]}")
        degraded = comparison.get("diff", {}).get("degraded", [])
        if degraded:
            print()
            print(f"  📉 恶化问题:")
            for d in degraded:
                print(f"     {d.get('now', '')} {d.get('item', {}).get('title', '')[:80]}"
                      f" (was {d.get('was', '')})")
        new_items = comparison.get("diff", {}).get("new", [])
        if new_items:
            print()
            print(f"  🆕 新问题:")
            for n in new_items:
                print(f"     {n.get('severity', '🟢')} {n.get('title', '')[:80]}")
        print()

    # ── Header ──
    print(f"{'='*60}")
    print(f"  🔬 OpenClaw 健康诊断报告")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print()
    print(f"  整体健康等级: {overall}")
    print(f"  🔴 阻断: {counts.get('🔴', 0)}"
          f"  🟠 高风险: {counts.get('🟠', 0)}"
          f"  🟡 可优化: {counts.get('🟡', 0)}"
          f"  🟢 正常: {counts.get('🟢', 0)}")
    print()

    # ── Items by severity ──
    for sev_label, sev_name in [("🔴", "阻断级问题"), ("🟠", "高风险问题"),
                                 ("🟡", "可优化项"), ("🟢", "正常项")]:
        sev_items = [i for i in items if i.get("severity") == sev_label]
        if not sev_items:
            continue
        print(f"  ── {sev_name} ({len(sev_items)}) {'─' * (50 - len(sev_name))}")
        for item in sev_items:
            cat = item.get("category", "")
            title = item.get("title", "")
            detail = item.get("detail", "")
            suggestion = item.get("suggestion", "")
            print(f"  {sev_label} [{cat}] {title[:90]}")
            if detail:
                print(f"       {detail[:120]}")
            if suggestion:
                print(f"      💡 {suggestion[:120]}")
        print()

    # ── Action items (all items with suggestions) ──
    actions = [i for i in items if i.get("suggestion")]
    if actions:
        print(f"  ── 📋 建议操作 ──")
        for a in actions:
            print(f"  {a['severity']} {a['suggestion'][:120]}")
        print()

    # ── Errors ──
    if errors:
        print(f"  ── ⚠️ 诊断错误 ──")
        for e in errors:
            print(f"  ❌ {e}")
        print()

    print(f"{'='*60}")
    print(f"  来源: openclaw doctor + runtime_health_check + api_key_validator")
    print(f"  总检测项: {len(items)} | 运行: python scripts/diagnosis_formatter.py")
    print()


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    as_json = "--json" in sys.argv
    save = "--save-baseline" in sys.argv
    compare = "--compare" in sys.argv

    # ── Collect all results ──
    results = collect_all_results()

    # ── Comparison mode (P4) ──
    comparison = None
    if compare:
        baseline = load_baseline()
        if not baseline:
            print("❌ 未找到基线文件。请先运行 --save-baseline。")
            return
        comparison = compare_with_baseline(results, baseline)

    # ── Save baseline (if requested) ──
    if save:
        if save_baseline(results):
            print(f"✅ 基线已保存至 {BASELINE_FILE}")
        else:
            print("❌ 基线保存失败")
        if not as_json:
            return

    # ── Output ──
    if as_json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "tool": "diagnosis_formatter",
            "version": "6.0-M3",
            "overall_severity": results["overall_severity"],
            "summary": results["summary"],
            "items": results["items"],
            "errors": results["errors"],
        }
        if comparison:
            output["regression"] = comparison["changes"]
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    else:
        render_report(results, comparison)


if __name__ == "__main__":
    main()
