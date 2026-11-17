import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent / "audit.py"

# why: exempt lines (control flow, imports, signatures) break a run, so a
#      fixture must hold several *consecutive* expressive lines to be measurable
DERIVED = '''"""Upstream docstring."""
import os


def scale(values, factor):
    total = compute_base(values)
    scaled = total * factor
    shifted = scaled - offset(values)
    return shifted
'''

ORIGINAL = '''from statistics import fmean


def summarise(rows):
    return fmean(rows) if rows else 0.0
'''


def _run(*args):
    proc = subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, timeout=120)
    return proc


def test_script_exists():
    assert SCRIPT.is_file()


def test_reports_json_for_a_clean_file(tmp_path):
    f = tmp_path / "m.py"
    f.write_text(ORIGINAL)
    out = _run(str(f), "--json")
    assert out.returncode == 0, out.stderr
    payload = json.loads(out.stdout)
    assert payload["files"] == 1
    assert payload["verdict"] in ("original", "unknown")


def test_flags_identical_file_as_derived(tmp_path):
    ref = tmp_path / "ref"
    ours = tmp_path / "ours"
    ref.mkdir()
    ours.mkdir()
    (ref / "m.py").write_text(DERIVED)
    (ours / "m.py").write_text(DERIVED)
    out = _run(str(ours), "--reference", str(ref), "--json")
    payload = json.loads(out.stdout)
    # why: an identical copy is the clearest possible derivative work
    assert payload["verdict"] == "derivative"
    assert payload["literal"]["max_run"] >= 3


def test_recognises_independent_rewrite(tmp_path):
    ref = tmp_path / "ref"
    ours = tmp_path / "ours"
    ref.mkdir()
    ours.mkdir()
    (ref / "m.py").write_text(DERIVED)
    (ours / "m.py").write_text(
        "def scale(values, factor):\n"
        "    return compute_base(values) * factor - offset(values)\n")
    out = _run(str(ours), "--reference", str(ref), "--json")
    payload = json.loads(out.stdout)
    assert payload["verdict"] == "original"
    assert payload["literal"]["max_run"] < 3


def test_counts_exempt_lines_by_reason(tmp_path):
    d = tmp_path / "ours"
    d.mkdir()
    (d / "m.py").write_text(
        "import os\nfrom sys import argv\n\n\n"
        "def run(items):\n    for item in items:\n        emit(item)\n")
    out = _run(str(d), "--reference", str(d), "--json")
    payload = json.loads(out.stdout)
    # why: these lines are identical by necessity — the report must say so rather
    #      than counting them against the caller
    assert payload["exemptions"].get("import") == 2
    assert payload["exemptions"].get("control_flow") == 1


def test_lists_offending_locations(tmp_path):
    ref = tmp_path / "ref"
    ours = tmp_path / "ours"
    ref.mkdir()
    ours.mkdir()
    (ref / "big.py").write_text(DERIVED)
    (ours / "big.py").write_text(DERIVED)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert payload["literal"]["findings"]
    first = payload["literal"]["findings"][0]
    assert first["path"] == "big.py"
    assert first["run"] >= 3
    assert first["lines"]
    # why: the paid tier sells exact locations — each matched line must carry its
    #      source text and a real line number
    for item in first["lines"]:
        assert item["text"].strip()
        assert isinstance(item["line"], int) and item["line"] > 0


def test_byte_identical_file_is_always_derivative(tmp_path):
    ref = tmp_path / "ref"
    ours = tmp_path / "ours"
    ref.mkdir()
    ours.mkdir()
    # a file whose expressive lines are all broken up by signatures
    body = ("def a(x):\n    return x + 1\n\n\n"
            "def b(y):\n    return y * 2\n")
    (ref / "m.py").write_text(body)
    (ours / "m.py").write_text(body)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    # why: the run-length rule alone reports "original" here because every
    #      expressive line stands between two signatures — but a byte-identical
    #      copy is a copy, and saying otherwise misleads the caller
    assert payload["verdict"] == "derivative"
    assert "m.py" in payload["identical_files"]


def test_identical_files_listed_separately(tmp_path):
    ref = tmp_path / "ref"
    ours = tmp_path / "ours"
    ref.mkdir()
    ours.mkdir()
    (ref / "same.py").write_text(ORIGINAL)
    (ref / "diff.py").write_text(ORIGINAL)
    (ours / "same.py").write_text(ORIGINAL)
    (ours / "diff.py").write_text("def other():\n    return 7\n")
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert payload["identical_files"] == ["same.py"]


def test_human_output_is_readable(tmp_path):
    d = tmp_path / "ours"
    d.mkdir()
    (d / "m.py").write_text(ORIGINAL)
    out = _run(str(d))
    assert out.returncode == 0
    assert "verdict" in out.stdout.lower()


def test_missing_path_fails_clearly(tmp_path):
    out = _run(str(tmp_path / "nope"))
    assert out.returncode != 0
    assert "not found" in (out.stdout + out.stderr).lower()


def test_skips_pycache(tmp_path):
    d = tmp_path / "ours"
    (d / "__pycache__").mkdir(parents=True)
    (d / "__pycache__" / "x.py").write_text("V = 1\n")
    (d / "m.py").write_text(ORIGINAL)
    payload = json.loads(_run(str(d), "--json").stdout)
    assert payload["files"] == 1


def test_handles_unparsable_file(tmp_path):
    d = tmp_path / "ours"
    d.mkdir()
    (d / "broken.py").write_text("def f(:\n")
    out = _run(str(d), "--json")
    assert out.returncode == 0
    payload = json.loads(out.stdout)
    # why: a syntax error is the caller's problem to know about, not a crash
    assert payload["unparsable"] == ["broken.py"]


def test_reference_without_match_is_reported(tmp_path):
    ref = tmp_path / "ref"
    ours = tmp_path / "ours"
    ref.mkdir()
    ours.mkdir()
    (ref / "other.py").write_text(ORIGINAL)
    (ours / "m.py").write_text(DERIVED)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert payload["uncompared"] == ["m.py"]


def test_reference_with_no_matching_files_yields_unknown(tmp_path):
    # a --reference was given but matched none of our files (different names /
    # layout) — the result must be unknown, NOT a silent "original" pass
    ref = tmp_path / "ref"
    ours = tmp_path / "ours"
    ref.mkdir()
    ours.mkdir()
    (ref / "other.py").write_text(ORIGINAL)
    (ours / "m.py").write_text(DERIVED)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert payload["compared"] == 0
    assert payload["verdict"] == "unknown"
    assert payload["evidence"]["reference_digest"] != "none"
