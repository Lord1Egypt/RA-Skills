"""Tests for prompt_generator audit-trail files."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import pytest

from business_blueprint.prompt_generator import generate_prompt_file

# ── Minimal blueprint fixture ─────────────────────────────────

SAMPLE_BLUEPRINT: dict = {
    "version": "1.0",
    "meta": {
        "title": "Test Blueprint",
        "industry": "retail",
        "version": "1.0",
    },
    "library": {
        "capabilities": [{"id": "cap-1"}] * 3,
        "actors": [{"id": "actor-1"}] * 2,
        "systems": [{"id": "sys-1"}] * 4,
        "flowSteps": [{"id": "flow-1"}] * 5,
    },
}


def _make_blueprint(**overrides: object) -> dict:
    bp = json.loads(json.dumps(SAMPLE_BLUEPRINT))
    bp.update(overrides)
    return bp


# ── Tests ──────────────────────────────────────────────────────


def test_generates_timestamped_file(tmp_path: Path) -> None:
    prompt_path = generate_prompt_file(SAMPLE_BLUEPRINT, tmp_path)
    assert prompt_path.name.startswith("generation-prompt-")
    assert prompt_path.name.endswith(".md")
    # timestamp format: YYYYMMDD-HHMMSS-mmm (millisecond precision)
    assert len(prompt_path.stem.split("-")) >= 4
    assert prompt_path.exists()


def test_content_has_mandatory_sections(tmp_path: Path) -> None:
    prompt_path = generate_prompt_file(SAMPLE_BLUEPRINT, tmp_path, theme="dark", fmt="svg")
    content = prompt_path.read_text(encoding="utf-8")

    assert "## Blueprint Summary" in content
    assert "## Provenance" in content
    assert "## Export Configuration" in content
    assert "blueprint_hash:" in content
    assert "cli_args:" in content


def test_blueprint_hash_is_correct(tmp_path: Path) -> None:
    prompt_path = generate_prompt_file(SAMPLE_BLUEPRINT, tmp_path)
    content = prompt_path.read_text(encoding="utf-8")

    expected = hashlib.sha256(
        json.dumps(SAMPLE_BLUEPRINT, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

    assert f"sha256:{expected}" in content


def test_cli_args_recorded(tmp_path: Path) -> None:
    original_argv = sys.argv
    try:
        sys.argv = ["python", "-m", "business_blueprint.cli", "--export", "test.json"]
        prompt_path = generate_prompt_file(SAMPLE_BLUEPRINT, tmp_path)
    finally:
        sys.argv = original_argv

    content = prompt_path.read_text(encoding="utf-8")
    assert "business_blueprint.cli" in content
    assert "--export" in content


def test_history_preserved(tmp_path: Path) -> None:
    """Two exports produce two distinct prompt files (anti-stale invariant)."""
    p1 = generate_prompt_file(SAMPLE_BLUEPRINT, tmp_path, fmt="svg")
    time.sleep(0.01)  # millisecond precision, tiny sleep is enough
    p2 = generate_prompt_file(SAMPLE_BLUEPRINT, tmp_path, fmt="svg")

    assert p1 != p2
    assert p1.exists()
    assert p2.exists()

    files = sorted(tmp_path.glob("generation-prompt-*.md"))
    assert len(files) >= 2


def test_export_config_reflects_params(tmp_path: Path) -> None:
    prompt_path = generate_prompt_file(
        SAMPLE_BLUEPRINT, tmp_path, theme="dark", fmt="drawio"
    )
    content = prompt_path.read_text(encoding="utf-8")

    assert "**Theme**: dark" in content
    assert "**Format**: drawio" in content
