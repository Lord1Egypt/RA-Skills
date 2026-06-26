#!/usr/bin/env python3
from __future__ import annotations

"""
ClawRank OpenClaw Ingestion Script

Scans local OpenClaw session transcripts, aggregates token usage into
daily agent facts, and POSTs them to the ClawRank API. Optionally collects
GitHub commit and PR metrics via the gh CLI.

Usage:
    python3 ingest.py [--dry-run] [--endpoint URL] [--agents-dir DIR]

Environment:
    CLAWRANK_API_TOKEN    - Required. Bearer token for ClawRank API.
    CLAWRANK_ENDPOINT     - API base URL (default: https://clawrank.dev).
    CLAWRANK_OWNER_NAME   - Display name for the owner (default: hostname).
    CLAWRANK_AGENTS_DIR   - Override agents directory (default: ~/.openclaw/agents).
"""

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import urllib.request
import urllib.error
import urllib.parse
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path


# ── Config ──────────────────────────────────────────────────────────────────

DEFAULT_ENDPOINT = "https://clawrank.dev"
SUBMIT_PATH = "/api/submit"
STATE_PATH_ENV = "CLAWRANK_STATE_PATH"


def get_agents_dir(override: str | None = None) -> Path:
    if override:
        return Path(override).expanduser()
    env = os.environ.get("CLAWRANK_AGENTS_DIR")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".openclaw" / "agents"


def get_endpoint(override: str | None = None) -> str:
    if override:
        return override.rstrip("/")
    return os.environ.get("CLAWRANK_ENDPOINT", DEFAULT_ENDPOINT).rstrip("/")


def get_token() -> str | None:
    return os.environ.get("CLAWRANK_API_TOKEN")


def get_state_path() -> Path:
    env = os.environ.get(STATE_PATH_ENV)
    if env:
        return Path(env).expanduser()
    return Path.home() / ".openclaw" / "clawrank-state.json"


def load_state() -> dict:
    state_path = get_state_path()
    if not state_path.is_file():
        return {}
    try:
        with open(state_path, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(state: dict) -> None:
    state_path = get_state_path()
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)
    except OSError:
        pass


def get_owner_name_override() -> str | None:
    """Return explicit owner name if set, otherwise None (triggers auto-resolve)."""
    return os.environ.get("CLAWRANK_OWNER_NAME") or None


def get_agent_name_override() -> str | None:
    """Return explicit agent name if set, otherwise None (triggers auto-resolve)."""
    return os.environ.get("CLAWRANK_AGENT_NAME") or None


def resolve_owner_name() -> str:
    """
    Auto-resolve owner display name. Priority:
    1. CLAWRANK_OWNER_NAME env (explicit opt-in)
    2. GitHub username from `gh auth status`
    3. First name from `git config user.name`
    4. Hostname (last resort)
    Never uses email or full name — PII protection.
    """
    explicit = get_owner_name_override()
    if explicit:
        return explicit

    # Try gh CLI username
    gh_user = _get_gh_username()
    if gh_user:
        return gh_user

    # Try git config — first name only
    git_name = _get_git_first_name()
    if git_name:
        return git_name

    # Hostname fallback
    hostname = platform.node() or ""
    # Strip common suffixes like .local, .lan
    hostname = re.sub(r"\.(local|lan|home|internal)$", "", hostname, flags=re.IGNORECASE)
    return hostname or "Anonymous"


def _get_gh_username() -> str | None:
    """Extract GitHub username from `gh auth status` output."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True, text=True, timeout=5,
        )
        # Parse "Logged in to github.com account USERNAME" from stderr
        output = result.stderr + result.stdout
        m = re.search(r"account\s+(\S+)", output)
        if m:
            return m.group(1).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return None


def _get_git_first_name() -> str | None:
    """Get first name from git config. Returns None if not set or looks like an email."""
    try:
        result = subprocess.run(
            ["git", "config", "--global", "user.name"],
            capture_output=True, text=True, timeout=5,
        )
        name = result.stdout.strip()
        if not name or "@" in name:
            return None
        # First name only — don't leak full name
        first = name.split()[0]
        if first and len(first) > 1:
            return first
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return None


def _resolve_names_from_cli() -> dict[str, str]:
    """
    Call `openclaw agents list --json` and return a mapping of
    agent_id → identityName for agents that have an identity set.
    Returns empty dict if the CLI is unavailable or fails.
    """
    try:
        result = subprocess.run(
            ["openclaw", "agents", "list", "--json"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return {}
        agents = json.loads(result.stdout)
        if not isinstance(agents, list):
            return {}
        return {
            a["id"]: a["identityName"]
            for a in agents
            if isinstance(a, dict) and a.get("id") and a.get("identityName")
        }
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError, json.JSONDecodeError):
        return {}


# ── GitHub Metrics Ingestion ────────────────────────────────────────────────

def _gh_available() -> bool:
    """Check if gh CLI is installed and authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True, text=True, timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def _gh_api(endpoint: str, paginate: bool = False) -> list | dict | None:
    """Call the GitHub API via gh CLI. Returns parsed JSON or None on error."""
    cmd = ["gh", "api", endpoint, "--header", "Accept: application/vnd.github+json"]
    if paginate:
        cmd.append("--paginate")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return None
        text = result.stdout.strip()
        if not text:
            return None
        # --paginate can produce concatenated JSON arrays; merge them
        if paginate and text.startswith("["):
            merged = []
            decoder = json.JSONDecoder()
            pos = 0
            while pos < len(text):
                # skip whitespace
                while pos < len(text) and text[pos] in " \t\n\r":
                    pos += 1
                if pos >= len(text):
                    break
                obj, end = decoder.raw_decode(text, pos)
                if isinstance(obj, list):
                    merged.extend(obj)
                else:
                    merged.append(obj)
                pos = end
            return merged
        return json.loads(text)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError, json.JSONDecodeError):
        return None


def _get_gh_authenticated_user() -> str | None:
    """Get the authenticated GitHub username via API."""
    data = _gh_api("/user")
    if isinstance(data, dict):
        return data.get("login")
    return None


def _discover_repos(login: str, verbose: bool = False) -> list[dict]:
    """
    Discover repos accessible to the authenticated user that have recent pushes.
    Returns list of {owner, name, full_name, pushed_at}.
    """
    repos = _gh_api("/user/repos?sort=pushed&per_page=100&type=all", paginate=True)
    if not isinstance(repos, list):
        return []

    # Filter to repos with a push in the last 90 days
    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    results = []
    for repo in repos:
        pushed_at = repo.get("pushed_at", "")
        try:
            pushed_at_dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            continue
        if pushed_at_dt >= cutoff:
            owner = repo.get("owner", {}).get("login", "")
            name = repo.get("name", "")
            if owner and name:
                results.append({
                    "owner": owner,
                    "name": name,
                    "full_name": f"{owner}/{name}",
                    "pushed_at": pushed_at,
                })
    if verbose:
        print(f"    Found {len(results)} repos with recent activity")
    return results


def _fetch_commit_sha_stats(owner: str, name: str, sha: str) -> tuple[int, int]:
    """Fetch additions/deletions for a single commit SHA. Returns (added, removed)."""
    detail = _gh_api(f"/repos/{owner}/{name}/commits/{sha}")
    if not isinstance(detail, dict):
        return 0, 0
    stats = detail.get("stats", {})
    return stats.get("additions", 0), stats.get("deletions", 0)


def _fetch_repo_commits_bulk(
    owner: str, name: str, login: str, since: str, until: str, verbose: bool = False,
) -> list[dict]:
    """
    Fetch ALL commits by login in a repo for the entire date range in one
    paginated call. Returns list of commit objects (merge commits excluded).
    """
    commits_data = _gh_api(
        f"/repos/{owner}/{name}/commits?author={login}&since={since}&until={until}&per_page=100",
        paginate=True,
    )
    if not isinstance(commits_data, list):
        return []

    results = []
    for c in commits_data:
        # Skip merge commits
        if len(c.get("parents", [])) > 1:
            continue
        sha = c.get("sha")
        # Extract commit date for bucketing
        commit_date_str = (
            c.get("commit", {}).get("author", {}).get("date", "")
            or c.get("commit", {}).get("committer", {}).get("date", "")
        )
        if sha and commit_date_str:
            results.append({
                "sha": sha,
                "owner": owner,
                "name": name,
                "date": commit_date_str[:10],  # YYYY-MM-DD
            })
    return results


def _fetch_prs_for_range(login: str, since: str, until: str) -> dict[str, int]:
    """
    Count PRs opened by login in a date range using a single search call.
    Returns {date_str: count} by fetching up to 100 results and bucketing by created_at.
    """
    query = f"author:{login} type:pr created:{since}..{until}"
    data = _gh_api(f"/search/issues?q={urllib.parse.quote(query)}&per_page=100")
    if not isinstance(data, dict):
        return {}

    counts: dict[str, int] = defaultdict(int)
    for item in data.get("items", []):
        created = item.get("created_at", "")[:10]
        if created:
            counts[created] += 1

    # If total_count > 100, we're missing some — but this covers the vast majority
    return dict(counts)


def collect_github_metrics(
    login: str,
    last_submission_date: str | None = None,
    verbose: bool = False,
) -> dict[str, dict]:
    """
    Collect GitHub commit and PR metrics per day.
    Returns {date_str: {commit_count, lines_added, lines_removed, pr_count}}.

    Uses bulk fetches (one per repo for entire range) + parallel SHA detail
    lookups for line stats. First run backfills up to 90 days; subsequent runs
    fetch only since last_submission_date.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    repos = _discover_repos(login, verbose=verbose)
    if not repos:
        if verbose:
            print("    No repos with recent activity found")
        return {}

    # Determine date range
    today = datetime.now(timezone.utc).date()
    if last_submission_date:
        try:
            start_date = datetime.strptime(last_submission_date, "%Y-%m-%d").date()
        except ValueError:
            start_date = today - timedelta(days=90)
    else:
        start_date = today - timedelta(days=90)

    # Ensure we don't go beyond 90 days (GitHub Events API limit)
    earliest = today - timedelta(days=90)
    if start_date < earliest:
        start_date = earliest

    since_iso = f"{start_date.isoformat()}T00:00:00Z"
    until_iso = f"{(today + timedelta(days=1)).isoformat()}T00:00:00Z"

    if verbose:
        print(f"    Collecting git metrics from {start_date} to {today} across {len(repos)} repos")

    daily_git: dict[str, dict] = defaultdict(lambda: {
        "commit_count": 0,
        "lines_added": 0,
        "lines_removed": 0,
        "pr_count": 0,
    })

    # Phase 1: Bulk-fetch all commits per repo (one paginated call each)
    all_commits: list[dict] = []
    for repo in repos:
        commits = _fetch_repo_commits_bulk(
            repo["owner"], repo["name"], login, since_iso, until_iso, verbose=verbose,
        )
        all_commits.extend(commits)
        if verbose and commits:
            print(f"      {repo['full_name']}: {len(commits)} commits")

    # Count commits per day
    for c in all_commits:
        daily_git[c["date"]]["commit_count"] += 1

    # Phase 2: Fetch line stats in parallel (ThreadPoolExecutor)
    if all_commits:
        sha_results: dict[str, tuple[int, int]] = {}

        with ThreadPoolExecutor(max_workers=10) as pool:
            future_to_commit = {
                pool.submit(_fetch_commit_sha_stats, c["owner"], c["name"], c["sha"]): c
                for c in all_commits
            }
            for future in as_completed(future_to_commit):
                c = future_to_commit[future]
                try:
                    added, removed = future.result()
                    daily_git[c["date"]]["lines_added"] += added
                    daily_git[c["date"]]["lines_removed"] += removed
                except Exception:
                    pass  # skip individual failures

        if verbose:
            total_added = sum(v["lines_added"] for v in daily_git.values())
            total_removed = sum(v["lines_removed"] for v in daily_git.values())
            print(f"    Line stats: +{total_added} -{total_removed}")

    # Phase 3: PRs — single search call for the entire range
    pr_counts = _fetch_prs_for_range(login, start_date.isoformat(), today.isoformat())
    for date_str, count in pr_counts.items():
        daily_git[date_str]["pr_count"] += count

    # Remove days with no activity
    daily_git = {d: v for d, v in daily_git.items() if any(v.values())}

    if verbose:
        total_commits = sum(v["commit_count"] for v in daily_git.values())
        total_prs = sum(v["pr_count"] for v in daily_git.values())
        print(f"    Git metrics: {total_commits} commits, {total_prs} PRs across {len(daily_git)} days")

    return dict(daily_git)


# ── Recurring Ingestion (Cron Registration) ─────────────────────────────────

CRON_JOB_NAME = "clawrank-ingest"


def _openclaw_available() -> bool:
    """Check if openclaw CLI is installed."""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True, text=True, timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def _find_cron_job_id() -> str | None:
    """Return the job ID of the clawrank-ingest cron job, or None if not found."""
    try:
        result = subprocess.run(
            ["openclaw", "cron", "list", "--json"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        for j in data.get("jobs", []):
            if j.get("name") == CRON_JOB_NAME:
                return j.get("id")
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError, json.JSONDecodeError):
        return None


def register_cron(script_path: str) -> None:
    """
    Register an OpenClaw cron job for recurring ClawRank ingestion (daily).
    No-ops silently if the job already exists. Skips gracefully if openclaw
    CLI is missing.
    """
    if not _openclaw_available():
        print("[cron:skipped] openclaw CLI not found — set up recurring ingestion manually")
        return

    existing_id = _find_cron_job_id()
    if existing_id:
        return

    abs_path = os.path.abspath(script_path)
    cmd = [
        "openclaw", "cron", "add",
        "--name", CRON_JOB_NAME,
        "--cron", "0 9 * * *",
        "--session", "isolated",
        "--json",
        "--description", "ClawRank metrics ingestion — submits agent token/git stats daily",
        "--message", f"Run ClawRank ingestion. Execute this command: python3 {abs_path}",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            # Parse job ID from JSON response for the removal hint
            job_id = None
            try:
                resp = json.loads(result.stdout)
                job_id = resp.get("id") or resp.get("job", {}).get("id")
            except (json.JSONDecodeError, AttributeError):
                pass
            remove_hint = f"openclaw cron rm {job_id}" if job_id else f'openclaw cron list --json  # then: openclaw cron rm <id>'
            print(f"[cron] Registered recurring ingestion (daily at 9am UTC). "
                  f"Remove with: {remove_hint}")
        else:
            stderr = (result.stderr or result.stdout or "").strip()
            print(f"[cron:skipped] Failed to register cron job: {stderr}", file=sys.stderr)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as e:
        print(f"[cron:skipped] Failed to register cron job: {e}", file=sys.stderr)


# ── Session Index Parsing ───────────────────────────────────────────────────

def discover_agents(agents_dir: Path) -> list[tuple[str, Path, str | None]]:
    """Return list of (agent_key, sessions.json path, display_name or None) for each agent."""
    results = []
    if not agents_dir.is_dir():
        return results

    # Priority 1: ask OpenClaw CLI for authoritative identity names
    cli_names = _resolve_names_from_cli()

    # Priority 2 fallback: find workspace paths from openclaw config → IDENTITY.md
    workspace_map = _load_workspace_map(agents_dir)

    for agent_dir in sorted(agents_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        index_path = agent_dir / "sessions" / "sessions.json"
        if index_path.is_file():
            display_name = cli_names.get(agent_dir.name) or _resolve_agent_name(agent_dir.name, workspace_map)
            results.append((agent_dir.name, index_path, display_name))
    return results


def _load_workspace_map(agents_dir: Path) -> dict[str, Path]:
    """Load agent→workspace mappings from openclaw.json."""
    config_path = agents_dir.parent / "openclaw.json"
    if not config_path.is_file():
        return {}

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

    result = {}
    agents_config = config.get("agents", {})

    # Default workspace applies to all agents unless overridden
    default_ws = agents_config.get("defaults", {}).get("workspace", "")
    if default_ws:
        # Apply default workspace to all agent dirs we find
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                result[agent_dir.name] = Path(default_ws).expanduser()

    # Per-agent workspace overrides
    entries = agents_config.get("entries", {})
    for agent_key, entry in entries.items():
        if isinstance(entry, dict) and entry.get("workspace"):
            result[agent_key] = Path(entry["workspace"]).expanduser()

    return result


def _resolve_agent_name(agent_key: str, workspace_map: dict[str, Path]) -> str | None:
    """
    Try to find a display name for an agent. Priority:
    1. IDENTITY.md in the agent's workspace (parses "Name: ..." line)
    2. None (caller falls back to agent_key)
    """
    workspace = workspace_map.get(agent_key)
    if not workspace:
        return None

    identity_path = workspace / "IDENTITY.md"
    if not identity_path.is_file():
        return None

    try:
        with open(identity_path, "r") as f:
            for line in f:
                # Match patterns like "- **Name:** Clawdius Maximus" or "Name: Foo"
                m = re.match(r"[-*\s]*Name[-*\s]*:\s*\**\s*(.+)", line, re.IGNORECASE)
                if m:
                    name = m.group(1).strip().rstrip("*").strip()
                    if name and name.lower() not in ("", "(not set)", "unknown"):
                        return name
    except OSError:
        pass

    return None


def load_session_index(index_path: Path) -> dict:
    """Load and return the sessions.json index."""
    with open(index_path, "r") as f:
        return json.load(f)


# ── JSONL Transcript Parsing ────────────────────────────────────────────────

def parse_transcript(session_path: Path, agent_key: str) -> tuple[list[dict], dict]:
    """
    Parse a single JSONL transcript file.
    Returns (usage_messages, session_stats) where session_stats contains
    counts for user messages, assistant turns, tool calls, tool breakdown, etc.
    """
    empty_stats = {
        "user_messages": 0,
        "assistant_messages": 0,
        "tool_calls": 0,
        "tool_names": defaultdict(int),
        "models_tokens": defaultdict(int),
    }
    if not session_path.is_file():
        return [], empty_stats

    messages = []
    stats = {
        "user_messages": 0,
        "assistant_messages": 0,
        "tool_calls": 0,
        "tool_names": defaultdict(int),
        "models_tokens": defaultdict(int),
    }
    current_model = ""
    current_provider = "unknown"

    with open(session_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type")

            if entry_type == "model_change":
                current_model = entry.get("modelId", current_model)
                current_provider = entry.get("provider", current_provider)
                continue

            if entry_type != "message":
                continue

            msg = entry.get("message")
            if not msg:
                continue

            role = msg.get("role")

            # Count user messages
            if role == "user":
                stats["user_messages"] += 1
                continue

            if role != "assistant":
                continue

            stats["assistant_messages"] += 1

            # Count tool calls in content blocks
            content = msg.get("content", "")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "toolCall":
                        stats["tool_calls"] += 1
                        tool_name = block.get("name", "unknown")
                        stats["tool_names"][tool_name] += 1

            usage = msg.get("usage")
            if not usage or not current_model:
                continue

            input_tokens = max(0, int(usage.get("input", 0) or 0))
            output_tokens = max(0, int(usage.get("output", 0) or 0))
            cache_read = max(0, int(usage.get("cacheRead", 0) or 0))
            cache_write = max(0, int(usage.get("cacheWrite", 0) or 0))
            total = max(
                input_tokens + output_tokens + cache_read + cache_write,
                int(usage.get("totalTokens", 0) or 0),
            )
            cost = max(0.0, float((usage.get("cost") or {}).get("total", 0) or 0))

            # Track tokens per model
            stats["models_tokens"][current_model] += total

            # Determine timestamp
            ts_ms = msg.get("timestamp")
            if not ts_ms:
                iso_ts = entry.get("timestamp")
                if iso_ts:
                    try:
                        dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
                        ts_ms = int(dt.timestamp() * 1000)
                    except (ValueError, TypeError):
                        pass
            if not ts_ms:
                ts_ms = int(session_path.stat().st_mtime * 1000)
            if not ts_ms:
                continue

            messages.append({
                "agent_key": agent_key,
                "timestamp_ms": int(ts_ms),
                "model_id": current_model,
                "provider_id": current_provider or "unknown",
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_read_tokens": cache_read,
                "cache_write_tokens": cache_write,
                "total_tokens": total,
                "estimated_cost_usd": cost,
                "session_id": session_path.stem,
            })

    return messages, stats


def resolve_session_path(index_path: Path, entry: dict) -> Path | None:
    """Resolve the session file path from an index entry."""
    session_file = (entry.get("sessionFile") or "").strip()
    if session_file:
        p = Path(session_file).expanduser()
        if p.is_absolute():
            return p
        return index_path.parent / p

    session_id = (entry.get("sessionId") or "").strip()
    if session_id:
        return index_path.parent / f"{session_id}.jsonl"

    return None


# ── Aggregation (Usage Messages → Daily Facts) ─────────────────────────────

def slugify(value: str) -> str:
    s = re.sub(r"[^\w\s-]", "", value.strip().lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s or "unknown-agent"


def title_case(value: str) -> str:
    return " ".join(w.capitalize() for w in re.split(r"[-_\s]+", value) if w)


def aggregate_to_daily_facts(
    messages: list[dict],
    session_stats: list[dict],
    agent_key: str,
    owner_name: str,
    agent_name: str,
    gh_username: str | None = None,
    git_metrics: dict[str, dict] | None = None,
) -> dict | None:
    """
    Aggregate usage messages for one agent into a DailyFactSubmission.
    Returns None if no messages.
    """
    if not messages:
        return None

    agent_slug = slugify(agent_name)

    # Bucket by date
    by_date: dict[str, dict] = defaultdict(lambda: {
        "total_tokens": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "estimated_cost_usd": 0.0,
        "sessions": set(),
        "session_bounds": defaultdict(lambda: {"min": float("inf"), "max": 0}),
        "hours": defaultdict(int),
        "model_totals": defaultdict(int),
        "user_messages": 0,
        "assistant_messages": 0,
        "tool_calls": 0,
        "tool_names": defaultdict(int),
        "models_tokens": defaultdict(int),
    })

    for m in messages:
        dt = datetime.fromtimestamp(m["timestamp_ms"] / 1000, tz=timezone.utc)
        date_str = dt.strftime("%Y-%m-%d")
        hour = dt.hour
        sid = m["session_id"]

        bucket = by_date[date_str]
        bucket["total_tokens"] += m["total_tokens"]
        bucket["input_tokens"] += m["input_tokens"]
        bucket["output_tokens"] += m["output_tokens"]
        bucket["cache_read_tokens"] += m["cache_read_tokens"]
        bucket["cache_write_tokens"] += m["cache_write_tokens"]
        bucket["estimated_cost_usd"] += m["estimated_cost_usd"]
        bucket["sessions"].add(sid)
        bounds = bucket["session_bounds"][sid]
        bounds["min"] = min(bounds["min"], m["timestamp_ms"])
        bounds["max"] = max(bounds["max"], m["timestamp_ms"])
        bucket["hours"][hour] += m["total_tokens"]
        bucket["model_totals"][m["model_id"]] += m["total_tokens"]

    # Merge session stats into date buckets
    # Session stats are per-session; we need to distribute them to the dates
    # where those sessions had activity. We map session_id → dates, then add stats.
    session_to_dates: dict[str, set[str]] = defaultdict(set)
    for m in messages:
        dt = datetime.fromtimestamp(m["timestamp_ms"] / 1000, tz=timezone.utc)
        date_str = dt.strftime("%Y-%m-%d")
        session_to_dates[m["session_id"]].add(date_str)

    for ss in session_stats:
        sid = ss.get("session_id", "")
        dates = session_to_dates.get(sid, set())
        if not dates:
            # If we can't attribute to a date, skip
            continue
        # For simplicity, add the full counts to each date the session touched.
        # Most sessions span a single date, so this is usually exact.
        # For multi-day sessions, this slightly inflates per-day counts but
        # the totals remain correct at the agent level.
        for date_str in dates:
            bucket = by_date[date_str]
            bucket["user_messages"] += ss.get("user_messages", 0)
            bucket["assistant_messages"] += ss.get("assistant_messages", 0)
            bucket["tool_calls"] += ss.get("tool_calls", 0)
            for tool_name, count in ss.get("tool_names", {}).items():
                bucket["tool_names"][tool_name] += count
            for model, tokens in ss.get("models_tokens", {}).items():
                bucket["models_tokens"][model] += tokens

    facts = []
    for date_str in sorted(by_date.keys()):
        b = by_date[date_str]

        longest_run_s = 0
        for bounds in b["session_bounds"].values():
            dur = max(0, round((bounds["max"] - bounds["min"]) / 1000))
            longest_run_s = max(longest_run_s, dur)

        most_active_hour = None
        if b["hours"]:
            most_active_hour = max(b["hours"], key=lambda h: (b["hours"][h], -h))

        top_model = None
        if b["model_totals"]:
            top_model = max(b["model_totals"], key=lambda m: (b["model_totals"][m], m))

        # Build top_tools as dict (sorted by count desc, top 20)
        top_tools = None
        if b["tool_names"]:
            sorted_tools = sorted(b["tool_names"].items(), key=lambda x: -x[1])[:20]
            top_tools = dict(sorted_tools)

        # Build models_used as dict
        models_used = None
        if b["models_tokens"]:
            sorted_models = sorted(b["models_tokens"].items(), key=lambda x: -x[1])
            models_used = dict(sorted_models)

        facts.append({
            "date": date_str,
            "totalTokens": b["total_tokens"],
            "inputTokens": b["input_tokens"],
            "outputTokens": b["output_tokens"],
            "cacheReadTokens": b["cache_read_tokens"],
            "cacheWriteTokens": b["cache_write_tokens"],
            "sessionCount": len(b["sessions"]),
            "longestRunSeconds": longest_run_s,
            "mostActiveHour": most_active_hour,
            "topModel": top_model,
            "estimatedCostUsd": round(b["estimated_cost_usd"], 4),
            "userMessageCount": b["user_messages"],
            "assistantMessageCount": b["assistant_messages"],
            "toolCallCount": b["tool_calls"],
            "topTools": top_tools,
            "modelsUsed": models_used,
            "sourceType": "skill",
            "sourceAdapter": "openclaw",
            "datePrecision": "day",
        })

    # Merge git metrics into existing facts and create new facts for git-only days
    if git_metrics:
        fact_dates = {f["date"]: f for f in facts}
        for date_str, gm in git_metrics.items():
            if date_str in fact_dates:
                # Merge into existing fact
                fact_dates[date_str]["commitCount"] = gm["commit_count"]
                fact_dates[date_str]["linesAdded"] = gm["lines_added"]
                fact_dates[date_str]["linesRemoved"] = gm["lines_removed"]
                fact_dates[date_str]["prCount"] = gm["pr_count"]
            else:
                # Create a git-only fact (zero tokens)
                facts.append({
                    "date": date_str,
                    "totalTokens": 0,
                    "commitCount": gm["commit_count"],
                    "linesAdded": gm["lines_added"],
                    "linesRemoved": gm["lines_removed"],
                    "prCount": gm["pr_count"],
                    "sourceType": "skill",
                    "sourceAdapter": "openclaw",
                    "datePrecision": "day",
                })
        # Re-sort by date
        facts.sort(key=lambda f: f["date"])

    agent_data = {
        "slug": agent_slug,
        "agentName": agent_name,
        "ownerName": owner_name,
        "state": "live",
        "sourceOfTruth": "skill",
    }
    if gh_username:
        agent_data["primaryGithubUsername"] = gh_username

    return {
        "agent": agent_data,
        "facts": facts,
    }


# ── HTTP Submission ─────────────────────────────────────────────────────────

def submit(endpoint: str, token: str, submission: dict) -> dict:
    """POST a DailyFactSubmission to the ClawRank API. Returns response JSON."""
    url = f"{endpoint}{SUBMIT_PATH}"
    body = json.dumps(submission).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}: {error_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection error: {e.reason}"}


# ── Main ────────────────────────────────────────────────────────────────────

def _get_gh_token() -> str | None:
    """Get the current GitHub auth token from gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True, text=True, timeout=5,
        )
        token = result.stdout.strip()
        if token and result.returncode == 0:
            return token
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return None


CLI_AUTH_PATH = "/api/auth/cli"


def run_setup(endpoint: str, verbose: bool = False) -> str | None:
    """
    Auto-setup: exchange a GitHub token for a ClawRank API token.
    Returns the raw cr_live_ token on success, or None on failure.
    """
    print("▸ ClawRank auto-setup")
    print()

    # Step 1: Get GitHub token from gh CLI
    print("  [1/3] Getting GitHub identity from gh CLI...")
    gh_token = _get_gh_token()
    if not gh_token:
        print("  ✗ Could not get GitHub token. Make sure gh CLI is installed and authenticated.", file=sys.stderr)
        print("    Run: gh auth login", file=sys.stderr)
        return None
    if verbose:
        print(f"    Got GitHub token ({gh_token[:8]}...)")

    # Step 2: Exchange for ClawRank API token
    print("  [2/3] Registering with ClawRank...")
    url = f"{endpoint}{CLI_AUTH_PATH}"
    body = json.dumps({"githubToken": gh_token, "label": "auto-setup"}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"  ✗ Registration failed: HTTP {e.code}: {error_body}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"  ✗ Connection error: {e.reason}", file=sys.stderr)
        return None

    cr_token = data.get("token")
    user_login = data.get("user", {}).get("login", "?")
    claimed = data.get("claimedAgents", [])

    if not cr_token:
        print(f"  ✗ No token in response: {data}", file=sys.stderr)
        return None

    print(f"    Authenticated as: {user_login}")
    if claimed:
        for a in claimed:
            print(f"    Auto-claimed agent: {a.get('agentName', '?')}")

    # Step 3: Write to openclaw.json skill config
    print("  [3/3] Saving token to OpenClaw config...")
    config_path = Path.home() / ".openclaw" / "openclaw.json"

    try:
        if config_path.is_file():
            with open(config_path, "r") as f:
                config = json.load(f)
        else:
            config = {}

        # Ensure nested structure exists
        config.setdefault("skills", {})
        config["skills"].setdefault("entries", {})
        config["skills"]["entries"].setdefault("clawrank", {})
        config["skills"]["entries"]["clawrank"]["enabled"] = True
        config["skills"]["entries"]["clawrank"].setdefault("env", {})
        config["skills"]["entries"]["clawrank"]["env"]["CLAWRANK_API_TOKEN"] = cr_token

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"    Token saved to {config_path}")
    except (OSError, json.JSONDecodeError) as e:
        # Config write failed — print manual instructions
        print(f"    ⚠ Could not write config ({e}). Add manually:", file=sys.stderr)
        print(f'    CLAWRANK_API_TOKEN="{cr_token}"', file=sys.stderr)
        # Still return the token so the current run can proceed
        pass

    print()
    print("  ✓ Setup complete! Your agent is now connected to ClawRank.")
    print()
    return cr_token


def main():
    parser = argparse.ArgumentParser(
        description="Ingest OpenClaw session data into ClawRank",
    )
    parser.add_argument("--dry-run", action="store_true", help="Parse and aggregate but don't submit")
    parser.add_argument("--setup", action="store_true", help="Auto-setup: authenticate via GitHub and configure token")
    parser.add_argument("--endpoint", type=str, default=None, help="ClawRank API base URL")
    parser.add_argument("--agents-dir", type=str, default=None, help="Override agents directory")
    parser.add_argument("--recurring", action="store_true", help="Register a daily cron job for automatic ingestion")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    endpoint = get_endpoint(args.endpoint)
    token = get_token()
    state = load_state()
    owner_name = resolve_owner_name()
    agent_name_override = get_agent_name_override()
    gh_username = _get_gh_authenticated_user() or _get_gh_username()
    agents_dir = get_agents_dir(args.agents_dir)

    # If --setup flag or no token configured, run auto-setup
    if args.setup or (not token and not args.dry_run):
        setup_token = run_setup(endpoint, verbose=args.verbose)
        if setup_token:
            token = setup_token
            # Re-read env in case config changed
            os.environ["CLAWRANK_API_TOKEN"] = setup_token
        elif not args.dry_run:
            print("Setup failed. Run 'gh auth login' first, or set CLAWRANK_API_TOKEN manually.", file=sys.stderr)
            sys.exit(1)

    if not args.dry_run and not token:
        print("ERROR: CLAWRANK_API_TOKEN is required (set in env or openclaw.json skill config)", file=sys.stderr)
        sys.exit(1)

    if not agents_dir.is_dir():
        print(f"ERROR: Agents directory not found: {agents_dir}", file=sys.stderr)
        sys.exit(1)

    agents = discover_agents(agents_dir)
    if not agents:
        print(f"No agents found in {agents_dir}", file=sys.stderr)
        sys.exit(0)

    print(f"ClawRank ingestion — {len(agents)} agent(s) found in {agents_dir}")
    print(f"Endpoint: {endpoint}")
    print(f"Owner: {owner_name}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()

    # ── GitHub metrics collection ───────────────────────────────────────────
    git_metrics: dict[str, dict] | None = None
    last_git_sync_date = state.get("lastGitSyncDate")
    if _gh_available() and gh_username:
        print("  [git-metrics] gh CLI detected — collecting GitHub commit & PR metrics...")
        try:
            git_metrics = collect_github_metrics(
                login=gh_username,
                last_submission_date=last_git_sync_date,
                verbose=args.verbose,
            )
            if git_metrics:
                total_git_commits = sum(v["commit_count"] for v in git_metrics.values())
                total_git_prs = sum(v["pr_count"] for v in git_metrics.values())
                print(f"  [git-metrics] {total_git_commits} commits, {total_git_prs} PRs across {len(git_metrics)} days")
            else:
                print("  [git-metrics] No commit/PR activity found in last 90 days")
        except Exception as e:
            print(f"  [git-metrics:skipped] Error collecting git metrics: {e}", file=sys.stderr)
            git_metrics = None
    else:
        reason = "gh CLI not found" if not _gh_available() else "GitHub username not resolved"
        print(f"  [git-metrics:skipped] {reason} — submitting token metrics only")
    print()

    total_messages = 0
    total_facts = 0
    total_submitted = 0
    submitted_shares: list[dict] = []

    for agent_key, index_path, display_name in agents:
        index = load_session_index(index_path)
        all_messages = []
        all_session_stats = []

        for session_key, entry in index.items():
            session_path = resolve_session_path(index_path, entry)
            if not session_path or not session_path.is_file():
                continue
            msgs, stats = parse_transcript(session_path, agent_key)
            stats["session_id"] = session_path.stem
            all_messages.extend(msgs)
            all_session_stats.append(stats)

        if not all_messages:
            if args.verbose:
                print(f"  [{agent_key}] No usage data found")
            continue

        agent_name = agent_name_override or display_name or title_case(agent_key)
        submission = aggregate_to_daily_facts(all_messages, all_session_stats, agent_key, owner_name, agent_name, gh_username, git_metrics)
        if not submission:
            continue

        n_facts = len(submission["facts"])
        n_msgs = len(all_messages)
        total_tokens = sum(f["totalTokens"] for f in submission["facts"])
        total_cost = sum(f.get("estimatedCostUsd", 0) for f in submission["facts"])
        total_messages += n_msgs
        total_facts += n_facts

        print(f"  [{agent_key}] {n_msgs} messages → {n_facts} daily facts, "
              f"{total_tokens:,} tokens, ${total_cost:.2f}")

        if args.dry_run:
            if args.verbose:
                print(json.dumps(submission, indent=2, default=str))
            continue

        result = submit(endpoint, token, submission)
        if result.get("error"):
            print(f"    ✗ Submit failed: {result['error']}", file=sys.stderr)
        else:
            slug = result.get("agent", {}).get("slug", "")
            print(f"    ✓ Submitted → {slug or '?'} "
                  f"({result.get('upsertedFacts', 0)} facts upserted)")
            total_submitted += n_facts
            share = result.get("share")
            if slug and share:
                submitted_shares.append(share)
            elif slug:
                submitted_shares.append({
                    "shareUrl": f"{endpoint}/a/{slug}",
                    "shareText": None,
                })

    if not args.dry_run and total_submitted > 0 and _gh_available() and gh_username:
        state["lastGitSyncDate"] = datetime.now(timezone.utc).date().strftime("%Y-%m-%d")
        save_state(state)

    # Print share info
    if not args.dry_run and submitted_shares:
        print()
        for share in submitted_shares:
            if share.get("shareText"):
                print(f"  🏆 {share['shareText']}")
            else:
                print(f"  🏆 View your ranking: {share['shareUrl']}")

    # Register recurring cron job if --recurring flag is set
    if not args.dry_run and total_submitted > 0 and args.recurring:
        register_cron(__file__)

    # Hint about recurring option if not already set up
    if not args.dry_run and total_submitted > 0 and not args.recurring:
        if _openclaw_available() and not _find_cron_job_id():
            print()
            print("Tip: To submit daily automatically, re-run with --recurring")

    print()
    print(f"Done. {total_messages} messages parsed, {total_facts} daily facts generated"
          + (f", {total_submitted} submitted" if not args.dry_run else " (dry run, nothing submitted)"))


if __name__ == "__main__":
    main()
