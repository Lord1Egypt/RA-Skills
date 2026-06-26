# FILE_META
# INPUT:  tool call records from conversation
# OUTPUT: Anthropic-format tool schema array
# POS:    skill lib — called by converter.py
# MISSION: Maintain built-in tool schemas and infer schemas for unknown tools.

"""Built-in OpenClaw tool schema definitions and schema inference for unknown tools.

Schemas are extracted from the OpenClaw source code (pi-coding-agent core tools
and OpenClaw extension tools). Parameter names use Claude-compatible aliases
(file_path, old_string, new_string) to match actual tool_use calls in trajectories.
"""

from __future__ import annotations

import json

# Built-in tool schemas (Anthropic format with input_schema)
# Source: pi-coding-agent/dist/core/tools/*.js + openclaw/src/agents/*.ts
BUILTIN_TOOLS: dict[str, dict] = {
    "exec": {
        "name": "exec",
        "description": "Run shell commands (pty available for TTY-required CLIs)",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to execute"},
                "workdir": {"type": "string", "description": "Working directory (defaults to cwd)"},
                "timeout": {"type": "number", "description": "Timeout in seconds (optional, kills process on expiry)"},
                "yieldMs": {"type": "number", "description": "Milliseconds to wait before backgrounding (default 10000)"},
                "background": {"type": "boolean", "description": "Run in background immediately"},
                "pty": {"type": "boolean", "description": "Run in a pseudo-terminal (PTY) when available (TTY-required CLIs, coding agents)"},
            },
            "required": ["command"],
        },
    },
    "read": {
        "name": "read",
        "description": "Read the contents of a file. Supports text files and images (jpg, png, gif, webp). Use offset/limit for large files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to read (relative or absolute)"},
                "file_path": {"type": "string", "description": "Path to the file to read (relative or absolute)"},
                "offset": {"type": "number", "description": "Line number to start reading from (1-indexed)"},
                "limit": {"type": "number", "description": "Maximum number of lines to read"},
            },
        },
    },
    "write": {
        "name": "write",
        "description": "Write content to a file. Creates the file if it doesn't exist, overwrites if it does. Automatically creates parent directories.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to write (relative or absolute)"},
                "file_path": {"type": "string", "description": "Path to the file to write (relative or absolute)"},
                "content": {"type": "string", "description": "Content to write to the file"},
            },
            "required": ["content"],
        },
    },
    "edit": {
        "name": "edit",
        "description": "Edit a file by replacing exact text. The oldText must match exactly (including whitespace). Use this for precise, surgical edits.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file to edit (relative or absolute)"},
                "file_path": {"type": "string", "description": "Path to the file to edit (relative or absolute)"},
                "oldText": {"type": "string", "description": "Exact text to find and replace (must match exactly)"},
                "old_string": {"type": "string", "description": "Exact text to find and replace (must match exactly)"},
                "newText": {"type": "string", "description": "New text to replace the old text with"},
                "new_string": {"type": "string", "description": "New text to replace the old text with"},
            },
        },
    },
    "web_search": {
        "name": "web_search",
        "description": "Search the web using Brave Search API",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string"},
                "count": {"type": "number", "description": "Number of results to return (1-10)"},
                "country": {"type": "string", "description": "2-letter country code for region-specific results (e.g., 'DE', 'US', 'ALL')"},
                "language": {"type": "string", "description": "ISO 639-1 language code for results (e.g., 'en', 'de', 'fr')"},
                "freshness": {"type": "string", "description": "Filter by time: 'day' (24h), 'week', 'month', or 'year'"},
                "date_after": {"type": "string", "description": "Only results published after this date (YYYY-MM-DD)"},
                "date_before": {"type": "string", "description": "Only results published before this date (YYYY-MM-DD)"},
                "search_lang": {"type": "string", "description": "Brave language code for search results (e.g., 'en', 'de', 'zh-hans')"},
                "ui_lang": {"type": "string", "description": "Locale code for UI elements in language-region format (e.g., 'en-US', 'de-DE')"},
            },
            "required": ["query"],
        },
    },
    "web_fetch": {
        "name": "web_fetch",
        "description": "Fetch and extract readable content from a URL",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "HTTP or HTTPS URL to fetch"},
                "extractMode": {"type": "string", "description": "Extraction mode ('markdown' or 'text'), default 'markdown'"},
                "maxChars": {"type": "number", "description": "Maximum characters to return (truncates when exceeded)"},
            },
            "required": ["url"],
        },
    },
    "browser": {
        "name": "browser",
        "description": "Control web browser for navigation and interaction",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Browser action: status, start, stop, profiles, tabs, open, focus, close, snapshot, screenshot, navigate, console, pdf, upload, dialog, act"},
                "target": {"type": "string", "description": "Browser target: sandbox, host, or node"},
                "node": {"type": "string", "description": "Node name for remote browser"},
                "profile": {"type": "string", "description": "Browser profile name"},
                "targetUrl": {"type": "string", "description": "URL for open/navigate actions"},
                "url": {"type": "string", "description": "URL for open/navigate actions"},
                "targetId": {"type": "string", "description": "Tab target ID"},
                "limit": {"type": "number", "description": "Result limit"},
                "maxChars": {"type": "number", "description": "Maximum characters for snapshot"},
                "mode": {"type": "string", "description": "Snapshot mode: efficient"},
                "snapshotFormat": {"type": "string", "description": "Snapshot format: aria or ai"},
                "refs": {"type": "string", "description": "Snapshot refs: role or aria"},
                "interactive": {"type": "boolean", "description": "Include interactive elements in snapshot"},
                "compact": {"type": "boolean", "description": "Compact snapshot output"},
                "depth": {"type": "number", "description": "Snapshot tree depth"},
                "selector": {"type": "string", "description": "CSS selector for element"},
                "frame": {"type": "string", "description": "Frame selector"},
                "labels": {"type": "boolean", "description": "Show labels in screenshot"},
                "fullPage": {"type": "boolean", "description": "Full page screenshot"},
                "ref": {"type": "string", "description": "Element reference"},
                "element": {"type": "string", "description": "Element identifier"},
                "type": {"type": "string", "description": "Image type: png or jpeg"},
                "level": {"type": "string", "description": "Console log level"},
                "paths": {"type": "array", "items": {"type": "string"}, "description": "File paths for upload"},
                "inputRef": {"type": "string", "description": "Input element reference for upload"},
                "timeoutMs": {"type": "number", "description": "Timeout in milliseconds"},
                "accept": {"type": "boolean", "description": "Accept dialog"},
                "promptText": {"type": "string", "description": "Text for dialog prompt"},
                "kind": {"type": "string", "description": "Act kind: click, type, press, hover, drag, select, fill, resize, wait, evaluate, close"},
                "text": {"type": "string", "description": "Text input for type action"},
                "submit": {"type": "boolean", "description": "Submit after type"},
                "slowly": {"type": "boolean", "description": "Type slowly"},
                "key": {"type": "string", "description": "Key to press"},
                "delayMs": {"type": "number", "description": "Delay between keystrokes"},
                "doubleClick": {"type": "boolean", "description": "Double click"},
                "button": {"type": "string", "description": "Mouse button"},
                "modifiers": {"type": "array", "items": {"type": "string"}, "description": "Key modifiers"},
                "startRef": {"type": "string", "description": "Drag start reference"},
                "endRef": {"type": "string", "description": "Drag end reference"},
                "values": {"type": "array", "items": {"type": "string"}, "description": "Select values"},
                "fields": {"type": "array", "items": {"type": "object"}, "description": "Form fields to fill"},
                "width": {"type": "number", "description": "Resize width"},
                "height": {"type": "number", "description": "Resize height"},
                "timeMs": {"type": "number", "description": "Wait time in milliseconds"},
                "textGone": {"type": "string", "description": "Wait until text disappears"},
                "loadState": {"type": "string", "description": "Wait for page load state"},
                "fn": {"type": "string", "description": "JavaScript function to evaluate"},
                "request": {"type": "object", "description": "Structured act request object"},
            },
            "required": ["action"],
        },
    },
    "process": {
        "name": "process",
        "description": "Manage background exec sessions",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Process action: poll, log, kill, list, write, send-keys, paste"},
                "sessionId": {"type": "string", "description": "Session id for actions other than list"},
                "data": {"type": "string", "description": "Data to write for write action"},
                "keys": {"type": "array", "items": {"type": "string"}, "description": "Key tokens to send for send-keys"},
                "hex": {"type": "array", "items": {"type": "string"}, "description": "Hex bytes to send for send-keys"},
                "literal": {"type": "string", "description": "Literal string for send-keys"},
                "text": {"type": "string", "description": "Text to paste for paste action"},
                "bracketed": {"type": "boolean", "description": "Wrap paste in bracketed mode"},
                "eof": {"type": "boolean", "description": "Close stdin after write"},
                "offset": {"type": "number", "description": "Log offset"},
                "limit": {"type": "number", "description": "Log length"},
                "timeout": {"type": "number", "description": "For poll: wait up to this many milliseconds before returning"},
            },
            "required": ["action"],
        },
    },
    "apply_patch": {
        "name": "apply_patch",
        "description": "Apply multi-file patches",
        "input_schema": {
            "type": "object",
            "properties": {
                "patch": {"type": "string", "description": "Unified diff patch content"},
            },
            "required": ["patch"],
        },
    },
    "grep": {
        "name": "grep",
        "description": "Search file contents for patterns",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Regular expression pattern to search for"},
                "path": {"type": "string", "description": "File or directory to search in"},
                "include": {"type": "string", "description": "Glob pattern to filter files (e.g., '*.ts')"},
            },
            "required": ["pattern"],
        },
    },
    "find": {
        "name": "find",
        "description": "Find files by glob pattern",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Glob pattern to match files"},
                "path": {"type": "string", "description": "Directory to search in"},
            },
            "required": ["pattern"],
        },
    },
    "ls": {
        "name": "ls",
        "description": "List directory contents",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory path to list"},
            },
            "required": ["path"],
        },
    },
}


def _infer_json_type(value) -> str:
    """Infer JSON Schema type from a Python value."""
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "number"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "string"


def _infer_schema_from_calls(calls: list[dict]) -> dict:
    """Infer a JSON Schema input_schema by merging arguments from all calls to the same tool.

    Collects all observed property names and their types across invocations.
    Properties that appear in every call are marked as required.
    """
    properties: dict[str, dict] = {}
    call_count = len(calls)
    property_counts: dict[str, int] = {}

    for call in calls:
        args = call.get("arguments", {})
        # arguments may be a JSON string in some OpenClaw versions
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except (json.JSONDecodeError, ValueError):
                continue
        if not isinstance(args, dict):
            continue
        for key, value in args.items():
            property_counts[key] = property_counts.get(key, 0) + 1
            if key not in properties:
                properties[key] = {"type": _infer_json_type(value)}

    # Properties present in every call are considered required
    required = sorted(k for k, count in property_counts.items() if count == call_count)

    schema: dict = {
        "type": "object",
        "properties": properties,
    }
    if required:
        schema["required"] = required

    return schema


def get_tool_schemas(tool_calls: list[dict]) -> list[dict]:
    """Build tool schema list from observed tool calls.

    For built-in tools, uses predefined schemas from BUILTIN_TOOLS.
    For non-built-in tools (plugins, MCP), reverse-engineers the schema
    from observed call arguments across all invocations.

    Every tool_use in messages will have a corresponding schema in the
    tools array (1:1 correspondence required by Anthropic format).

    Args:
        tool_calls: List of toolCall blocks from the conversation
    """
    schemas = []
    builtin_added: set[str] = set()
    # Group non-builtin calls by name for schema inference
    non_builtin_calls: dict[str, list[dict]] = {}

    for call in tool_calls:
        name = call.get("name", "")
        if not name:
            continue

        if name in BUILTIN_TOOLS:
            if name not in builtin_added:
                builtin_added.add(name)
                schemas.append(BUILTIN_TOOLS[name])
        else:
            if name not in non_builtin_calls:
                non_builtin_calls[name] = []
            non_builtin_calls[name].append(call)

    # Add inferred schemas for non-builtin tools
    for name, calls in non_builtin_calls.items():
        inferred_schema = _infer_schema_from_calls(calls)
        schemas.append({
            "name": name,
            "description": "",
            "input_schema": inferred_schema,
        })

    return schemas
