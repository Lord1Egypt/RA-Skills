#!/usr/bin/env python3
"""Markdown and CSV output for every command (ROADMAP T2.23)."""

import csv
import io
import json
from typing import ClassVar

import pytest
from test_degradation import SCRIPTS, db_without, run

from _common import render_csv, render_markdown


def tables(value, path=""):
    """Every list of objects in a JSON result, with its dotted path (what CSV should contain)."""
    if isinstance(value, list) and value and all(isinstance(v, dict) for v in value):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from tables(item, f"{path}.{key}" if path else key)


class TestRenderers:
    DATA: ClassVar[dict] = {
        "summary": {"count": 2, "size": "1 KB"},
        "items": [{"name": "a|b", "tags": ["x", "y"]}, {"name": "c\nd", "extra": None}],
        "nested": {"deeper": {"rows": [{"k": 1}]}},
        "empty": [],
        "words": ["one", "two"],
        "flag": True,
    }

    def test_markdown(self):
        md = render_markdown(self.DATA, "demo")
        assert md.startswith("# demo\n")
        assert "- **flag**: True" in md
        assert "## summary" in md and "- **count**: 2" in md
        assert "| name | tags | extra |" in md
        assert "| a\\|b |" in md  # pipes escaped
        assert "| c d |" in md  # newlines can't break a table row
        assert '["x","y"]' in md  # nested values as compact JSON
        assert "#### rows" in md  # heading depth follows nesting
        assert "- **empty**: (none)" in md
        assert "- **words**: one, two" in md

    def test_csv(self):
        rows = list(csv.DictReader(io.StringIO(render_csv(self.DATA))))
        assert [r["section"] for r in rows] == ["items", "items", "nested.deeper.rows"]
        assert rows[0]["name"] == "a|b" and json.loads(rows[0]["tags"]) == ["x", "y"]
        assert rows[1]["extra"] == ""
        assert rows[2]["k"] == "1"

    def test_csv_with_no_rows_still_has_a_header(self):
        assert render_csv({"summary": {"count": 0}}) == "section\r\n"

    def test_line_breaks_inside_values_stay_inside_their_cell(self):
        text = render_csv({"rows": [{"a": "one\rtwo", "b": "three\nfour"}, {"a": "x", "b": "y"}]})
        rows = list(csv.DictReader(io.StringIO(text, newline="")))
        assert [(r["a"], r["b"]) for r in rows] == [("one\rtwo", "three\nfour"), ("x", "y")]


@pytest.mark.parametrize("script", SCRIPTS)
def test_every_command_supports_md_and_csv(script, tmp_path):
    db = db_without(tmp_path, None, None)
    code, out = run(script, db, tmp_path)  # JSON (doctor / smart_export pass --format json in the sweep)
    assert code == 0
    result = json.loads(out)

    code, md = run(script, db, tmp_path, extra=["--format", "md"])
    assert code == 0
    assert md.startswith("# ")

    code, text = run(script, db, tmp_path, extra=["--format", "csv"])
    assert code == 0
    rows = list(csv.DictReader(io.StringIO(text, newline="")))
    expected = 1 + sum(len(table) for _, table in tables(result))  # + the envelope row
    assert len(rows) == expected, f"{script}: {len(rows)} CSV rows for {expected} expected"
    assert {r["section"] for r in rows} == {"envelope"} | {path for path, _ in tables(result)}
    assert (rows[0]["section"], rows[0]["command"]) == ("envelope", script)


def test_output_file(tmp_path):
    db = db_without(tmp_path, None, None)
    out = tmp_path / "report.md"
    code, stdout = run("library_analysis", db, tmp_path, extra=["--format", "md", "-o", str(out)])
    assert code == 0
    assert stdout == ""
    assert out.read_text().startswith("# ")


@pytest.mark.parametrize("script", SCRIPTS)
def test_every_result_has_the_envelope(script, tmp_path):
    """ROADMAP T1.7: the same leading fields on every structured result (additive; see SCHEMA_VERSION)."""
    from datetime import datetime

    from _common import SCHEMA_VERSION

    code, out = run(script, db_without(tmp_path, None, None), tmp_path)
    assert code == 0
    result = json.loads(out)
    assert list(result)[:4] == ["schema_version", "command", "generated_at", "warnings"]
    assert result["schema_version"] == SCHEMA_VERSION
    assert result["command"] == script
    assert datetime.fromisoformat(result["generated_at"]).utcoffset().total_seconds() == 0
    assert result["warnings"] == []


def test_envelope_names_the_command_through_the_dispatcher(tmp_path):
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    out = subprocess.run(
        [sys.executable, str(root / "photos_cleaner.py"), "storage-analyzer", "--db-path", db_without(tmp_path, None, None).as_posix(), "-q"],
        capture_output=True, text=True, timeout=60,
    )  # fmt: skip
    assert json.loads(out.stdout)["command"] == "storage_analyzer"


def test_envelope_keeps_existing_warnings():
    from _common import with_envelope

    wrapped = with_envelope({"warnings": [{"code": "deprecated"}], "summary": {}})
    assert wrapped["warnings"] == [{"code": "deprecated"}]
    assert list(wrapped) == ["schema_version", "command", "generated_at", "warnings", "summary"]


class TestEnvelopeRendering:
    """The envelope must lead in Markdown and survive in CSV, with or without other content."""

    @pytest.mark.parametrize("warnings", [[], [{"code": "deprecated", "message": "use --format"}]])
    def test_markdown_envelope_comes_first(self, warnings):
        from _common import with_envelope

        result = with_envelope({"warnings": warnings, "output_dir": "/x", "exported": 3, "items": [{"a": 1}]})
        md = render_markdown(result, "smart_export")
        order = [md.index(marker) for marker in ("**schema_version**", "**command**", "**generated_at**", "warnings")]
        assert order == sorted(order)
        assert max(order) < md.index("**output_dir**") < md.index("## items")

    def test_csv_keeps_the_envelope_even_without_rows(self):
        from _common import with_envelope

        rows = list(csv.DictReader(io.StringIO(render_csv(with_envelope({"summary": {"count": 0}})), newline="")))
        assert len(rows) == 1
        assert rows[0]["section"] == "envelope"
        assert rows[0]["schema_version"] == "1" and rows[0]["generated_at"]

    def test_csv_warnings_are_rows(self):
        from _common import with_envelope

        result = with_envelope({"warnings": [{"code": "deprecated", "message": "m"}]})
        rows = list(csv.DictReader(io.StringIO(render_csv(result), newline="")))
        assert [r["section"] for r in rows] == ["envelope", "warnings"]
        assert rows[1]["code"] == "deprecated"
