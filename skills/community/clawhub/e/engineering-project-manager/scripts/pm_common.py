#!/usr/bin/env python3

import json
import hashlib
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

LEGACY_REQ_PATTERN = (
    r"(?:STK|SYS|SWE|HWE|MLE|MEC|CYB)-REQ-\d+"
)

PROJECT_PATTERN = r"[A-Z][A-Z0-9]{1,15}"
PROCESS_PATTERN = r"[A-Z]{2,6}\d{1,2}"
SEQUENCE_PATTERN = r"\d{3,6}"

BASE_REQ_PATTERN = (
    rf"{PROJECT_PATTERN}_"
    rf"{PROCESS_PATTERN}_REQ_"
    rf"{SEQUENCE_PATTERN}"
)

VERSIONED_REQ_PATTERN = (
    rf"{BASE_REQ_PATTERN}@R\d+"
)

# Transitional V1.0 + V1.1 parser.
REQ_PATTERN = (
    rf"(?:{VERSIONED_REQ_PATTERN}|"
    rf"{LEGACY_REQ_PATTERN})"
)

REQ_ID_RE = re.compile(
    rf"(?<![A-Z0-9_])"
    rf"{REQ_PATTERN}"
    rf"(?![A-Z0-9_@])"
)

HEADING_DEF_RE = re.compile(
    # Double braces are required inside an f-string; otherwise ``{2,6}``
    # becomes the tuple text ``(2, 6)`` and no Markdown heading can match.
    rf"^\s*#{{2,6}}\s+"
    rf"({REQ_PATTERN})"
    rf"(?=\s|$|[-–—:])"
)

TABLE_DEF_RE = re.compile(
    rf"^\s*\|\s*"
    rf"({REQ_PATTERN})"
    rf"\s*\|"
)

V11_REQ_RE = re.compile(
    rf"^(?P<base>{BASE_REQ_PATTERN})"
    rf"@R(?P<revision>\d+)$"
)

BASE_REQ_RE = re.compile(
    rf"^(?P<project>{PROJECT_PATTERN})_"
    rf"(?P<process>{PROCESS_PATTERN})_REQ_"
    rf"(?P<sequence>{SEQUENCE_PATTERN})$"
)


V11_BLOCK_START_RE = re.compile(
    rf"^\s*\[({VERSIONED_REQ_PATTERN})\]\s*$"
)

V11_BLOCK_END_RE = re.compile(
    r"^\s*\[END_REQ\]\s*$"
)

LEGACY_REQ_RE = re.compile(
    rf"^(?P<legacy>{LEGACY_REQ_PATTERN})$"
)


def parse_requirement_id(value):
    """Return structured requirement identity metadata."""

    match = V11_REQ_RE.fullmatch(value)

    if match:
        base_id = match.group("base")
        base_match = BASE_REQ_RE.fullmatch(base_id)

        return {
            "scheme": "V1.1",
            "base_id": base_id,
            "revision": f"R{match.group('revision')}",
            "revision_number": int(match.group("revision")),
            "project": base_match.group("project"),
            "process": base_match.group("process"),
            "sequence": base_match.group("sequence"),
            "revisioned": True,
        }

    if LEGACY_REQ_RE.fullmatch(value):
        return {
            "scheme": "LEGACY",
            "base_id": value,
            "revision": None,
            "revision_number": None,
            "project": None,
            "process": None,
            "sequence": value.rsplit("-", 1)[-1],
            "revisioned": False,
        }

    return None

REQ_STATUS_VALUES = {
    "DRAFT",
    "REVIEWED",
    "RELEASED",
    "CANCELLED",
}

VERIFICATION_METHODS = {
    "TEST",
    "ANALYSIS",
    "INSPECTION",
    "SIMULATION",
    "CODE_REVIEW",
    "REVIEW",
    "DEMONSTRATION",
}

VERIFICATION_SCOPES = {
    "UNIT",
    "COMPONENT",
    "SOFTWARE",
    "HARDWARE",
    "MODEL",
    "SUBSYSTEM",
    "SYSTEM",
    "PRODUCT",
}

VERIFICATION_ACTIVITIES = {
    "UNIT_VERIFICATION",
    "INTEGRATION",
    "VERIFICATION",
    "VALIDATION",
    "ACCEPTANCE",
}






def requirement_section(block, title):
    lines = block.splitlines()
    start = None
    level = None

    for index, line in enumerate(lines):
        match = re.match(
            r"^\s*(#{2,6})\s+(.+?)\s*$",
            line,
        )

        if not match:
            continue

        if match.group(2).strip().lower() == title.lower():
            start = index + 1
            level = len(match.group(1))
            break

    if start is None:
        return None

    content = []

    for line in lines[start:]:
        match = re.match(
            r"^\s*(#{2,6})\s+",
            line,
        )

        if match and len(match.group(1)) <= level:
            break

        content.append(line)

    value = "\n".join(content).strip()
    return value or None




def parse_verification_table(block):
    section = requirement_section(
        block,
        "Verification",
    )

    if not section:
        return []

    rows = [
        line.strip()
        for line in section.splitlines()
        if line.strip().startswith("|")
    ]

    if len(rows) < 3:
        return []

    headers = [
        cell.strip().lower()
        for cell in rows[0].strip("|").split("|")
    ]

    result = []

    for line in rows[2:]:
        cells = [
            cell.strip()
            for cell in line.strip("|").split("|")
        ]

        if len(cells) != len(headers):
            continue

        row = dict(zip(headers, cells))

        if any("<" in value and ">" in value for value in cells):
            continue

        result.append({
            "method": row.get("method", "").upper(),
            "scope": row.get("scope", "").upper(),
            "activity": row.get("activity", "").upper(),
            "process": row.get("process", "").upper(),
            "mandatory": row.get("mandatory", "").upper(),
        })

    return result





def requirement_block_text(item):
    lines = item["lines"]
    start = item["line"] - 1

    if item.get("format") != "BLOCK_V1.1":
        return lines[start]

    block = []

    for line in lines[start:]:
        # A new requirement cannot close an unterminated preceding block.
        # Leave this block unterminated so lint reports its own missing end.
        if block and V11_BLOCK_START_RE.match(line):
            break
        block.append(line)

        if V11_BLOCK_END_RE.match(line):
            return "\n".join(block)

    # Unterminated block is returned as-is so the linter
    # can report the missing END_REQ marker.
    return "\n".join(block)


def requirement_metadata(block):
    result = {}
    lines = block.splitlines()

    for line in lines[1:]:
        if V11_BLOCK_END_RE.match(line):
            break

        if re.match(r"^\s*Text\s*:\s*$", line, re.IGNORECASE):
            break

        match = re.match(
            r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*:\s*(.*)$",
            line,
        )

        if not match:
            continue

        key = match.group(1).strip().lower()
        result[key] = match.group(2).strip()

    return result


def requirement_text_body(block):
    lines = block.splitlines()
    start = None

    for index, line in enumerate(lines):
        if re.match(
            r"^\s*Text\s*:\s*$",
            line,
            re.IGNORECASE,
        ):
            start = index + 1
            break

    if start is None:
        return None

    body = []

    for line in lines[start:]:
        if V11_BLOCK_END_RE.match(line):
            value = "\\n".join(body).strip()
            return value or None

        body.append(line)

    value = "\\n".join(body).strip()
    return value or None


def parse_upstream(value):
    value = (value or "").strip()

    if not value:
        return []

    upper = value.upper()

    if upper in {"ROOT", "DERIVED"}:
        return upper

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def parse_requirement_record(item):
    record = dict(item)

    if item.get("scheme") != "V1.1":
        record["attributes"] = {}
        return record

    block = requirement_block_text(item)
    meta = requirement_metadata(block)

    record["attributes"] = meta
    record["status"] = meta.get("status")
    record["upstream"] = parse_upstream(
        meta.get("upstream")
    )
    record["allocated_to"] = meta.get("allocated_to")

    record["verification_method"] = meta.get(
        "verification_method"
    )
    record["verification_scope"] = meta.get(
        "verification_scope"
    )
    record["verification_activity"] = meta.get(
        "verification_activity"
    )
    record["verification_process"] = meta.get(
        "verification_process"
    )

    record["implementation_milestone"] = meta.get(
        "implementation_milestone"
    )
    record["verification_milestone"] = meta.get(
        "verification_milestone"
    )

    record["owner"] = meta.get("owner")
    record["priority"] = meta.get("priority")
    record["change_id"] = meta.get("change_id")
    record["rationale"] = meta.get("rationale")
    record["acceptance_criteria"] = meta.get(
        "acceptance_criteria"
    )

    record["requirement_text"] = requirement_text_body(
        block
    )

    record["terminated"] = any(
        V11_BLOCK_END_RE.match(line)
        for line in block.splitlines()
    )

    return record


VALID_TASK_STATUS = {
    "BACKLOG",
    "READY",
    "IN_PROGRESS",
    "BLOCKED",
    "REVIEW",
    "REWORK",
    "DONE",
    "CANCELLED",
}


def read_text(path):
    return Path(path).read_text(
        encoding="utf-8",
        errors="replace",
    )


def utc_timestamp():
    """Return a deterministic, timezone-aware ISO 8601 timestamp."""

    return datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat().replace("+00:00", "Z")


def write_text_atomic(path, content):
    """Atomically replace a UTF-8 text file on the same filesystem."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=path.parent,
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def write_json_atomic(path, value):
    write_text_atomic(
        path,
        json.dumps(value, indent=2, sort_keys=True) + "\n",
    )


def canonical_sha256(value):
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def active_requirement_records(project):
    """Return the latest non-cancelled V1.1 revision per stable ID."""

    latest = {}
    for item in requirement_definitions(project):
        if item.get("scheme") != "V1.1":
            continue
        record = parse_requirement_record(item)
        current = latest.get(record["base_id"])
        if (
            current is None
            or record["revision_number"] > current["revision_number"]
        ):
            latest[record["base_id"]] = record
    return sorted(
        (
            record for record in latest.values()
            if (record.get("status") or "").upper() != "CANCELLED"
        ),
        key=lambda record: record["id"],
    )


def requirement_files(project):
    root = Path(project) / "01-requirements"

    if not root.exists():
        return []

    return [
        p for p in root.rglob("*.md")
        if p.name != "TRACEABILITY.md" and "intake" not in p.relative_to(root).parts
    ]


def requirement_definitions(project):
    result = []

    for path in requirement_files(project):
        lines = read_text(path).splitlines()

        for number, line in enumerate(lines, 1):
            # V1.1 block format.
            block_match = V11_BLOCK_START_RE.match(line)

            if block_match:
                rid = block_match.group(1)
                identity = parse_requirement_id(rid)

                result.append({
                    "id": rid,
                    "full_id": rid,
                    **identity,
                    "path": path,
                    "line": number,
                    "text": line,
                    "lines": lines,
                    "format": "BLOCK_V1.1",
                })
                continue

            # Transitional legacy support.
            match = (
                HEADING_DEF_RE.match(line)
                or TABLE_DEF_RE.match(line)
            )

            if not match:
                continue

            rid = match.group(1)
            identity = parse_requirement_id(rid)

            if identity is None:
                continue

            result.append({
                "id": rid,
                "full_id": rid,
                **identity,
                "path": path,
                "line": number,
                "text": line,
                "lines": lines,
                "format": "LEGACY",
            })

    return result




def load_tasks(project):
    path = (
        Path(project)
        / "00-project"
        / "management"
        / "TASKS.json"
    )

    if not path.exists():
        return None

    with path.open(encoding="utf-8") as f:
        return json.load(f)


def git_capture(project, *args):
    result = subprocess.run(
        ["git", *args],
        cwd=project,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def contains_placeholder(text):
    low = text.lower()

    if "todo" in low or "tbd" in low:
        return True

    return bool(
        re.search(r"<[^>\n]+>", text)
    )
