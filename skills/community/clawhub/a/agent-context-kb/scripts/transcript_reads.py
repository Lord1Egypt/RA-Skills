"""Extract KB read events from local agent transcript files."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import shlex


KB_READ_COMMANDS = {"cat", "head", "tail", "sed", "nl", "less", "more"}
KB_ENTRY_FILES = {"start.md", "routes.yaml"}
AGENTS_INSTRUCTION_FILE = "AGENTS.md"
SOURCE_SEARCH_TOOLS = {"Grep", "Glob", "LS"}
SOURCE_EDIT_TOOLS = {"Edit", "MultiEdit", "Write", "NotebookEdit"}
SHELL_SEARCH_COMMANDS = {"rg", "grep", "find", "ls"}
SHELL_EDIT_COMMANDS = {"apply_patch", "perl", "ruby"}


@dataclass(frozen=True)
class KbReadEvent:
    session: str
    harness: str
    timestamp: str
    file: str
    chars: int


@dataclass(frozen=True)
class TranscriptScan:
    sessions: set[str]
    reads: list[KbReadEvent]


@dataclass(frozen=True)
class ToolEvent:
    session: str
    harness: str
    timestamp: str
    order: int
    kind: str
    path: str = ""


# Returns a resolved Path while tolerating missing files and user-relative input.
def resolve_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


# Reads JSONL records from a transcript one line at a time, skipping blank or malformed lines.
def read_jsonl(path: Path) -> list[dict]:
    records = []
    try:
        handle = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return records
    with handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                records.append(value)
    return records


# Yields JSONL records from a transcript one line at a time, skipping malformed lines.
def iter_jsonl(path: Path):
    try:
        handle = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return
    with handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                yield value


# Builds Claude's project-directory encoding for a repo path using non-alphanumeric separators.
def claude_project_name(root: Path) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", str(root))


# Builds the older slash-only Claude project-directory encoding used by early fixtures.
def legacy_claude_project_name(root: Path) -> str:
    return str(root).replace("/", "-")


# Returns likely Claude project directories for root without making them authoritative.
def claude_project_dirs(base: Path, root: Path) -> list[Path]:
    names = {claude_project_name(root), legacy_claude_project_name(root)}
    return sorted(path for path in (base / name for name in names) if path.exists() and path.is_dir())


# Returns whether a path is inside root and, if so, its relative path.
def root_relative(path_value: str, root: Path) -> Path | None:
    if not path_value:
        return None
    try:
        candidate = resolve_path(path_value)
        return candidate.relative_to(root)
    except (OSError, ValueError):
        return None


# Returns whether candidate points at root or any path below it.
def path_is_inside_root(candidate: Path | None, root: Path) -> bool:
    if candidate is None:
        return False
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


# Extracts a cwd/workdir value from common transcript record shapes.
def record_cwd(record: dict) -> Path | None:
    values = [
        record.get("cwd"),
        record.get("workdir"),
        record.get("currentWorkingDirectory"),
        record.get("project_dir"),
    ]
    message = record.get("message") if isinstance(record.get("message"), dict) else {}
    values.extend([message.get("cwd"), message.get("workdir")])
    for value in values:
        if value:
            try:
                return resolve_path(str(value))
            except OSError:
                return None
    return None


# Returns a current-size char estimate for a KB file read.
def file_chars(root: Path, relative: Path) -> int:
    path = root / relative
    try:
        return len(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return 0


# Returns the KB-relative path when a repo-relative path is inside `.agent-kb/`.
def kb_relative(relative: Path) -> str | None:
    if not relative.parts or relative.parts[0] != ".agent-kb" or len(relative.parts) == 1:
        return None
    return str(Path(*relative.parts[1:]))


# Classifies a root-relative read path as KB, AGENTS.md, or source exploration.
def read_kind_for_relative(relative: Path) -> str:
    kb_path = kb_relative(relative)
    if kb_path is not None:
        return "kb_entry_read" if kb_path in KB_ENTRY_FILES else "kb_read"
    if str(relative) == AGENTS_INSTRUCTION_FILE:
        return "agents_read"
    return "source_explore"


# Walks nested Claude message content and yields tool_use dictionaries.
def claude_tool_uses(record: dict) -> list[dict]:
    message = record.get("message") if isinstance(record.get("message"), dict) else record
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, dict):
        content = [content]
    if not isinstance(content, list):
        return []
    return [item for item in content if isinstance(item, dict) and item.get("type") == "tool_use"]


# Extracts KB read events and root-owned session membership from one Claude Code transcript.
def parse_claude_transcript(path: Path, root: Path) -> TranscriptScan:
    session = f"claude:{path.stem}"
    sessions: set[str] = set()
    reads: list[KbReadEvent] = []
    for index, record in enumerate(iter_jsonl(path)):
        cwd = record_cwd(record)
        if path_is_inside_root(cwd, root):
            sessions.add(session)
        timestamp = str(record.get("timestamp") or f"{path.name}:{index}")
        for tool_use in claude_tool_uses(record):
            if tool_use.get("name") != "Read":
                continue
            tool_input = tool_use.get("input") if isinstance(tool_use.get("input"), dict) else {}
            relative = root_relative(str(tool_input.get("file_path") or ""), root)
            if relative is None:
                continue
            sessions.add(session)
            kb_path = kb_relative(relative)
            if kb_path is not None:
                reads.append(KbReadEvent(session, "claude", timestamp, kb_path, file_chars(root, relative)))
    return TranscriptScan(sessions, reads)


# Extracts normalized compliance events from one Claude Code transcript.
def parse_claude_tool_events(path: Path, root: Path) -> list[ToolEvent]:
    events: list[ToolEvent] = []
    belongs_to_root = False
    session = f"claude:{path.stem}"
    for index, record in enumerate(iter_jsonl(path)):
        if path_is_inside_root(record_cwd(record), root):
            belongs_to_root = True
        timestamp = str(record.get("timestamp", ""))
        for tool_use in claude_tool_uses(record):
            name = str(tool_use.get("name", ""))
            tool_input = tool_use.get("input") if isinstance(tool_use.get("input"), dict) else {}
            file_path = str(tool_input.get("file_path") or tool_input.get("path") or "")
            relative = root_relative(file_path, root)
            if relative is not None:
                belongs_to_root = True
            if name == "Read" and relative is not None:
                events.append(ToolEvent(session, "claude", timestamp, index, read_kind_for_relative(relative), str(relative)))
            elif name in SOURCE_SEARCH_TOOLS:
                if relative is not None and kb_relative(relative) is not None:
                    continue
                if belongs_to_root or relative is not None:
                    events.append(ToolEvent(session, "claude", timestamp, index, "source_explore", str(relative or "")))
            elif name in SOURCE_EDIT_TOOLS and relative is not None and kb_relative(relative) is None:
                events.append(ToolEvent(session, "claude", timestamp, index, "source_edit", str(relative)))
    return events if belongs_to_root else []


# Parses a Codex function-call payload into a tool name and argument dictionary.
def codex_tool_call(payload: dict) -> tuple[str, dict]:
    name = str(payload.get("name") or payload.get("tool_name") or "")
    raw_args = payload.get("arguments") or payload.get("input") or payload.get("parameters") or {}
    if isinstance(raw_args, str):
        try:
            parsed = json.loads(raw_args)
        except json.JSONDecodeError:
            parsed = {}
    elif isinstance(raw_args, dict):
        parsed = raw_args
    else:
        parsed = {}
    return name, parsed


# Returns a normalized command string, unwrapping common shell -c wrappers when present.
def codex_command_arg(args: dict) -> str:
    raw = args.get("cmd") or args.get("command") or ""
    if isinstance(raw, list):
        parts = [str(part) for part in raw]
        if len(parts) >= 3 and Path(parts[0]).name in {"bash", "sh", "zsh"} and parts[1] in {"-c", "-lc"}:
            return parts[2]
        return " ".join(shlex.quote(part) for part in parts)
    command = str(raw)
    words = command_words(command)
    if len(words) >= 3 and Path(words[0]).name in {"bash", "sh", "zsh"} and words[1] in {"-c", "-lc"}:
        return words[2]
    return command


# Returns the tool payload for the known Codex transcript record shapes.
def codex_record_tool_payload(record: dict) -> dict | None:
    payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
    if record.get("type") in {"function_call", "tool_call"}:
        return payload
    if record.get("type") == "response_item" and payload.get("type") in {"function_call", "custom_tool_call"}:
        return payload
    return None


# Returns the executable-like words from a shell command using shlex when possible.
def command_words(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


# Finds root-relative paths mentioned in a shell command.
def command_paths(command: str, root: Path, workdir: Path | None) -> list[Path]:
    relatives: list[Path] = []
    for word in command_words(command):
        cleaned = word.strip("'\"")
        relative = root_relative(cleaned, root)
        if relative is not None:
            relatives.append(relative)
            continue
        if workdir is not None and not cleaned.startswith("-"):
            relative = root_relative(str(workdir / cleaned), root)
            if relative is not None:
                relatives.append(relative)
    return relatives


# Extracts the first `.agent-kb/` path read by a Codex shell command.
def codex_kb_read_path(command: str, root: Path, workdir: Path | None) -> Path | None:
    words = command_words(command)
    if not words or Path(words[0]).name not in KB_READ_COMMANDS:
        return None
    for relative in command_paths(command, root, workdir):
        if kb_relative(relative) is not None:
            return relative
    return None


# Classifies a Codex shell command as KB read, AGENTS.md read, source action, or irrelevant.
def classify_codex_command(command: str, root: Path, workdir: Path | None) -> tuple[str | None, str]:
    words = command_words(command)
    if not words:
        return None, ""
    executable = Path(words[0]).name
    paths = command_paths(command, root, workdir)
    kb_read_path = codex_kb_read_path(command, root, workdir)
    if kb_read_path is not None:
        rel = kb_relative(kb_read_path) or ""
        return ("kb_entry_read" if rel in KB_ENTRY_FILES else "kb_read"), str(kb_read_path)
    if executable in KB_READ_COMMANDS:
        for path in paths:
            if str(path) == AGENTS_INSTRUCTION_FILE:
                return "agents_read", str(path)
    source_paths = [path for path in paths if kb_relative(path) is None]
    if executable in SHELL_SEARCH_COMMANDS:
        if source_paths:
            return "source_explore", str(source_paths[0])
        if path_is_inside_root(workdir, root):
            return "source_explore", ""
    if executable in KB_READ_COMMANDS and source_paths:
        return "source_explore", str(source_paths[0])
    if executable in SHELL_EDIT_COMMANDS and source_paths:
        return "source_edit", str(source_paths[0])
    return None, ""


# Extracts KB read events and root-owned session membership from one Codex transcript.
def parse_codex_transcript(path: Path, root: Path) -> TranscriptScan:
    session = f"codex:{path.stem}"
    sessions: set[str] = set()
    reads: list[KbReadEvent] = []
    current_workdir: Path | None = None
    for index, record in enumerate(iter_jsonl(path)):
        payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
        timestamp = str(record.get("timestamp") or f"{path.name}:{index}")
        if record.get("type") == "session_meta":
            cwd = str(payload.get("cwd") or payload.get("workdir") or "")
            cwd_path = resolve_path(cwd) if cwd else None
            if path_is_inside_root(cwd_path, root):
                sessions.add(session)
                current_workdir = cwd_path
            continue
        tool_payload = codex_record_tool_payload(record)
        if tool_payload is None:
            continue
        _name, args = codex_tool_call(tool_payload)
        command = codex_command_arg(args)
        workdir_raw = str(args.get("workdir") or "")
        workdir = resolve_path(workdir_raw) if workdir_raw else current_workdir
        if path_is_inside_root(workdir, root):
            sessions.add(session)
        relative = codex_kb_read_path(command, root, workdir)
        kb_path = kb_relative(relative) if relative is not None else None
        if kb_path is not None:
            sessions.add(session)
            reads.append(KbReadEvent(session, "codex", timestamp, kb_path, file_chars(root, relative)))
    return TranscriptScan(sessions, reads)


# Extracts normalized compliance events from one Codex transcript.
def parse_codex_tool_events(path: Path, root: Path) -> list[ToolEvent]:
    events: list[ToolEvent] = []
    session = f"codex:{path.stem}"
    belongs_to_root = False
    current_workdir: Path | None = None
    for index, record in enumerate(iter_jsonl(path)):
        payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
        timestamp = str(record.get("timestamp", ""))
        if record.get("type") == "session_meta":
            cwd = str(payload.get("cwd") or payload.get("workdir") or "")
            cwd_path = resolve_path(cwd) if cwd else None
            if path_is_inside_root(cwd_path, root):
                belongs_to_root = True
                current_workdir = cwd_path
            continue
        tool_payload = codex_record_tool_payload(record)
        if tool_payload is None:
            continue
        name, args = codex_tool_call(tool_payload)
        command = codex_command_arg(args)
        workdir_raw = str(args.get("workdir") or "")
        workdir = resolve_path(workdir_raw) if workdir_raw else current_workdir
        in_root_workdir = path_is_inside_root(workdir, root)
        if in_root_workdir:
            belongs_to_root = True
        if "apply_patch" in name:
            if in_root_workdir:
                events.append(ToolEvent(session, "codex", timestamp, index, "source_edit"))
            continue
        kind, event_path = classify_codex_command(command, root, workdir)
        if kind and (in_root_workdir or event_path):
            events.append(ToolEvent(session, "codex", timestamp, index, kind, event_path))
            belongs_to_root = True
    return events if belongs_to_root else []


# Collects transcript paths under a directory using the harness' JSONL layout.
def transcript_paths(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("*.jsonl") if path.is_file())


# Returns whether a transcript's raw text mentions any needle before JSON parsing.
def transcript_mentions(path: Path, needles: set[str]) -> bool:
    try:
        handle = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return False
    with handle:
        for line in handle:
            if any(needle in line for needle in needles):
                return True
    return False


# Collects Claude transcript paths from likely project directories for this root.
def claude_transcript_paths(base: Path, root: Path) -> list[Path]:
    paths: list[Path] = []
    for project_dir in claude_project_dirs(base, root):
        paths.extend(transcript_paths(project_dir))
    return sorted(paths)


# Collects Codex transcript paths that cheaply mention this root or KB paths.
def codex_transcript_paths(base: Path, root: Path) -> list[Path]:
    needles = {str(root), root.name, ".agent-kb"}
    return [path for path in transcript_paths(base) if transcript_mentions(path, needles)]


# Merges multiple transcript scan results into one result.
def merge_scans(scans: list[TranscriptScan]) -> TranscriptScan:
    sessions: set[str] = set()
    reads: list[KbReadEvent] = []
    for scan in scans:
        sessions.update(scan.sessions)
        reads.extend(scan.reads)
    return TranscriptScan(sessions, reads)


# Scans local Claude Code and Codex transcripts for KB reads belonging to root.
def scan_transcripts(root: Path, claude_dir: Path | None, codex_dir: Path | None) -> TranscriptScan:
    scans: list[TranscriptScan] = []
    if claude_dir is not None:
        scans.extend(parse_claude_transcript(path, root) for path in claude_transcript_paths(claude_dir, root))
    if codex_dir is not None:
        scans.extend(parse_codex_transcript(path, root) for path in codex_transcript_paths(codex_dir, root))
    return merge_scans(scans)


# Collects normalized compliance events from local Claude Code and Codex transcripts.
def collect_tool_events(root: Path, claude_dir: Path | None, codex_dir: Path | None) -> list[ToolEvent]:
    events: list[ToolEvent] = []
    if claude_dir is not None:
        for path in claude_transcript_paths(claude_dir, root):
            events.extend(parse_claude_tool_events(path, root))
    if codex_dir is not None:
        for path in codex_transcript_paths(codex_dir, root):
            events.extend(parse_codex_tool_events(path, root))
    return events
