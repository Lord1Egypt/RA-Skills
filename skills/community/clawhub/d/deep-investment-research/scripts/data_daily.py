"""data_daily.py — 每日预处理主入口（进程隔离+并行调度）

由 cron 08:30 调用。每个 fetcher 在独立子进程中运行，
进程结束 = 内存释放。无依赖的 fetcher 并行执行。

架构：
  主进程（轻量调度器，<50MB）
    → Group 1: 10个无依赖fetcher并行（max 4 workers）
    → Group 2: finnhub_client
    → Group 3: analyst_revision
    → Group 4: policy_gov
  每个子进程独立，超时180s自动kill

支持 tag-based 选择性执行：
  --tags morning      全量晨间采集
  --tags us_refresh   美股盘前刷新
  --tags hk_close     港股收盘补充
  --tags all          全部（默认）
  --dry-run           只打印将执行的 fetcher 列表
"""
import argparse
import os
import json
import sys
import subprocess
import time
from datetime import date, datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
RESEARCH_DATA_ROOT = os.path.expanduser(os.environ.get("RESEARCH_DATA_ROOT", "~/research-data"))
DATA_DIR = os.path.join(RESEARCH_DATA_ROOT, "data")

# Fetcher definitions: each declares tags, group, and optional heavy/depends/special
FETCHERS = {
    # Group 1: Independent
    "edgar_filings":         {"tags": ["morning", "us_refresh"], "group": 1},
    "hkex_announcements":          {"tags": ["morning"], "group": 1},
    "insider_transactions":   {"tags": ["morning", "us_refresh"], "group": 1},
    "superinvestor_moves":      {"tags": ["morning", "us_refresh"], "group": 1},
    "southbound_top10": {"tags": ["morning"], "group": 1},
    "macro_snapshot":         {"tags": ["morning", "us_refresh"], "group": 1},
    "short_interest":      {"tags": ["morning", "hk_close"], "group": 1},
    "sec_13f":             {"tags": ["morning", "us_refresh"], "group": 1},
    # "etf_holdings":      {"tags": ["morning"], "group": 1},  # 低频低价值，已降级
    # "fred_calendar":    {"tags": ["morning"], "group": 1},  # Removed: always empty, no consumer
    "china_macro":         {"tags": ["morning", "us_refresh"], "group": 1},
    "earnings_surprise":   {"tags": ["morning", "us_refresh"], "group": 1},
    # Group 2: Heavy
    "analyst_consensus":      {"tags": ["morning", "us_refresh"], "group": 2},
    # Group 3: Depends on finnhub
    "analyst_revision":    {"tags": ["morning"], "group": 3, "depends": "analyst_consensus"},
    # Group 4: Post-processing
    "policy_gov":   {"tags": ["morning"], "group": 4, "special": True},
}


def get_active_fetchers(tags):
    """Filter fetchers by tags. Returns dict of active fetchers."""
    if "all" in tags:
        return dict(FETCHERS)
    active = {}
    for name, config in FETCHERS.items():
        if any(t in config["tags"] for t in tags):
            # Check depends: skip if dependency won't run in this tag set
            dep = config.get("depends")
            if dep and dep not in active:
                # Check if dependency itself matches any of the requested tags
                dep_config = FETCHERS.get(dep, {})
                if not any(t in dep_config.get("tags", []) for t in tags):
                    continue  # Skip: dependency not in this run
            active[name] = config
    return active


def build_groups(active_fetchers):
    """Organize active fetchers into ordered groups for execution."""
    groups = {}
    for name, config in active_fetchers.items():
        g = config["group"]
        if g not in groups:
            groups[g] = []
        groups[g].append(name)
    # Return as list of lists, sorted by group number
    return [groups[g] for g in sorted(groups.keys())]

# Per-fetcher timeout in seconds
FETCHER_TIMEOUT = 180  # 3 minutes max per fetcher
FETCHER_TIMEOUT_HEAVY = 600  # Reserve for future heavy fetchers (finnhub_client no longer heavy)
MAX_WORKERS = 4


def run_fetcher_subprocess(module_name: str, today: str, output_dir: str) -> dict:
    """Run a single fetcher in an isolated subprocess.
    
    Returns status dict: {"name": ..., "status": "ok"/"rejected"/"unavailable", ...}
    """
    module_path = os.path.join(SCRIPTS_DIR, f"{module_name}.py")
    
    if not os.path.exists(module_path):
        return {"name": module_name, "status": "unavailable", "reason": "Module not found"}
    
    cmd = [
        sys.executable, module_path,
        "--today", today,
        "--output-dir", output_dir,
    ]
    
    env = os.environ.copy()
    env["PYTHONPATH"] = SCRIPTS_DIR
    
    is_heavy = FETCHERS.get(module_name, {}).get("heavy", False)
    timeout = FETCHER_TIMEOUT_HEAVY if is_heavy else FETCHER_TIMEOUT
    
    try:
        start = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=SCRIPTS_DIR,
        )
        elapsed = time.time() - start
        
        # Try to parse status from stdout (last JSON line)
        status = None
        for line in reversed(result.stdout.strip().split('\n')):
            line = line.strip()
            if line.startswith('{'):
                try:
                    status = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue
        
        if status and isinstance(status, dict):
            status["elapsed_s"] = round(elapsed, 1)
            if "name" not in status:
                status["name"] = module_name
            return status
        
        # No parseable status - infer from exit code
        if result.returncode == 0:
            return {"name": module_name, "status": "ok", "elapsed_s": round(elapsed, 1)}
        else:
            stderr_tail = result.stderr[-200:] if result.stderr else ""
            return {
                "name": module_name,
                "status": "rejected",
                "reason": f"Exit code {result.returncode}: {stderr_tail}",
                "elapsed_s": round(elapsed, 1),
            }
    
    except subprocess.TimeoutExpired:
        return {"name": module_name, "status": "rejected", "reason": f"Timeout ({timeout}s)"}
    except Exception as e:
        return {"name": module_name, "status": "rejected", "reason": str(e)[:200]}


def run_special_fetcher(name: str, today: str, output_dir: str) -> dict:
    """Run policy_gov which has a different entry point."""
    env = os.environ.copy()
    env["PYTHONPATH"] = SCRIPTS_DIR
    
    if name == "policy_gov":
        cmd = [sys.executable, "-c", f"""
import sys, os, json
sys.path.insert(0, '{SCRIPTS_DIR}')
os.environ['RESEARCH_DATA_ROOT'] = os.path.expanduser(os.environ.get('RESEARCH_DATA_ROOT', '~/research-data'))
from policy_gov_fetcher import run as run_policy_gov
result = run_policy_gov(target_date='{today}')
summary = result.get('summary', {{}})
status = 'ok' if summary.get('sources_ok', 0) > 0 else 'unavailable'
print(json.dumps({{
    "name": "policy_gov",
    "status": status,
    "total_items": summary.get('items_total', summary.get('total_items', 0)),
    "new_today": len(result.get('new_items', [])),
    "sources_ok": summary.get('sources_ok', 0),
}}))
"""]
    else:
        return {"name": name, "status": "unavailable", "reason": "Unknown special fetcher"}
    
    try:
        start = time.time()
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=FETCHER_TIMEOUT,
            env=env, cwd=SCRIPTS_DIR,
        )
        elapsed = time.time() - start
        
        for line in reversed(result.stdout.strip().split('\n')):
            if line.strip().startswith('{'):
                try:
                    status = json.loads(line.strip())
                    status["elapsed_s"] = round(elapsed, 1)
                    return status
                except json.JSONDecodeError:
                    continue
        
        if result.returncode == 0:
            return {"name": name.replace("_runner", ""), "status": "ok", "elapsed_s": round(elapsed, 1)}
        return {"name": name.replace("_runner", ""), "status": "rejected",
                "reason": result.stderr[-200:], "elapsed_s": round(elapsed, 1)}
    except subprocess.TimeoutExpired:
        return {"name": name.replace("_runner", ""), "status": "rejected", "reason": f"Timeout ({FETCHER_TIMEOUT}s)"}
    except Exception as e:
        return {"name": name.replace("_runner", ""), "status": "rejected", "reason": str(e)[:200]}


def run_group(group: list, today: str, output_dir: str) -> list:
    """Run a group of fetchers in parallel with ThreadPoolExecutor."""
    results = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for module_name in group:
            config = FETCHERS.get(module_name, {})
            if config.get("special"):
                future = executor.submit(run_special_fetcher, module_name, today, output_dir)
            else:
                future = executor.submit(run_fetcher_subprocess, module_name, today, output_dir)
            futures[future] = module_name
        
        for future in as_completed(futures):
            module_name = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({"name": module_name, "status": "rejected", "reason": str(e)[:200]})
    
    return results


def run_all(tags=None, dry_run=False):
    """Main entry point. Supports tag-based filtering and dry-run mode."""
    if tags is None:
        tags = ["all"]
    
    # Get active fetchers based on tags
    active = get_active_fetchers(tags)
    groups = build_groups(active)
    
    today = date.today().isoformat()
    
    # Dry-run: just print the plan and exit
    if dry_run:
        print(f"[data_daily] DRY RUN — tags: {tags}")
        print(f"[data_daily] Active fetchers: {len(active)}")
        for i, group in enumerate(groups):
            print(f"  Group {i+1}: {', '.join(group)}")
        print(f"\nFetcher list: {sorted(active.keys())}")
        return {"dry_run": True, "tags": tags, "fetchers": sorted(active.keys())}
    
    daily_dir = os.path.join(DATA_DIR, "daily", today)
    os.makedirs(daily_dir, exist_ok=True)
    
    total_start = time.time()
    all_results = []
    
    print(f"[data_daily] Starting {today} — tags: {tags} — {len(active)} fetchers in {len(groups)} groups")
    
    for i, group in enumerate(groups):
        group_start = time.time()
        print(f"[data_daily] Group {i+1}/{len(groups)}: {', '.join(group)}")
        results = run_group(group, today, daily_dir)
        all_results.extend(results)
        group_elapsed = time.time() - group_start
        
        ok_count = sum(1 for r in results if r.get("status") == "ok")
        print(f"[data_daily] Group {i+1} done in {group_elapsed:.1f}s — {ok_count}/{len(results)} OK")
    
    total_elapsed = time.time() - total_start
    
    # Build _status.json (backward-compatible format)
    status = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "tags": tags,
        "sources": {},
        "agent_notice": "",
        "total_elapsed_s": round(total_elapsed, 1),
    }
    
    notices = []
    for r in all_results:
        name = r.get("name", "unknown")
        status_val = r.get("status", "unknown")
        entry = {"status": status_val}
        
        if "records" in r:
            entry["records"] = r["records"]
        if "reason" in r and status_val != "ok":
            entry["reason"] = r["reason"]
        if "elapsed_s" in r:
            entry["elapsed_s"] = r["elapsed_s"]
        # Copy any extra fields
        for k in ("total_items", "new_today", "sources_ok", "sources_failed", "opportunities"):
            if k in r:
                entry[k] = r[k]
        
        status["sources"][name] = entry
        
        if status_val not in ("ok",):
            notices.append(f"{name}: {status_val} ({r.get('reason', '?')[:60]})")
    
    if notices:
        status["agent_notice"] = "⚠ " + "; ".join(notices)
    
    # Write _status.json (MERGE with existing if partial run)
    # Key invariant: only keep merged entries if their output file actually exists on disk.
    # This prevents ghost entries (status=ok but no file) from persisting.
    status_path = os.path.join(daily_dir, "_status.json")
    if "all" not in tags:
        # Partial run: merge new results into existing status
        try:
            with open(status_path) as f:
                existing = json.load(f)
            for src_name, src_data in existing.get("sources", {}).items():
                if src_name not in status["sources"]:
                    # Only keep if the output file actually exists
                    expected_file = os.path.join(daily_dir, f"{src_name}.json")
                    if os.path.exists(expected_file):
                        status["sources"][src_name] = src_data
                    else:
                        # Ghost entry: was 'ok' but file doesn't exist — drop it
                        pass
            # Rebuild agent_notice with merged sources
            notices = []
            for src_name, src_data in status["sources"].items():
                if src_data.get("status") not in ("ok",):
                    notices.append(f"{src_name}: {src_data['status']} ({src_data.get('reason', '?')[:60]})")
            status["agent_notice"] = ("⚠ " + "; ".join(notices)) if notices else ""
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # No existing file, write fresh
    with open(status_path, "w") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    
    # Summary
    ok_total = sum(1 for r in all_results if r.get("status") == "ok")
    print(f"\n[data_daily] Complete: {ok_total}/{len(all_results)} OK in {total_elapsed:.1f}s")
    
    if notices:
        print(f"[data_daily] Issues: {'; '.join(notices)}")
    
    # Auto-cleanup raw/ directories older than 7 days
    try:
        import shutil
        from datetime import timedelta
        raw_dir = os.path.join(DATA_DIR, "raw")
        cutoff = date.today() - timedelta(days=7)
        if os.path.isdir(raw_dir):
            for name in os.listdir(raw_dir):
                try:
                    d = date.fromisoformat(name)
                    if d < cutoff:
                        shutil.rmtree(os.path.join(raw_dir, name), ignore_errors=True)
                except ValueError:
                    continue
    except Exception:
        pass  # Cleanup is best-effort, never block the pipeline

    # Output status for cron agent to read
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return status


def main():
    parser = argparse.ArgumentParser(description="Daily data fetcher with tag-based execution")
    parser.add_argument("--tags", nargs="+", default=["all"],
                        help="Tags to run: morning, us_refresh, hk_close, all (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only print the fetcher plan without executing")
    args = parser.parse_args()
    run_all(tags=args.tags, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
