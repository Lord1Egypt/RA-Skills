#!/usr/bin/env python3
"""
circleci_config_validator.py — Validate .circleci/config.yml files.

Commands: validate, check, jobs, graph
Flags:    --format text|json|summary   --strict
Exit codes: 0=ok, 1=errors, 2=parse/file error
"""

import sys
import os
import re
import json
import argparse
from collections import defaultdict, deque

# ---------------------------------------------------------------------------
# PyYAML import with graceful fallback
# ---------------------------------------------------------------------------
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VALID_VERSIONS = {2, 2.1, "2", "2.1"}

KNOWN_TOP_LEVEL_KEYS = {
    "version", "jobs", "workflows", "orbs", "executors",
    "commands", "parameters", "setup",
}

KNOWN_STEP_NAMES = {
    "run", "checkout", "save_cache", "restore_cache",
    "persist_to_workspace", "attach_workspace", "store_artifacts",
    "store_test_results", "deploy", "add_ssh_keys", "setup_remote_docker",
    "when", "unless",
}

EXECUTION_ENV_KEYS = {"docker", "machine", "macos", "executor", "vm"}

SECRET_PATTERNS = [
    re.compile(r'(?i)(api[_-]?key|api[_-]?secret|secret[_-]?key|auth[_-]?token|'
               r'access[_-]?token|private[_-]?key|password|passwd|'
               r'aws[_-]?secret|github[_-]?token|slack[_-]?token)\s*[:=]\s*\S+'),
    re.compile(r'(?i)(AKIA[0-9A-Z]{16})'),                     # AWS access key
    re.compile(r'(?i)(sk-[a-zA-Z0-9]{20,})'),                  # OpenAI-style secret
    re.compile(r'(?i)(ghp_[a-zA-Z0-9]{36,})'),                 # GitHub PAT
    re.compile(r'(?i)(xox[baprs]-[a-zA-Z0-9\-]+)'),            # Slack token
]

SEV_ORDER = {"E": 0, "W": 1, "I": 2}
SEV_LABEL = {"E": "ERROR", "W": "WARN ", "I": "INFO "}
SEV_PREFIX = {"E": "[E]", "W": "[W]", "I": "[I]"}


# ---------------------------------------------------------------------------
# Issue dataclass (plain dict for py3.6 compat)
# ---------------------------------------------------------------------------
def make_issue(rule_id, severity, category, message, location=None):
    return {
        "rule_id": rule_id,
        "severity": severity,
        "category": category,
        "message": message,
        "location": location or "",
    }


# ---------------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------------
def load_yaml(filepath):
    """Return (data, error_message). data=None on error."""
    if not os.path.exists(filepath):
        return None, f"File not found: {filepath}"

    if not HAS_YAML:
        return None, (
            "PyYAML is not installed. Install with: pip install pyyaml\n"
            "Cannot parse YAML without it."
        )

    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data, None
    except yaml.YAMLError as exc:
        return None, f"YAML syntax error: {exc}"
    except OSError as exc:
        return None, f"Cannot read file: {exc}"


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def check_structure(data, issues):
    """Rules S002–S005 (S001 handled at parse time)."""
    if not isinstance(data, dict):
        issues.append(make_issue("S002", "E", "Structure",
                                 "Config root must be a YAML mapping"))
        return

    # S002 — version key
    if "version" not in data:
        issues.append(make_issue("S002", "E", "Structure",
                                 "Missing required `version` key"))
    else:
        # S003 — version value
        v = data["version"]
        if v not in VALID_VERSIONS:
            issues.append(make_issue("S003", "E", "Structure",
                                     f"Invalid version `{v}` — must be 2 or 2.1"))

    # S004 — jobs or workflows
    if "jobs" not in data and "workflows" not in data:
        issues.append(make_issue("S004", "W", "Structure",
                                 "Missing both `jobs` and `workflows` sections"))

    # S005 — unknown top-level keys
    for key in data:
        if key not in KNOWN_TOP_LEVEL_KEYS:
            issues.append(make_issue("S005", "W", "Structure",
                                     f"Unknown top-level key: `{key}`",
                                     location=f"key: {key}"))


def check_jobs(data, issues):
    """Rules J001–J005."""
    if not isinstance(data, dict):
        return
    jobs = data.get("jobs")
    if not isinstance(jobs, dict):
        return

    for job_name, job_body in jobs.items():
        loc = f"jobs.{job_name}"
        if not isinstance(job_body, dict):
            issues.append(make_issue("J001", "E", "Jobs",
                                     f"Job `{job_name}` body must be a mapping",
                                     location=loc))
            continue

        # J001 — execution environment
        if not any(k in job_body for k in EXECUTION_ENV_KEYS):
            issues.append(make_issue("J001", "E", "Jobs",
                                     f"Job `{job_name}` missing execution environment "
                                     f"(docker/machine/macos/executor)",
                                     location=loc))

        # J002 — steps present
        if "steps" not in job_body:
            issues.append(make_issue("J002", "E", "Jobs",
                                     f"Job `{job_name}` missing `steps`",
                                     location=loc))
            continue

        steps = job_body["steps"]

        # J003 — non-empty steps
        if not steps:
            issues.append(make_issue("J003", "W", "Jobs",
                                     f"Job `{job_name}` has empty steps list",
                                     location=loc))
            continue

        if not isinstance(steps, list):
            continue

        has_save_cache = False
        has_restore_cache = False

        for idx, step in enumerate(steps):
            step_loc = f"{loc}.steps[{idx}]"

            if isinstance(step, str):
                step_name = step
                step_body = {}
            elif isinstance(step, dict):
                if not step:
                    continue
                step_name = next(iter(step))
                step_body = step.get(step_name) or {}
            else:
                continue

            # J004 — known step names
            if step_name not in KNOWN_STEP_NAMES:
                issues.append(make_issue("J004", "W", "Jobs",
                                         f"Job `{job_name}`: unknown step `{step_name}`",
                                         location=step_loc))

            # J005 — run step needs command
            if step_name == "run":
                if isinstance(step_body, dict) and "command" not in step_body:
                    # allow string shorthand: run: echo hello
                    if not isinstance(step_body, str):
                        issues.append(make_issue("J005", "E", "Jobs",
                                                 f"Job `{job_name}`: `run` step missing `command`",
                                                 location=step_loc))
                # string shorthand is fine

            if step_name == "save_cache":
                has_save_cache = True
            if step_name == "restore_cache":
                has_restore_cache = True

        # B003 — save/restore cache pairing (per-job)
        if has_save_cache and not has_restore_cache:
            issues.append(make_issue("B003", "W", "Best Practices",
                                     f"Job `{job_name}` uses `save_cache` but no `restore_cache`",
                                     location=loc))
        if has_restore_cache and not has_save_cache:
            issues.append(make_issue("B003", "W", "Best Practices",
                                     f"Job `{job_name}` uses `restore_cache` but no `save_cache`",
                                     location=loc))


def check_workflows(data, issues):
    """Rules W001–W004."""
    if not isinstance(data, dict):
        return

    defined_jobs = set(data.get("jobs", {}).keys()) if isinstance(data.get("jobs"), dict) else set()
    workflows = data.get("workflows")
    if not isinstance(workflows, dict):
        return

    # Filter out the `version` key sometimes nested in workflows
    wf_entries = {k: v for k, v in workflows.items() if k != "version"}

    for wf_name, wf_body in wf_entries.items():
        loc = f"workflows.{wf_name}"
        if not isinstance(wf_body, dict):
            continue

        wf_jobs = wf_body.get("jobs")

        # W004 — empty workflow
        if not wf_jobs:
            issues.append(make_issue("W004", "W", "Workflows",
                                     f"Workflow `{wf_name}` has no jobs",
                                     location=loc))
            continue

        if not isinstance(wf_jobs, list):
            continue

        # Collect job names used in this workflow and build dependency map
        wf_job_names = set()
        dep_map = defaultdict(list)   # job_name -> [required_jobs]

        for entry in wf_jobs:
            if isinstance(entry, str):
                wf_job_names.add(entry)
            elif isinstance(entry, dict):
                job_name = next(iter(entry))
                wf_job_names.add(job_name)
                job_cfg = entry.get(job_name) or {}
                if isinstance(job_cfg, dict):
                    requires = job_cfg.get("requires", [])
                    if isinstance(requires, list):
                        dep_map[job_name] = requires

        for job_ref in wf_job_names:
            # W001 — workflow references undefined job
            if defined_jobs and job_ref not in defined_jobs:
                issues.append(make_issue("W001", "E", "Workflows",
                                         f"Workflow `{wf_name}` references undefined job `{job_ref}`",
                                         location=loc))

        # W003 — requires references undefined job (in workflow scope)
        for job_name, reqs in dep_map.items():
            for req in reqs:
                if req not in wf_job_names:
                    issues.append(make_issue("W003", "E", "Workflows",
                                             f"Workflow `{wf_name}`: job `{job_name}` requires "
                                             f"undefined job `{req}`",
                                             location=f"{loc}.jobs.{job_name}"))

        # W002 — circular dependency detection (Kahn's algorithm)
        cycles = _find_cycles(dep_map, wf_job_names)
        for cycle in cycles:
            issues.append(make_issue("W002", "E", "Workflows",
                                     f"Workflow `{wf_name}`: circular dependency: {' -> '.join(cycle)}",
                                     location=loc))


def _find_cycles(dep_map, all_nodes):
    """Return list of cycles as node lists using DFS."""
    cycles = []
    visited = set()
    in_stack = set()
    stack = []

    def dfs(node):
        visited.add(node)
        in_stack.add(node)
        stack.append(node)
        for neighbor in dep_map.get(node, []):
            if neighbor not in visited:
                if neighbor in all_nodes:
                    dfs(neighbor)
            elif neighbor in in_stack:
                # Found cycle — extract it
                idx = stack.index(neighbor)
                cycles.append(stack[idx:] + [neighbor])
        stack.pop()
        in_stack.discard(node)

    for node in all_nodes:
        if node not in visited:
            dfs(node)

    return cycles


def check_security(data, issues):
    """Rules SEC1–SEC4."""
    if not isinstance(data, dict):
        return
    jobs = data.get("jobs") or {}
    if not isinstance(jobs, dict):
        jobs = {}

    for job_name, job_body in jobs.items():
        if not isinstance(job_body, dict):
            continue
        loc = f"jobs.{job_name}"

        # SEC1 — hardcoded secrets in environment variables
        env = job_body.get("environment") or {}
        if isinstance(env, dict):
            for var_name, var_val in env.items():
                val_str = str(var_val) if var_val is not None else ""
                combined = f"{var_name}={val_str}"
                for pat in SECRET_PATTERNS:
                    if pat.search(combined):
                        issues.append(make_issue("SEC1", "E", "Security",
                                                 f"Job `{job_name}`: possible hardcoded secret "
                                                 f"in env var `{var_name}`",
                                                 location=f"{loc}.environment.{var_name}"))
                        break

        steps = job_body.get("steps") or []
        if not isinstance(steps, list):
            continue

        for idx, step in enumerate(steps):
            step_loc = f"{loc}.steps[{idx}]"

            if isinstance(step, str):
                step_name = step
                step_body = {}
            elif isinstance(step, dict):
                if not step:
                    continue
                step_name = next(iter(step))
                step_body = step.get(step_name) or {}
            else:
                continue

            # SEC1 — secrets in run step environment
            if step_name == "run" and isinstance(step_body, dict):
                step_env = step_body.get("environment") or {}
                if isinstance(step_env, dict):
                    for var_name, var_val in step_env.items():
                        val_str = str(var_val) if var_val is not None else ""
                        combined = f"{var_name}={val_str}"
                        for pat in SECRET_PATTERNS:
                            if pat.search(combined):
                                issues.append(make_issue("SEC1", "E", "Security",
                                                         f"Job `{job_name}` step[{idx}]: possible "
                                                         f"hardcoded secret in env var `{var_name}`",
                                                         location=step_loc))
                                break

                # SEC1 — secrets in run command string
                cmd = step_body.get("command", "")
                if isinstance(cmd, str):
                    for pat in SECRET_PATTERNS:
                        if pat.search(cmd):
                            issues.append(make_issue("SEC1", "E", "Security",
                                                     f"Job `{job_name}` step[{idx}]: possible "
                                                     f"hardcoded secret in `run.command`",
                                                     location=step_loc))
                            break

            # SEC2 — setup_remote_docker without version
            if step_name == "setup_remote_docker":
                if not isinstance(step_body, dict) or "version" not in step_body:
                    issues.append(make_issue("SEC2", "W", "Security",
                                             f"Job `{job_name}`: `setup_remote_docker` without "
                                             f"version pinning (e.g. version: 20.10.14)",
                                             location=step_loc))

            # SEC3 — deprecated deploy step
            if step_name == "deploy":
                issues.append(make_issue("SEC3", "W", "Security",
                                         f"Job `{job_name}`: `deploy` step is deprecated, "
                                         f"use `run` instead",
                                         location=step_loc))

    # SEC4 — context without branch filters in workflows
    workflows = data.get("workflows") or {}
    if not isinstance(workflows, dict):
        return
    for wf_name, wf_body in workflows.items():
        if wf_name == "version" or not isinstance(wf_body, dict):
            continue
        wf_jobs = wf_body.get("jobs") or []
        if not isinstance(wf_jobs, list):
            continue
        for entry in wf_jobs:
            if not isinstance(entry, dict):
                continue
            job_name = next(iter(entry))
            job_cfg = entry.get(job_name) or {}
            if not isinstance(job_cfg, dict):
                continue
            if "context" in job_cfg and "filters" not in job_cfg:
                issues.append(make_issue("SEC4", "I", "Security",
                                         f"Workflow `{wf_name}`, job `{job_name}`: uses `context` "
                                         f"without branch/tag `filters` — context secrets exposed "
                                         f"on all branches",
                                         location=f"workflows.{wf_name}.jobs.{job_name}"))


def check_best_practices(data, issues):
    """Rules B001–B004 (B003 is handled in check_jobs)."""
    if not isinstance(data, dict):
        return
    jobs = data.get("jobs") or {}
    if not isinstance(jobs, dict):
        return

    for job_name, job_body in jobs.items():
        if not isinstance(job_body, dict):
            continue
        loc = f"jobs.{job_name}"

        # B001 — missing resource_class
        if "resource_class" not in job_body:
            issues.append(make_issue("B001", "I", "Best Practices",
                                     f"Job `{job_name}`: no `resource_class` set "
                                     f"(defaults to medium — may be undersized)",
                                     location=loc))

        # B002 — no working_directory
        if "working_directory" not in job_body:
            issues.append(make_issue("B002", "I", "Best Practices",
                                     f"Job `{job_name}`: no `working_directory` set",
                                     location=loc))

        # B004 — docker image with :latest or no tag
        docker_cfg = job_body.get("docker")
        if isinstance(docker_cfg, list):
            for img_entry in docker_cfg:
                if not isinstance(img_entry, dict):
                    continue
                image = img_entry.get("image", "")
                if isinstance(image, str):
                    if image.endswith(":latest") or (":" not in image and "/" not in image and image):
                        issues.append(make_issue("B004", "W", "Best Practices",
                                                 f"Job `{job_name}`: Docker image `{image}` "
                                                 f"is not version-pinned (avoid `:latest`)",
                                                 location=loc))
                    elif ":" not in image and image:
                        issues.append(make_issue("B004", "W", "Best Practices",
                                                 f"Job `{job_name}`: Docker image `{image}` "
                                                 f"has no tag — defaults to `:latest`",
                                                 location=loc))

        steps = job_body.get("steps") or []
        if not isinstance(steps, list):
            continue

        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            step_name = next(iter(step))
            step_body = step.get(step_name) or {}

            # B004 — latest in run commands (docker pull/run)
            if step_name == "run" and isinstance(step_body, dict):
                cmd = step_body.get("command", "")
                if isinstance(cmd, str) and re.search(r'docker\s+(pull|run)\s+\S+:latest', cmd):
                    issues.append(make_issue("B004", "W", "Best Practices",
                                             f"Job `{job_name}` step[{idx}]: pulling/running "
                                             f"`:latest` Docker image in command",
                                             location=f"{loc}.steps[{idx}]"))


# ---------------------------------------------------------------------------
# Validators grouped by command
# ---------------------------------------------------------------------------

def run_validate(data, issues):
    """Full validation — all rule categories."""
    check_structure(data, issues)
    check_jobs(data, issues)
    check_workflows(data, issues)
    check_security(data, issues)
    check_best_practices(data, issues)


def run_check(data, issues):
    """Quick check — structure only."""
    check_structure(data, issues)


# ---------------------------------------------------------------------------
# Non-validation commands: jobs, graph
# ---------------------------------------------------------------------------

def cmd_jobs(data, fmt):
    """List all jobs with executor type and step count."""
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), dict):
        print("No jobs defined.")
        return 0

    rows = []
    for job_name, job_body in data["jobs"].items():
        if not isinstance(job_body, dict):
            rows.append((job_name, "?", "?"))
            continue

        executor = "none"
        for key in EXECUTION_ENV_KEYS:
            if key in job_body:
                executor = key
                break

        steps = job_body.get("steps") or []
        step_count = len(steps) if isinstance(steps, list) else "?"
        rows.append((job_name, executor, str(step_count)))

    if fmt == "json":
        out = [{"job": r[0], "executor": r[1], "steps": r[2]} for r in rows]
        print(json.dumps(out, indent=2))
    else:
        col1 = max(len(r[0]) for r in rows) if rows else 10
        col2 = max(len(r[1]) for r in rows) if rows else 8
        header = f"{'JOB':<{col1}}  {'EXECUTOR':<{col2}}  STEPS"
        print(header)
        print("-" * len(header))
        for r in rows:
            print(f"{r[0]:<{col1}}  {r[1]:<{col2}}  {r[2]}")
    return 0


def cmd_graph(data, fmt):
    """Show workflow dependency graph as text."""
    if not isinstance(data, dict):
        print("No data.")
        return 0

    workflows = data.get("workflows")
    if not isinstance(workflows, dict):
        print("No workflows defined.")
        return 0

    graph_data = {}

    for wf_name, wf_body in workflows.items():
        if wf_name == "version" or not isinstance(wf_body, dict):
            continue
        wf_jobs = wf_body.get("jobs") or []
        if not isinstance(wf_jobs, list):
            continue

        nodes = {}
        for entry in wf_jobs:
            if isinstance(entry, str):
                nodes[entry] = []
            elif isinstance(entry, dict):
                job_name = next(iter(entry))
                job_cfg = entry.get(job_name) or {}
                requires = []
                if isinstance(job_cfg, dict):
                    requires = job_cfg.get("requires") or []
                nodes[job_name] = requires if isinstance(requires, list) else []
        graph_data[wf_name] = nodes

    if fmt == "json":
        print(json.dumps(graph_data, indent=2))
        return 0

    for wf_name, nodes in graph_data.items():
        print(f"Workflow: {wf_name}")
        print("=" * (len(wf_name) + 10))

        # Topological sort for display order
        order = _topo_sort(nodes)

        for job in order:
            reqs = nodes.get(job, [])
            if reqs:
                print(f"  {', '.join(reqs)} --> {job}")
            else:
                print(f"  (start) --> {job}")
        print()

    return 0


def _topo_sort(nodes):
    """Simple topological sort (Kahn's). Returns list of nodes in order."""
    in_degree = defaultdict(int)
    adj = defaultdict(list)

    all_nodes = set(nodes.keys())
    for node, reqs in nodes.items():
        for req in reqs:
            if req in all_nodes:
                adj[req].append(node)
                in_degree[node] += 1

    queue = deque(n for n in all_nodes if in_degree[n] == 0)
    result = []
    while queue:
        n = queue.popleft()
        result.append(n)
        for neighbor in adj[n]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Add any remaining (cycle members) at end
    remaining = [n for n in all_nodes if n not in result]
    return result + remaining


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(issues, filepath):
    lines = [f"Validating: {filepath}", ""]
    if not issues:
        lines.append("No issues found.")
        return "\n".join(lines)

    by_cat = defaultdict(list)
    for iss in issues:
        by_cat[iss["category"]].append(iss)

    for cat, cat_issues in sorted(by_cat.items()):
        lines.append(f"[{cat}]")
        for iss in sorted(cat_issues, key=lambda x: SEV_ORDER[x["severity"]]):
            loc = f" ({iss['location']})" if iss["location"] else ""
            lines.append(f"  {SEV_PREFIX[iss['severity']]} {iss['rule_id']}: {iss['message']}{loc}")
        lines.append("")

    errors = sum(1 for i in issues if i["severity"] == "E")
    warnings = sum(1 for i in issues if i["severity"] == "W")
    infos = sum(1 for i in issues if i["severity"] == "I")
    lines.append(f"Total: {errors} error(s), {warnings} warning(s), {infos} info(s)")
    return "\n".join(lines)


def format_json(issues, filepath):
    errors = sum(1 for i in issues if i["severity"] == "E")
    warnings = sum(1 for i in issues if i["severity"] == "W")
    infos = sum(1 for i in issues if i["severity"] == "I")
    out = {
        "file": filepath,
        "summary": {"errors": errors, "warnings": warnings, "infos": infos},
        "issues": issues,
    }
    return json.dumps(out, indent=2)


def format_summary(issues, filepath, strict):
    errors = sum(1 for i in issues if i["severity"] == "E")
    warnings = sum(1 for i in issues if i["severity"] == "W")
    infos = sum(1 for i in issues if i["severity"] == "I")

    if errors > 0:
        status = "FAIL"
    elif warnings > 0 and strict:
        status = "FAIL"
    elif warnings > 0:
        status = "WARN"
    else:
        status = "PASS"

    return (f"{status} {filepath} — "
            f"{errors} error(s), {warnings} warning(s), {infos} info(s)")


def determine_exit_code(issues, strict):
    errors = [i for i in issues if i["severity"] == "E"]
    warnings = [i for i in issues if i["severity"] == "W"]
    if errors:
        return 1
    if strict and warnings:
        return 1
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="circleci_config_validator.py",
        description="Validate .circleci/config.yml files",
    )
    parser.add_argument("command",
                        choices=["validate", "check", "jobs", "graph"],
                        help="Command to run")
    parser.add_argument("file",
                        help="Path to config.yml")
    parser.add_argument("--format", dest="fmt",
                        choices=["text", "json", "summary"],
                        default="text",
                        help="Output format (default: text)")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (exit 1)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    filepath = args.file
    command = args.command
    fmt = args.fmt
    strict = args.strict

    # Non-validation commands that still need parsed YAML
    data, err = load_yaml(filepath)

    if err:
        if fmt == "json":
            print(json.dumps({"error": err, "file": filepath}, indent=2))
        elif fmt == "summary":
            print(f"FAIL {filepath} — {err}")
        else:
            print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(2)

    if data is None:
        if fmt == "json":
            print(json.dumps({"error": "Empty or null config", "file": filepath}, indent=2))
        else:
            print("ERROR: Config file is empty or null.", file=sys.stderr)
        sys.exit(2)

    # Non-issue commands
    if command == "jobs":
        sys.exit(cmd_jobs(data, fmt))

    if command == "graph":
        sys.exit(cmd_graph(data, fmt))

    # Validation commands
    issues = []

    if command == "validate":
        run_validate(data, issues)
    elif command == "check":
        run_check(data, issues)

    # Output
    if fmt == "json":
        print(format_json(issues, filepath))
    elif fmt == "summary":
        print(format_summary(issues, filepath, strict))
    else:
        print(format_text(issues, filepath))

    sys.exit(determine_exit_code(issues, strict))


if __name__ == "__main__":
    main()
