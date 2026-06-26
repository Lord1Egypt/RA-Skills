#!/usr/bin/env python3
"""claw-config — grounded self-diagnosis and safe self-modification
of openclaw.json for any single OpenClaw agent.

All reads go through `openclaw config get|schema|file`. All writes go through
`openclaw config patch` (with `--dry-run` for `plan`). Official documentation is
fetched from docs.openclaw.ai as Mintlify `.md` raw and the full-content
corpus `llms-full.txt`. No LLM in the loop — output is grounded facts the
caller can read before composing a patch.

The skill refuses to guess the caller's identity: it requires `$OPENCLAW_AGENT_ID`
or an explicit `--agent <id>` flag, and verifies the id exists in
`agents.list[]` before proceeding. This makes wrong-agent writes impossible
by construction.

Subcommands:
  whoami     identity + telegram flags + bindings + crons + skills inventory
  schema     print JSON schema (or sub-tree at a JSON pointer / dot path)
  docs       fetch official documentation from docs.openclaw.ai (per-version cache)
  diagnose   12 structural self-checks; exits 3 if any check fails
  plan       dry-run a patch file (invokes `openclaw config patch --dry-run`)
  apply      backup → patch → restore-from-backup on failure
  report     whoami + diagnose as a single markdown block

Project home: https://github.com/<YOUR-GITHUB-HANDLE>/claw-config
License: MIT
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

OPENCLAW = "openclaw"
CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
DOCS_BASE = "https://docs.openclaw.ai"
DOCS_CACHE_ROOT = Path.home() / ".openclaw" / ".maintenance-cache" / "docs"
DOCS_CACHE_TTL_SEC = 24 * 3600  # default; override per-call via --max-age
CRON_JOBS_PATH = Path.home() / ".openclaw" / "cron" / "jobs.json"
SHARED_SKILLS_DIR = Path.home() / ".openclaw" / "skills"


# ───── shell wrappers (the only place we touch the openclaw CLI) ─────

def ocw(*args, stdin=None, check=True, timeout=60):
    """Run `openclaw <args>`. Return (stdout, stderr, rc)."""
    try:
        p = subprocess.run(
            [OPENCLAW, *args],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        sys.stderr.write("openclaw CLI not on PATH\n")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        sys.stderr.write(f"openclaw {' '.join(args)} timed out after {timeout}s\n")
        sys.exit(1)
    if check and p.returncode != 0:
        raise RuntimeError(f"openclaw {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout, p.stderr, p.returncode


def cfg_get(path):
    """`openclaw config get <path>` → parsed JSON or stripped string. None if missing."""
    out, err, rc = ocw("config", "get", path, check=False)
    if rc != 0:
        return None
    out = out.strip()
    if not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out


def cfg_schema(pointer=None):
    """Cached `openclaw config schema`. Walk via /a/b/c JSON pointer style."""
    if not hasattr(cfg_schema, "_cache"):
        out, _, _ = ocw("config", "schema")
        cfg_schema._cache = json.loads(out)
    schema = cfg_schema._cache
    if not pointer:
        return schema
    cur = schema
    for tok in [t for t in pointer.replace(".", "/").split("/") if t]:
        if isinstance(cur, dict) and "properties" in cur and tok in cur["properties"]:
            cur = cur["properties"][tok]
        elif isinstance(cur, dict) and tok in cur:
            cur = cur[tok]
        elif (
            isinstance(cur, dict)
            and "additionalProperties" in cur
            and isinstance(cur["additionalProperties"], dict)
        ):
            # for maps like channels.telegram.accounts.<arbitrary-key>
            cur = cur["additionalProperties"]
        else:
            raise KeyError(f"schema path not found: {pointer} (stopped at '{tok}')")
    return cur


# ───── self-identification (refuse to guess) ─────

def resolve_self(cli_arg):
    aid = os.environ.get("OPENCLAW_AGENT_ID") or cli_arg
    if not aid:
        sys.stderr.write(
            "cannot resolve self: set $OPENCLAW_AGENT_ID or pass --agent <id>. "
            "refusing to guess — wrong-agent patches are the #1 risk class.\n"
        )
        sys.exit(2)
    agents = cfg_get("agents.list") or []
    ids = [a.get("id") for a in agents]
    if aid not in ids:
        sys.stderr.write(
            f"cannot resolve self: '{aid}' not in agents.list[]. known ids: {ids}\n"
        )
        sys.exit(2)
    return aid


def my_record(aid):
    defaults = cfg_get("agents.defaults") or {}
    for a in cfg_get("agents.list") or []:
        if a.get("id") == aid:
            # shallow merge — explicit record fields override defaults
            return {**defaults, **a}
    raise RuntimeError(f"agent '{aid}' vanished from agents.list[]")


# ───── JSON5-ish lightweight parser (for cross-agent guard) ─────

_JSON5_LINE_COMMENT = re.compile(r"(^|[^:])//[^\n]*")
_JSON5_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_TRAILING_COMMA = re.compile(r",(\s*[}\]])")
_UNQUOTED_KEY = re.compile(r"([{,]\s*)([A-Za-z_$][A-Za-z0-9_$]*)\s*:")
_SINGLE_QUOTED = re.compile(r"'((?:[^'\\]|\\.)*)'")


def parse_json5_loose(text):
    """Parse a JSON5-ish patch file just well enough to inspect top-level structure.
    Not a full JSON5 parser — only handles what `openclaw config patch` already accepts
    in practice: // and /* */ comments, trailing commas, unquoted keys, single quotes."""
    s = _JSON5_BLOCK_COMMENT.sub("", text)
    s = _JSON5_LINE_COMMENT.sub(lambda m: m.group(1), s)
    s = _TRAILING_COMMA.sub(r"\1", s)
    s = _UNQUOTED_KEY.sub(r'\1"\2":', s)
    s = _SINGLE_QUOTED.sub(lambda m: json.dumps(m.group(1)), s)
    return json.loads(s)


def refuse_other_agent(self_id, patch_path, force_shared=False):
    """Walk top-level paths inside the patch. If they reference another agent's
    slice (channels.<chan>.accounts.<x>, agents.list[i].id != self), refuse."""
    text = Path(patch_path).read_text()
    try:
        patch = parse_json5_loose(text)
    except Exception as e:
        sys.stderr.write(
            f"could not parse patch as JSON5 for cross-agent check: {e}\n"
            f"hint: stick to JSON5 basics (// comments, trailing commas, unquoted keys).\n"
        )
        sys.exit(1)

    other_agents = []
    shared_paths = []

    def walk(node, path):
        # channels.<chan>.accounts.<x> → x must == self_id
        if (
            len(path) == 3
            and path[0] == "channels"
            and path[2] == "accounts"
            and isinstance(node, dict)
        ):
            for k in node:
                if k != self_id:
                    other_agents.append(f"channels.{path[1]}.accounts.{k}")
            return
        # agents.list[*].id check
        if path == ["agents", "list"] and isinstance(node, list):
            for i, entry in enumerate(node):
                if isinstance(entry, dict):
                    eid = entry.get("id")
                    if eid and eid != self_id:
                        other_agents.append(f"agents.list[{i}] (id={eid})")
            return
        # bindings — entries with agentId != self
        if path == ["bindings"] and isinstance(node, list):
            for i, b in enumerate(node):
                if isinstance(b, dict):
                    aid = b.get("agentId")
                    if aid and aid != self_id:
                        other_agents.append(f"bindings[{i}] (agentId={aid})")
                    elif not aid:
                        shared_paths.append(f"bindings[{i}] (no agentId)")
            return
        # generic shared top-level keys
        if len(path) == 1 and path[0] in {"agents", "gateway", "secrets", "auth", "session", "models", "meta", "wizard", "plugins", "acp", "tools", "hooks", "commands", "talk", "env", "messages", "skills", "browser", "canvasHost"}:
            if path[0] == "agents" and isinstance(node, dict):
                # allow agents.list (handled above) but flag agents.defaults etc.
                for k in node:
                    if k != "list":
                        shared_paths.append(f"agents.{k}")
                if "list" in node:
                    walk(node["list"], ["agents", "list"])
                return
            shared_paths.append(".".join(path))
            return
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + [k])

    if isinstance(patch, dict):
        for k, v in patch.items():
            walk(v, [k])

    if other_agents:
        sys.stderr.write(
            "patch refers to other agent(s):\n  - "
            + "\n  - ".join(other_agents)
            + f"\nself is '{self_id}'. refusing — wrong-agent writes are the #1 risk class.\n"
        )
        sys.exit(1)

    if shared_paths and not force_shared:
        sys.stderr.write(
            "patch touches shared / non-self config sections:\n  - "
            + "\n  - ".join(shared_paths)
            + "\nthese are not bound to a single agent. re-run with --force-shared if intentional.\n"
        )
        sys.exit(1)


# ───── data gatherers ─────

def my_crons(aid):
    """Crons from `~/.openclaw/cron/jobs.json` (read file directly — no gateway needed)."""
    if not CRON_JOBS_PATH.is_file():
        return []
    try:
        data = json.loads(CRON_JOBS_PATH.read_text())
    except Exception:
        return []
    jobs = data.get("jobs") if isinstance(data, dict) else data
    if not isinstance(jobs, list):
        return []
    out = []
    for j in jobs:
        if j.get("agentId") != aid:
            continue
        out.append({
            "id": j.get("id"),
            "name": j.get("name"),
            "expr": (j.get("schedule") or {}).get("expr"),
            "tz": (j.get("schedule") or {}).get("tz"),
            "enabled": j.get("enabled", True),
            "sessionTarget": j.get("sessionTarget"),
            "deliveryMode": (j.get("delivery") or {}).get("mode"),
        })
    return out


def my_skills(aid, workspace):
    """Walk workspace/skills and shared skills. We don't shell out to
    `openclaw skills list` because it requires the gateway and we want this
    to work even when the gateway is offline (diagnosing a broken setup)."""
    ws = Path(os.path.expanduser(workspace)) if workspace else None
    workspace_skills = []
    if ws and (ws / "skills").is_dir():
        for d in sorted((ws / "skills").iterdir()):
            if d.is_dir() and (d / "SKILL.md").is_file():
                workspace_skills.append(d.name)
    shared = []
    if SHARED_SKILLS_DIR.is_dir():
        for d in sorted(SHARED_SKILLS_DIR.iterdir()):
            if d.is_dir() and (d / "SKILL.md").is_file():
                shared.append(d.name)
    return {"workspace": workspace_skills, "shared": shared}


def my_bindings(aid):
    bindings = cfg_get("bindings") or []
    return [b for b in bindings if isinstance(b, dict) and b.get("agentId") == aid]


# ───── whoami ─────

def cmd_whoami(args):
    aid = resolve_self(args.agent)
    rec = my_record(aid)
    workspace = rec.get("workspace") or str(Path.home() / ".openclaw" / f"workspace-{aid}")
    agent_dir = rec.get("agentDir") or str(Path.home() / ".openclaw" / "agents" / aid / "agent")

    tg_raw = cfg_get(f"channels.telegram.accounts.{aid}")
    tg = None
    if isinstance(tg_raw, dict):
        cmd = tg_raw.get("commands") or {}
        bt = tg_raw.get("botToken")
        tg = {
            "enabled": tg_raw.get("enabled"),
            "commands_native": cmd.get("native"),
            "commands_nativeSkills": cmd.get("nativeSkills"),
            "dmPolicy": tg_raw.get("dmPolicy"),
            "groupPolicy": tg_raw.get("groupPolicy"),
            "botToken_present": bool(bt) if not isinstance(bt, dict) else "secretRef",
        }

    m = rec.get("model")
    model_primary = m if isinstance(m, str) else (m or {}).get("primary")
    info = {
        "agent": {
            "id": aid,
            "name": rec.get("name"),
            "workspace": workspace,
            "agentDir": agent_dir,
            "model_primary": model_primary,
            "identity_emoji": (rec.get("identity") or {}).get("emoji"),
            "memorySearch_provider": (rec.get("memorySearch") or {}).get("provider"),
        },
        "telegram": tg,
        "bindings": my_bindings(aid),
        "crons": my_crons(aid),
        "skills": my_skills(aid, workspace),
    }

    if args.json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return

    a = info["agent"]
    print(f"agent: {a['id']}  ({a.get('name') or '—'})  {a.get('identity_emoji') or ''}")
    print(f"  workspace:    {a['workspace']}")
    print(f"  agentDir:     {a['agentDir']}")
    print(f"  model:        {a.get('model_primary') or '(inherits defaults)'}")
    print(f"  memorySearch: {a.get('memorySearch_provider') or '(inherits defaults)'}")
    print()
    print("telegram:")
    if tg is None:
        print("  (no account at channels.telegram.accounts." + aid + ")")
    else:
        for k, v in tg.items():
            print(f"  {k}: {v}")
    print()
    print(f"bindings ({len(info['bindings'])}):")
    for b in info["bindings"]:
        m = b.get("match") or {}
        peer = m.get("peer") or {}
        print(f"  - channel={m.get('channel')} peer={peer.get('kind')}:{peer.get('id')}")
    print()
    print(f"crons ({len(info['crons'])}):")
    for c in info["crons"]:
        print(f"  - {c['id']}: {c['expr']} {c.get('tz') or ''}  enabled={c['enabled']}  ({c.get('name')})")
    print()
    sk = info["skills"]
    print(f"skills.workspace ({len(sk['workspace'])}): {', '.join(sk['workspace']) or '—'}")
    print(f"skills.shared ({len(sk['shared'])}):    {', '.join(sk['shared']) or '—'}")


# ───── schema ─────

def cmd_schema(args):
    try:
        node = cfg_schema(args.pointer)
    except KeyError as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)
    print(json.dumps(node, indent=2, ensure_ascii=False))


# ───── docs (official openclaw documentation) ─────
# docs.openclaw.ai is a Mintlify site. Mintlify exposes:
#   <path>.md       — raw markdown of any docs page
#   /llms.txt       — full sitemap with title + 1-line description per page
#   /llms-full.txt  — every page's content concatenated (search corpus)
# We use these directly. No HTML stripping needed.
#
# Versioning: docs.openclaw.ai always reflects the LATEST published version.
# The installed openclaw binary may lag (stable lane) or lead (dev lane). Two
# defenses:
#   1. cache key = installed openclaw version → upgrade auto-invalidates
#   2. callers are told (in stderr) how old the cached file is — they can
#      decide to --refresh
# When docs and schema disagree, trust schema (it comes from the installed
# binary). This is documented in SKILL.md.


def _installed_version():
    """e.g. '2026.5.6_c97b9f7'. Cached per-process. Used as cache shard key."""
    if not hasattr(_installed_version, "_v"):
        out, _, _ = ocw("--version", check=False)
        m = re.search(r"(\d+\.\d+\.\d+(?:[-.][\w.]+)?)\s*(?:\(([\w.]+)\))?", out)
        if m:
            _installed_version._v = f"{m.group(1)}_{m.group(2) or 'unknown'}"
        else:
            _installed_version._v = "unknown"
    return _installed_version._v


def _docs_cache_dir():
    """Per-version subdir; prune any other version dirs found at the root."""
    cur = _installed_version()
    root = DOCS_CACHE_ROOT
    root.mkdir(parents=True, exist_ok=True)
    cur_dir = root / cur
    cur_dir.mkdir(exist_ok=True)
    # cleanup: any sibling dir that isn't the current version is stale
    for sib in root.iterdir():
        if sib.is_dir() and sib.name != cur:
            try:
                shutil.rmtree(sib)
            except OSError:
                pass
    return cur_dir


def _human_age(sec):
    if sec < 60: return f"{int(sec)}s"
    if sec < 3600: return f"{int(sec / 60)}m"
    if sec < 86400: return f"{int(sec / 3600)}h"
    return f"{int(sec / 86400)}d"


def _fetch_docs(url, refresh=False, max_age_sec=DOCS_CACHE_TTL_SEC):
    """Return (markdown_body, cache_age_sec_or_None).
    cache_age_sec_or_None: int seconds if served from cache, None if just fetched.
    cron context never makes outbound HTTPS — falls back to (stale) cache or errors."""
    slug = url.replace(DOCS_BASE, "").strip("/") or "index"
    slug_safe = re.sub(r"[^A-Za-z0-9._/-]", "_", slug)
    cache_file = _docs_cache_dir() / slug_safe
    cache_file.parent.mkdir(parents=True, exist_ok=True)

    now = time.time()
    cache_age = (now - cache_file.stat().st_mtime) if cache_file.is_file() else None
    fresh = cache_age is not None and cache_age < max_age_sec

    if fresh and not refresh:
        return cache_file.read_text(), int(cache_age)

    # cron: never make outbound HTTP. Serve any cached copy (even stale) or fail.
    if os.environ.get("OPENCLAW_CRON_CONTEXT"):
        if cache_file.is_file():
            return (cache_file.read_text() +
                    f"\n\n[cache age {_human_age(cache_age)}; docs fetch disabled in cron]"), int(cache_age)
        raise RuntimeError(f"docs fetch disabled in cron and no cached copy at {cache_file}")

    try:
        p = subprocess.run(
            ["curl", "-fsSL", "--max-time", "10", url],
            capture_output=True, text=True, timeout=12,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        if cache_file.is_file():
            return (cache_file.read_text() +
                    f"\n\n[stale cache age {_human_age(cache_age)}; fetch failed: {e}]"), int(cache_age)
        raise RuntimeError(f"curl unavailable / timed out: {e}")

    if p.returncode != 0:
        if cache_file.is_file():
            return (cache_file.read_text() +
                    f"\n\n[stale cache age {_human_age(cache_age)}; HTTP rc={p.returncode}]"), int(cache_age)
        raise RuntimeError(f"fetch {url} failed (rc={p.returncode}): {p.stderr.strip() or 'see HTTP response'}")

    body = p.stdout
    cache_file.write_text(body)
    return body, None


def cmd_docs(args):
    refresh = getattr(args, "refresh", False)
    # argparse default is 24h; --max-age 0 means "always re-fetch" (equiv to --refresh)
    max_age_sec = int(getattr(args, "max_age", 24)) * 3600
    topic = (args.topic or "").strip()

    def _src_note(url, age):
        ver = _installed_version()
        if age is None:
            return f"(fetched {url} for openclaw {ver})"
        return f"(cached {_human_age(age)} ago from {url} for openclaw {ver}; --refresh to re-fetch)"

    # no arg → site index
    if not topic:
        url = f"{DOCS_BASE}/llms.txt"
        try:
            body, age = _fetch_docs(url, refresh=refresh, max_age_sec=max_age_sec)
        except RuntimeError as e:
            sys.stderr.write(str(e) + "\n"); sys.exit(1)
        print(body)
        sys.stderr.write(_src_note(url, age) + "\n")
        sys.stderr.write("\nhint: maintenance docs <slug>  (e.g. cli/config, channels/telegram, tools/skills)\n")
        sys.stderr.write("      maintenance docs search:<keyword>\n")
        sys.stderr.write("      maintenance docs announcements  ← read this after upgrading openclaw\n")
        return

    # search:<kw> → grep the full-content corpus (llms-full.txt), attribute matches by source page
    if topic.startswith("search:"):
        kw = topic[len("search:"):].strip()
        if not kw:
            sys.stderr.write("usage: maintenance docs search:<keyword>\n"); sys.exit(2)
        try:
            body, age = _fetch_docs(f"{DOCS_BASE}/llms-full.txt", refresh=refresh, max_age_sec=max_age_sec)
        except RuntimeError as e:
            sys.stderr.write(str(e) + "\n"); sys.exit(1)
        # walk lines, tracking current source page; record each matching line with attribution
        kw_lc = kw.lower()
        current_slug = "(unknown)"
        matches = []  # [(slug, line)]
        for ln in body.splitlines():
            stripped = ln.lstrip()
            if stripped.startswith("Source: "):
                src = stripped[len("Source: "):].strip()
                current_slug = src.replace(DOCS_BASE, "").lstrip("/") or "(root)"
                continue
            if kw_lc in ln.lower():
                matches.append((current_slug, ln.rstrip()))
        if not matches:
            print(f"no docs page mentions '{kw}'  (searched {len(body):,} chars of llms-full.txt)")
            sys.exit(0)
        # group by slug
        by_slug = {}
        for s, ln in matches:
            by_slug.setdefault(s, []).append(ln)
        for s in sorted(by_slug):
            print(f"=== {s} ===")
            for ln in by_slug[s][:6]:  # cap at 6 lines per page
                print(f"  {ln}")
            if len(by_slug[s]) > 6:
                print(f"  … +{len(by_slug[s]) - 6} more hit(s)")
            print()
        sys.stderr.write(f"{sum(len(v) for v in by_slug.values())} hit(s) across {len(by_slug)} page(s). "
                         f"`maintenance docs <slug>` to read a page in full.\n")
        sys.stderr.write(_src_note(f"{DOCS_BASE}/llms-full.txt", age) + "\n")
        return

    # full URL or slug
    if topic.startswith("http://") or topic.startswith("https://"):
        url = topic
    else:
        slug = topic.lstrip("/")
        if slug.endswith(".md"):
            slug = slug[:-3]
        url = f"{DOCS_BASE}/{slug}.md"

    try:
        body, age = _fetch_docs(url, refresh=refresh, max_age_sec=max_age_sec)
    except RuntimeError as e:
        sys.stderr.write(str(e) + "\n"); sys.exit(1)
    print(body)
    sys.stderr.write(_src_note(url, age) + "\n")


# ───── diagnose ─────

_CRON_EXPR_RE = re.compile(r"^\s*\S+(?:\s+\S+){4,5}\s*$")


def _check(status, pointer, detail):
    return {"status": status, "pointer": pointer, "detail": detail}


def run_checks(aid, rec):
    """Return list of {check, status, pointer, detail}."""
    results = []
    agents_list = cfg_get("agents.list") or []
    idx = next((i for i, a in enumerate(agents_list) if a.get("id") == aid), None)

    # pointers are dot/bracket notation — directly pasteable into
    # `openclaw config get <ptr>`. Docs at docs.openclaw.ai/cli/config confirm
    # dot+bracket is the canonical address form (JSON-pointer is not).
    tg_ptr_base = f"channels.telegram.accounts.{aid}"

    # 1. agent_record_present
    results.append({"check": "agent_record_present",
        **(_check("pass", f"agents.list[{idx}]", "found")
           if idx is not None else
           _check("fail", "agents.list", f"no entry with id='{aid}'"))})

    # 2. workspace_dir_exists
    ws = rec.get("workspace")
    ws_exists = bool(ws) and Path(os.path.expanduser(ws)).is_dir()
    results.append({"check": "workspace_dir_exists",
        **_check("pass" if ws_exists else "fail",
                f"agents.list[{idx}].workspace",
                f"path={ws}  exists={ws_exists}")})

    # 3. agent_dir_exists
    ad = rec.get("agentDir")
    ad_exists = bool(ad) and Path(os.path.expanduser(ad)).is_dir()
    results.append({"check": "agent_dir_exists",
        **_check("pass" if ad_exists else "warn",
                f"agents.list[{idx}].agentDir",
                f"path={ad}  exists={ad_exists}")})

    # 4. workspace_skills_readable
    ws_skills = Path(os.path.expanduser(ws or "")) / "skills" if ws else None
    skills_ok = ws_skills is not None and ws_skills.is_dir() and os.access(ws_skills, os.R_OK)
    results.append({"check": "workspace_skills_readable",
        **_check("pass" if skills_ok else "warn",
                f"(filesystem) {ws_skills}",
                f"readable={skills_ok}")})

    # telegram block
    tg = cfg_get(f"channels.telegram.accounts.{aid}")
    tg_present = isinstance(tg, dict)

    # 5. telegram_enabled
    if tg_present:
        en = tg.get("enabled")
        results.append({"check": "telegram_enabled",
            **_check("pass" if en is True else "warn",
                    f"{tg_ptr_base}.enabled",
                    f"value={en}")})
    else:
        results.append({"check": "telegram_enabled",
            **_check("warn",
                    tg_ptr_base,
                    "no telegram account configured for this agent")})

    # 6. telegram_native_skills — fail-severe so `diagnose` exits 3 on regression.
    # Motivation: a real production incident where commands.nativeSkills was
    # silently false on a Telegram account, which hid that agent's workspace
    # skills from chat dispatch. The agent could not self-diagnose because
    # `--help` did not describe the field and schema only said `boolean | "auto"`.
    # The actual routing semantics live in `tools/slash-commands` and are
    # reachable via `claw-config docs search:nativeSkills`.
    if tg_present:
        ns = (tg.get("commands") or {}).get("nativeSkills")
        results.append({"check": "telegram_native_skills",
            **_check("pass" if ns is True else "fail",
                    f"{tg_ptr_base}.commands.nativeSkills",
                    f"value={ns}  (false silently hides workspace skills from telegram dispatch; see `docs search:nativeSkills`)")})
    else:
        results.append({"check": "telegram_native_skills",
            **_check("warn",
                    f"{tg_ptr_base}.commands.nativeSkills",
                    "n/a (no telegram account)")})

    # 7. telegram_native
    if tg_present:
        n = (tg.get("commands") or {}).get("native")
        results.append({"check": "telegram_native",
            **_check("pass" if n is True else "warn",
                    f"{tg_ptr_base}.commands.native",
                    f"value={n}")})
    else:
        results.append({"check": "telegram_native",
            **_check("warn",
                    f"{tg_ptr_base}.commands.native",
                    "n/a (no telegram account)")})

    # 8. telegram_bot_token_present
    if tg_present:
        bt = tg.get("botToken")
        bt_ok = bool(bt) if not isinstance(bt, dict) else True  # SecretRef object counts
        results.append({"check": "telegram_bot_token_present",
            **_check("pass" if bt_ok else "fail",
                    f"{tg_ptr_base}.botToken",
                    f"present={bt_ok}  type={'SecretRef' if isinstance(bt, dict) else type(bt).__name__}")})
    else:
        results.append({"check": "telegram_bot_token_present",
            **_check("warn",
                    f"{tg_ptr_base}.botToken",
                    "n/a")})

    # 9. crons_valid_expr
    crons = my_crons(aid)
    bad_cron = []
    for c in crons:
        if not (c.get("expr") and _CRON_EXPR_RE.match(c["expr"])):
            bad_cron.append(c["id"])
    results.append({"check": "crons_valid_expr",
        **_check("pass" if not bad_cron else "warn",
                "cron:jobs/<id>/schedule/expr",  # cron lives in jobs.json, not openclaw.json
                f"total={len(crons)}  invalid={bad_cron or 'none'}")})

    # 10. crons_agent_match
    results.append({"check": "crons_agent_match",
        **_check("pass",
                "cron:jobs/*/agentId",
                f"{len(crons)} cron job(s) registered to '{aid}'")})

    # 11. bindings_valid_peer
    bindings = my_bindings(aid)
    bad_b = []
    for i, b in enumerate(bindings):
        peer = (b.get("match") or {}).get("peer") or {}
        if not (peer.get("kind") and peer.get("id") is not None):
            bad_b.append(i)
    results.append({"check": "bindings_valid_peer",
        **_check("pass" if not bad_b else "warn",
                "bindings[<idx>].match.peer",
                f"total={len(bindings)}  malformed={bad_b or 'none'}  (note: telegram bindings use match.{{channel,accountId}}, not peer)")})

    # 12. memorySearch_provider
    ms_prov = (rec.get("memorySearch") or {}).get("provider")
    results.append({"check": "memorySearch_provider",
        **_check("pass" if ms_prov else "warn",
                f"agents.list[{idx}].memorySearch.provider",
                f"value={ms_prov or '(inherits defaults)'}")})

    return results


def cmd_diagnose(args):
    aid = resolve_self(args.agent)
    rec = my_record(aid)
    results = run_checks(aid, rec)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        _render_diagnose(aid, results)

    any_fail = any(r["status"] == "fail" for r in results)
    sys.exit(3 if any_fail else 0)


def _render_diagnose(aid, results):
    icon = {"pass": "✓", "warn": "!", "fail": "✗"}
    print(f"diagnose: agent={aid}")
    print()
    for r in results:
        print(f"  [{icon[r['status']]}] {r['check']:<30s}  pointer: {r['pointer']}")
        if r["status"] != "pass":
            print(f"        ↳ {r['detail']}")
    print()
    counts = {s: sum(1 for r in results if r["status"] == s) for s in ("pass", "warn", "fail")}
    print(f"summary: {counts['pass']} pass / {counts['warn']} warn / {counts['fail']} fail")


# ───── plan (dry-run) ─────

def cmd_plan(args):
    aid = resolve_self(args.agent)
    patch_path = Path(args.patch).expanduser().resolve()
    if not patch_path.is_file():
        sys.stderr.write(f"patch file not found: {patch_path}\n")
        sys.exit(2)
    refuse_other_agent(aid, patch_path, force_shared=getattr(args, "force_shared", False))

    # snapshot top-level paths the patch touches
    text = patch_path.read_text()
    try:
        patch_obj = parse_json5_loose(text)
    except Exception:
        patch_obj = {}
    touched = _collect_dot_paths(patch_obj)

    print("─── patch ───")
    print(text.rstrip())
    print()
    print("─── current values at touched paths ───")
    for p in touched:
        cur = cfg_get(p)
        cur_s = json.dumps(cur, ensure_ascii=False) if cur is not None else "(absent)"
        print(f"  {p}: {cur_s}")
    print()

    out, err, rc = ocw(
        "config", "patch", "--file", str(patch_path), "--dry-run", "--json",
        check=False,
    )
    if rc != 0:
        sys.stderr.write(f"validate failed: {err.strip()}\n")
        if out.strip():
            sys.stderr.write(out)
        sys.exit(1)

    print("─── validate ───")
    print("PASS")
    if out.strip():
        # surface any structured info openclaw printed
        print()
        print(out.rstrip())


def _collect_dot_paths(obj, prefix=""):
    """Walk a patch object → list of leaf dot-paths (sorted, deduped)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            pk = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict) and v:
                out.extend(_collect_dot_paths(v, pk))
            else:
                out.append(pk)
    return sorted(set(out))


# ───── apply (live write) ─────

def cmd_apply(args):
    aid = resolve_self(args.agent)
    patch_path = Path(args.patch).expanduser().resolve()
    if not patch_path.is_file():
        sys.stderr.write(f"patch file not found: {patch_path}\n")
        sys.exit(2)
    refuse_other_agent(aid, patch_path, force_shared=getattr(args, "force_shared", False))

    ts = time.strftime("%Y%m%d-%H%M%S")
    op = patch_path.stem.replace(" ", "-")[:48]
    # name avoids `.bak.` substring so it's not caught by openclaw's internal
    # rotating-backup cleanup (which keeps openclaw.json.bak through .bak.4).
    backup_dir = CONFIG_PATH.parent / ".maintenance-backups"
    backup_dir.mkdir(exist_ok=True)
    backup = backup_dir / f"openclaw.{ts}.pre-{op}.json"
    shutil.copy2(CONFIG_PATH, backup)

    # `openclaw config patch` validates against the schema internally before
    # writing — rc=0 means schema-clean. Our backup + rollback is defense in
    # depth in case patch's own atomicity ever fails (e.g. interrupted write).
    _, err, rc = ocw("config", "patch", "--file", str(patch_path), check=False)
    if rc != 0:
        shutil.copy2(backup, CONFIG_PATH)
        sys.stderr.write(f"patch failed, backup restored from {backup}\n{err}\n")
        sys.exit(1)

    # show resulting values at touched paths
    try:
        patch_obj = parse_json5_loose(patch_path.read_text())
    except Exception:
        patch_obj = {}
    touched = _collect_dot_paths(patch_obj)
    print("apply: OK")
    print(f"backup: {backup}")
    print()
    print("─── values now ───")
    for p in touched:
        cur = cfg_get(p)
        cur_s = json.dumps(cur, ensure_ascii=False) if cur is not None else "(absent)"
        print(f"  {p}: {cur_s}")


# ───── report ─────

def cmd_report(args):
    aid = resolve_self(args.agent)
    rec = my_record(aid)
    print(f"# Maintenance report — agent `{aid}` @ {time.strftime('%Y-%m-%d %H:%M %Z')}")
    print()
    print("## whoami")
    print()
    print("```json")
    # re-invoke whoami in json mode without exiting
    class _W: pass
    w = _W(); w.agent = aid; w.json = True
    cmd_whoami(w)
    print("```")
    print()
    print("## diagnose")
    print()
    results = run_checks(aid, rec)
    icon = {"pass": "✓", "warn": "!", "fail": "✗"}
    for r in results:
        line = f"- [{icon[r['status']]}] **{r['check']}** — `{r['pointer']}`"
        if r["status"] != "pass":
            line += f" — {r['detail']}"
        print(line)
    print()
    counts = {s: sum(1 for r in results if r["status"] == s) for s in ("pass", "warn", "fail")}
    print(f"**summary:** {counts['pass']} pass / {counts['warn']} warn / {counts['fail']} fail")


# ───── main ─────

def main():
    # prog follows the invoking symlink name so aliases (e.g. ~/.local/bin/oclm)
    # show their own name in --help output instead of always saying "maintenance".
    p = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]) or "claw-config",
        description="Grounded self-diagnosis and safe self-modification of openclaw.json for a single agent.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    for n in ("whoami", "diagnose", "report"):
        sp = sub.add_parser(n)
        sp.add_argument("--agent", help="agent id (defaults to $OPENCLAW_AGENT_ID)")
        sp.add_argument("--json", action="store_true", help="output JSON")

    sp = sub.add_parser("schema", help="print JSON schema fragment at a pointer (e.g. channels/telegram/accounts)")
    sp.add_argument("pointer", nargs="?")

    sp = sub.add_parser("docs", help="fetch openclaw official docs page (markdown) from docs.openclaw.ai")
    sp.add_argument("topic", nargs="?",
                    help="path slug (e.g. cli/config, channels/telegram, tools/skills), full URL, or 'search:<keyword>'. Omit for site index (llms.txt).")
    sp.add_argument("--refresh", action="store_true", help="bypass cache (force re-fetch)")
    sp.add_argument("--max-age", type=int, default=24, metavar="HOURS",
                    help="max cache age in hours before re-fetching (default 24)")

    for n in ("plan", "apply"):
        sp = sub.add_parser(n)
        sp.add_argument("patch", help="path to JSON5 patch file")
        sp.add_argument("--agent")
        sp.add_argument("--force-shared", action="store_true",
                       help="permit touching agents.defaults / gateway / etc.")

    args = p.parse_args()

    # Cron gate: only `apply` is hard-disabled in cron (destructive write).
    # Read-only subcommands work fine in cron; `docs` has its own cache-only
    # fallback inside _fetch_docs() so it never hits the network from cron.
    if args.cmd == "apply" and os.environ.get("OPENCLAW_CRON_CONTEXT"):
        sys.stderr.write("maintenance apply is interactive; disabled in cron.\n")
        sys.exit(2)
    {
        "whoami": cmd_whoami,
        "schema": cmd_schema,
        "docs": cmd_docs,
        "diagnose": cmd_diagnose,
        "plan": cmd_plan,
        "apply": cmd_apply,
        "report": cmd_report,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
