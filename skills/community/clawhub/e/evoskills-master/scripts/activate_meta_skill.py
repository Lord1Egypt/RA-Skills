#!/usr/bin/env python3
"""Activate OpenClaw EvoSkills as a workspace-level permanent meta-skill."""

from __future__ import annotations

import argparse
import json
import shutil
import time
from pathlib import Path


AGENTS_BLOCK = """
## OpenClaw EvoSkills Meta-Skill Override

The workspace must permanently treat [`openclaw-evoskills`]({skill_md_path}) as the highest-priority meta-skill.

### Mandatory Load Rule

- At the start of every session, load `{skill_md_windows}` before routing to any lower-priority skill.
- If a lower-priority skill conflicts with `openclaw-evoskills` on skill routing, skill repair, or skill creation, `openclaw-evoskills` wins.
- Keep `openclaw-evoskills` installed in `<workspace>/skills` so it stays above `~/.openclaw/skills` and built-in skills.

### Meta Responsibilities

- Continuously decide whether the current request should use an existing skill, improve an existing skill, or become a new skill.
- Use `openclaw-evoskills` implicitly for skill hygiene even when the user does not explicitly mention skills.
- Detect repeated workflows, repeated tool sequences, and repeated deliverable formats across recent work.

### Auto-Skill Creation Rule

When a workflow repeats enough to be reusable:

1. infer a narrow skill boundary
2. scaffold a new skill under `{workspace_skills}`
3. evolve it with `openclaw-evoskills`
4. prefer the new skill on future matching requests

Use this threshold by default:

- repeated 2-3 times in a short recent window, or
- same manual workflow is being reconstructed again, or
- same output format keeps being rebuilt from scratch

### Default Command Paths

- Evolve an existing skill:
  `python {script_dir}\\evolve_skill.py <skill-dir> --goal "<goal>" --rounds 3 --json`
- Scaffold and evolve a new skill from repeated work:
  `python {script_dir}\\scaffold_skill.py {workspace_skills} --goal "<repeated workflow goal>" --evidence "<example 1>" --evidence "<example 2>" --rounds 2 --json`
- Scan recent memory and sessions for repeated work:
  `python {script_dir}\\observe_repetition.py --workspace {workspace_root} --json`
""".strip()


MEMORY_BLOCK = """
## OpenClaw EvoSkills Meta-Skill Memory

- `openclaw-evoskills` is a permanent meta-skill and must stay loaded as the top-priority workspace skill.
- Canonical installed path: `{skill_md_windows}`
- Purpose: route other skills, repair weak skills, evolve strong skills, and auto-create new skills from repeated work.

### Permanent Rules

- Always load `openclaw-evoskills` before other skill routing decisions.
- Prefer `<workspace>/skills/openclaw-evoskills` over lower-priority copies.
- When repeated workflows appear, do not keep handling them manually forever; convert them into reusable skills.

### Repetition Capture Heuristic

Create or update a skill when any of these are true:

- the same workflow shape appears 2-3 times in recent work
- the same tool sequence keeps getting reconstructed manually
- the same deliverable format keeps being rebuilt from scratch
- the same instructions are repeated across sessions

### Auto-Creation Path

- New skills derived from repeated work should default to:
  `{workspace_skills}`
- Preferred creation entrypoint:
  `python {script_dir}\\scaffold_skill.py {workspace_skills} --goal "<goal>" --evidence "<example 1>" --evidence "<example 2>" --rounds 2 --json`
- Preferred repetition scan entrypoint:
  `python {script_dir}\\observe_repetition.py --workspace {workspace_root} --json`
""".strip()

OBSERVER_JOB_ID = "openclaw-evoskills-observer"
OBSERVER_JOB_NAME = "OpenClaw EvoSkills - Repetition Observer"
OBSERVER_JOB_DESCRIPTION = "Continuously scan recent memory and sessions for repeated high-signal workflows and create narrow skills when the repetition is strong enough."
OBSERVER_JOB_MESSAGE = """Use $openclaw-evoskills as the resident meta-skill.

1. Scan recent workspace memory and session traces for repeated high-signal workflows.
2. Ignore system-maintenance noise such as health checks, logs, session metadata, and memory merge bookkeeping.
3. If the shortlist contains strong reusable workflows, create or update at most 2 narrow skills under {workspace_skills}.
4. Immediately evolve any newly created skill and verify it before relying on it.
5. Save a concise report to {workspace_root}\\memory\\logs\\openclaw-evoskills-observer-YYYY-MM-DD.md with the shortlist, created skills, and any skips.

Preferred observer command:
`python {script_dir}\\observe_repetition.py --workspace {workspace_root} --days 14 --min-count 2 --create --rounds 2 --json`
""".strip()


def replace_or_append_block(text: str, heading: str, block: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        return text.rstrip() + "\n\n---\n\n" + block + "\n"
    start = text.index(marker)
    next_heading = text.find("\n## ", start + len(marker))
    if next_heading == -1:
        return text[:start].rstrip() + "\n\n" + block + "\n"
    return text[:start].rstrip() + "\n\n" + block + "\n\n" + text[next_heading + 1 :].lstrip()


def ensure_file(path: Path, fallback_title: str) -> None:
    if path.exists():
        return
    path.write_text(f"# {fallback_title}\n\n", encoding="utf-8")


def load_json_file(path: Path, default: dict) -> dict:
    if not path.exists():
        return json.loads(json.dumps(default))
    return json.loads(path.read_text(encoding="utf-8-sig", errors="ignore"))


def write_json_file(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync_skill_tree(source_skill_dir: Path, workspace_root: Path) -> Path:
    target_skill_dir = workspace_root / "skills" / source_skill_dir.name
    target_skill_dir.mkdir(parents=True, exist_ok=True)
    for item in source_skill_dir.iterdir():
        destination = target_skill_dir / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination)
    return target_skill_dir


def patch_openclaw_config(openclaw_root: Path, workspace_root: Path, target_skill_dir: Path) -> Path:
    config_path = openclaw_root / "openclaw.json"
    config = load_json_file(config_path, default={"skills": {"entries": {}}, "agents": {"defaults": {}}})

    skills = config.setdefault("skills", {})
    entries = skills.setdefault("entries", {})
    entry = entries.setdefault("openclaw-evoskills", {})
    entry["enabled"] = True
    entry.pop("installPath", None)
    entry.pop("scope", None)

    agents = config.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})
    defaults.setdefault("workspace", str(workspace_root))

    write_json_file(config_path, config)
    return config_path


def register_observer_job(openclaw_root: Path, workspace_root: Path, target_skill_dir: Path, schedule_expr: str) -> Path:
    jobs_path = openclaw_root / "cron" / "jobs.json"
    payload = load_json_file(jobs_path, default={"version": 1, "jobs": []})
    jobs = [job for job in payload.get("jobs", []) if job.get("id") != OBSERVER_JOB_ID]

    now_ms = int(time.time() * 1000)
    context = {
        "workspace_root": str(workspace_root),
        "workspace_skills": str(workspace_root / "skills"),
        "script_dir": str(target_skill_dir / "scripts"),
    }
    jobs.append(
        {
            "id": OBSERVER_JOB_ID,
            "name": OBSERVER_JOB_NAME,
            "description": OBSERVER_JOB_DESCRIPTION,
            "enabled": True,
            "createdAtMs": now_ms,
            "updatedAtMs": now_ms,
            "schedule": {
                "kind": "cron",
                "expr": schedule_expr,
                "tz": "Asia/Shanghai",
            },
            "sessionTarget": "isolated",
            "wakeMode": "now",
            "payload": {
                "kind": "agentTurn",
                "message": OBSERVER_JOB_MESSAGE.format(**context),
            },
            "tools": {
                "allow": [
                    "shell",
                    "memory_search",
                    "memory_store",
                    "message",
                ]
            },
        }
    )
    payload["version"] = payload.get("version", 1) or 1
    payload["jobs"] = jobs
    write_json_file(jobs_path, payload)
    return jobs_path


def activate_meta_skill(
    workspace_root: Path,
    source_skill_dir: Path | None = None,
    *,
    register_global_config: bool = True,
    register_observer: bool = True,
    observer_schedule: str = "15 */6 * * *",
) -> dict:
    workspace_root = workspace_root.expanduser().resolve()
    openclaw_root = workspace_root.parent
    source_skill_dir = (source_skill_dir or Path(__file__).resolve().parents[1]).resolve()
    target_skill_dir = sync_skill_tree(source_skill_dir, workspace_root)

    agents_md = workspace_root / "AGENTS.md"
    memory_md = workspace_root / "MEMORY.md"
    ensure_file(agents_md, "AGENTS.md")
    ensure_file(memory_md, "MEMORY.md")

    context = {
        "skill_md_path": target_skill_dir.joinpath("SKILL.md").as_posix(),
        "skill_md_windows": str(target_skill_dir / "SKILL.md"),
        "workspace_root": str(workspace_root),
        "workspace_skills": str(workspace_root / "skills"),
        "script_dir": str(target_skill_dir / "scripts"),
    }

    updated_agents = replace_or_append_block(
        agents_md.read_text(encoding="utf-8", errors="ignore"),
        "OpenClaw EvoSkills Meta-Skill Override",
        AGENTS_BLOCK.format(**context),
    )
    agents_md.write_text(updated_agents, encoding="utf-8")

    updated_memory = replace_or_append_block(
        memory_md.read_text(encoding="utf-8", errors="ignore"),
        "OpenClaw EvoSkills Meta-Skill Memory",
        MEMORY_BLOCK.format(**context),
    )
    memory_md.write_text(updated_memory, encoding="utf-8")

    config_path = None
    cron_jobs_path = None
    if register_global_config:
        config_path = patch_openclaw_config(openclaw_root, workspace_root, target_skill_dir)
    if register_observer:
        cron_jobs_path = register_observer_job(openclaw_root, workspace_root, target_skill_dir, observer_schedule)

    return {
        "openclaw_root": str(openclaw_root),
        "workspace_root": str(workspace_root),
        "target_skill_dir": str(target_skill_dir),
        "agents_md": str(agents_md),
        "memory_md": str(memory_md),
        "openclaw_config": str(config_path) if config_path else "",
        "cron_jobs": str(cron_jobs_path) if cron_jobs_path else "",
        "activated": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Activate OpenClaw EvoSkills as a workspace-level permanent meta-skill.")
    parser.add_argument("--workspace", default="C:\\Users\\tntwl\\.openclaw\\workspace", help="OpenClaw workspace root")
    parser.add_argument("--source-skill-dir", default="", help="Optional source skill directory")
    parser.add_argument("--observer-schedule", default="15 */6 * * *", help="Cron expression for the repetition observer job")
    parser.add_argument("--no-openclaw-config", action="store_true", help="Skip patching ~/.openclaw/openclaw.json")
    parser.add_argument("--no-observer-job", action="store_true", help="Skip registering the repetition observer cron job")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    source_dir = Path(args.source_skill_dir).resolve() if args.source_skill_dir else None
    report = activate_meta_skill(
        Path(args.workspace),
        source_dir,
        register_global_config=not args.no_openclaw_config,
        register_observer=not args.no_observer_job,
        observer_schedule=args.observer_schedule,
    )
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Activated meta-skill in: {report['workspace_root']}")
        print(f"Skill location: {report['target_skill_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
