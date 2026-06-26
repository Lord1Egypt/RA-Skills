from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "workspace_manager.py"
SPEC = spec_from_file_location("workspace_manager", MODULE_PATH)
workspace_manager = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(workspace_manager)


def test_find_current_workspace_returns_active_segment_for_date():
    data = {
        "segments": [
            {"from": "2026-05-19", "to": "2026-05-21", "workspace": "丽金智地中心 B座"},
            {"from": "2026-05-22", "to": "2026-05-25", "workspace": "紫金数码园4号楼"},
        ],
        "next_week": None,
    }

    resolved = workspace_manager.find_current_workspace(data, "2026-05-20")

    assert resolved == "丽金智地中心 B座"


def test_resolve_workspace_for_date_uses_next_week_only_for_matching_week():
    data = {
        "segments": [],
        "next_week": {
            "week_start": "2026-05-25",
            "workspace": "紫金数码园4号楼",
        },
    }

    current_week = workspace_manager.resolve_workspace_for_date(data, "2026-05-20")
    next_week = workspace_manager.resolve_workspace_for_date(data, "2026-05-26")

    assert current_week is None
    assert next_week == "紫金数码园4号楼"


def test_merge_segment_trims_overlapping_ranges():
    data = {
        "segments": [
            {"from": "2026-05-19", "to": "2026-05-25", "workspace": "丽金智地中心 B座"},
        ],
        "next_week": None,
    }

    merged = workspace_manager.merge_segment(data, "紫金数码园4号楼", "2026-05-21", "2026-05-22")

    assert merged["segments"] == [
        {"from": "2026-05-19", "to": "2026-05-20", "workspace": "丽金智地中心 B座"},
        {
            "from": "2026-05-21",
            "to": "2026-05-22",
            "workspace": "紫金数码园4号楼",
            "set_at": merged["segments"][1]["set_at"],
            "set_by": "manual",
        },
        {"from": "2026-05-23", "to": "2026-05-25", "workspace": "丽金智地中心 B座"},
    ]


def test_recommend_workspace_uses_recent_selection_history():
    preferences = {
        "preferences": {
            "ou_a": {
                "selection_history": [
                    {"building": "丽金智地中心 B座"},
                    {"building": "丽金智地中心 B座"},
                    {"building": "紫金数码园4号楼"},
                ]
            },
            "ou_b": {
                "selection_history": [
                    {"building": "丽金智地中心 B座"},
                ]
            },
        }
    }

    recommendation, ranking = workspace_manager.recommend_workspace(preferences)

    assert recommendation == "丽金智地中心 B座"
    assert ranking[0] == ("丽金智地中心 B座", 3)
