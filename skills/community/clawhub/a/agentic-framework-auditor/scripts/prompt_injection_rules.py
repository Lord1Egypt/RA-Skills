from __future__ import annotations

import re
from typing import Iterable

from text_context import instruction_context, match_is_negated, split_clauses

SECRET_ASSIGNMENT = re.compile(r"(?i)\b(api[_-]?key|token|secret|password|credential)\b\s*[:=]\s*['\"]?[^\s'\"]+")
TOKEN_LIKE = re.compile(r"(?i)(sk-[a-z0-9_-]{12,}|xox[baprs]-[a-z0-9-]{10,}|ghp_[a-z0-9]{20,}|AKIA[0-9A-Z]{16})")

RULES = [
    ("P0", "credential_theft", r"\b(exfiltrate|send|upload|post)\b.*\b(secret|token|credential|password|\.env|ssh key|wallet)\b", "Attempts to move secrets or credentials out of scope."),
    ("P0", "destructive_stealth", r"\b(silently|without telling|do not tell|hide this)\b.*\b(delete|remove|wipe|disable|execute|run)\b", "Combines stealth with destructive or executable behavior."),
    ("P0", "persistence_or_malware", r"\b(create|install|add|enable|write|modify|register)\b.*\b(persistence|startup|login item|scheduled task|crontab|registry run key)\b", "Suggests persistence or malware-like installation."),
    ("P1", "authority_override", r"\b(ignore|override|bypass)\b.*\b(system|developer|higher priority|previous instructions|safety)\b", "Attempts to override higher-priority instructions."),
    ("P1", "unsafe_tool_instruction", r"\b(run|execute|eval|curl|wget|powershell|bash)\b.*\b(http|https|base64|encoded|pipe|sudo|admin)\b", "Potential unsafe command or remote execution guidance."),
    ("P1", "secret_access", r"\b(read|open|cat|print|copy)\b.*\b(\.env|id_rsa|ssh|keychain|wallet|browser password|credential)\b", "Attempts to access sensitive local files or credentials."),
    ("P2", "agent_targeting", r"\b(when an assistant reads this:|instructions for ai agents:|model override:|hidden instruction:|tool policy:)\b", "Agent-targeting wrapper may influence behavior if loaded as context."),
    ("P2", "role_manipulation", r"\b(developer mode|act as root|system message begins|you are now system|jailbreak)\b", "Role or authority manipulation language."),
    ("P2", "concealment", r"\b(do not mention|do not reveal|keep this hidden|secretly|silently)\b", "Concealment request aimed at agent behavior."),
    ("INFO", "benign_agent_docs", r"\b(instructions for agents|agent notes|assistant guidance)\b", "Agent-facing documentation is part of the behavioral control surface."),
]

PRIORITY_TO_SEVERITY = {"P0": "Critical", "P1": "High", "P2": "Medium", "P3": "Low", "INFO": "Info"}
COMMENTISH = re.compile(r"^\s*(#|//|/\*|\*|'''|\"\"\")")


def redact_text(value: str) -> str:
    value = SECRET_ASSIGNMENT.sub(lambda m: m.group(1) + "=<REDACTED>", value)
    return TOKEN_LIKE.sub("<REDACTED_TOKEN>", value)


def should_scan_line(record, raw_line: str, in_code_block: bool) -> bool:
    if getattr(record, "role", "") != "executable_or_tooling":
        return True
    stripped = raw_line.strip()
    if COMMENTISH.match(stripped):
        return True
    if in_code_block and stripped.startswith(("#", "//", "*")):
        return True
    return False


def scan_record(record) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    in_code = False
    section = "root"
    for index, raw_line in enumerate(record.text.splitlines(), start=1):
        stripped = raw_line.strip()
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            section = heading.group(2).strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
        if not should_scan_line(record, raw_line, in_code):
            continue
        context = "code_example" if in_code else instruction_context(stripped, section)
        for clause in split_clauses(raw_line):
            for priority, tag, pattern, rationale in RULES:
                matches = [match for match in re.finditer(pattern, clause, re.I) if not match_is_negated(clause, match.start())]
                if not matches:
                    continue
                adjusted = priority
                if context != "active":
                    adjusted = {"P0": "P1", "P1": "P3", "P2": "P3", "P3": "INFO", "INFO": "INFO"}[priority]
                events.append({
                    "file": record.path,
                    "rel_path": record.rel_path,
                    "line_start": index,
                    "line_end": index,
                    "priority": adjusted,
                    "original_priority": priority,
                    "severity": PRIORITY_TO_SEVERITY[adjusted],
                    "tag": tag,
                    "category": "agent_facing_surface" if tag == "benign_agent_docs" else "prompt_injection",
                    "evidence": redact_text(clause.strip())[:500],
                    "rationale": rationale,
                    "in_code_block": in_code,
                    "section": section,
                    "context": context,
                })
    return events


def scan_all(records: Iterable[object]) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for record in records:
        events.extend(scan_record(record))
    return events