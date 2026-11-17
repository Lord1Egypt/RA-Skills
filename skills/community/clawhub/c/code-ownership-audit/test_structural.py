import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent / "audit.py"

# structurally identical, every local name changed — the case literal comparison misses
REF_RENAMED = '''def compute(rows):
    total = tally(rows)
    scaled = total * 3
    shifted = scaled - 1
    return shifted
'''

OURS_RENAMED = '''def compute(rows):
    acc = tally(rows)
    boosted = acc * 3
    adjusted = boosted - 1
    return adjusted
'''

# genuinely different algorithm, same public name
OURS_REWRITTEN = '''def compute(rows):
    return sum(r for r in rows if r) * 3 - 1
'''


def _run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, timeout=180)


def _pair(tmp_path, ref_src, our_src, name="m.py"):
    ref = tmp_path / "ref"
    ours = tmp_path / "ours"
    ref.mkdir()
    ours.mkdir()
    (ref / name).write_text(ref_src)
    (ours / name).write_text(our_src)
    return ref, ours


def test_detects_structural_copy_behind_renamed_locals(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    # why: renaming locals defeats literal comparison entirely — this is the gap
    #      every cheap "code similarity" tool has
    assert payload["verdict"] == "derivative"
    assert payload["structural"]["max_run"] >= 3


def test_literal_run_stays_zero_for_renamed_copy(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    # why: proves the structural check is what caught it, not the literal one
    assert payload["literal"]["max_run"] < 3


def test_genuine_rewrite_passes_both_checks(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_REWRITTEN)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert payload["verdict"] == "original"
    assert payload["structural"]["max_run"] < 3
    assert payload["literal"]["max_run"] < 3


def test_structural_findings_report_shapes_not_raw_lines(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    f = payload["structural"]["findings"][0]
    assert f["path"] == "m.py"
    assert f["run"] >= 3
    # why: the report must show the normalised shape, so a reader can see *why*
    #      two differently-named snippets are the same code
    assert f["shapes"]
    shapes = [item["shape"] for item in f["shapes"]]
    assert any("Assign" in s or "Call" in s for s in shapes)
    # why: the paid tier promises real code locations, so every shape must carry
    #      the line it came from
    assert all(isinstance(item["line"], int) and item["line"] > 0
               for item in f["shapes"])


def test_preview_tier_withholds_locations_and_fixes(tmp_path):
    """Free tier must show counts but never locations or fix advice."""
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    prev = json.loads(_run(str(ours), "--reference", str(ref),
                           "--tier", "preview", "--json").stdout)
    assert prev["tier"] == "preview"
    assert prev["total_findings"] >= 1
    assert set(prev["by_level"]) == {"high", "medium", "low"}
    assert prev["by_type"]["structural"] >= 1
    # why: paying customers buy the detail — the preview must not leak it
    blob = json.dumps(prev, ensure_ascii=False)
    assert "fix" not in blob
    for item in prev["items"]:
        assert set(item) == {"level", "kind", "summary"}
        assert "line" not in item


def test_full_tier_carries_levels_and_fixes(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    full = json.loads(_run(str(ours), "--reference", str(ref),
                           "--tier", "full", "--json").stdout)
    f = full["structural"]["findings"][0]
    assert f["level"] in {"high", "medium", "low"}
    assert f["kind"] == "structural"
    assert f["fix"]
    assert full["summary"]["total"] >= 1


def test_threshold_can_be_tightened(tmp_path):
    # two structurally identical statements are enough to trigger at threshold 1
    close = "def compute(rows):\n    a = tally(rows)\n    b = a * 3\n    return b\n"
    ref, ours = _pair(tmp_path, REF_RENAMED, close)
    strict = json.loads(_run(str(ours), "--reference", str(ref),
                             "--threshold", "1", "--json").stdout)
    assert strict["threshold"] == 1
    assert strict["verdict"] == "derivative"


def test_threshold_cannot_be_loosened_below_evidence_floor(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    out = _run(str(ours), "--reference", str(ref), "--threshold", "99", "--json")
    # why: a caller could otherwise set the bar high enough to declare anything
    #      original — the tool would become a rubber stamp
    assert out.returncode != 0
    assert "floor" in (out.stdout + out.stderr).lower()


def test_evidence_report_is_self_contained(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    ev = payload["evidence"]
    # why: a paid report has to be archivable — reproducible months later
    assert ev["tool_version"]
    assert ev["generated_at"]
    assert ev["target_digest"]
    assert ev["reference_digest"]
    assert ev["threshold_basis"]


def test_digests_change_when_sources_change(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    first = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    (ours / "m.py").write_text(OURS_REWRITTEN)
    second = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert first["evidence"]["target_digest"] != second["evidence"]["target_digest"]
    assert first["evidence"]["reference_digest"] == second["evidence"]["reference_digest"]


def test_threshold_basis_cites_measured_population(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_REWRITTEN)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    basis = payload["evidence"]["threshold_basis"]
    # why: "3 lines" must be traceable to real measurement, not an opinion
    assert "363" in basis
    assert "P90" in basis or "p90" in basis


def test_markdown_report_written_to_file(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    dest = tmp_path / "report.md"
    out = _run(str(ours), "--reference", str(ref), "--report", str(dest))
    assert out.returncode == 0
    text = dest.read_text()
    assert "# " in text
    assert "derivative" in text
    assert "m.py" in text


def test_markdown_report_records_digests(tmp_path):
    ref, ours = _pair(tmp_path, REF_RENAMED, OURS_RENAMED)
    dest = tmp_path / "report.md"
    _run(str(ours), "--reference", str(ref), "--report", str(dest))
    text = dest.read_text()
    assert "sha256" in text.lower()


def test_structural_ignores_pure_signature_sequences(tmp_path):
    body = ("def a(x):\n    return x\n\n\n"
            "def b(y):\n    return y\n\n\n"
            "def c(z):\n    return z\n")
    ref, ours = _pair(tmp_path, body, body)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert payload["structural"]["max_run"] < 3


def test_normalisation_keeps_call_targets(tmp_path):
    # calling a different function is a real difference, not just a renamed local
    ours = "def compute(rows):\n    a = other(rows)\n    b = a * 3\n    c = b - 1\n    return c\n"
    ref, our_dir = _pair(tmp_path, REF_RENAMED, ours)
    payload = json.loads(_run(str(our_dir), "--reference", str(ref), "--json").stdout)
    assert payload["structural"]["max_run"] < 4


def test_cleanroom_dataclass_interface_is_not_false_positive(tmp_path):
    # upstream and clean-room keep the same public dataclass schema but differ in
    # method bodies. The structural layer must NOT flag the shared schema fields
    # as "copied shape" — that is the false positive reported in 众测 (review Aime).
    UP = '''from dataclasses import dataclass

@dataclass
class Bucket:
    label: str
    count: int = 0
    total: float = 0.0

    def add(self, n):
        self.count += n
        self.total += n
'''
    RE = '''from dataclasses import dataclass

@dataclass
class Bucket:
    label: str
    count: int = 0
    total: float = 0.0

    def add(self, amount):
        self.count = self.count + amount
        self.total = self.total + float(amount)
'''
    ref, ours = _pair(tmp_path, UP, RE)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert payload["verdict"] == "original"
    assert payload["structural"]["max_run"] < 3


def test_init_field_binding_is_not_false_positive(tmp_path):
    # constructor field bindings (`self.x = x`) are interface-mandated, like the
    # dataclass case above — the structural layer must skip them too
    UP = '''class Bucket:
    def __init__(self, label, count, total):
        self.label = label
        self.count = count
        self.total = total
'''
    RE = '''class Bucket:
    def __init__(self, name, n, t):
        self.label = name
        self.count = n
        self.total = t
'''
    ref, ours = _pair(tmp_path, UP, RE)
    payload = json.loads(_run(str(ours), "--reference", str(ref), "--json").stdout)
    assert payload["verdict"] == "original"
    assert payload["structural"]["max_run"] < 3
