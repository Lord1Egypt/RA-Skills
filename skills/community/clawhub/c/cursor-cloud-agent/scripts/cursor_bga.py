#!/usr/bin/env python3
"""
cursor-agent skill: Manage Cursor Cloud Agents via the official API v0.

Usage:
  cursor_bga.py create   --repo owner/repo --prompt "task" [--ref main] [--model MODEL] [--auto-pr] [--branch NAME] [--wait] [--no-direct]
  cursor_bga.py list     [--limit N] [--pr-url URL]
  cursor_bga.py get      --agent-id ID
  cursor_bga.py conversation --agent-id ID
  cursor_bga.py followup --agent-id ID --message "instructions"
  cursor_bga.py stop     --agent-id ID
  cursor_bga.py delete   --agent-id ID
  cursor_bga.py check    --agent-id ID [--interval SEC] [--timeout SEC]
  cursor_bga.py models
  cursor_bga.py repos    [--search QUERY]
  cursor_bga.py setup    # interactive API key setup

Authentication:
  API key is read from (in priority order):
    1. --api-key argument
    2. CURSOR_API_KEY environment variable
    3. ~/.cursor_api_key file

API Docs: https://cursor.com/docs/cloud-agent/api/endpoints
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = "https://api.cursor.com/v0"
KEY_FILE = os.path.expanduser("~/.cursor_api_key")
DIRECT_SUFFIX = "\n\n请直接执行修改并提交代码，不需要等待确认，不要只输出方案。"


# ── Helpers ──────────────────────────────────────────────────────────────

def load_api_key(key_arg: str = "") -> str:
    """Load API key from arg, env, or file."""
    if key_arg:
        return key_arg.strip()
    key = os.environ.get("CURSOR_API_KEY", "").strip()
    if key:
        return key
    if os.path.isfile(KEY_FILE):
        return open(KEY_FILE).read().strip()
    print(
        "[ERROR] No Cursor API key found.\n"
        "  Provide via --api-key, CURSOR_API_KEY env, or ~/.cursor_api_key\n"
        "  Run: cursor_bga.py setup  for instructions.",
        file=sys.stderr,
    )
    sys.exit(1)


def api(method: str, path: str, api_key: str, body: dict | None = None) -> dict | list | None:
    """Call the Cursor Cloud Agents API v0."""
    url = f"{API_BASE}{path}"
    credentials = base64.b64encode(f"{api_key}:".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "User-Agent": "openclaw-cursor-agent/2.0",
    }

    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            if not raw:
                return None
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        if e.code == 401:
            print("[ERROR] Authentication failed (401). Check your API key.", file=sys.stderr)
            print("  Get a new key at: https://cursor.com/dashboard (Integrations tab)", file=sys.stderr)
        elif e.code == 403:
            print("[ERROR] Forbidden (403). Your plan may not support this feature.", file=sys.stderr)
        elif e.code == 404:
            print(f"[ERROR] Not found (404): {path}", file=sys.stderr)
        elif e.code == 429:
            print("[ERROR] Rate limited (429). Please wait and try again.", file=sys.stderr)
        else:
            print(f"[ERROR] HTTP {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)


def format_agent(a: dict) -> str:
    """Format an agent summary line."""
    aid = a.get("id", "?")
    status = a.get("status", "?")
    name = a.get("name", "")[:50]
    repo = a.get("source", {}).get("repository", "")
    created = a.get("createdAt", "")[:19]
    return f"  {aid}  {status:<10}  {created}  {repo}  {name}"


# ── Background Watcher ────────────────────────────────────────────────────

def _find_openclaw_bin() -> str:
    """Find the correct openclaw binary (prefer npm-global version which supports all plugins)."""
    import shutil
    candidates = [
        os.path.expanduser("~/.npm-global/bin/openclaw"),
        "/usr/local/bin/openclaw",
    ]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return shutil.which("openclaw") or "openclaw"


def _send_feishu(message: str, target: str = ""):
    """Send message to Feishu via openclaw CLI."""
    import subprocess
    resolved_target = target or os.environ.get("CURSOR_NOTIFY_TARGET", "")
    if not resolved_target:
        return False
    bin_path = _find_openclaw_bin()
    cmd = [
        bin_path, "message", "send",
        "--channel", "feishu",
        "--target", resolved_target,
        "--message", message,
    ]
    try:
        result = subprocess.run(cmd, timeout=30, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def _spawn_background_watcher(agent_id: str, api_key: str, agent_url: str, name: str, notify_target: str = ""):
    """Spawn a background process that polls until done, then notifies Feishu."""
    import subprocess, sys, textwrap

    watcher_code = textwrap.dedent(f"""
        import time, json, urllib.request, urllib.error, base64, subprocess, shutil, os

        API_BASE = "https://api.cursor.com/v0"
        agent_id = {repr(agent_id)}
        api_key  = {repr(api_key)}
        agent_url = {repr(agent_url)}
        name      = {repr(name)}
        notify_target = {repr(notify_target)}

        def call(path):
            creds = base64.b64encode(f"{{api_key}}:".encode()).decode()
            req = urllib.request.Request(
                f"{{API_BASE}}{{path}}",
                headers={{"Authorization": f"Basic {{creds}}", "User-Agent": "openclaw-cursor-watcher/1.0"}},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())

        def notify(msg):
            target = notify_target or os.environ.get("CURSOR_NOTIFY_TARGET", "")
            if not target:
                return
            # prefer npm-global openclaw which supports all plugins
            bin_candidates = [
                os.path.expanduser("~/.npm-global/bin/openclaw"),
                "/usr/local/bin/openclaw",
            ]
            bin_path = next((c for c in bin_candidates if os.path.isfile(c)), "openclaw")
            cmd = [
                bin_path, "message", "send",
                "--channel", "feishu",
                "--target", target,
                "--message", msg,
            ]
            subprocess.run(cmd, timeout=30, capture_output=True)

        # Poll every 3s for up to 30min
        for _ in range(600):
            time.sleep(3)
            try:
                d = call(f"/agents/{{agent_id}}")
                status = d.get("status", "?")
                branch = d.get("target", {{}}).get("branchName", "")
                pr_url = d.get("target", {{}}).get("prUrl", "")
                if status == "FINISHED":
                    msg = (
                        f"✅ Cursor Agent 完成\\n"
                        f"任务：{{name}}\\n"
                        f"分支：{{branch}}\\n"
                        + (f"PR：{{pr_url}}\\n" if pr_url else "")
                        + f"Agent：{{agent_url}}"
                    )
                    notify(msg)
                    break
                elif status in ("FAILED", "STOPPED"):
                    conv = call(f"/agents/{{agent_id}}/conversation")
                    msgs = conv if isinstance(conv, list) else conv.get("messages", [])
                    last = msgs[-1].get("text", "") if msgs else ""
                    msg = (
                        f"❌ Cursor Agent {{status}}\\n"
                        f"任务：{{name}}\\n"
                        f"最后输出：{{last[:200]}}\\n"
                        f"Agent：{{agent_url}}"
                    )
                    notify(msg)
                    break
            except Exception as e:
                pass
    """)

    subprocess.Popen(
        [sys.executable, "-c", watcher_code],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


# ── Commands ─────────────────────────────────────────────────────────────

def _preflight(args, key):
    """Pre-flight checks before creating an agent. Exits on failure."""
    errors = []
    warnings = []

    # 1. API key validity
    print("[PRE] Checking API key ...", file=sys.stderr)
    try:
        models = api("GET", "/models", key)
        model_list = models if isinstance(models, list) else models.get("models", [])
        if not model_list:
            errors.append("API key valid but no models available — check your Cursor plan.")
        else:
            print(f"  ✓ API key OK ({len(model_list)} models available)", file=sys.stderr)
    except SystemExit:
        # api() already printed the error and called sys.exit
        raise
    except Exception as e:
        errors.append(f"API key check failed: {e}")

    # 2. Repo accessibility
    repo_name = args.repo.replace("github.com/", "").replace("https://", "").rstrip("/")
    print(f"[PRE] Checking repo access: {repo_name} ...", file=sys.stderr)
    try:
        import urllib.parse
        search_term = repo_name.split("/")[-1] if "/" in repo_name else repo_name
        result = api("GET", f"/repositories?search={urllib.parse.quote(search_term)}", key)
        repos = result if isinstance(result, list) else result.get("repositories", [])
        repo_names = [_normalize_repo_name(r) for r in repos]
        # Check if our repo is in the list (match with or without owner)
        found = any(repo_name in rn or rn.endswith(f"/{repo_name}") or repo_name.endswith(f"/{rn}") for rn in repo_names)
        if found:
            print(f"  ✓ Repo '{repo_name}' accessible", file=sys.stderr)
        else:
            errors.append(
                f"Repo '{repo_name}' not found in Cursor's accessible repos.\n"
                f"  Available: {', '.join(repo_names[:10])}\n"
                f"  Fix: Go to GitHub → Settings → Applications → Cursor and grant access to the repo."
            )
    except SystemExit:
        raise
    except Exception as e:
        warnings.append(f"Repo check inconclusive: {e}")

    # 3. Auto-PR permission check (via gh CLI)
    if args.auto_pr:
        print("[PRE] Checking GitHub PR permissions ...", file=sys.stderr)
        import shutil, subprocess
        gh = shutil.which("gh")
        if gh:
            try:
                # Check if we can query the repo's installed apps / collaborator permissions
                r = subprocess.run(
                    [gh, "api", f"repos/{repo_name}", "--jq", ".permissions"],
                    capture_output=True, text=True, timeout=10,
                )
                if r.returncode == 0 and r.stdout.strip():
                    perms = json.loads(r.stdout.strip()) if r.stdout.strip().startswith("{") else {}
                    if perms.get("push") or perms.get("admin"):
                        print(f"  ✓ GitHub push/admin access confirmed", file=sys.stderr)
                    else:
                        warnings.append(
                            "GitHub user has read-only access to this repo. "
                            "auto-PR depends on Cursor's GitHub App having write access. "
                            "If PR creation fails, use `gh pr create` as fallback."
                        )
                else:
                    warnings.append("Could not verify GitHub permissions (gh api returned non-zero).")
            except Exception as e:
                warnings.append(f"GitHub permission check skipped: {e}")
        else:
            warnings.append("gh CLI not found — skipping GitHub permission check.")

    # Report
    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}", file=sys.stderr)
    if errors:
        print(f"\n[PREFLIGHT FAILED] {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

    print("[PRE] All checks passed ✓\n", file=sys.stderr)


def cmd_create(args):
    """Launch a new Cloud Agent."""
    key = load_api_key(args.api_key)

    # Pre-flight checks
    if not getattr(args, "skip_preflight", False):
        _preflight(args, key)

    prompt_text = args.prompt
    if not args.no_direct:
        prompt_text += DIRECT_SUFFIX
    body = {
        "prompt": {"text": prompt_text},
        "source": {"repository": args.repo if args.repo.startswith("github.com/") or args.repo.startswith("https://") else f"github.com/{args.repo}"},
    }
    if args.ref:
        body["source"]["ref"] = args.ref
    if args.model:
        body["model"] = args.model

    target = {}
    if args.auto_pr:
        target["autoCreatePr"] = True
    if args.branch:
        target["autoBranch"] = True
        target["branchName"] = args.branch
    elif args.auto_pr:
        target["autoBranch"] = True
    if target:
        body["target"] = target

    print(f"[...] Launching Cloud Agent for repo: {args.repo}", file=sys.stderr)
    result = api("POST", "/agents", key, body)

    agent_id = result.get("id", "?")
    status = result.get("status", "?")
    name = result.get("name", "")
    agent_url = f"https://cursor.com/agents/{agent_id}"

    print(f"\n{'='*56}")
    print(f"  🤖 Cursor Cloud Agent Launched!")
    print(f"{'='*56}")
    print(f"  Agent ID : {agent_id}")
    print(f"  Status   : {status}")
    if name:
        print(f"  Name     : {name}")
    print(f"{'='*56}")
    print(f"  🔗 {agent_url}")
    print(f"{'='*56}\n")

    # Try to open URL in browser
    import subprocess, shutil
    for cmd in ["xdg-open", "open", "sensible-browser"]:
        if shutil.which(cmd):
            try:
                subprocess.Popen([cmd, agent_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break
            except Exception:
                pass

    # ── 立即通知飞书 ──────────────────────────────────────────
    notify_target = getattr(args, "notify", None) or os.environ.get("CURSOR_NOTIFY_TARGET", "")
    branch = result.get("target", {}).get("branchName", "")
    instant_msg = (
        f"🤖 Cursor Agent 已启动\n"
        f"任务：{name}\n"
        f"分支：{branch}\n"
        f"Agent：{agent_url}"
    )
    _send_feishu(instant_msg, notify_target)

    # ── 后台监控，完成后再发一条 ─────────────────────────────
    _spawn_background_watcher(agent_id, key, agent_url, name, notify_target)

    print(f"\n[OK] Cloud Agent launched: {agent_id}", file=sys.stderr)

    # ── --wait: block until agent finishes ────────────────────
    if args.wait:
        import types
        check_args = types.SimpleNamespace(
            api_key=args.api_key,
            agent_id=agent_id,
            interval=15,
            timeout=600,
        )
        return _do_check(check_args, key)

    return result


def cmd_list(args):
    """List Cloud Agents."""
    key = load_api_key(args.api_key)
    params = []
    if args.limit:
        params.append(f"limit={args.limit}")
    if args.pr_url:
        params.append(f"prUrl={urllib.parse.quote(args.pr_url)}")
    query = f"?{'&'.join(params)}" if params else ""

    result = api("GET", f"/agents{query}", key)
    agents = result if isinstance(result, list) else result.get("agents", result.get("data", []))

    if not agents:
        print("No agents found.")
        return

    print(f"  {'ID':<36}  {'STATUS':<10}  {'CREATED':<19}  {'REPO':<30}  NAME")
    print("  " + "-" * 110)
    for a in agents:
        print(format_agent(a))
    print(f"\n  Total: {len(agents)} agent(s)")


def cmd_get(args):
    """Get agent details."""
    key = load_api_key(args.api_key)
    result = api("GET", f"/agents/{args.agent_id}", key)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_conversation(args):
    """Get agent conversation history."""
    key = load_api_key(args.api_key)
    result = api("GET", f"/agents/{args.agent_id}/conversation", key)
    messages = result if isinstance(result, list) else result.get("messages", [])
    for msg in messages:
        role = msg.get("role", "?")
        text = msg.get("text", msg.get("content", ""))
        print(f"[{role}] {text}\n")


def cmd_followup(args):
    """Send follow-up instructions to a running agent."""
    key = load_api_key(args.api_key)
    body = {"prompt": {"text": args.message}}
    result = api("POST", f"/agents/{args.agent_id}/followup", key, body)
    print(f"[OK] Follow-up sent to agent {args.agent_id}", file=sys.stderr)
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_stop(args):
    """Stop a running agent."""
    key = load_api_key(args.api_key)
    api("POST", f"/agents/{args.agent_id}/stop", key, {})
    print(f"[OK] Agent {args.agent_id} stopped.", file=sys.stderr)


def cmd_delete(args):
    """Delete an agent permanently."""
    key = load_api_key(args.api_key)
    api("DELETE", f"/agents/{args.agent_id}", key)
    print(f"[OK] Agent {args.agent_id} deleted.", file=sys.stderr)


def cmd_models(args):
    """List available models."""
    key = load_api_key(args.api_key)
    result = api("GET", "/models", key)
    models = result if isinstance(result, list) else result.get("models", [])
    print("Available models:")
    for m in models:
        if isinstance(m, str):
            print(f"  - {m}")
        else:
            name = m.get("id", m.get("name", str(m)))
            print(f"  - {name}")


def _normalize_repo_name(r) -> str:
    """Extract owner/repo from various API response formats."""
    if isinstance(r, str):
        # Strip github.com/ prefix if present
        name = r.replace("https://github.com/", "").replace("github.com/", "").rstrip("/")
        return name
    # Dict: prefer full_name, fall back to name, then url parsing
    full = r.get("full_name", "")
    if full and "/" in full:
        return full.replace("github.com/", "")
    name = r.get("name", "")
    owner = r.get("owner", {})
    if isinstance(owner, dict):
        owner_name = owner.get("login", owner.get("name", ""))
        if owner_name and name:
            return f"{owner_name}/{name}"
    url = r.get("url", r.get("html_url", ""))
    if "github.com/" in url:
        parts = url.split("github.com/")[-1].rstrip("/").split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
    return full or name or str(r)


def cmd_repos(args):
    """List accessible repositories."""
    key = load_api_key(args.api_key)
    params = f"?search={urllib.parse.quote(args.search)}" if args.search else ""
    result = api("GET", f"/repositories{params}", key)
    repos = result if isinstance(result, list) else result.get("repositories", [])
    if not repos:
        print("No repositories found.")
        return
    print("Accessible repositories (use with --repo):")
    for r in repos:
        print(f"  - {_normalize_repo_name(r)}")


def _do_check(args, key):
    """Shared check logic: poll agent until terminal state, print summary."""
    import time
    agent_id = args.agent_id
    interval = args.interval
    timeout = args.timeout
    elapsed = 0

    print(f"[...] Watching agent {agent_id} (poll every {interval}s, timeout {timeout}s)", file=sys.stderr)

    status = "?"
    while elapsed < timeout:
        result = api("GET", f"/agents/{agent_id}", key)
        status = result.get("status", "?")
        name = result.get("name", "")
        branch = result.get("target", {}).get("branchName", "")
        pr_url = result.get("target", {}).get("prUrl", "")
        auto_pr = result.get("target", {}).get("autoCreatePr", False)
        agent_url = f"https://cursor.com/agents/{agent_id}"

        if status in ("FINISHED", "FAILED", "STOPPED"):
            lines_added = result.get("linesAdded", 0)
            lines_removed = result.get("linesRemoved", 0)
            files_changed = result.get("filesChanged", 0)

            print(f"\n{'='*56}")
            print(f"  Agent {status}")
            print(f"{'='*56}")
            if name:
                print(f"  Name     : {name}")
            print(f"  Status   : {status}")
            if branch:
                print(f"  Branch   : {branch}")
            if pr_url:
                print(f"  PR       : {pr_url}")
            if files_changed:
                print(f"  Changes  : {files_changed} file(s), +{lines_added} -{lines_removed}")
            print(f"  Agent    : {agent_url}")

            # PR fallback hint
            if auto_pr and not pr_url and status == "FINISHED" and branch:
                repo = result.get("source", {}).get("repository", "")
                repo_short = repo.replace("github.com/", "")
                print(f"\n  [WARN] --auto-pr was set but no PR was created.")
                print(f"  Create manually:")
                print(f"    gh pr create --repo {repo_short} --head {branch} --base main --fill")

            print(f"{'='*56}")

            # Conversation summary
            if status == "FINISHED":
                try:
                    conv = api("GET", f"/agents/{agent_id}/conversation", key)
                    messages = conv if isinstance(conv, list) else conv.get("messages", [])
                    if messages:
                        last_text = messages[-1].get("text", messages[-1].get("content", ""))
                        # Truncate to last 500 chars for summary
                        summary = last_text.strip()
                        if len(summary) > 500:
                            summary = "..." + summary[-500:]
                        print(f"\n  [Summary] Agent's final message:\n")
                        for line in summary.split("\n"):
                            print(f"    {line}")
                        print()
                except Exception:
                    pass

            if status != "FINISHED":
                print(f"[WARN] Agent did not finish successfully (status: {status})", file=sys.stderr)
                sys.exit(1)
            return result

        # Still running
        mins, secs = divmod(elapsed, 60)
        print(f"  [{mins:02d}:{secs:02d}] status={status}", file=sys.stderr)
        time.sleep(interval)
        elapsed += interval

    print(f"[ERROR] Timeout after {timeout}s. Agent still {status}.", file=sys.stderr)
    print(f"  Check manually: python3 cursor_bga.py get --agent-id {agent_id}", file=sys.stderr)
    sys.exit(1)


def cmd_check(args):
    """Poll agent status until finished, then print summary."""
    key = load_api_key(args.api_key)
    return _do_check(args, key)


def cmd_setup(_args):
    """Print API key setup instructions."""
    print("""
┌─────────────────────────────────────────────────────────┐
│           Cursor Cloud Agent - API Key Setup            │
└─────────────────────────────────────────────────────────┘

Step 1: Get your API key
  1. Open https://cursor.com/dashboard
  2. Navigate to "Integrations" tab
  3. Click "Generate API Key"
  4. Copy the key

Step 2: Save the key (choose one method)

  Method A — File (recommended):
    echo 'your_api_key_here' > ~/.cursor_api_key
    chmod 600 ~/.cursor_api_key

  Method B — Environment variable:
    export CURSOR_API_KEY='your_api_key_here'
    # Add to ~/.bashrc or ~/.zshrc for persistence

Step 3: Verify
    python3 cursor_bga.py models
    # Should list available models

Requirements:
  - Active Cursor account (Trial or Paid plan)
  - Usage-based pricing enabled
  - GitHub/GitLab account connected with repo permissions

Docs: https://cursor.com/docs/cloud-agent/api/endpoints
""")


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    import urllib.parse  # deferred import for param encoding

    p = argparse.ArgumentParser(
        description="Cursor Cloud Agent CLI (Official API v0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--api-key", default="", dest="api_key", help="Cursor API key")
    sub = p.add_subparsers(dest="cmd")

    # create
    cr = sub.add_parser("create", help="Launch a new Cloud Agent")
    cr.add_argument("--repo", required=True, help="GitHub repo (owner/repo format)")
    cr.add_argument("--prompt", required=True, help="Task description for the agent")
    cr.add_argument("--ref", default="", help="Branch/tag/commit ref (default: repo default branch)")
    cr.add_argument("--model", default="", help="Model name (e.g. claude-4-sonnet)")
    cr.add_argument("--auto-pr", action="store_true", dest="auto_pr", help="Auto-create PR when done")
    cr.add_argument("--branch", default="", help="Target branch name")
    cr.add_argument("--wait", action="store_true", help="Block until agent finishes, print summary")
    cr.add_argument("--no-direct", action="store_true", dest="no_direct", help="Do not append 'execute directly' instruction to prompt")
    cr.add_argument("--notify", default="", help="Feishu user/channel to notify when agent finishes")
    cr.add_argument("--skip-preflight", action="store_true", dest="skip_preflight", help="Skip pre-flight checks")

    # list
    ls = sub.add_parser("list", help="List Cloud Agents")
    ls.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    ls.add_argument("--pr-url", default="", dest="pr_url", help="Filter by PR URL")

    # get
    gt = sub.add_parser("get", help="Get agent details")
    gt.add_argument("--agent-id", required=True, dest="agent_id", help="Agent ID")

    # check
    ck = sub.add_parser("check", help="Poll agent until finished, print summary")
    ck.add_argument("--agent-id", required=True, dest="agent_id", help="Agent ID")
    ck.add_argument("--interval", type=int, default=15, help="Poll interval in seconds (default: 15)")
    ck.add_argument("--timeout", type=int, default=600, help="Max wait time in seconds (default: 600)")

    # conversation
    cv = sub.add_parser("conversation", help="Get agent conversation")
    cv.add_argument("--agent-id", required=True, dest="agent_id", help="Agent ID")

    # followup
    fu = sub.add_parser("followup", help="Send follow-up to agent")
    fu.add_argument("--agent-id", required=True, dest="agent_id", help="Agent ID")
    fu.add_argument("--message", required=True, help="Follow-up instruction")

    # stop
    sp = sub.add_parser("stop", help="Stop a running agent")
    sp.add_argument("--agent-id", required=True, dest="agent_id", help="Agent ID")

    # delete
    dl = sub.add_parser("delete", help="Delete an agent")
    dl.add_argument("--agent-id", required=True, dest="agent_id", help="Agent ID")

    # models
    sub.add_parser("models", help="List available models")

    # repos
    rp = sub.add_parser("repos", help="List accessible repositories")
    rp.add_argument("--search", default="", help="Search filter")

    # setup
    sub.add_parser("setup", help="API key setup instructions")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(1)

    dispatch = {
        "create": cmd_create,
        "list": cmd_list,
        "get": cmd_get,
        "check": cmd_check,
        "conversation": cmd_conversation,
        "followup": cmd_followup,
        "stop": cmd_stop,
        "delete": cmd_delete,
        "models": cmd_models,
        "repos": cmd_repos,
        "setup": cmd_setup,
    }
    dispatch[args.cmd](args)


if __name__ == "__main__":
    main()
