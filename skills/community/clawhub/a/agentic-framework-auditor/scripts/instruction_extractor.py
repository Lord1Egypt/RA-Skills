from __future__ import annotations

import re
from typing import Iterable

from text_context import instruction_context

MODAL_PATTERNS = [
    ("hard requirement", re.compile(r"\b(must|required|mandatory|always|shall)\b", re.I)),
    ("prohibition", re.compile(r"\b(never|do not|don't|forbidden|must not|avoid)\b", re.I)),
    ("soft preference", re.compile(r"\b(should|prefer|recommended|try to|usually)\b", re.I)),
    ("permission", re.compile(r"\b(may|allowed|can|permitted)\b", re.I)),
    ("exception", re.compile(r"\b(unless|except|only if|when necessary|fallback)\b", re.I)),
    ("workflow step", re.compile(r"\b(before|after|when|then|next|first|finally)\b", re.I)),
    ("meta-instruction", re.compile(r"\b(ignore|override|system instruction|developer instruction|prompt)\b", re.I)),
]

INSTRUCTION_TRIGGER = re.compile(
    r"\b(must|always|never|should|do not|don't|required|mandatory|forbidden|allowed|"
    r"prefer|avoid|ignore|override|use|before|after|when|confirm|ask|read|write|edit|"
    r"execute|delete|send|exfiltrate|memory|tool|skill|planner|agent|assistant)\b",
    re.I,
)

IMPERATIVE_START = re.compile(
    r"^[-*0-9.\s]*(use|avoid|read|write|edit|run|execute|confirm|ask|check|inspect|"
    r"load|search|prefer|keep|move|delete|create|generate|treat|do|do not|never|always)\b",
    re.I,
)

ABSOLUTE_RE = re.compile(r"\b(always|never|must|required|mandatory|forbidden|all|every|only)\b", re.I)
SECRET_RE = re.compile(r"(?i)\b(api[_-]?key|token|secret|password|credential)\b\s*[:=]\s*['\"]?[^\s'\"]+")
COMMENTISH = re.compile(r"^\s*(#|//|/\*|\*)")

DOMAIN_KEYWORDS = {
    "identity": ["identity", "persona", "soul", "values", "voice"],
    "planning": ["plan", "planner", "decompose", "milestone", "task list"],
    "tool_use": ["tool", "shell", "terminal", "command", "execute", "run", "browser", "mcp"],
    "file_inspection": ["read", "file", "chunk", "grep", "rg", "search", "inspect", "inventory"],
    "coding": ["code", "patch", "edit", "refactor", "implementation"],
    "testing": ["test", "verify", "validation", "eval"],
    "security": ["secret", "credential", "token", "permission", "sandbox", "untrusted"],
    "autonomy": ["autonomous", "proceed", "approval", "confirmation", "ask", "permission"],
    "confirmation": ["confirm", "confirmation", "ask before", "approval"],
    "memory": ["memory", "remember", "persistent", "durable"],
    "skills": ["skill", "SKILL.md", "plugin"],
    "session_search": ["search", "grep", "rg", "find", "index"],
    "terminal": ["terminal", "shell", "command", "powershell", "bash"],
    "editing": ["edit", "patch", "write", "modify", "delete"],
    "reporting": ["report", "summary", "finding", "final answer"],
    "user_interaction": ["user", "ask", "clarify", "question", "message"],
    "safety": ["safe", "safety", "destructive", "risk", "harm"],
}


def redact_text(value: str) -> str:
    value = SECRET_RE.sub(lambda m: m.group(0).split("=")[0].split(":")[0] + "=<REDACTED>", value)
    value = re.sub(r"AKIA[0-9A-Z]{16}", "<REDACTED_AWS_KEY>", value)
    value = re.sub(r"(?i)(sk-[a-z0-9_-]{12,})", "<REDACTED_TOKEN>", value)
    return value


def classify_modality(line: str) -> str:
    for label, pattern in MODAL_PATTERNS:
        if pattern.search(line):
            return label
    return "instruction"


def classify_strength(line: str, modality: str) -> str:
    if modality in {"hard requirement", "prohibition"} or ABSOLUTE_RE.search(line):
        return "hard"
    if modality in {"soft preference", "permission", "exception"}:
        return "soft"
    return "medium"


def classify_domain(line: str) -> str:
    lower = line.lower()
    scores: dict[str, int] = {}
    for domain, words in DOMAIN_KEYWORDS.items():
        score = sum(1 for word in words if word.lower() in lower)
        if score:
            scores[domain] = score
    if not scores:
        return "general"
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))[0][0]


def classify_scope(line: str, file_role: str) -> str:
    lower = line.lower()
    if any(word in lower for word in ("always", "all", "every", "global", "system-wide")):
        return "global"
    if "project" in lower or file_role == "project_instructions":
        return "project"
    if "skill" in lower or file_role == "skill":
        return "skill"
    if "file" in lower or "section" in lower:
        return "local"
    return "unspecified"


def classify_actor(line: str) -> str:
    lower = line.lower()
    if any(word in lower for word in ("agent", "assistant", "model", "codex", "hermes", "claude")):
        return "agent"
    if "user" in lower or "operator" in lower:
        return "operator"
    return "agent"


def risk_tags(line: str, modality: str, domain: str, context: str) -> list[str]:
    lower = line.lower()
    tags: set[str] = set()
    if context == "active" and modality in {"hard requirement", "prohibition"} and ABSOLUTE_RE.search(line):
        tags.add("over_enforcement")
    if any(phrase in lower for phrase in ("ignore previous", "override", "system instruction", "developer instruction")):
        tags.add("prompt_injection")
    if domain in {"tool_use", "terminal", "editing"} and any(word in lower for word in ("always", "never", "must")):
        tags.add("tool_use_rigidity")
    if any(word in lower for word in ("secret", "token", "credential", ".env")):
        tags.add("secret_handling")
    if any(word in lower for word in ("confirm", "approval", "ask before")):
        tags.add("confirmation_policy")
    if any(word in lower for word in ("memory", "remember", "persistent")):
        tags.add("memory")
    return sorted(tags)


def normalize_instruction(value: str) -> str:
    value = redact_text(value).lower()
    value = re.sub(r"[`*_#>\[\]()]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def extract_instructions(record) -> list[dict[str, object]]:
    instructions: list[dict[str, object]] = []
    section = "root"
    in_code = False
    for index, raw_line in enumerate(record.text.splitlines(), start=1):
        line = raw_line.strip()
        if line.startswith("```") or line.startswith("~~~"):
            in_code = not in_code
            continue
        if not line:
            continue
        if getattr(record, "role", "") == "executable_or_tooling" and not COMMENTISH.match(raw_line.strip()):
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            section = heading.group(2).strip()
            continue
        if in_code:
            continue
        if not (INSTRUCTION_TRIGGER.search(line) or IMPERATIVE_START.search(line)):
            continue
        if len(line) < 12:
            continue
        modality = classify_modality(line)
        domain = classify_domain(line)
        cleaned = redact_text(line)
        context = instruction_context(line, section)
        instructions.append({
            "file": record.path,
            "rel_path": record.rel_path,
            "line_start": index,
            "line_end": index,
            "section": section,
            "instruction": cleaned,
            "normalized": normalize_instruction(cleaned),
            "actor": classify_actor(line),
            "modality": modality,
            "domain": domain,
            "strength": classify_strength(line, modality),
            "scope": classify_scope(line, record.role),
            "context": context,
            "risk_tags": risk_tags(line, modality, domain, context),
        })
    return instructions


def extract_all(records: Iterable[object]) -> list[dict[str, object]]:
    all_instructions: list[dict[str, object]] = []
    for record in records:
        all_instructions.extend(extract_instructions(record))
    return all_instructions
