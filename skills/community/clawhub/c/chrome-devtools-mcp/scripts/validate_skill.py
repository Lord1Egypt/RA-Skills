#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "references/configuration.md",
    "references/browser-modes.md",
    "references/security-policy.md",
    "references/user-settings.md",
    "references/skillspector.md",
    "references/openclaw-mcp-install.md",
    "examples/mcp.chrome.isolated.json",
    "examples/mcp.chromium.executable.json",
    "examples/mcp.existing-session.json",
    "examples/mcp.allowed-domain.json",
    "examples/user-settings.example.json",
    "examples/openclaw.mcp.chrome.isolated.json5",
    "examples/openclaw.mcp.chromium.executable.json5",
    "examples/openclaw.mcp.existing-session.json5",
    "examples/openclaw.mcp.allowed-domain.json5",
]

REQUIRED_JSON = [
    "examples/mcp.chrome.isolated.json",
    "examples/mcp.chromium.executable.json",
    "examples/mcp.existing-session.json",
    "examples/mcp.allowed-domain.json",
    "examples/user-settings.example.json",
]

REQUIRED_OPENCLAW_JSON5 = [
    "examples/openclaw.mcp.chrome.isolated.json5",
    "examples/openclaw.mcp.chromium.executable.json5",
    "examples/openclaw.mcp.existing-session.json5",
    "examples/openclaw.mcp.allowed-domain.json5",
]

UNSAFE_EXACT_STRINGS_IN_SKILL = [
    "ignore previous instructions",
    "reveal system prompt",
    "remote-debugging-address=0.0.0.0",
    "curl | bash",
]

REQUIRED_FRONTMATTER_FIELDS = ["name", "description"]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def ok(message: str) -> None:
    print(f"OK: {message}")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def extract_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        fail("SKILL.md does not start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail("SKILL.md YAML frontmatter is not closed")
    return text[4:end]


def frontmatter_has_field(frontmatter: str, field: str) -> bool:
    return re.search(rf"(?m)^{re.escape(field)}\s*:\s*.+$", frontmatter) is not None


def validate_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))
    ok("required files exist")


def validate_frontmatter() -> None:
    text = read("SKILL.md")
    frontmatter = extract_frontmatter(text)
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if not frontmatter_has_field(frontmatter, field):
            fail(f"SKILL.md frontmatter missing required field: {field}")
    if "metadata:" not in frontmatter or "openclaw:" not in frontmatter:
        fail("SKILL.md frontmatter missing OpenClaw metadata")
    ok("SKILL.md frontmatter has required fields")


def validate_json_examples() -> None:
    for path in REQUIRED_JSON:
        with (ROOT / path).open("r", encoding="utf-8") as f:
            json.load(f)
    ok("JSON examples parse correctly")


def validate_openclaw_json5_examples() -> None:
    for path in REQUIRED_OPENCLAW_JSON5:
        text = read(path)
        required = [
            "mcp:",
            "servers:",
            '"chrome-devtools"',
            "enabled: true",
            'transport: "stdio"',
            'command: "npx"',
            "args:",
            '"chrome-devtools-mcp@latest"',
        ]
        for needle in required:
            if needle not in text:
                fail(f"{path} missing required OpenClaw MCP field: {needle}")
    ok("OpenClaw MCP JSON5 examples contain required server fields")


def validate_safe_defaults() -> None:
    settings = json.loads(read("examples/user-settings.example.json"))["chromeDevtools"]
    expected = {
        "mode": "isolated",
        "browser": "chrome",
        "isolated": True,
        "allowExistingSession": False,
        "allowReadingCookies": True,
        "allowReadingStorage": True,
        "allowDownloads": True,
        "allowFormSubmit": True,
        "allowDestructiveActions": False,
        "requireConfirmationForSubmit": True,
        "requireConfirmationForPayments": True,
        "requireConfirmationForAccountChanges": True,
        "disableUsageStatistics": True,
        "disablePerformanceCrux": True,
    }
    for key, value in expected.items():
        if settings.get(key) != value:
            fail(f"unsafe or incorrect default for chromeDevtools.{key}: {settings.get(key)!r}")
    if "file://*" not in settings.get("blockedUrlPatterns", []):
        fail("blockedUrlPatterns missing default blocked pattern: file://*")
    ok("user settings example uses safe defaults")


def validate_skill_text() -> None:
    text = read("SKILL.md").lower()
    for unsafe in UNSAFE_EXACT_STRINGS_IN_SKILL:
        if unsafe in text:
            fail(f"SKILL.md contains unsafe string: {unsafe}")
    required_phrases = [
        "transport: \"stdio\"",
        "openclaw mcp probe chrome-devtools",
        "missing transport",
        "do not use the user's normal chrome profile by default",
        "prefer isolated browser sessions",
        "keep remote debugging bound to localhost",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            fail(f"SKILL.md missing required operational/security phrase: {phrase}")
    ok("SKILL.md includes MCP setup and avoids obvious unsafe strings")


def main() -> None:
    validate_required_files()
    validate_frontmatter()
    validate_json_examples()
    validate_openclaw_json5_examples()
    validate_safe_defaults()
    validate_skill_text()
    print("PASS: chrome-devtools-mcp skill package is valid")


if __name__ == "__main__":
    main()
