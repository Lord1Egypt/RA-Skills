import json
from pathlib import Path

import pytest

from engram_server.loader import EngramLoader
from engram_server.server import build_parser
from engram_server.stats import (
    StatsReport,
    gather_stats,
    render_csv,
    render_json,
    render_plain,
)


def _make_engram(tmp_path: Path, name: str = "test-expert") -> EngramLoader:
    engram_dir = tmp_path / name
    engram_dir.mkdir(exist_ok=True)
    (engram_dir / "meta.json").write_text(
        f'{{"name": "{name}", "description": "test desc",'
        f' "knowledge_count": 0, "examples_count": 0}}',
        encoding="utf-8",
    )
    (engram_dir / "role.md").write_text("# test role", encoding="utf-8")
    return EngramLoader(tmp_path)


def test_gather_stats_empty(tmp_path: Path) -> None:
    loader = EngramLoader(tmp_path)
    report = gather_stats(loader)

    assert report.total_engrams == 0
    assert report.total_memory_entries == 0
    assert report.engram_stats == []
    assert report.recent_entries == []


def test_gather_stats_counts_engrams(tmp_path: Path) -> None:
    _make_engram(tmp_path, "expert-a")
    loader = _make_engram(tmp_path, "expert-b")

    report = gather_stats(loader)

    assert report.total_engrams == 2
    names = {es.name for es in report.engram_stats}
    assert names == {"expert-a", "expert-b"}


def test_gather_stats_with_memory(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    loader.capture_memory(
        "test-expert", "用户偏好晨练", "preferences", "偏好晨练",
        memory_type="preference", tags=["fitness"],
    )
    loader.capture_memory(
        "test-expert", "用户左膝旧伤", "user-profile", "膝关节受限",
        memory_type="fact",
    )

    report = gather_stats(loader)

    assert report.total_memory_entries == 2
    es = report.engram_stats[0]
    assert es.memory_entry_count == 2
    assert es.memory_categories == {"preferences": 1, "user-profile": 1}
    assert es.memory_type_distribution == {"preference": 1, "fact": 1}
    assert len(report.recent_entries) == 2


def test_gather_stats_global_memory(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    loader.capture_memory(
        "test-expert", "用户居住在深圳", "user-profile", "居住地：深圳",
        memory_type="fact", is_global=True,
    )

    report = gather_stats(loader)

    assert report.global_memory.entry_count == 1
    assert report.global_memory.categories == {"user-profile": 1}
    assert any(e.engram_name == "_global" for e in report.recent_entries)


def test_gather_stats_recent_entries_sorted_and_limited(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)

    for i in range(15):
        loader._throttle_cache.clear()
        loader.capture_memory(
            "test-expert", f"内容{i}", "history", f"摘要{i}",
            memory_type="history",
        )

    report = gather_stats(loader)

    assert len(report.recent_entries) == 10
    timestamps = [e.timestamp for e in report.recent_entries]
    assert timestamps == sorted(timestamps, reverse=True)


def test_render_plain_output(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    loader.capture_memory(
        "test-expert", "内容", "preferences", "摘要",
        memory_type="preference",
    )

    report = gather_stats(loader)
    output = render_plain(report)

    assert "Engram Stats" in output
    assert "Total engrams: 1" in output
    assert "Total memory entries: 1" in output
    assert "test-expert" in output
    assert "preference" in output
    assert "Recent Activity" in output


def test_render_plain_empty() -> None:
    report = StatsReport()
    output = render_plain(report)

    assert "Total engrams: 0" in output
    assert "Total memory entries: 0" in output


def test_render_json_output_is_valid_and_complete(tmp_path: Path) -> None:
    loader = _make_engram(tmp_path)
    loader.capture_memory(
        "test-expert",
        "用户偏好晨练",
        "preferences",
        "偏好晨练",
        memory_type="preference",
    )

    report = gather_stats(loader)
    output = render_json(report)
    data = json.loads(output)

    assert "generated_at" in data
    assert "engrams" in data
    assert "global_memory" in data
    assert len(data["engrams"]) == 1
    engram = data["engrams"][0]
    assert {
        "name",
        "knowledge_count",
        "examples_count",
        "memory_count",
        "memory_types",
        "recent_entries",
    }.issubset(engram.keys())


def test_render_csv_row_count_matches_engrams(tmp_path: Path) -> None:
    _make_engram(tmp_path, "expert-a")
    loader = _make_engram(tmp_path, "expert-b")
    report = gather_stats(loader)

    csv_text = render_csv(report)
    lines = [line for line in csv_text.splitlines() if line.strip()]
    assert len(lines) == report.total_engrams + 1


def test_stats_output_flags_are_mutually_exclusive() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["stats", "--json", "--csv"])
