#!/usr/bin/env python3
"""
databricks-helper — Query, inspect, and control Databricks from plain text.

Usage highlights (v1.1.0):
    python databricks_helper.py list-runs [--limit 10]
    python databricks_helper.py running-jobs [--pattern name]
    python databricks_helper.py failures [--hours 24]
    python databricks_helper.py summary
    python databricks_helper.py top-failures [--hours 24]
    python databricks_helper.py run-job "job name"
    python databricks_helper.py retry-run RUN_ID
    python databricks_helper.py cancel-run RUN_ID
    python databricks_helper.py run-details RUN_ID
    python databricks_helper.py jobs [--pattern foo] [--tag key=value]
    python databricks_helper.py sla-watch [--minutes 60]
    python databricks_helper.py list-catalogs
    python databricks_helper.py list-schemas --catalog main
    python databricks_helper.py list-tables --catalog main --schema bronze
    python databricks_helper.py preview-table main.bronze.events [--limit 20]
    python databricks_helper.py run-sql --query "SELECT COUNT(*) FROM main.bronze.events"

Environment:
    DATABRICKS_HOST              — e.g. https://adb-1234567890.12.azuredatabricks.net
    DATABRICKS_TOKEN             — personal access token
    DATABRICKS_SQL_WAREHOUSE_ID  — (for SQL/preview) default warehouse id
    DATABRICKS_ALLOW_WRITE_SQL   — set to true only if write SQL is allowed
    DATABRICKS_MAX_ROWS          — default max rows returned for SQL (default 200)
    DATABRICKS_SQL_TIMEOUT_SEC   — SQL polling timeout seconds (default 60)
    DATABRICKS_SLA_MINUTES       — SLA minutes for sla-watch (default 60)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from urllib.parse import urlencode

__version__ = "1.1.0"

MAX_JOBS = 200
RUNS_PAGE_SIZE = 25
DEFAULT_SQL_LIMIT = int(os.environ.get("DATABRICKS_MAX_ROWS", 200))
DEFAULT_SQL_TIMEOUT = int(os.environ.get("DATABRICKS_SQL_TIMEOUT_SEC", 60))
DEFAULT_SLA_MINUTES = int(os.environ.get("DATABRICKS_SLA_MINUTES", 60))


def get_env() -> tuple[str, str]:
    host = os.environ.get("DATABRICKS_HOST", "").rstrip("/")
    token = os.environ.get("DATABRICKS_TOKEN", "")
    if not host or not token:
        print("ERROR: DATABRICKS_HOST and DATABRICKS_TOKEN must be set.")
        print("")
        print("Setup:")
        print("  export DATABRICKS_HOST=https://adb-xxxx.azuredatabricks.net")
        print("  export DATABRICKS_TOKEN=dapiXXXXXXXXXXXXXXXX")
        sys.exit(1)
    return host, token


def build_url(host: str, api_version: str, path: str, params: Optional[Dict[str, str]] = None) -> str:
    url = f"{host}/api/{api_version}/{path}"
    if params:
        safe_params = {k: str(v) for k, v in params.items() if v is not None}
        query = urlencode(safe_params, doseq=True)
        url = f"{url}?{query}"
    return url


def api_get(host: str, token: str, path: str, params: Optional[Dict[str, str]] = None, api_version: str = "2.1") -> Dict:
    url = build_url(host, api_version, path, params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}")
        sys.exit(1)


def api_post(host: str, token: str, path: str, payload: Dict, api_version: str = "2.1") -> Dict:
    url = build_url(host, api_version, path)
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read()
            if body:
                return json.loads(body)
            return {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}")
        sys.exit(1)


def now_ms() -> int:
    return int(time.time() * 1000)


def ms_to_human(ms: Optional[int]) -> str:
    if not ms:
        return "-"
    s = max(0, int(ms / 1000))
    if s < 60:
        return f"{s}s"
    m = s // 60
    s = s % 60
    if m < 60:
        return f"{m}m{s:02d}s"
    h = m // 60
    m = m % 60
    return f"{h}h{m:02d}m"


def ts_to_human(ms: Optional[int]) -> str:
    if not ms:
        return "-"
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def stream_runs(
    host: str,
    token: str,
    base_params: Optional[Dict[str, str]] = None,
    max_runs: int = 200,
    stop_when_before: Optional[int] = None,
) -> List[Dict]:
    collected: List[Dict] = []
    page_token: Optional[str] = None
    while len(collected) < max_runs:
        params = dict(base_params or {})
        params["limit"] = min(RUNS_PAGE_SIZE, max_runs - len(collected))
        if page_token:
            params["page_token"] = page_token
        data = api_get(host, token, "jobs/runs/list", params)
        runs = data.get("runs", [])
        if not runs:
            break
        for run in runs:
            start = run.get("start_time") or 0
            if stop_when_before and start and start < stop_when_before:
                return collected
            collected.append(run)
            if len(collected) >= max_runs:
                break
        page_token = data.get("next_page_token")
        if not page_token:
            break
    return collected


def list_runs(host: str, token: str, limit: int = 10) -> None:
    runs = stream_runs(host, token, max_runs=limit)
    if not runs:
        print("No recent runs found.")
        return
    print(f"Last {len(runs)} runs:\n")
    for run in runs:
        status = run.get("state", {}).get("result_state") or run.get("state", {}).get("life_cycle_state", "UNKNOWN")
        job_name = run.get("run_name", f"Job {run.get('job_id')}")
        start_time = ts_to_human(run.get("start_time"))
        duration = ms_to_human(run.get("execution_duration") or run.get("run_duration"))
        print(f"  [{status:10s}] {job_name}")
        print(f"             Started: {start_time}  Duration: {duration}")
        run_url = run.get("run_page_url")
        if run_url:
            print(f"             URL: {run_url}")
        print()


def list_failures(host: str, token: str, hours: int = 24) -> None:
    since_ms = now_ms() - hours * 3600 * 1000
    runs = stream_runs(host, token, max_runs=200, stop_when_before=since_ms)
    failed = [
        r for r in runs
        if r.get("state", {}).get("result_state") == "FAILED"
        and (r.get("start_time") or 0) >= since_ms
    ]
    if not failed:
        print(f"No failed runs in the last {hours} hours.")
        return
    print(f"{len(failed)} failed run(s) in the last {hours} hours:\n")
    for run in failed:
        job_name = run.get("run_name", f"Job {run.get('job_id')}")
        start_time = ts_to_human(run.get("start_time"))
        state_message = run.get("state", {}).get("state_message", "No error message available.")
        print(f"  [FAILED] {job_name}")
        print(f"           Started: {start_time}")
        print(f"           Error:   {state_message[:300]}")
        run_url = run.get("run_page_url")
        if run_url:
            print(f"           URL:     {run_url}")
        print()


def find_job_by_name(jobs: List[Dict], job_name: str) -> Optional[Dict]:
    for job in jobs:
        name = job.get("settings", {}).get("name", "")
        if name.lower() == job_name.lower():
            return job
    candidates = [j for j in jobs if job_name.lower() in j.get("settings", {}).get("name", "").lower()]
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        print(f"Multiple jobs match '{job_name}':")
        for c in candidates:
            print(f"  - {c['settings']['name']}")
        print("Please use the exact job name.")
        sys.exit(1)
    return None


def run_job(host: str, token: str, job_name: str) -> None:
    jobs_data = api_get(host, token, "jobs/list", {"limit": MAX_JOBS})
    jobs = jobs_data.get("jobs", [])
    match = find_job_by_name(jobs, job_name)
    if not match:
        print(f"No job found matching '{job_name}'.")
        print("\nAvailable jobs:")
        for job in jobs[:20]:
            print(f"  - {job['settings']['name']}")
        sys.exit(1)
    job_id = match["job_id"]
    job_display_name = match["settings"].get("name", f"Job {job_id}")
    result = api_post(host, token, "jobs/run-now", {"job_id": job_id})
    run_id = result.get("run_id")
    print(f"Triggered job: {job_display_name}")
    print(f"Run ID: {run_id}")
    print(f"Monitor at: {host}/#job/{job_id}/run/{run_id}")


def job_status(host: str, token: str, job_name: str, limit: int = 5) -> None:
    jobs_data = api_get(host, token, "jobs/list", {"limit": MAX_JOBS})
    jobs = jobs_data.get("jobs", [])
    match = find_job_by_name(jobs, job_name)
    if not match:
        print(f"Job '{job_name}' not found.")
        sys.exit(1)
    job_id = match["job_id"]
    job_display_name = match["settings"].get("name", f"Job {job_id}")
    runs_data = api_get(host, token, "jobs/runs/list", {"job_id": job_id, "limit": limit})
    runs = runs_data.get("runs", [])
    print(f"Last {len(runs)} runs for: {job_display_name}\n")
    for run in runs:
        status = run.get("state", {}).get("result_state") or run.get("state", {}).get("life_cycle_state", "UNKNOWN")
        start_time = ts_to_human(run.get("start_time"))
        duration = ms_to_human(run.get("execution_duration") or run.get("run_duration"))
        print(f"  [{status:10s}] {start_time}  Duration: {duration}")
        url = run.get("run_page_url")
        if url:
            print(f"               {url}")


def retry_run(host: str, token: str, run_id: int) -> None:
    payload = {"run_id": run_id, "rerun_all_failed_tasks": True}
    result = api_post(host, token, "jobs/runs/repair", payload)
    new_run = result.get("repair_id") or result.get("run_id")
    if new_run:
        print(f"Re-run requested. Track at run {new_run}.")
    else:
        print("Repair request sent.")


def cancel_run(host: str, token: str, run_id: int) -> None:
    api_post(host, token, "jobs/runs/cancel", {"run_id": run_id})
    print(f"Cancellation requested for run {run_id}.")


def show_run_details(host: str, token: str, run_id: int) -> None:
    run = api_get(host, token, "jobs/runs/get", {"run_id": run_id})
    state = run.get("state", {})
    job_name = run.get("run_name", f"Job {run.get('job_id')}")
    print(f"Run: {run_id}")
    print(f"Job: {job_name}")
    print(f"State: {state.get('life_cycle_state')} / {state.get('result_state')}")
    if state.get("state_message"):
        print(f"Message: {state['state_message']}")
    print(f"Start: {ts_to_human(run.get('start_time'))}")
    print(f"End:   {ts_to_human(run.get('end_time'))}")
    duration = run.get("execution_duration") or run.get("run_duration") or 0
    print(f"Duration: {ms_to_human(duration)}")
    if run.get("cluster_spec"):
        cluster = run["cluster_spec"].get("existing_cluster_id") or run["cluster_spec"].get("new_cluster")
        print(f"Cluster: {cluster}")
    if run.get("tasks"):
        print("Tasks:")
        for task in run["tasks"]:
            t_state = task.get("state", {})
            print(f"  - {task.get('task_key')}: {t_state.get('result_state') or t_state.get('life_cycle_state')}")
    output = api_get(host, token, "jobs/runs/get-output", {"run_id": run_id})
    if output.get("error"):
        print(f"Error: {output['error']}")
    if output.get("logs"):
        logs = output["logs"]
        snippet = logs if len(logs) < 1000 else logs[:1000] + "... (truncated)"
        print("Logs:")
        print(snippet)
    if output.get("notebook_output", {}).get("result"):
        res = output["notebook_output"]["result"]
        print("Notebook result snippet:")
        print(res[:1000])


def list_running_jobs(host: str, token: str, pattern: Optional[str] = None) -> None:
    runs = stream_runs(host, token, {"active_only": "true"}, max_runs=100)
    if pattern:
        runs = [r for r in runs if pattern.lower() in r.get("run_name", "").lower()]
    if not runs:
        print("No running jobs match filters.")
        return
    print(f"{len(runs)} run(s) currently active:\n")
    now = now_ms()
    for run in runs:
        job_name = run.get("run_name", f"Job {run.get('job_id')}")
        start = run.get("start_time") or now
        elapsed = ms_to_human(max(0, now - start))
        print(f"  [RUNNING] {job_name}")
        print(f"             Run ID: {run.get('run_id')}  Started: {ts_to_human(start)}  Elapsed: {elapsed}")
        url = run.get("run_page_url")
        if url:
            print(f"             {url}")
        print()


def parse_tag_filters(tag_items: Optional[List[str]]) -> Dict[str, str]:
    tags: Dict[str, str] = {}
    if not tag_items:
        return tags
    for item in tag_items:
        if "=" not in item:
            print(f"Invalid tag filter '{item}'. Use key=value.")
            sys.exit(1)
        key, value = item.split("=", 1)
        tags[key.strip()] = value.strip()
    return tags


def filter_jobs(jobs: List[Dict], pattern: Optional[str], tag_filters: Dict[str, str]) -> List[Dict]:
    results = []
    for job in jobs:
        name = job.get("settings", {}).get("name", "")
        if pattern and pattern.lower() not in name.lower():
            continue
        tags = job.get("settings", {}).get("tags", {}) or {}
        if any(tags.get(k) != v for k, v in tag_filters.items()):
            continue
        results.append(job)
    return results


def list_jobs(host: str, token: str, pattern: Optional[str], tag_filters: Dict[str, str], limit: int) -> None:
    jobs_data = api_get(host, token, "jobs/list", {"limit": MAX_JOBS})
    jobs = jobs_data.get("jobs", [])
    matches = filter_jobs(jobs, pattern, tag_filters)
    if not matches:
        print("No jobs match the supplied filters.")
        return
    print(f"{len(matches)} job(s) match filters:")
    for job in matches[:limit]:
        name = job.get("settings", {}).get("name", "(unnamed)")
        tags = job.get("settings", {}).get("tags", {}) or {}
        tag_str = ", ".join(f"{k}={v}" for k, v in tags.items())
        print(f"  - {name} (id {job.get('job_id')})")
        if tag_str:
            print(f"      tags: {tag_str}")


def sla_watch(host: str, token: str, minutes: int, limit: int) -> None:
    threshold_ms = minutes * 60 * 1000
    active = stream_runs(host, token, {"active_only": "true"}, max_runs=100)
    recent = stream_runs(host, token, {"completed_only": "true"}, max_runs=limit)
    print(f"SLA threshold: {minutes} minutes\n")
    if active:
        print("Active runs:")
    now = now_ms()
    for run in active:
        start = run.get("start_time") or now
        elapsed = now - start
        job_name = run.get("run_name", f"Job {run.get('job_id')}")
        status = "BREACH" if elapsed >= threshold_ms else "OK"
        print(f"  [{status:6s}] {job_name}  Run {run.get('run_id')}  Elapsed {ms_to_human(elapsed)}")
    breached = [
        run for run in recent
        if (run.get("execution_duration") or run.get("run_duration") or 0) >= threshold_ms
    ]
    if breached:
        print("\nRecent SLA breaches:")
        for run in breached:
            job_name = run.get("run_name", f"Job {run.get('job_id')}")
            duration = run.get("execution_duration") or run.get("run_duration") or 0
            print(f"  [DONE] {job_name} {ms_to_human(duration)} at {ts_to_human(run.get('start_time'))}")
    elif not active:
        print("No active runs or recent breaches detected.")


def summarize_success(host: str, token: str) -> None:
    now = now_ms()
    daily_runs = stream_runs(host, token, max_runs=500, stop_when_before=now - 24 * 3600 * 1000)
    weekly_runs = stream_runs(host, token, max_runs=1000, stop_when_before=now - 7 * 24 * 3600 * 1000)
    def tally(runs: List[Dict]) -> Dict[str, int]:
        counts = {"SUCCESS": 0, "FAILED": 0, "CANCELED": 0, "RUNNING": 0, "OTHER": 0}
        for run in runs:
            result = run.get("state", {}).get("result_state")
            life = run.get("state", {}).get("life_cycle_state")
            if result in counts:
                counts[result] += 1
            elif life == "RUNNING":
                counts["RUNNING"] += 1
            else:
                counts["OTHER"] += 1
        return counts
    daily = tally(daily_runs)
    weekly = tally(weekly_runs)
    print("Success/failure summary:\n")
    print("Last 24h:")
    for key, value in daily.items():
        print(f"  {key:8s}: {value}")
    print("\nLast 7d:")
    for key, value in weekly.items():
        print(f"  {key:8s}: {value}")


def top_failures(host: str, token: str, hours: int, limit: int) -> None:
    since_ms = now_ms() - hours * 3600 * 1000
    runs = stream_runs(host, token, max_runs=1000, stop_when_before=since_ms)
    counts: Dict[str, int] = {}
    for run in runs:
        if run.get("state", {}).get("result_state") != "FAILED":
            continue
        if (run.get("start_time") or 0) < since_ms:
            continue
        job_name = run.get("run_name", f"Job {run.get('job_id')}")
        counts[job_name] = counts.get(job_name, 0) + 1
    if not counts:
        print(f"No failures in the last {hours} hours.")
        return
    print(f"Top failing jobs in last {hours} hours:\n")
    for job, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]:
        print(f"  {job}: {count} failure(s)")


def list_catalogs(host: str, token: str) -> None:
    data = api_get(host, token, "unity-catalog/catalogs")
    catalogs = data.get("catalogs", [])
    if not catalogs:
        print("No catalogs found (requires Unity Catalog permissions).")
        return
    print("Catalogs:")
    for cat in catalogs:
        print(f"  - {cat.get('name')}  (type: {cat.get('catalog_type', 'unknown')})")


def list_schemas(host: str, token: str, catalog: str, pattern: Optional[str]) -> None:
    data = api_get(host, token, "unity-catalog/schemas", {"catalog_name": catalog})
    schemas = data.get("schemas", [])
    if pattern:
        schemas = [s for s in schemas if pattern.lower() in s.get("name", "").lower()]
    if not schemas:
        print("No schemas match the supplied filters.")
        return
    print(f"Schemas in {catalog}:")
    for schema in schemas:
        comment = schema.get("comment") or ""
        suffix = f" — {comment}" if comment else ""
        print(f"  - {schema.get('name')}{suffix}")


def list_tables(host: str, token: str, catalog: str, schema: str, pattern: Optional[str]) -> None:
    params = {"catalog_name": catalog, "schema_name": schema}
    data = api_get(host, token, "unity-catalog/tables", params)
    tables = data.get("tables", [])
    if pattern:
        tables = [t for t in tables if pattern.lower() in t.get("name", "").lower()]
    if not tables:
        print("No tables match the supplied filters.")
        return
    print(f"Tables in {catalog}.{schema}:")
    for table in tables:
        kind = table.get("table_type", "TABLE")
        comment = table.get("comment") or ""
        suffix = f" — {comment}" if comment else ""
        print(f"  - {table.get('name')} ({kind}){suffix}")


def allow_write_sql() -> bool:
    return os.environ.get("DATABRICKS_ALLOW_WRITE_SQL", "").lower() in {"1", "true", "yes", "on"}


def is_sql_safe(query: str) -> bool:
    """Best-effort check that a statement is read-only."""
    stripped = re.sub(r"(--.*?$)|(/\*.*?\*/)", "", query, flags=re.MULTILINE | re.DOTALL).strip()
    if not stripped:
        return False
    lowered = stripped.lower()
    forbidden = [
        "insert", "update", "delete", "merge", "create", "alter", "drop", "truncate",
        "comment", "grant", "revoke", "replace", "set", "attach", "detach", "vacuum",
        "optimize", "use", "call", "refresh", "repair table"
    ]
    for keyword in forbidden:
        if re.search(rf"\b{keyword}\b", lowered):
            return False
    return True


def apply_sql_limit(query: str, limit: Optional[int]) -> str:
    if not limit or limit <= 0:
        return query
    clean = query.strip().rstrip(";")
    lowered = clean.lower().lstrip()
    if lowered.startswith("select") or lowered.startswith("with"):
        return f"SELECT * FROM ({clean}) LIMIT {limit}"
    return query


def execute_sql(host: str, token: str, query: str, warehouse_id: Optional[str], limit: int, timeout: int) -> None:
    if not warehouse_id:
        print("SQL warehouse is required. Set DATABRICKS_SQL_WAREHOUSE_ID or pass --warehouse.")
        sys.exit(1)
    if not allow_write_sql() and not is_sql_safe(query):
        print("Blocked query that appears to modify data. Set DATABRICKS_ALLOW_WRITE_SQL=true to override.")
        sys.exit(1)
    limited_query = apply_sql_limit(query, limit)
    wait = max(5, min(timeout, 120))
    payload = {
        "statement": limited_query,
        "warehouse_id": warehouse_id,
        "disposition": "INLINE",
        "wait_timeout": f"{wait}s",
    }
    response = api_post(host, token, "sql/statements", payload, api_version="2.0")
    statement_id = response.get("statement_id")
    status = response.get("status", {}).get("state")
    start = time.time()
    result = response.get("result") if status == "SUCCEEDED" else None
    while not result:
        if status in {"FAILED", "CANCELED"}:
            error = response.get("error", {}).get("message") or response.get("status", {}).get("error")
            print(f"Statement {status}. {error or 'No message provided.'}")
            return
        if time.time() - start > timeout:
            api_post(host, token, f"sql/statements/{statement_id}/cancel", {}, api_version="2.0")
            print("Timed out waiting for SQL statement to finish.")
            return
        time.sleep(2)
        response = api_get(host, token, f"sql/statements/{statement_id}", api_version="2.0")
        status = response.get("status", {}).get("state")
        result = response.get("result") if status == "SUCCEEDED" else None
    rows = result.get("data_array", [])
    schema = result.get("schema", {}).get("columns", [])
    columns = [col.get("name", f"col_{idx}") for idx, col in enumerate(schema)]
    if not rows:
        print("Query returned no rows.")
        return
    print(f"Returned {len(rows)} row(s). Showing up to {limit} rows:\n")
    header = " | ".join(columns)
    print(header)
    print("-" * len(header))
    for row in rows[:limit]:
        values = [json.dumps(val) if isinstance(val, (dict, list)) else str(val) for val in row]
        print(" | ".join(values))


def preview_table(host: str, token: str, table: str, warehouse_id: Optional[str], limit: int) -> None:
    table = table.strip()
    if len(table.split('.')) not in {2, 3}:
        print("Table must be provided as schema.table or catalog.schema.table")
        sys.exit(1)
    query = f"SELECT * FROM {table} LIMIT {limit}"
    execute_sql(host, token, query, warehouse_id, limit=limit, timeout=DEFAULT_SQL_TIMEOUT)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Databricks helper for AI agents")
    subparsers = parser.add_subparsers(dest="command")

    p_list = subparsers.add_parser("list-runs", help="List recent runs")
    p_list.add_argument("--limit", type=int, default=10)

    p_fail = subparsers.add_parser("failures", help="Show failed runs")
    p_fail.add_argument("--hours", type=int, default=24)

    p_run = subparsers.add_parser("run-job", help="Trigger a job by name")
    p_run.add_argument("job_name")

    p_status = subparsers.add_parser("job-status", help="Show status of a specific job")
    p_status.add_argument("job_name")
    p_status.add_argument("--limit", type=int, default=5)

    p_retry = subparsers.add_parser("retry-run", help="Retry a run by run_id")
    p_retry.add_argument("run_id", type=int)

    p_cancel = subparsers.add_parser("cancel-run", help="Cancel a running run by run_id")
    p_cancel.add_argument("run_id", type=int)

    p_details = subparsers.add_parser("run-details", help="Fetch run logs and diagnostics")
    p_details.add_argument("run_id", type=int)

    p_running = subparsers.add_parser("running-jobs", help="List currently running jobs")
    p_running.add_argument("--pattern", help="Filter by job name pattern")

    p_jobs = subparsers.add_parser("jobs", help="List jobs filtered by name/tags")
    p_jobs.add_argument("--pattern", help="Match job names containing pattern")
    p_jobs.add_argument("--tag", action="append", help="Filter by tag key=value", dest="tags")
    p_jobs.add_argument("--limit", type=int, default=20)

    p_sla = subparsers.add_parser("sla-watch", help="Highlight long running jobs vs SLA")
    p_sla.add_argument("--minutes", type=int, default=DEFAULT_SLA_MINUTES)
    p_sla.add_argument("--limit", type=int, default=50)

    subparsers.add_parser("summary", help="Show 24h/7d success/failure summary")

    p_top = subparsers.add_parser("top-failures", help="Show top failing jobs")
    p_top.add_argument("--hours", type=int, default=24)
    p_top.add_argument("--limit", type=int, default=5)

    subparsers.add_parser("list-catalogs", help="List Unity Catalog catalogs")

    p_schema = subparsers.add_parser("list-schemas", help="List schemas in a catalog")
    p_schema.add_argument("--catalog", required=True)
    p_schema.add_argument("--pattern")

    p_tables = subparsers.add_parser("list-tables", help="List tables in a schema")
    p_tables.add_argument("--catalog", required=True)
    p_tables.add_argument("--schema", required=True)
    p_tables.add_argument("--pattern")

    p_preview = subparsers.add_parser("preview-table", help="Preview table rows via SQL")
    p_preview.add_argument("table")
    p_preview.add_argument("--warehouse", help="SQL warehouse override")
    p_preview.add_argument("--limit", type=int, default=20)

    p_sql = subparsers.add_parser("run-sql", help="Run a read-only SQL query")
    p_sql.add_argument("--query", required=True)
    p_sql.add_argument("--warehouse", help="SQL warehouse override")
    p_sql.add_argument("--limit", type=int, default=DEFAULT_SQL_LIMIT)
    p_sql.add_argument("--timeout", type=int, default=DEFAULT_SQL_TIMEOUT)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.command:
        print(f"databricks-helper v{__version__}")
        print("Use --help for available commands.")
        sys.exit(1)
    host, token = get_env()
    if args.command == "list-runs":
        list_runs(host, token, args.limit)
    elif args.command == "failures":
        list_failures(host, token, args.hours)
    elif args.command == "run-job":
        run_job(host, token, args.job_name)
    elif args.command == "job-status":
        job_status(host, token, args.job_name, args.limit)
    elif args.command == "retry-run":
        retry_run(host, token, args.run_id)
    elif args.command == "cancel-run":
        cancel_run(host, token, args.run_id)
    elif args.command == "run-details":
        show_run_details(host, token, args.run_id)
    elif args.command == "running-jobs":
        list_running_jobs(host, token, args.pattern)
    elif args.command == "jobs":
        tags = parse_tag_filters(args.tags)
        list_jobs(host, token, args.pattern, tags, args.limit)
    elif args.command == "sla-watch":
        sla_watch(host, token, args.minutes, args.limit)
    elif args.command == "summary":
        summarize_success(host, token)
    elif args.command == "top-failures":
        top_failures(host, token, args.hours, args.limit)
    elif args.command == "list-catalogs":
        list_catalogs(host, token)
    elif args.command == "list-schemas":
        list_schemas(host, token, args.catalog, args.pattern)
    elif args.command == "list-tables":
        list_tables(host, token, args.catalog, args.schema, args.pattern)
    elif args.command == "preview-table":
        warehouse = args.warehouse or os.environ.get("DATABRICKS_SQL_WAREHOUSE_ID")
        preview_table(host, token, args.table, warehouse, args.limit)
    elif args.command == "run-sql":
        warehouse = args.warehouse or os.environ.get("DATABRICKS_SQL_WAREHOUSE_ID")
        execute_sql(host, token, args.query, warehouse, args.limit, args.timeout)


if __name__ == "__main__":
    main()
