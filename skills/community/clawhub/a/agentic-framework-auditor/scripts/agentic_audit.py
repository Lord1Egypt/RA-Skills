from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from agent_review import build_agent_review_state
from audit_engine import build_audit
from instruction_extractor import extract_all
from prompt_injection_rules import scan_all
from prompt_inventory import PROFILE_HOME_DEFAULTS, collect_files, detect_profile, split_patterns
from render_report import render_all

VALID_MODES = {"shallow", "standard", "full", "custom"}
VALID_PROFILES = {"auto", "generic", "hermes", "codex", "openclaw", "langgraph", "crewai", "autogen"}
VALID_FAIL_LEVELS = {"none", "high", "critical"}
VALID_REVIEW_PROFILES = {"bounded", "diminished"}


def scalar(value: str) -> Any:
    value = value.strip().strip('"').strip("'")
    if value.lower() in {"true", "yes", "on"}:
        return True
    if value.lower() in {"false", "no", "off"}:
        return False
    try:
        return int(value)
    except ValueError:
        return value


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)] if str(value).strip() else []


def strip_yaml_comment(raw: str) -> str:
    quote: str | None = None
    escaped = False
    for index, char in enumerate(raw):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote:
            escaped = True
            continue
        if char in {"'", '"'}:
            quote = None if quote == char else char if quote is None else quote
            continue
        if char == "#" and quote is None:
            return raw[:index]
    return raw


def load_config(path: str | None) -> dict[str, object]:
    if not path:
        return {}
    cfg_path = Path(path).expanduser()
    if not cfg_path.exists():
        raise FileNotFoundError(f"config not found: {cfg_path}")
    if cfg_path.suffix.lower() == ".json":
        import json

        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("audit config must be a JSON object")
        nested = data.get("audit", data)
        if not isinstance(nested, dict):
            raise ValueError("audit config field must be an object")
        return nested

    data: dict[str, object] = {}
    current_key: str | None = None
    in_audit = False
    for raw in cfg_path.read_text(encoding="utf-8").splitlines():
        line = strip_yaml_comment(raw).rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped == "audit:":
            in_audit = True
            current_key = None
            continue
        if in_audit and not raw.startswith((" ", "\t")):
            break
        if not in_audit and raw.startswith((" ", "\t")) and not stripped.startswith("-"):
            continue
        if stripped.startswith("-") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(scalar(stripped[1:].strip()))
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            current_key = key.strip()
            data[current_key] = scalar(value) if value.strip() else []
    return data


def choice(name: str, value: object, allowed: set[str]) -> str:
    normalized = str(value).strip().lower()
    if normalized not in allowed:
        raise ValueError(f"invalid {name}: {value!r}; expected one of {', '.join(sorted(allowed))}")
    return normalized


def positive_int(name: str, value: object) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Audit agentic framework prompts, configs, skills, workflows, and local behavioral guidance.")
    value.add_argument("--mode", choices=sorted(VALID_MODES), default=None)
    value.add_argument("--root", action="append", help="Root directory or file to audit. Repeatable. Defaults to current directory or config roots.")
    value.add_argument("--profile", choices=sorted(VALID_PROFILES), default=None)
    value.add_argument("--framework-home", action="append", help="Additional framework home directory to include. Repeatable.")
    value.add_argument("--hermes-home", action="append", help="Alias for --framework-home with --profile hermes.")
    value.add_argument("--include-profile-home", action="store_true", help="Opt in to the selected profile's default home directory, such as ~/.hermes.")
    value.add_argument("--include", action="append", help="Glob include pattern. Repeatable or comma-separated.")
    value.add_argument("--exclude", action="append", help="Glob exclude pattern. Repeatable or comma-separated.")
    value.add_argument("--no-default-excludes", action="store_true", help="Disable dependency/build/cache default exclusions.")
    value.add_argument("--include-sensitive-files", action="store_true", help="Explicitly scan likely secret-bearing files. Values are redacted heuristically, not guaranteed.")
    value.add_argument("--operator-edited-only", action="store_true", help="Restrict to likely operator-edited behavior files.")
    value.add_argument("--operator-edited-file", action="append", help="Operator-edited file or glob to include when --operator-edited-only is active.")
    value.add_argument("--only-role", action="append", help="Filter by role or alias: skill, prompt, config, memory, planner, workflow, docs, tooling, instructions.")
    value.add_argument("--only-skills", action="store_true", help="Alias for --only-role skill.")
    value.add_argument("--only-prompts", action="store_true", help="Alias for --only-role prompt.")
    value.add_argument("--only-config", action="store_true", help="Alias for --only-role config.")
    value.add_argument("--only-memory", action="store_true", help="Alias for --only-role memory.")
    value.add_argument("--only-prompt-bearing", action="store_true", help="Filter out non prompt-bearing tooling files after inventory classification.")
    value.add_argument("--config", help="JSON or flat/simple YAML audit config.")
    value.add_argument("--output", default=None, help="Output directory for audit artifacts.")
    value.add_argument("--artifact-prefix", help="Output artifact prefix. Defaults to hermes_audit for Hermes, otherwise agentic_audit.")
    value.add_argument("--max-file-bytes", type=int, default=None, help="Maximum bytes read from each file for text analysis.")
    value.add_argument("--report-only", action="store_true", help="Explicitly request report-only behavior. This is the default.")
    value.add_argument("--dry-run-fixes", action="store_true", help="Generate a reviewable fix plan. This is already produced by default.")
    value.add_argument("--apply-fixes", action="store_true", help="Intentionally disabled. Present only to fail safely if requested.")
    value.add_argument("--fail-on", choices=sorted(VALID_FAIL_LEVELS), default=None, help="Exit nonzero if findings meet this severity threshold.")
    value.add_argument("--agent-review", action="store_true", help="Generate a bounded same-agent review packet when no review-integrity blockers are present.")
    value.add_argument("--deterministic-only", action="store_true", help="Disable same-agent review artifacts even if config requests them.")
    value.add_argument("--agent-reviewer-id", default=None, help="Specific accountable identity for the current agent/task. Required for a ready packet.")
    value.add_argument("--agent-review-profile", choices=sorted(VALID_REVIEW_PROFILES), default=None, help="Review profile label. Defaults to diminished.")
    value.add_argument("--agent-review-max-findings", type=int, default=None, help="Maximum deterministic findings in the same-agent packet.")
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.apply_fixes:
        print("ERROR: --apply-fixes is intentionally disabled. Use the generated fix plan and apply patches only after explicit operator approval.", file=sys.stderr)
        return 2

    try:
        cfg = load_config(args.config)
        mode = choice("mode", args.mode or cfg.get("mode") or "standard", VALID_MODES)
        profile = choice("profile", args.profile or cfg.get("profile") or "auto", VALID_PROFILES)
        fail_on = choice("fail_on", args.fail_on or cfg.get("fail_on") or "none", VALID_FAIL_LEVELS)
        review_profile = choice("agent_review_profile", args.agent_review_profile or cfg.get("agent_review_profile") or "diminished", VALID_REVIEW_PROFILES)
        max_file_bytes = args.max_file_bytes if args.max_file_bytes is not None else positive_int("max_file_bytes", cfg.get("max_file_bytes") or 512000)
        max_review_findings = args.agent_review_max_findings if args.agent_review_max_findings is not None else positive_int("agent_review_max_findings", cfg.get("agent_review_max_findings") or 30)
        max_file_bytes = positive_int("max_file_bytes", max_file_bytes)
        max_review_findings = positive_int("agent_review_max_findings", max_review_findings)
    except Exception as exc:
        print(f"ERROR: invalid audit configuration: {exc}", file=sys.stderr)
        return 2

    roots = args.root or as_list(cfg.get("roots")) or as_list(cfg.get("root")) or ["."]
    if profile == "auto":
        profile = detect_profile(roots)

    homes: list[str] = []
    homes.extend(split_patterns(cfg.get("framework_home")))
    homes.extend(split_patterns(cfg.get("framework_homes")))
    homes.extend(split_patterns(cfg.get("hermes_home")))
    homes.extend(split_patterns(cfg.get("hermes_homes")))
    homes.extend(split_patterns(args.framework_home))
    homes.extend(split_patterns(args.hermes_home))
    include_profile_home = bool(cfg.get("include_profile_home", False)) or args.include_profile_home
    if include_profile_home:
        homes.extend(PROFILE_HOME_DEFAULTS.get(profile, []))
    roots = list(roots) + homes

    includes = split_patterns(cfg.get("include")) + split_patterns(args.include)
    excludes = split_patterns(cfg.get("exclude")) + split_patterns(args.exclude)
    operator_patterns = split_patterns(cfg.get("operator_edited_files")) + split_patterns(args.operator_edited_file)
    operator_only = bool(cfg.get("operator_edited_only", False)) or args.operator_edited_only

    only_roles = split_patterns(cfg.get("only_roles")) + split_patterns(cfg.get("only_role")) + split_patterns(args.only_role)
    if args.only_skills:
        only_roles.append("skill")
    if args.only_prompts:
        only_roles.append("prompt")
    if args.only_config:
        only_roles.append("config")
    if args.only_memory:
        only_roles.append("memory")
    prompt_bearing_only = bool(cfg.get("prompt_bearing_only", False)) or bool(cfg.get("only_prompt_bearing", False)) or args.only_prompt_bearing

    output = args.output or str(cfg.get("output") or ".agentic-audit")
    no_default_excludes = args.no_default_excludes or bool(cfg.get("no_default_excludes", False))
    include_sensitive_files = args.include_sensitive_files or bool(cfg.get("include_sensitive_files", False))
    agent_review_requested = bool(cfg.get("agent_review", False)) or args.agent_review
    deterministic_only = bool(cfg.get("deterministic_only", False)) or args.deterministic_only
    reviewer_id = args.agent_reviewer_id or str(cfg.get("agent_reviewer_id") or "")

    try:
        records, warnings = collect_files(
            roots=roots,
            mode=mode,
            profile=profile,
            includes=includes,
            excludes=excludes,
            no_default_excludes=no_default_excludes,
            operator_edited_only=operator_only,
            operator_edited_patterns=operator_patterns,
            only_roles=only_roles,
            prompt_bearing_only=prompt_bearing_only,
            max_file_bytes=max_file_bytes,
            include_sensitive_files=include_sensitive_files,
        )
        instructions = extract_all(records)
        prompt_events = scan_all(records)
        audit = build_audit(records, instructions, prompt_events, warnings, profile=profile, mode=mode)
        if agent_review_requested or deterministic_only:
            audit["agent_review"] = build_agent_review_state(
                audit,
                requested=agent_review_requested,
                deterministic_only=deterministic_only,
                reviewer_id=reviewer_id,
                review_profile=review_profile,
                max_findings=max_review_findings,
            )
        prefix = args.artifact_prefix or str(cfg.get("artifact_prefix") or ("hermes_audit" if profile == "hermes" else "agentic_audit"))
        paths = render_all(audit, output, prefix, {
            "roots": roots,
            "includes": includes or "default",
            "excludes": excludes or "default",
            "include_profile_home": include_profile_home,
            "include_sensitive_files": include_sensitive_files,
            "operator_edited_only": operator_only,
            "operator_edited_files": operator_patterns,
            "only_roles": only_roles or "all",
            "prompt_bearing_only": prompt_bearing_only,
        })
    except Exception as exc:
        print(f"ERROR: audit failed: {exc}", file=sys.stderr)
        return 2

    summary = audit["summary"]
    print(f"Audit ID: {audit.get('audit_id')}")
    print(f"Profile: {profile}")
    print(f"Mode: {mode}")
    print(f"Files scanned: {summary['files_scanned']}")
    print(f"Instructions extracted: {summary['instructions_extracted']} ({summary.get('active_instructions')} active)")
    print(f"Findings: {summary['findings_total']} {summary['severity_counts']}")
    for warning in audit.get("warnings") or []:
        print(f"Warning: {warning}")
    for name, path in paths.items():
        print(f"{name}: {path}")
    review = audit.get("agent_review")
    if review:
        print(f"Agent review: {review.get('status')} (reviewer={review.get('reviewer_id') or 'unidentified'}, profile={review.get('review_profile')})")
        blockers = review.get("blocked_reasons") or []
        for item in blockers[:5]:
            print(f"  - {item.get('severity')} {item.get('reason')}: {item.get('detail')}")
            if item.get("operator_action"):
                print(f"    action: {item.get('operator_action')}")
        if len(blockers) > 5:
            print(f"  - ... {len(blockers) - 5} more blocker(s) in the gate artifact")

    severities = summary.get("severity_counts", {})
    if fail_on == "critical" and severities.get("Critical", 0):
        return 1
    if fail_on == "high" and (severities.get("Critical", 0) or severities.get("High", 0)):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
