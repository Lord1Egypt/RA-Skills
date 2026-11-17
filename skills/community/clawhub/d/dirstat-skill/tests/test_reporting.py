from pathlib import Path

import pytest

from dirstat_skill.models import AnalysisFinding, NormalizedNode
from dirstat_skill.reporting import (
    _find_nearby_references,
    build_analysis_findings,
    build_top_lists,
    render_review_report,
    select_dominant_candidates,
)


def test_build_top_lists_filters_by_threshold_and_type() -> None:
    nodes = [
        NormalizedNode(path="/sample", name="sample", is_dir=True, asize=0, dsize=4096),
        NormalizedNode(path="/sample/cache", name="cache", is_dir=True, asize=0, dsize=8000),
        NormalizedNode(
            path="/sample/cache/huge.log",
            name="huge.log",
            is_dir=False,
            asize=0,
            dsize=3000,
        ),
        NormalizedNode(
            path="/sample/media.iso",
            name="media.iso",
            is_dir=False,
            asize=0,
            dsize=9000,
        ),
    ]

    report = build_top_lists(nodes=nodes, min_bytes=5000, top_n=5)

    assert [item.path for item in report.top_dirs] == ["/sample/cache"]
    assert [item.path for item in report.top_files] == ["/sample/media.iso"]


def test_select_dominant_nodes_walks_recursively_until_concrete_candidates() -> None:
    nodes = [
        NormalizedNode(path="/root", name="root", is_dir=True, asize=0, dsize=1000),
        NormalizedNode(path="/root/a", name="a", is_dir=True, asize=0, dsize=850),
        NormalizedNode(path="/root/b", name="b", is_dir=True, asize=0, dsize=150),
        NormalizedNode(path="/root/a/f1.bin", name="f1.bin", is_dir=False, asize=0, dsize=500),
        NormalizedNode(path="/root/a/f2.bin", name="f2.bin", is_dir=False, asize=0, dsize=350),
    ]

    selected = select_dominant_candidates(
        nodes=nodes,
        root_path="/root",
        dominant_percent=0.8,
        min_candidate_bytes=100,
    )

    assert [item.path for item in selected] == ["/root/a/f1.bin", "/root/a/f2.bin"]


def test_select_dominant_candidates_keeps_flat_directory_when_no_clear_winner() -> None:
    nodes = [
        NormalizedNode(path="/root", name="root", is_dir=True, asize=0, dsize=900),
        NormalizedNode(path="/root/a", name="a", is_dir=True, asize=0, dsize=300),
        NormalizedNode(path="/root/b", name="b", is_dir=True, asize=0, dsize=300),
        NormalizedNode(path="/root/c", name="c", is_dir=True, asize=0, dsize=300),
    ]

    selected = select_dominant_candidates(
        nodes=nodes,
        root_path="/root",
        dominant_percent=0.8,
        min_candidate_bytes=100,
    )

    assert [item.path for item in selected] == ["/root"]


def test_select_dominant_candidates_keeps_many_medium_files_that_dominate_together() -> None:
    nodes = [
        NormalizedNode(path="/root", name="root", is_dir=True, asize=0, dsize=1000),
        NormalizedNode(path="/root/cache", name="cache", is_dir=True, asize=0, dsize=900),
        NormalizedNode(path="/root/other", name="other", is_dir=True, asize=0, dsize=100),
        NormalizedNode(path="/root/cache/a.bin", name="a.bin", is_dir=False, asize=0, dsize=300),
        NormalizedNode(path="/root/cache/b.bin", name="b.bin", is_dir=False, asize=0, dsize=300),
        NormalizedNode(path="/root/cache/c.bin", name="c.bin", is_dir=False, asize=0, dsize=200),
        NormalizedNode(path="/root/cache/d.bin", name="d.bin", is_dir=False, asize=0, dsize=100),
    ]

    selected = select_dominant_candidates(
        nodes=nodes,
        root_path="/root",
        dominant_percent=0.8,
        min_candidate_bytes=100,
    )

    assert [item.path for item in selected] == [
        "/root/cache/a.bin",
        "/root/cache/b.bin",
        "/root/cache/c.bin",
    ]


def test_select_dominant_candidates_for_roots_preserves_single_posix_root_tree() -> None:
    nodes = [
        NormalizedNode(path="/", name="/", is_dir=True, asize=0, dsize=1000),
        NormalizedNode(path="/home", name="home", is_dir=True, asize=0, dsize=900),
        NormalizedNode(path="/var", name="var", is_dir=True, asize=0, dsize=100),
        NormalizedNode(path="/home/model.gguf", name="model.gguf", is_dir=False, asize=0, dsize=900),
    ]

    selected = select_dominant_candidates(
        nodes=nodes,
        root_path="/",
        dominant_percent=0.8,
        min_candidate_bytes=100,
    )

    assert [item.path for item in selected] == ["/home/model.gguf"]


def test_build_analysis_findings_emits_analysis_kind_and_evidence(tmp_path: Path) -> None:
    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir()
    blob_path = cache_dir / "blob.bin"
    blob_path.write_bytes(b"x" * 8)

    nodes = [
        NormalizedNode(path=str(blob_path), name="blob.bin", is_dir=False, asize=0, dsize=2000),
    ]

    findings = build_analysis_findings(
        selected_nodes=nodes,
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=["/data"],
        nearby_reference_extensions=[".json", ".yaml"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
        min_candidate_bytes=1024,
    )

    assert findings[0].review_reason
    assert findings[0].analysis_kind == "signature heuristics"
    assert "cache" in findings[0].evidence.lower()
    assert findings[0].attention_level == "review first"
    assert findings[0].configured_dominant_percent == 0.8


def test_build_analysis_findings_marks_huggingface_cache_as_signature_heuristic(
    tmp_path: Path,
) -> None:
    cache_dir = tmp_path / "huggingface_cache" / "models--wan"
    cache_dir.mkdir(parents=True)
    blob_path = cache_dir / "blob.bin"
    blob_path.write_bytes(b"x" * 8)

    nodes = [
        NormalizedNode(path=str(cache_dir), name=cache_dir.name, is_dir=True, asize=0, dsize=2000),
        NormalizedNode(path=str(blob_path), name="blob.bin", is_dir=False, asize=0, dsize=1500),
    ]

    findings = build_analysis_findings(
        selected_nodes=[nodes[0]],
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=[str(tmp_path)],
        nearby_reference_extensions=[".json", ".yaml"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
        min_candidate_bytes=1024,
    )

    assert findings[0].analysis_kind == "signature heuristics"
    assert findings[0].attention_level == "review first"
    assert "cache" in findings[0].evidence.lower()


def test_build_analysis_findings_marks_trash_path_as_signature_heuristic(
    tmp_path: Path,
) -> None:
    trash_dir = tmp_path / "games" / "trash" / "backup"
    trash_dir.mkdir(parents=True)

    nodes = [
        NormalizedNode(path=str(trash_dir), name=trash_dir.name, is_dir=True, asize=0, dsize=2000),
    ]

    findings = build_analysis_findings(
        selected_nodes=nodes,
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=[str(tmp_path)],
        nearby_reference_extensions=[".json", ".yaml"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
        min_candidate_bytes=1024,
    )

    assert findings[0].analysis_kind == "signature heuristics"
    assert findings[0].attention_level == "review first"
    assert "trash" in findings[0].review_reason.lower()


def test_build_analysis_findings_marks_system_storage_as_path_safety() -> None:
    nodes = [
        NormalizedNode(path="/var/lib/docker-loop.xfs", name="docker-loop.xfs", is_dir=False, asize=0, dsize=2000),
    ]

    findings = build_analysis_findings(
        selected_nodes=nodes,
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=["/home"],
        nearby_reference_extensions=[".json", ".yaml"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
        min_candidate_bytes=1024,
    )

    assert findings[0].analysis_kind == "path safety"
    assert findings[0].attention_level == "keep protected"
    assert "protected" in findings[0].evidence.lower()


def test_build_analysis_findings_marks_user_model_as_dominant_space(
    tmp_path: Path,
) -> None:
    # A user-owned model on a normal (non cache/temp/trash) path must be
    # surfaced as dominant space, independent of the host temporary dir.
    nodes = [
        NormalizedNode(path="/data/models/model.gguf", name="model.gguf", is_dir=False, asize=0, dsize=2000),
    ]

    findings = build_analysis_findings(
        selected_nodes=nodes,
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=[str(tmp_path)],
        nearby_reference_extensions=[".json", ".yaml"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
        min_candidate_bytes=1024,
    )

    assert findings[0].analysis_kind == "dominant space"
    assert findings[0].attention_level == "review carefully"
    assert "dominant-space walk" in findings[0].evidence.lower()


def test_build_analysis_findings_surfaces_probable_duplicates(tmp_path: Path) -> None:
    a_dir = tmp_path / "a"
    b_dir = tmp_path / "b"
    a_dir.mkdir()
    b_dir.mkdir()
    first = a_dir / "model.safetensors"
    second = b_dir / "model.safetensors"
    first.write_bytes(b"x")
    second.write_bytes(b"y")

    nodes = [
        NormalizedNode(path=str(first), name="model.safetensors", is_dir=False, asize=0, dsize=2000),
        NormalizedNode(path=str(second), name="model.safetensors", is_dir=False, asize=0, dsize=2000),
    ]

    findings = build_analysis_findings(
        selected_nodes=[],
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=[str(tmp_path)],
        nearby_reference_extensions=[".json"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
        min_candidate_bytes=1024,
    )

    duplicate_findings = [item for item in findings if item.analysis_kind == "probable duplicates"]
    assert len(duplicate_findings) == 2
    assert duplicate_findings[0].group_key


def test_build_analysis_findings_surfaces_protected_huge_hotspot() -> None:
    nodes = [
        NormalizedNode(path="/var/lib/docker-loop.xfs", name="docker-loop.xfs", is_dir=False, asize=0, dsize=2000),
    ]

    findings = build_analysis_findings(
        selected_nodes=[],
        all_nodes=nodes,
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=["/home"],
        nearby_reference_extensions=[".json"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
        min_candidate_bytes=1024,
    )

    hotspot_findings = [item for item in findings if item.analysis_kind == "protected huge hotspots"]
    assert len(hotspot_findings) == 1
    assert hotspot_findings[0].attention_level == "keep protected"


def test_render_review_report_shows_analysis_sections(tmp_path: Path) -> None:
    findings = [
        AnalysisFinding(
            path="/var/lib/docker-loop.xfs",
            dsize=2000,
            is_dir=False,
            analysis_kind="protected huge hotspots",
            attention_level="keep protected",
            review_reason="protected runtime area dominates space",
            evidence="matched protected prefix `/var/lib` with `2.0 KB`",
            dependency_check_confidence="high",
            selection_source="protected_hotspot",
            group_key="hotspot:/var/lib",
            configured_dominant_percent=0.8,
        )
    ]

    report = render_review_report("/", findings)

    assert "# Review Report" in report
    assert "## Protected Huge Hotspots" in report
    assert "configured_dominant_percent" in report


def test_render_review_report_includes_dominant_space_findings(tmp_path: Path) -> None:
    model_path = tmp_path / "model.gguf"
    model_path.write_bytes(b"x")
    findings = build_analysis_findings(
        selected_nodes=[
            NormalizedNode(path=str(model_path), name="model.gguf", is_dir=False, asize=0, dsize=2000)
        ],
        all_nodes=[
            NormalizedNode(path=str(model_path), name="model.gguf", is_dir=False, asize=0, dsize=2000)
        ],
        protected_prefixes=["/etc", "/usr", "/var/lib"],
        inspection_prefixes=[str(tmp_path)],
        nearby_reference_extensions=[".json"],
        max_nearby_reference_files=5,
        dominant_percent=0.8,
        min_candidate_bytes=1024,
    )

    report = render_review_report(root_path=str(tmp_path), findings=findings)

    assert "# Review Report" in report
    assert "## Dominant Space" in report
    assert str(model_path) in report


def test_find_nearby_references_ignores_untrusted_mount_on_path_probe(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    candidate = Path(r"C:\Users\giova\AppData\Local\Sandfall")
    original_exists = Path.exists

    def fake_exists(self: Path) -> bool:
        if self == candidate:
            raise OSError("[WinError 448] untrusted mount point")
        return original_exists(self)

    monkeypatch.setattr(Path, "exists", fake_exists)

    assert _find_nearby_references(str(candidate), [".json"], 5) == []


def test_find_nearby_references_ignores_untrusted_mount_during_entry_probe(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    target = tmp_path / "weights.gguf"
    target.write_bytes(b"x")
    ref_dir = tmp_path / "refs"
    ref_dir.mkdir()

    class FakeEntry:
        name = "bad-mount.json"
        suffix = ".json"

        def is_file(self) -> bool:
            raise OSError("[WinError 448] untrusted mount point")

        def read_text(self, encoding: str = "utf-8", errors: str = "ignore") -> str:
            return "weights.gguf"

    original_iterdir = Path.iterdir

    def fake_iterdir(self: Path):
        if self == tmp_path:
            return iter([FakeEntry()])
        return original_iterdir(self)

    monkeypatch.setattr(Path, "iterdir", fake_iterdir)

    assert _find_nearby_references(str(target), [".json"], 5) == []

