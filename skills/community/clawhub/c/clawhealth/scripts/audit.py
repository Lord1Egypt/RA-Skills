#!/usr/bin/env python3
"""
openclaw-doctor: Comprehensive OpenClaw installation audit.

Four modules:
  --security  Secrets exposure, token hygiene, SecretRef usage
  --cron      Cron operational health (errors, staleness, conflicts)
  --config    Config optimization (heartbeat, models, maintenance)
  --skills    Skill structural quality + heuristic scoring

No flags = run all four.

Outputs JSON. Zero external dependencies (stdlib only).
"""

import argparse
import json
import os
import re
import shutil
import stat
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def find_openclaw_dir():
    env_dir = os.environ.get("OPENCLAW_DIR") or os.environ.get("OPENCLAW_STATE_DIR")
    if env_dir:
        p = Path(env_dir)
        return p if p.is_dir() else None
    for d in [Path.home() / ".openclaw", Path.home() / "openclaw",
              Path.home() / ".config" / "openclaw"]:
        if d.is_dir():
            return d
    return None


def load_json(path):
    try:
        return json.loads(Path(path).read_text()), None
    except (json.JSONDecodeError, OSError) as e:
        return None, str(e)


def is_secret_ref(value):
    """A SecretRef is a dict with 'source' key (exec, env, etc.)."""
    return isinstance(value, dict) and "source" in value


def finding(severity, category, message, fix=None):
    f = {"severity": severity, "category": category, "message": message}
    if fix:
        f["fix"] = fix
    return f


def deep_get(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


# ---------------------------------------------------------------------------
# Module 1: Security Audit
# ---------------------------------------------------------------------------

def audit_security(oc_dir, config):
    findings = []
    score = 100

    # 1. Inline secrets in env.vars
    env_vars = deep_get(config, "env", "vars", default={})
    secret_keys = []
    for key, val in env_vars.items():
        if isinstance(val, str) and len(val) > 10:
            kl = key.lower()
            if any(t in kl for t in ("key", "token", "secret", "password", "private")):
                secret_keys.append(key)
    if secret_keys:
        score -= 15
        findings.append(finding(
            "critical", "security",
            f"Inline secrets in env.vars: {', '.join(secret_keys[:8])}{'...' if len(secret_keys) > 8 else ''}",
            "Move to 1Password SecretRefs or environment variables"
        ))

    # 2. Plaintext bot tokens in channels
    channels = config.get("channels", {})
    for ch_name, ch_conf in channels.items():
        if not isinstance(ch_conf, dict):
            continue
        token = ch_conf.get("botToken")
        if isinstance(token, str) and len(token) > 20:
            score -= 10
            findings.append(finding(
                "warning", "security",
                f"Plaintext bot token in channels.{ch_name}.botToken",
                'Use SecretRef: {"source": "exec", "provider": "op-telegram", "id": "value"}'
            ))

    # 3. Plaintext gateway password
    gw_auth = deep_get(config, "gateway", "auth", "password", default=None)
    if isinstance(gw_auth, str) and len(gw_auth) > 5:
        score -= 10
        findings.append(finding(
            "warning", "security",
            "Plaintext password in gateway.auth.password",
            "Use SecretRef for gateway auth password"
        ))

    # 4. Skills with inline apiKey strings
    entries = deep_get(config, "skills", "entries", default={})
    inline_skill_keys = [name for name, conf in entries.items()
                         if isinstance(conf, dict) and isinstance(conf.get("apiKey"), str)]
    if inline_skill_keys:
        score -= 5
        findings.append(finding(
            "info", "security",
            f"Inline apiKey strings in skills.entries: {', '.join(inline_skill_keys[:5])}",
            "Use SecretRef objects instead of plaintext strings"
        ))

    # 5. .env files without .gitignore
    env_files = list(oc_dir.rglob(".env"))
    if env_files:
        gitignore = oc_dir / ".gitignore"
        protected = False
        if gitignore.is_file():
            try:
                protected = ".env" in gitignore.read_text()
            except OSError:
                pass
        if not protected:
            score -= 5
            findings.append(finding(
                "warning", "security",
                f"{len(env_files)} .env file(s) found without .gitignore protection",
                "Add '.env' to .gitignore"
            ))

    # 6. Secrets in workspace files (markdown, scripts, JSON, YAML)
    secret_patterns = [
        (r'sk-[A-Za-z0-9]{20,}', "OpenAI-style API key (sk-...)"),
        (r'sk-proj-[A-Za-z0-9_-]{20,}', "OpenAI project key"),
        (r'ghp_[A-Za-z0-9]{36,}', "GitHub personal token (ghp_)"),
        (r'ghs_[A-Za-z0-9]{36,}', "GitHub server token (ghs_)"),
        (r'xoxb-[0-9]+-[A-Za-z0-9]+', "Slack bot token (xoxb-)"),
        (r'AIzaSy[A-Za-z0-9_-]{33}', "Google API key"),
        (r'pplx-[A-Za-z0-9]{40,}', "Perplexity API key"),
        (r'pcp_[a-f0-9]{40,}', "Paperclip API key"),
        (r'fc-[a-f0-9]{30,}', "Firecrawl API key"),
        (r'ops_ey[A-Za-z0-9+/=]{50,}', "1Password service account token"),
        (r'(?i)(?:private.?key|secret|signing)["\s:=]+0x[a-f0-9]{64}', "Private key (hex)"),
        (r'(?i)Bearer\s+[A-Za-z0-9._~+/=-]{20,}', "Bearer token"),
    ]
    workspace_dir = oc_dir / "workspace"
    skip_dirs = {".git", "node_modules", "venv", "__pycache__", "archive", "browser"}
    scan_exts = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt", ".env", ".toml"}
    workspace_secrets = []  # (file, pattern_label)

    if workspace_dir.is_dir():
        files_scanned = 0
        for root, dirs, files in os.walk(str(workspace_dir)):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for fname in files:
                fp = Path(root) / fname
                if fp.suffix not in scan_exts:
                    continue
                if files_scanned >= 500:
                    break
                files_scanned += 1
                try:
                    content = fp.read_text(errors="replace")[:16384]
                except OSError:
                    continue
                for pattern, label in secret_patterns:
                    if re.search(pattern, content):
                        rel = str(fp.relative_to(oc_dir))
                        workspace_secrets.append((rel, label))
                        break  # one finding per file

    if workspace_secrets:
        score -= min(15, 3 * len(workspace_secrets))
        # Dedupe by label for cleaner output
        by_label = defaultdict(list)
        for path, label in workspace_secrets:
            by_label[label].append(path)
        for label, paths in list(by_label.items())[:5]:
            findings.append(finding(
                "critical", "security",
                f"{label} in workspace: {', '.join(paths[:3])}{'...' if len(paths) > 3 else ''}",
                "Remove secrets from workspace files. Use SecretRefs or environment variables."
            ))

    if not findings:
        findings.append(finding("ok", "security", "No security issues found"))

    return max(0, score), findings


# ---------------------------------------------------------------------------
# Module 2: Cron Operations Audit
# ---------------------------------------------------------------------------

def audit_cron(oc_dir, config):
    findings = []
    score = 100

    jobs_file = oc_dir / "cron" / "jobs.json"
    if not jobs_file.is_file():
        findings.append(finding("info", "cron", "No cron/jobs.json found"))
        return score, findings

    data, err = load_json(jobs_file)
    if err:
        findings.append(finding("warning", "cron", f"Cannot parse cron/jobs.json: {err}"))
        return 80, findings

    jobs = data.get("jobs", []) if isinstance(data, dict) else []
    if not jobs:
        findings.append(finding("info", "cron", "No cron jobs defined"))
        return score, findings

    enabled = [j for j in jobs if j.get("enabled", True)]
    disabled = [j for j in jobs if not j.get("enabled", True)]
    findings.append(finding("ok", "cron",
                            f"{len(jobs)} jobs ({len(enabled)} enabled, {len(disabled)} disabled)"))

    now_ms = int(datetime.now().timestamp() * 1000)

    # Per-job checks
    error_jobs = []
    stale_jobs = []
    no_tz = []
    no_timeout = []
    no_isolated = []

    for job in enabled:
        name = job.get("name", "unnamed")
        state = job.get("state", {})
        sched = job.get("schedule", {})
        payload = job.get("payload", {})
        expr = sched.get("expr", "") if isinstance(sched, dict) else ""

        # Error state
        if state.get("lastStatus") == "error":
            error_jobs.append(name)

        # Consecutive errors
        consec = state.get("consecutiveErrors", 0)
        if isinstance(consec, int) and consec > 3:
            findings.append(finding("warning", "cron",
                                    f"'{name}' has {consec} consecutive errors"))
            score -= 5

        # Staleness
        last_run = state.get("lastRunAtMs", 0)
        if last_run > 0:
            age_h = (now_ms - last_run) / (1000 * 3600)
            # Weekly jobs get longer threshold
            is_weekly = bool(re.search(r'\b[0-6](,[0-6])*\b', expr.split()[-1])) if len(expr.split()) >= 5 else False
            threshold = 240 if is_weekly else 48
            if age_h > threshold:
                stale_jobs.append((name, int(age_h)))

        # Missing timezone
        if isinstance(sched, dict) and not sched.get("tz"):
            no_tz.append(name)

        # Missing timeout
        if isinstance(payload, dict) and not payload.get("timeoutSeconds"):
            no_timeout.append(name)

        # Missing sessionTarget
        if not job.get("sessionTarget"):
            no_isolated.append(name)

    if error_jobs:
        score -= 10
        findings.append(finding("warning", "cron",
                                f"Jobs in error state: {', '.join(error_jobs)}",
                                "Check job logs, trigger manual run, or review the job prompt for issues"))

    if stale_jobs:
        score -= 5
        for name, hours in stale_jobs[:5]:
            findings.append(finding("warning", "cron",
                                    f"'{name}' hasn't run in {hours}h"))

    # Schedule conflicts
    sched_groups = defaultdict(list)
    for job in enabled:
        sched = job.get("schedule", {})
        expr = sched.get("expr", "") if isinstance(sched, dict) else ""
        if expr:
            sched_groups[expr].append(job.get("name", "unnamed"))
    for expr, names in sched_groups.items():
        if len(names) > 1:
            score -= 2
            findings.append(finding("info", "cron",
                                    f"Schedule conflict '{expr}': {', '.join(names)}",
                                    "Stagger by 5-10 minutes"))

    if no_tz:
        score -= 3
        findings.append(finding("info", "cron",
                                f"{len(no_tz)} jobs without timezone (DST drift risk): "
                                f"{', '.join(no_tz[:5])}{'...' if len(no_tz) > 5 else ''}",
                                'Add "tz": "Your/Timezone" to schedule'))

    if len(no_timeout) > len(enabled) // 2:
        findings.append(finding("info", "cron",
                                f"{len(no_timeout)}/{len(enabled)} jobs without timeout",
                                "Add payload.timeoutSeconds to prevent runaway jobs"))

    # Concurrent pressure
    max_concurrent = deep_get(config, "cron", "maxConcurrentRuns", default=2)
    frequent = [j for j in enabled
                if "*/" in (j.get("schedule", {}).get("expr", "") if isinstance(j.get("schedule"), dict) else "")]
    if len(frequent) > max_concurrent:
        findings.append(finding("info", "cron",
                                f"{len(frequent)} frequent jobs but maxConcurrentRuns={max_concurrent}",
                                "Increase cron.maxConcurrentRuns or stagger jobs"))

    return max(0, score), findings


# ---------------------------------------------------------------------------
# Module 3: Config Optimization
# ---------------------------------------------------------------------------

def audit_config(config):
    findings = []
    score = 100

    defaults = deep_get(config, "agents", "defaults", default={})

    # Heartbeat
    if not defaults.get("heartbeat"):
        score -= 10
        findings.append(finding("warning", "config",
                                "No heartbeat at agents.defaults.heartbeat",
                                'Add heartbeat with "every", "model", and "prompt" fields'))

    # Model fallbacks
    fallbacks = deep_get(defaults, "model", "fallbacks", default=[])
    if not fallbacks:
        score -= 3
        findings.append(finding("info", "config",
                                "No model fallbacks at agents.defaults.model.fallbacks",
                                "Add fallback models for provider outage resilience"))

    # Subagent model
    sub_model = deep_get(defaults, "subagents", "model", default=None)
    primary = deep_get(defaults, "model", "primary", default="")
    if not sub_model and primary and "opus" in str(primary).lower():
        score -= 3
        findings.append(finding("info", "config",
                                "No subagent model set; subagents use expensive primary (opus)",
                                'Set agents.defaults.subagents.model to "sonnet" to save costs'))

    # Session maintenance
    if not deep_get(config, "session", "maintenance", default=None):
        score -= 3
        findings.append(finding("info", "config",
                                "No session maintenance configured",
                                "Add session.maintenance with pruneAfter, maxEntries, rotateBytes"))

    # Compaction
    if not defaults.get("compaction"):
        score -= 3
        findings.append(finding("info", "config",
                                "No compaction config at agents.defaults.compaction",
                                "Configure compaction for context window management"))

    # Context pruning
    if not defaults.get("contextPruning"):
        score -= 2
        findings.append(finding("info", "config",
                                "No context pruning at agents.defaults.contextPruning",
                                "Configure pruning to manage large tool results"))

    # Memory search
    mem = defaults.get("memorySearch", {})
    if isinstance(mem, dict) and not mem.get("enabled", False):
        findings.append(finding("info", "config",
                                "Memory search is disabled",
                                "Enable agents.defaults.memorySearch for cross-session recall"))

    # Cron enabled vs jobs exist
    cron_enabled = deep_get(config, "cron", "enabled", default=True)
    if not cron_enabled:
        findings.append(finding("warning", "config",
                                "Cron is disabled in config",
                                "Set cron.enabled: true if you have scheduled jobs"))

    if not findings:
        findings.append(finding("ok", "config", "Config looks well-optimized"))

    return max(0, score), findings


# ---------------------------------------------------------------------------
# Module 4: Skill Quality Scorer
# ---------------------------------------------------------------------------

def parse_frontmatter(content):
    """Extract YAML frontmatter from SKILL.md."""
    fm = {}
    if not content.startswith("---"):
        return fm
    end = content.find("---", 3)
    if end < 0:
        return fm
    block = content[3:end].strip()
    for line in block.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val
    return fm


def score_structure(content, fm, skill_dir):
    """Deterministic structural quality (1-5)."""
    score = 1
    issues = []

    # Required: name + description in frontmatter
    has_name = bool(fm.get("name"))
    has_desc = bool(fm.get("description"))

    if has_name and has_desc:
        score = 3
    elif has_name or has_desc:
        score = 2
        if not has_name:
            issues.append("Missing 'name' in frontmatter")
        if not has_desc:
            issues.append("Missing 'description' in frontmatter")
    else:
        issues.append("Missing frontmatter (name + description required)")
        return score, issues

    # Description length
    desc = fm.get("description", "")
    if len(desc) < 30:
        issues.append(f"Description too short ({len(desc)} chars, aim for 50-200)")
    elif len(desc) > 250:
        issues.append(f"Description too long ({len(desc)} chars, may get truncated)")

    # Metadata.openclaw
    metadata_str = fm.get("metadata", "")
    has_metadata = False
    if metadata_str:
        try:
            meta = json.loads(metadata_str)
            has_metadata = "openclaw" in meta
            # Verify declared bins exist
            bins = deep_get(meta, "openclaw", "requires", "bins", default=[])
            for b in bins:
                if not shutil.which(b):
                    score = max(1, score - 1)
                    issues.append(f"Required binary '{b}' not found on PATH")
        except (json.JSONDecodeError, TypeError):
            pass

    if has_metadata:
        score = min(5, score + 1)

    # Section headers
    sections = len(re.findall(r"^#{2,4}\s+", content, re.MULTILINE))
    if sections >= 3:
        score = min(5, score + 1)
    elif sections < 2:
        issues.append("Fewer than 2 section headers; add structure")

    # Scripts executability
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for sf in scripts_dir.iterdir():
            if sf.is_file() and not sf.name.startswith("."):
                if not os.access(sf, os.X_OK):
                    issues.append(f"Script not executable: scripts/{sf.name}")

    return min(5, max(1, score)), issues


def score_completeness(content):
    """Heuristic content completeness (1-5)."""
    score = 1
    issues = []

    checks = {
        "examples": bool(re.search(r"(?i)(example|e\.g\.|for instance|usage|```)", content)),
        "commands": bool(re.search(r"(?i)(command|action|run |execute|invoke|```bash|```sh)", content)),
        "output": bool(re.search(r"(?i)(output|result|returns|response|format|```json)", content)),
        "setup": bool(re.search(r"(?i)(setup|install|prerequisite|require|depend|config)", content)),
        "errors": bool(re.search(r"(?i)(error|fail|fallback|missing|invalid|not found|recover)", content)),
        "scope": bool(re.search(r"(?i)(when to use|scope|purpose|this skill|does not|won't|boundary)", content)),
    }

    passed = sum(checks.values())
    score = min(5, 1 + passed)

    if not checks["examples"]:
        issues.append("Add examples or code blocks")
    if not checks["errors"]:
        issues.append("Add error handling guidance")
    if not checks["scope"]:
        issues.append("Define when to use this skill (scope/boundaries)")

    return score, issues


def score_clarity(content):
    """Heuristic clarity scoring (1-5)."""
    score = 2
    issues = []

    # Imperative language
    imperative = len(re.findall(
        r"(?im)^(do|run|check|use|add|create|set|ensure|verify|scan|read|write|"
        r"output|return|call|execute|send|log|update|remove|delete|skip|avoid|never|always)\b",
        content))

    # Hedging
    hedging = len(re.findall(
        r"(?i)(you might want to|you could|perhaps|maybe|consider|it.s possible)", content))

    # Structure
    has_lists = bool(re.search(r"^[\s]*[-*]\s", content, re.MULTILINE))
    has_numbered = bool(re.search(r"^[\s]*\d+\.\s", content, re.MULTILINE))
    sections = len(re.findall(r"^#{2,4}\s+", content, re.MULTILINE))

    if sections >= 3:
        score = 3
    if imperative >= 5:
        score = min(5, score + 1)
    if (has_lists or has_numbered) and hedging < 2:
        score = min(5, score + 1)
    if hedging >= 3:
        score = max(1, score - 1)
        issues.append(f"Reduce hedging language ({hedging} instances)")
    if imperative < 3:
        issues.append("Use more imperative verbs (Do X, Run Y, Check Z)")

    return min(5, max(1, score)), issues


def score_efficiency(content):
    """Heuristic efficiency scoring (1-5)."""
    score = 3
    issues = []
    words = len(content.split())

    # Token footprint
    if words > 5000:
        score = max(1, score - 1)
        issues.append(f"SKILL.md is {words} words; consider trimming")
    elif words < 800:
        score = min(5, score + 1)

    # Efficiency patterns
    eff_terms = ["cache", "lazy", "conditional", "skip if", "only when",
                 "batch", "minimize", "efficient", "structured output", "json"]
    eff_count = sum(1 for t in eff_terms if t in content.lower())
    if eff_count >= 2:
        score = min(5, score + 1)

    # Cross-skill references
    if re.search(r"(?i)(related skill|chain|pipe|combine with|see also|/\w+)", content):
        score = min(5, score + 1)

    return min(5, max(1, score)), issues


def audit_skills(oc_dir):
    findings = []
    score = 100

    # All skill locations
    locations = [
        ("workspace", oc_dir / "workspace" / "skills"),
        ("managed", oc_dir / "skills"),
        ("personal", Path.home() / ".agents" / "skills"),
    ]

    # Also scan bundled skills if accessible
    bundled_dir = Path("/usr/local/Cellar/node") / os.listdir("/usr/local/Cellar/node")[0] / "lib/node_modules/openclaw/skills" if Path("/usr/local/Cellar/node").is_dir() else None
    if bundled_dir and bundled_dir.is_dir():
        locations.append(("bundled", bundled_dir))

    all_skills = {}
    for source, sdir in locations:
        if not sdir.is_dir():
            continue
        for d in sdir.iterdir():
            if d.is_dir() and not d.name.startswith("_") and d.name not in all_skills:
                all_skills[d.name] = (d, source)

    if not all_skills:
        findings.append(finding("info", "skills", "No skills found"))
        return score, findings, []

    skill_results = []
    total_score = 0
    scored_count = 0

    for name, (skill_dir, source) in sorted(all_skills.items()):
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.is_file():
            skill_results.append({
                "name": name, "source": source, "status": "broken",
                "scores": {}, "overall": 0,
                "top_issues": ["Missing SKILL.md"]
            })
            continue

        try:
            content = skill_md.read_text(errors="replace")
        except OSError:
            skill_results.append({
                "name": name, "source": source, "status": "error",
                "scores": {}, "overall": 0,
                "top_issues": ["Cannot read SKILL.md"]
            })
            continue

        if not content.strip():
            skill_results.append({
                "name": name, "source": source, "status": "empty",
                "scores": {}, "overall": 0,
                "top_issues": ["SKILL.md is empty"]
            })
            continue

        fm = parse_frontmatter(content)
        s_struct, i_struct = score_structure(content, fm, skill_dir)
        s_comp, i_comp = score_completeness(content)
        s_clar, i_clar = score_clarity(content)
        s_eff, i_eff = score_efficiency(content)

        # Weighted: structure 2x, completeness 1.5x, clarity 1x, efficiency 1x
        overall_raw = (s_struct * 2 + s_comp * 1.5 + s_clar + s_eff) / 5.5
        overall = round(overall_raw * 20)

        all_issues = i_struct + i_comp + i_clar + i_eff
        skill_results.append({
            "name": name,
            "source": source,
            "status": "scored",
            "scores": {
                "structure": s_struct,
                "completeness": s_comp,
                "clarity": s_clar,
                "efficiency": s_eff,
            },
            "overall": overall,
            "top_issues": all_issues[:5],
        })
        total_score += overall
        scored_count += 1

    broken = sum(1 for s in skill_results if s["status"] in ("broken", "empty"))
    avg = round(total_score / scored_count) if scored_count else 0

    # Convert average skill score to section score
    section_score = min(100, avg + 10) if avg > 0 else 50
    if broken > 5:
        section_score -= 10

    findings.append(finding("ok", "skills",
                            f"{scored_count} skills scored, {broken} broken, avg={avg}/100"))

    if broken > 0:
        broken_names = [s["name"] for s in skill_results if s["status"] in ("broken", "empty")]
        findings.append(finding("warning", "skills",
                                f"Broken skills (missing/empty SKILL.md): {', '.join(broken_names[:10])}",
                                "Add a SKILL.md with frontmatter (name + description) or remove the skill directory"))

    low_skills = [s for s in skill_results if s["status"] == "scored" and s["overall"] < 50]
    if low_skills:
        names = ", ".join(s["name"] for s in low_skills[:5])
        findings.append(finding("info", "skills",
                                f"{len(low_skills)} skills scored below 50: {names}{'...' if len(low_skills) > 5 else ''}"))

    return max(0, section_score), findings, skill_results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Doctor: security, cron, config, and skill quality audits")
    parser.add_argument("--security", action="store_true", help="Security audit only")
    parser.add_argument("--cron", action="store_true", help="Cron operations audit only")
    parser.add_argument("--config", action="store_true", help="Config optimization audit only")
    parser.add_argument("--skills", action="store_true", help="Skill quality scoring only")
    parser.add_argument("--all", action="store_true", help="Run all audits (default)")
    args = parser.parse_args()

    run_all = not (args.security or args.cron or args.config or args.skills) or args.all

    oc_dir = find_openclaw_dir()
    if not oc_dir:
        print(json.dumps({
            "score": 0, "status": "error",
            "message": "OpenClaw installation not found. Set OPENCLAW_DIR to override.",
        }, indent=2))
        sys.exit(1)

    config, err = load_json(oc_dir / "openclaw.json")
    if err:
        print(json.dumps({
            "score": 0, "status": "error",
            "message": f"Cannot load openclaw.json: {err}",
        }, indent=2))
        sys.exit(1)

    sections = {}
    all_findings = []
    skill_details = []

    if run_all or args.security:
        s, f = audit_security(oc_dir, config)
        sections["security"] = {"score": s, "findings": f}
        all_findings.extend(f)

    if run_all or args.cron:
        s, f = audit_cron(oc_dir, config)
        sections["cron"] = {"score": s, "findings": f}
        all_findings.extend(f)

    if run_all or args.config:
        s, f = audit_config(config)
        sections["config"] = {"score": s, "findings": f}
        all_findings.extend(f)

    if run_all or args.skills:
        s, f, details = audit_skills(oc_dir)
        sections["skills"] = {"score": s, "findings": f, "skills": details}
        all_findings.extend(f)
        skill_details = details

    # Overall weighted score
    weights = {"security": 30, "cron": 25, "config": 20, "skills": 25}
    total_w = sum(weights[k] for k in sections)
    overall = round(sum(sections[k]["score"] * weights[k] for k in sections) / total_w) if total_w else 0

    result = {
        "score": overall,
        "score_type": "structural_hygiene",
        "score_note": "Measures structural correctness and hygiene, not content quality. Use compound-learning or LLM-based review for deep quality audits.",
        "status": "healthy" if overall >= 80 else "needs_attention" if overall >= 50 else "needs_work",
        "openclaw_dir": str(oc_dir),
        "checked_at": datetime.now().isoformat(),
        "sections": {k: {"score": v["score"], "finding_count": len(v["findings"])} for k, v in sections.items()},
        "summary": {
            "critical": sum(1 for f in all_findings if f["severity"] == "critical"),
            "warnings": sum(1 for f in all_findings if f["severity"] == "warning"),
            "info": sum(1 for f in all_findings if f["severity"] == "info"),
        },
        "findings": [f for f in all_findings if f["severity"] != "ok"],
    }

    if skill_details:
        scored = [s for s in skill_details if s["status"] == "scored"]
        result["skills_summary"] = {
            "total": len(skill_details),
            "scored": len(scored),
            "broken": sum(1 for s in skill_details if s["status"] in ("broken", "empty")),
            "average": round(sum(s["overall"] for s in scored) / len(scored)) if scored else 0,
            "top_5": sorted(scored, key=lambda x: -x["overall"])[:5],
            "bottom_5": sorted(scored, key=lambda x: x["overall"])[:5],
        }

    print(json.dumps(result, indent=2))
    sys.exit(0 if overall >= 50 else 1)


if __name__ == "__main__":
    main()
