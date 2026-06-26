#!/usr/bin/env python3
"""
brain proc evolve — Error-driven procedure evolution
Inspired by Mengram's procedural memory concept.

Analyzes failure history for a procedure and rewrites steps to prevent
recurring failures. Uses LLM to synthesize patterns and propose fixes.

The cerebellum doesn't just remember — it adapts.
"""

import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime

BRAIN_DB = os.environ.get("BRAIN_DB", os.path.join(os.path.dirname(__file__), "brain.db"))
BRAIN_AGENT = os.environ.get("BRAIN_AGENT", "margot")

# --- LLM Configuration ---
# Config file (optional): tools/brain/brain.conf
# Environment variables override config file values.
#
# BRAIN_LLM_URL      — OpenAI-compatible chat completions endpoint
# BRAIN_LLM_KEY      — API key (Bearer token)
# BRAIN_LLM_MODEL    — Model name to use for evolution
#
# Supported providers (just point URL + key at any OpenAI-compatible API):
#   - OpenAI:     https://api.openai.com/v1/chat/completions + OPENAI_API_KEY
#   - Anthropic:  (via proxy) 
#   - Google:     https://generativelanguage.googleapis.com/v1beta/openai/chat/completions + BRAIN_LLM_KEY
#   - Ollama:     http://localhost:11434/v1/chat/completions (no key needed)
#   - LiteLLM:    http://localhost:4000/v1/chat/completions + proxy key

SCRIPT_DIR_EVOLVE = os.path.dirname(os.path.abspath(__file__))
CONF_FILE = os.path.join(SCRIPT_DIR_EVOLVE, "brain.conf")


def _load_config():
    """Load config from brain.conf (INI-style key=value), then overlay env vars."""
    conf = {
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "key": "",
        "model": "gemini-2.5-flash",
    }
    
    # Read config file if it exists
    if os.path.exists(CONF_FILE):
        with open(CONF_FILE) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip().lower()
                    v = v.strip().strip('"').strip("'")
                    if k in ("url", "llm_url"):
                        conf["url"] = v
                    elif k in ("key", "llm_key", "api_key"):
                        conf["key"] = v
                    elif k in ("model", "llm_model"):
                        conf["model"] = v

    # Environment overrides (highest priority)
    if os.environ.get("BRAIN_LLM_URL"):
        conf["url"] = os.environ["BRAIN_LLM_URL"]
    if os.environ.get("BRAIN_LLM_KEY"):
        conf["key"] = os.environ["BRAIN_LLM_KEY"]
    if os.environ.get("BRAIN_LLM_MODEL"):
        conf["model"] = os.environ["BRAIN_LLM_MODEL"]
    
    return conf


LLM_CONFIG = _load_config()
EVOLVE_URL = LLM_CONFIG["url"]
EVOLVE_KEY = LLM_CONFIG["key"]
EVOLVE_MODEL = LLM_CONFIG["model"]


def get_db():
    conn = sqlite3.connect(BRAIN_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def get_procedure(slug):
    """Get a procedure by slug, scoped to current agent + shared."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM procedures WHERE slug = ? AND agent IN (?, 'shared')",
        (slug, BRAIN_AGENT)
    ).fetchone()
    db.close()
    return dict(row) if row else None


def get_failure_history(procedure_id, limit=20):
    """Get recent failures for a procedure."""
    db = get_db()
    rows = db.execute(
        """SELECT * FROM procedure_history 
           WHERE procedure_id = ? AND event_type = 'failure'
           ORDER BY occurred_at DESC LIMIT ?""",
        (procedure_id, limit)
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_full_history(procedure_id, limit=50):
    """Get all history for a procedure."""
    db = get_db()
    rows = db.execute(
        """SELECT * FROM procedure_history 
           WHERE procedure_id = ?
           ORDER BY occurred_at DESC LIMIT ?""",
        (procedure_id, limit)
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def analyze_failures_local(proc, failures):
    """
    Analyze failure patterns without LLM — pattern matching.
    Returns analysis dict with patterns found.
    """
    steps = json.loads(proc["steps"]) if isinstance(proc["steps"], str) else proc["steps"]
    
    # Count failures per step
    step_failures = {}
    for f in failures:
        step_num = f.get("failed_step")
        if step_num is not None:
            step_failures[step_num] = step_failures.get(step_num, 0) + 1
    
    # Find repeat offenders (same step failing multiple times)
    repeat_offenders = {k: v for k, v in step_failures.items() if v >= 2}
    
    # Find sequential failures (consecutive steps failing = brittle chain)
    sorted_steps = sorted(step_failures.keys())
    brittle_chains = []
    for i in range(len(sorted_steps) - 1):
        if sorted_steps[i + 1] - sorted_steps[i] == 1:
            brittle_chains.append((sorted_steps[i], sorted_steps[i + 1]))
    
    # Extract error descriptions for keyword analysis
    error_keywords = {}
    for f in failures:
        desc = (f.get("description") or "").lower()
        for keyword in ["timeout", "permission", "connection", "not found", "refused",
                        "crash", "oom", "memory", "disk", "auth", "token", "missing",
                        "race condition", "already exists", "conflict"]:
            if keyword in desc:
                error_keywords[keyword] = error_keywords.get(keyword, 0) + 1

    return {
        "total_failures": len(failures),
        "step_failures": step_failures,
        "repeat_offenders": repeat_offenders,
        "brittle_chains": brittle_chains,
        "error_keywords": error_keywords,
        "steps": steps,
    }


def evolve_with_llm(proc, failures, analysis, dry_run=False):
    """
    Use LLM to synthesize failure patterns and propose evolved steps.
    Returns new steps JSON array.
    """
    steps = analysis["steps"]
    
    # Build a rich context for the LLM
    failure_descriptions = []
    for f in failures:
        entry = f"- Step {f.get('failed_step', '?')}: {f.get('description', 'no description')}"
        if f.get("fix_applied"):
            entry += f"\n  Fix applied: {f['fix_applied']}"
        entry += f" ({f.get('occurred_at', '?')})"
        failure_descriptions.append(entry)

    prompt = f"""You are a procedural memory evolution engine. Your job is to analyze a procedure's
failure history and produce an improved version of the steps that prevents recurring failures.

## Current Procedure: {proc['title']}
**Slug:** {proc['slug']}
**Version:** {proc['version']}
**Success rate:** {proc['success_count']}/{proc['success_count'] + proc['failure_count']}
**Description:** {proc.get('description') or 'None'}

## Current Steps (JSON array):
{json.dumps(steps, indent=2)}

## Failure History ({len(failures)} failures):
{chr(10).join(failure_descriptions)}

## Pattern Analysis:
- Repeat offender steps: {analysis['repeat_offenders'] or 'None'}
- Brittle chains (consecutive failures): {analysis['brittle_chains'] or 'None'}
- Common error types: {analysis['error_keywords'] or 'None'}

## Your Task:
1. Identify the root patterns causing failures
2. Rewrite the steps to prevent these failures
3. Add pre-flight checks where needed (e.g., "Verify X is running before Y")
4. Add error handling steps (e.g., "If X fails, try Y before giving up")
5. Remove or merge steps that are consistently problematic
6. Annotate evolved steps with [vN: reason] tags

## Rules:
- Output ONLY a JSON object with two keys:
  - "steps": the new steps array (array of strings)
  - "changelog": a one-line summary of what changed and why
- Keep steps actionable and specific
- Don't add unnecessary steps — lean procedures are better
- Preserve working steps unchanged
- Every fix must trace to an actual failure in the history
"""

    try:
        import urllib.request
        
        payload = json.dumps({
            "model": EVOLVE_MODEL,
            "messages": [
                {"role": "system", "content": "You are a procedure evolution engine. Output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000,
        })

        headers = {"Content-Type": "application/json"}
        if EVOLVE_KEY:
            headers["Authorization"] = f"Bearer {EVOLVE_KEY}"

        req = urllib.request.Request(
            EVOLVE_URL,
            data=payload.encode(),
            headers=headers,
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        
        content = result["choices"][0]["message"]["content"]
        
        # Strip markdown code fences if present
        content = content.strip()
        if content.startswith("```"):
            # Remove first line (```json or ```)
            content = content.split("\n", 1)[1] if "\n" in content else content[3:]
            # Remove trailing fence
            if "```" in content:
                content = content[:content.rfind("```")]
            content = content.strip()
        
        # Try to extract JSON object if there's surrounding text
        if not content.startswith("{"):
            start = content.find("{")
            if start >= 0:
                content = content[start:]
        if not content.endswith("}"):
            end = content.rfind("}")
            if end >= 0:
                content = content[:end + 1]
        
        # Try parsing as-is first, then try progressively more aggressive extraction
        evolved = None
        for attempt_content in [content]:
            try:
                evolved = json.loads(attempt_content)
                break
            except json.JSONDecodeError:
                pass
        
        # If that failed, try finding balanced braces
        if evolved is None:
            brace_start = content.find("{")
            if brace_start >= 0:
                depth = 0
                for i in range(brace_start, len(content)):
                    if content[i] == "{":
                        depth += 1
                    elif content[i] == "}":
                        depth -= 1
                        if depth == 0:
                            try:
                                evolved = json.loads(content[brace_start:i+1])
                                break
                            except json.JSONDecodeError:
                                continue
        
        if evolved is None:
            raise ValueError(f"Could not parse JSON from LLM response: {content[:200]}")
        
        # Validate expected keys
        if "steps" not in evolved:
            raise ValueError("LLM response missing 'steps' key")
        if not isinstance(evolved["steps"], list):
            raise ValueError("'steps' must be an array")
            
        return evolved

    except Exception as e:
        print(f"❌ LLM evolution failed: {e}", file=sys.stderr)
        print("⚠️ Falling back to LOCAL pattern-based evolution (not LLM)", file=sys.stderr)
        return evolve_local(proc, failures, analysis)


def evolve_local(proc, failures, analysis):
    """
    Fallback: evolve procedure using pattern matching without LLM.
    Less sophisticated but always available.
    """
    steps = list(analysis["steps"])  # copy
    changes = []
    
    # For each repeat offender step, add a pre-check before it
    for step_num, count in sorted(analysis["repeat_offenders"].items(), reverse=True):
        idx = step_num - 1  # 0-indexed
        if idx < len(steps):
            # Find the most common error for this step
            step_errors = [f for f in failures if f.get("failed_step") == step_num]
            if step_errors:
                latest_fix = step_errors[0].get("fix_applied", "")
                latest_error = step_errors[0].get("description", "unknown error")
                
                # Add the fix as a pre-check step
                if latest_fix:
                    pre_check = f"Pre-check: {latest_fix} [v{proc['version']+1}: added after {count}x failures — {latest_error}]"
                    steps.insert(idx, pre_check)
                    changes.append(f"Added pre-check before step {step_num}")

    # For common error keywords, add defensive steps
    if "timeout" in analysis["error_keywords"]:
        steps.append(f"Set timeout limits and retry once on timeout [v{proc['version']+1}: timeout pattern detected]")
        changes.append("Added timeout retry")
    
    if "permission" in analysis["error_keywords"] or "auth" in analysis["error_keywords"]:
        steps.insert(0, f"Verify credentials/permissions are valid before starting [v{proc['version']+1}: auth failure pattern]")
        changes.append("Added credential pre-check")

    changelog = "; ".join(changes) if changes else "No automatic fixes found — review manually"
    return {"steps": steps, "changelog": changelog}


def apply_evolution(slug, evolved_result):
    """Apply evolved steps to the procedure, bump version, record history."""
    db = get_db()
    
    proc = db.execute(
        "SELECT * FROM procedures WHERE slug = ? AND agent IN (?, 'shared')",
        (slug, BRAIN_AGENT)
    ).fetchone()
    
    if not proc:
        print(f"❌ Procedure '{slug}' not found")
        return False

    new_version = proc["version"] + 1
    new_steps = json.dumps(evolved_result["steps"])
    changelog = evolved_result.get("changelog", "Evolved from failure patterns")

    # Update procedure
    db.execute(
        """UPDATE procedures SET 
           steps = ?, version = ?, updated_at = datetime('now')
           WHERE id = ?""",
        (new_steps, new_version, proc["id"])
    )

    # Record evolution in history
    db.execute(
        """INSERT INTO procedure_history 
           (procedure_id, version, event_type, description, agent)
           VALUES (?, ?, 'evolved', ?, ?)""",
        (proc["id"], new_version, changelog, BRAIN_AGENT)
    )

    db.commit()
    db.close()

    return new_version


def cmd_evolve(slug, dry_run=False):
    """Main evolution command."""
    proc = get_procedure(slug)
    if not proc:
        print(f"❌ Procedure '{slug}' not found (agent: {BRAIN_AGENT})")
        sys.exit(1)

    failures = get_failure_history(proc["id"])
    if not failures:
        print(f"✅ No failures recorded for '{slug}' — nothing to evolve")
        print(f"   (Success rate: {proc['success_count']}/{proc['success_count'] + proc['failure_count']})")
        return

    print(f"🧠 Analyzing {len(failures)} failures for '{slug}' v{proc['version']}...")
    analysis = analyze_failures_local(proc, failures)

    if analysis["repeat_offenders"]:
        print(f"   🔴 Repeat offenders: {analysis['repeat_offenders']}")
    if analysis["brittle_chains"]:
        print(f"   ⛓️ Brittle chains: {analysis['brittle_chains']}")
    if analysis["error_keywords"]:
        print(f"   🏷️ Error patterns: {analysis['error_keywords']}")

    print(f"\n🔬 Evolving procedure with LLM ({EVOLVE_MODEL})...")
    evolved = evolve_with_llm(proc, failures, analysis, dry_run=dry_run)

    if dry_run:
        print("\n📋 PROPOSED EVOLUTION (dry run — not applied):")
        print(f"   Changelog: {evolved.get('changelog', 'N/A')}")
        print(f"\n   New steps:")
        for i, step in enumerate(evolved["steps"], 1):
            print(f"   {i}. {step}")
        return

    new_version = apply_evolution(slug, evolved)
    if new_version:
        print(f"\n✅ Evolved '{slug}' → v{new_version}")
        print(f"   Changelog: {evolved.get('changelog', 'N/A')}")
        print(f"   Steps: {len(evolved['steps'])}")
    else:
        print(f"❌ Evolution failed to apply")


def cmd_history(slug):
    """Show evolution history for a procedure."""
    proc = get_procedure(slug)
    if not proc:
        print(f"❌ Procedure '{slug}' not found")
        sys.exit(1)

    history = get_full_history(proc["id"])
    if not history:
        print(f"No history for '{slug}'")
        return

    print(f"=== PROCEDURE HISTORY: {proc['title']} (v{proc['version']}) ===")
    print(f"Success rate: {proc['success_count']}/{proc['success_count'] + proc['failure_count']}")
    print()

    for h in reversed(history):
        icon = {"success": "✅", "failure": "❌", "evolved": "🧬"}.get(h["event_type"], "•")
        line = f"{icon} v{h['version']} [{h['occurred_at']}] {h['event_type']}"
        if h.get("failed_step"):
            line += f" (step {h['failed_step']})"
        if h.get("description"):
            line += f" — {h['description']}"
        if h.get("fix_applied"):
            line += f"\n   Fix: {h['fix_applied']}"
        print(line)


def cmd_fail(slug, step_num, error_desc, fix_applied=None):
    """Record a failure for a procedure."""
    db = get_db()
    
    proc = db.execute(
        "SELECT * FROM procedures WHERE slug = ? AND agent IN (?, 'shared')",
        (slug, BRAIN_AGENT)
    ).fetchone()
    
    if not proc:
        print(f"❌ Procedure '{slug}' not found")
        db.close()
        sys.exit(1)

    # Update procedure stats
    db.execute(
        """UPDATE procedures SET 
           failure_count = failure_count + 1,
           last_run = datetime('now'),
           last_outcome = 'failure',
           updated_at = datetime('now')
           WHERE id = ?""",
        (proc["id"],)
    )

    # Record in history
    db.execute(
        """INSERT INTO procedure_history 
           (procedure_id, version, event_type, failed_step, description, fix_applied, agent)
           VALUES (?, ?, 'failure', ?, ?, ?, ?)""",
        (proc["id"], proc["version"], step_num, error_desc, fix_applied, BRAIN_AGENT)
    )

    db.commit()
    db.close()

    total = proc["failure_count"] + 1 + proc["success_count"]
    print(f"❌ Failure recorded for '{slug}' v{proc['version']} at step {step_num}")
    print(f"   Error: {error_desc}")
    if fix_applied:
        print(f"   Fix: {fix_applied}")
    print(f"   Record: {proc['success_count']}/{total}")

    # Auto-suggest evolution if failure count crosses threshold
    if (proc["failure_count"] + 1) >= 3 and (proc["failure_count"] + 1) % 2 == 1:
        print(f"\n💡 '{slug}' has {proc['failure_count'] + 1} failures — consider: brain proc evolve {slug}")


def cmd_success(slug):
    """Record a success for a procedure."""
    db = get_db()
    
    proc = db.execute(
        "SELECT * FROM procedures WHERE slug = ? AND agent IN (?, 'shared')",
        (slug, BRAIN_AGENT)
    ).fetchone()
    
    if not proc:
        print(f"❌ Procedure '{slug}' not found")
        db.close()
        sys.exit(1)

    db.execute(
        """UPDATE procedures SET 
           success_count = success_count + 1,
           last_run = datetime('now'),
           last_outcome = 'success',
           updated_at = datetime('now')
           WHERE id = ?""",
        (proc["id"],)
    )

    db.execute(
        """INSERT INTO procedure_history 
           (procedure_id, version, event_type, description, agent)
           VALUES (?, ?, 'success', 'Completed successfully', ?)""",
        (proc["id"], proc["version"], BRAIN_AGENT)
    )

    db.commit()
    
    new_total = proc["success_count"] + 1 + proc["failure_count"]
    new_success = proc["success_count"] + 1
    pct = round(new_success / new_total * 100) if new_total > 0 else 0
    db.close()
    
    print(f"✅ Success recorded for '{slug}' v{proc['version']}")
    print(f"   Record: {new_success}/{new_total} ({pct}%)")


def cmd_create(slug, title, steps_json, description=None, tags=None):
    """Create a new procedure."""
    db = get_db()
    
    existing = db.execute("SELECT id FROM procedures WHERE slug = ?", (slug,)).fetchone()
    if existing:
        print(f"❌ Procedure '{slug}' already exists")
        db.close()
        sys.exit(1)

    steps = json.loads(steps_json) if isinstance(steps_json, str) else steps_json
    
    db.execute(
        """INSERT INTO procedures (slug, title, description, tags, steps, agent)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (slug, title, description, tags, json.dumps(steps), BRAIN_AGENT)
    )
    db.commit()
    
    proc_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.close()
    
    print(f"✅ Created procedure '{slug}' (#{proc_id})")
    print(f"   Title: {title}")
    print(f"   Steps: {len(steps)}")


def cmd_list():
    """List all procedures visible to current agent."""
    db = get_db()
    rows = db.execute(
        """SELECT slug, title, version, success_count, failure_count, 
                  last_outcome, agent, tags
           FROM procedures 
           WHERE agent IN (?, 'shared')
           ORDER BY slug""",
        (BRAIN_AGENT,)
    ).fetchall()
    db.close()

    if not rows:
        print("No procedures found")
        return

    print(f"{'SLUG':<25} {'VER':>4} {'SUCCESS':>8} {'LAST':>8} {'AGENT':<10} TITLE")
    print(f"{'─'*25} {'─'*4} {'─'*8} {'─'*8} {'─'*10} {'─'*30}")
    for r in rows:
        total = r["success_count"] + r["failure_count"]
        rate = f"{r['success_count']}/{total}" if total > 0 else "N/A"
        last = (r["last_outcome"] or "—")[:8]
        print(f"{r['slug']:<25} v{r['version']:<3} {rate:>8} {last:>8} {r['agent']:<10} {r['title']}")


def cmd_show(slug):
    """Show a procedure's details."""
    proc = get_procedure(slug)
    if not proc:
        print(f"❌ Procedure '{slug}' not found")
        sys.exit(1)

    steps = json.loads(proc["steps"]) if isinstance(proc["steps"], str) else proc["steps"]
    total = proc["success_count"] + proc["failure_count"]
    pct = round(proc["success_count"] / total * 100) if total > 0 else 0

    print(f"# {proc['title']}")
    print(f"**Slug:** {proc['slug']} | **Version:** v{proc['version']} | **Agent:** {proc['agent']}")
    if proc.get("description"):
        print(f"**Description:** {proc['description']}")
    if proc.get("tags"):
        print(f"**Tags:** {proc['tags']}")
    print(f"**Success rate:** {proc['success_count']}/{total} ({pct}%)")
    print(f"**Last run:** {proc.get('last_run') or 'never'} ({proc.get('last_outcome') or 'N/A'})")
    print()
    print("## Steps")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")


# --- CLI dispatch ---

def main():
    if len(sys.argv) < 2:
        print("Usage: evolve.py <command> [args]")
        print("Commands: evolve, fail, success, create, list, show, history")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "evolve":
        if len(sys.argv) < 3:
            print("Usage: evolve.py evolve <slug> [--dry-run]")
            sys.exit(1)
        dry_run = "--dry-run" in sys.argv
        cmd_evolve(sys.argv[2], dry_run=dry_run)

    elif cmd == "fail":
        # evolve.py fail <slug> --step N --error "desc" [--fix "fix"]
        slug = sys.argv[2] if len(sys.argv) > 2 else None
        step_num = None
        error_desc = None
        fix_applied = None
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--step":
                step_num = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--error":
                error_desc = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--fix":
                fix_applied = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        if not all([slug, step_num, error_desc]):
            print('Usage: evolve.py fail <slug> --step N --error "what happened" [--fix "what fixed it"]')
            sys.exit(1)
        
        cmd_fail(slug, step_num, error_desc, fix_applied)

    elif cmd == "success":
        if len(sys.argv) < 3:
            print("Usage: evolve.py success <slug>")
            sys.exit(1)
        cmd_success(sys.argv[2])

    elif cmd == "create":
        # evolve.py create <slug> --title "T" --steps '["s1","s2"]' [--desc "D"] [--tags "t1,t2"]
        slug = sys.argv[2] if len(sys.argv) > 2 else None
        title = None
        steps_json = None
        description = None
        tags = None

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--title":
                title = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--steps":
                steps_json = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--desc":
                description = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags":
                tags = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        if not all([slug, title, steps_json]):
            print('Usage: evolve.py create <slug> --title "Title" --steps \'["step1","step2"]\'')
            sys.exit(1)
        
        cmd_create(slug, title, steps_json, description, tags)

    elif cmd == "list":
        cmd_list()

    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: evolve.py show <slug>")
            sys.exit(1)
        cmd_show(sys.argv[2])

    elif cmd == "history":
        if len(sys.argv) < 3:
            print("Usage: evolve.py history <slug>")
            sys.exit(1)
        cmd_history(sys.argv[2])

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
