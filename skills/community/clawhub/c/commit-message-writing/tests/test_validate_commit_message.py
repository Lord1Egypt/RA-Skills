import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_commit_message import validate


@pytest.mark.parametrize(
    "message,expected_semver",
    [
        ("feat: add login flow", "minor"),
        ("fix: resolve null pointer", "patch"),
        ("refactor: simplify parser", "none"),
        ("docs: update readme usage", "none"),
        ("test: add validator edge cases", "none"),
        ("build: pin poetry version", "none"),
        ("ci: cache pip dependencies", "none"),
        ("chore: clean temporary files", "none"),
        ("style: format lint spacing", "none"),
        ("perf: improve query latency", "patch"),
        ("revert: revert parser rewrite", "depends"),
        ("feat(parser): add token stream", "minor"),
        ("fix(api)!: drop legacy endpoint", "major"),
        (
            "feat(core): add event bus\n\nIntroduce a minimal event bus for internal dispatch.\n\nRefs: #42",
            "minor",
        ),
        (
            "feat(auth): add oauth fallback\n\nBREAKING CHANGE: remove legacy session cookie",
            "major",
        ),
    ],
)
def test_valid_messages(message, expected_semver):
    result = validate(message)
    assert result.valid is True
    assert result.errors == []
    assert result.semver == expected_semver


@pytest.mark.parametrize(
    "message,expected_error",
    [
        ("add login flow", "header must match <type>[scope][!]: <description>"),
        ("feat: Add login flow", "description must be lowercase"),
        ("feat: add login flow.", "description must not end with a period"),
        (
            "feat: " + "a" * 73,
            "description must be 72 characters or fewer",
        ),
        ("feat: wip", "description is too vague"),
        ("feat: misc changes", "description is too vague"),
        ("feat: update", "description is too vague"),
        ("", "missing commit header"),
        ("feat:add login flow", "header must match <type>[scope][!]: <description>"),
    ],
)
def test_invalid_messages(message, expected_error):
    result = validate(message)
    assert result.valid is False
    assert expected_error in result.errors


def test_requires_blank_line_before_body_or_footer():
    msg = "feat: add login flow\nthis should be separated"
    result = validate(msg)

    assert result.valid is False
    assert "body or footer must start after one blank line" in result.errors


def test_invalid_footer_is_rejected():
    msg = "feat: add login flow\n\nBody text\n\nRefs: #42\nBad footer"
    result = validate(msg)

    assert result.valid is False
    assert "invalid footer: Bad footer" in result.errors
