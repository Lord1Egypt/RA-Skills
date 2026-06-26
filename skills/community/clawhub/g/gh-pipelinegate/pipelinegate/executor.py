"""
Pipeline step executor.

Routes tool names to actual function calls using existing product code.
"""

from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from products.promptguard.promptguard.detectors import scan as injection_scan
from products.promptguard.promptguard.detectors import TOTAL_PATTERNS as INJECTION_TOTAL
from products.skillscan.skillscan.detectors import scan as skillscan_scan
from products.skillscan.skillscan.detectors import TOTAL_PATTERNS as SCAN_TOTAL
from products.scopecheck.scopecheck.extractors import (
    extract_cli_tools,
    extract_declared,
    extract_env_vars,
    extract_filesystem_paths,
    extract_network_urls,
)

import difflib
import json
import os
import re
import shutil

import jsonschema
import yaml


def _score(matched: int, total: int, invert: bool = False) -> str:
    if total == 0:
        return "1.0000" if invert else "0.0000"
    ratio = Decimal(matched) / Decimal(total)
    val = (1 - ratio) if invert else ratio
    return str(val.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


_NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)


def _name(content: str) -> str:
    m = _NAME_RE.search(content)
    return m.group(1).strip() if m else "unknown"


def _undeclared(declared: dict, env: list, cli: list, fs: list, urls: list) -> list[str]:
    result = []
    d_env, d_bins = set(declared.get("env", [])), set(declared.get("bins", []))
    for e in env:
        if e not in d_env:
            result.append(f"env:{e}")
    for t in cli:
        if t not in d_bins:
            result.append(f"bin:{t}")
    for p in fs:
        result.append(f"fs:{p}")
    for u in urls:
        result.append(f"net:{u}")
    return result


# ── Tool implementations ───────────────────────────────────────────────────

def exec_scan_text(inp: dict) -> dict:
    text = inp["text"]
    detected = injection_scan(text)
    return {
        "risk_score": _score(len(detected), INJECTION_TOTAL),
        "patterns_detected": detected,
        "input_length": len(text),
    }


def exec_scan_skill(inp: dict) -> dict:
    content = inp["skill_content"]
    findings = skillscan_scan(content)
    safety = _score(len(findings), SCAN_TOTAL, invert=True)
    verdict = "SAFE" if not findings else ("DANGEROUS" if Decimal(safety) < Decimal("0.5") else "CAUTION")
    return {
        "safety_score": safety,
        "findings": findings,
        "verdict": verdict,
        "skill_name": _name(content),
    }


def exec_check_scope(inp: dict) -> dict:
    content = inp["skill_content"]
    declared = extract_declared(content)
    env = extract_env_vars(content)
    cli = extract_cli_tools(content)
    fs = extract_filesystem_paths(content)
    urls = extract_network_urls(content)
    return {
        "skill_name": _name(content),
        "declared": {"env": declared.get("env", []), "bins": declared.get("bins", [])},
        "detected": {"env_vars": env, "cli_tools": cli, "filesystem_paths": fs, "network_urls": urls},
        "undeclared_access": _undeclared(declared, env, cli, fs, urls),
    }


def exec_validate(inp: dict) -> dict:
    schema = inp["json_schema"]
    payload = inp["payload"]
    errors = []
    try:
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
    except jsonschema.SchemaError as e:
        return {"valid": False, "error_count": 1, "errors": [{"path": "$schema", "message": str(e.message)}]}

    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in err.absolute_path) or "$"
        errors.append({"path": path, "message": err.message})
    return {"valid": len(errors) == 0, "error_count": len(errors), "errors": errors}


def exec_diff(inp: dict) -> dict:
    lines_a = inp["text_a"].splitlines(keepends=True)
    lines_b = inp["text_b"].splitlines(keepends=True)
    matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
    if not lines_a and not lines_b:
        sim = "1.0000"
    else:
        sim = str(Decimal(str(matcher.ratio())).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
    changes = []
    additions = deletions = 0
    for line in difflib.unified_diff(lines_a, lines_b, lineterm=""):
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue
        if line.startswith("+"):
            additions += 1
            changes.append({"type": "add", "content": line[1:]})
        elif line.startswith("-"):
            deletions += 1
            changes.append({"type": "delete", "content": line[1:]})
    return {"similarity": sim, "additions": additions, "deletions": deletions, "changes": changes}


def exec_check_env(inp: dict) -> dict:
    req_env = inp.get("required_env", [])
    req_bins = inp.get("required_bins", [])
    present_env = [v for v in req_env if os.environ.get(v) is not None]
    missing_env = [v for v in req_env if os.environ.get(v) is None]
    present_bins = [b for b in req_bins if shutil.which(b) is not None]
    missing_bins = [b for b in req_bins if shutil.which(b) is None]
    return {
        "ready": len(missing_env) == 0 and len(missing_bins) == 0,
        "present_env": present_env, "missing_env": missing_env,
        "present_bins": present_bins, "missing_bins": missing_bins,
    }


def exec_convert(inp: dict) -> dict:
    content = inp["content"]
    in_fmt = inp["input_format"]
    out_fmt = inp["output_format"]
    try:
        if in_fmt == "json":
            data = json.loads(content)
        elif in_fmt == "yaml":
            data = yaml.safe_load(content)
        else:
            return {"success": False, "result": "", "error": f"Unsupported input: {in_fmt}"}

        if out_fmt == "json":
            result = json.dumps(data, indent=2, default=str)
        elif out_fmt == "yaml":
            result = yaml.dump(data, default_flow_style=False, sort_keys=False)
        else:
            return {"success": False, "result": "", "error": f"Unsupported output: {out_fmt}"}

        return {"success": True, "result": result, "error": ""}
    except Exception as e:
        return {"success": False, "result": "", "error": str(e)}


# ── Tool registry ──────────────────────────────────────────────────────────

TOOLS: dict[str, dict[str, Any]] = {
    "scan-text": {"fn": exec_scan_text, "description": "Scan text for prompt injection.", "fields": ["text"]},
    "scan-skill": {"fn": exec_scan_skill, "description": "Scan SKILL.md for malware.", "fields": ["skill_content"]},
    "check-scope": {"fn": exec_check_scope, "description": "Analyze SKILL.md permission scope.", "fields": ["skill_content"]},
    "validate": {"fn": exec_validate, "description": "Validate JSON against schema.", "fields": ["json_schema", "payload"]},
    "diff": {"fn": exec_diff, "description": "Compare two texts.", "fields": ["text_a", "text_b"]},
    "check-env": {"fn": exec_check_env, "description": "Check environment readiness.", "fields": ["required_env", "required_bins"]},
    "convert": {"fn": exec_convert, "description": "Convert between JSON/YAML/TOML.", "fields": ["content", "input_format", "output_format"]},
}


def execute_step(tool_name: str, input_data: dict) -> tuple[bool, dict, str]:
    """Execute a pipeline step. Returns (success, output, error)."""
    if tool_name not in TOOLS:
        return False, {}, f"Unknown tool: {tool_name}. Available: {', '.join(TOOLS.keys())}"
    try:
        result = TOOLS[tool_name]["fn"](input_data)
        return True, result, ""
    except Exception as e:
        return False, {}, str(e)
