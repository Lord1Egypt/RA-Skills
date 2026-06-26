import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from retention_scorer import ScoredEntry, classify, score_entry, score_file


def test_recent_correction_scores_high() -> None:
    score = score_entry(
        entry_date=date(2026, 3, 10),
        category="Correction",
        takeaway="Omar said X",
        today=date(2026, 3, 15),
        category_counts={"Correction": 1},
    )
    assert score >= 5  # recent (+3) + correction (+2)
    assert classify(score) == "keep"


def test_old_unreferenced_entry_gets_archived_or_deleted() -> None:
    score = score_entry(
        entry_date=date(2025, 11, 1),
        category="Testing",
        takeaway="some old test tip",
        today=date(2026, 3, 15),
        category_counts={"Testing": 1},
    )
    assert score < 2
    action = classify(score)
    assert action in ("archive", "delete")


def test_env_entry_with_recurrence_keeps() -> None:
    score = score_entry(
        entry_date=date(2026, 2, 20),
        category="Env",
        takeaway="use python3 not python",
        today=date(2026, 3, 15),
        category_counts={"Env": 3},
        active_categories={"Env"},
    )
    assert score >= 2
    assert classify(score) == "keep"


def test_score_file_with_sample(tmp_path: Path) -> None:
    learnings = tmp_path / "LEARNINGS.md"
    learnings.write_text(
        "# LEARNINGS\n"
        "- [2026-03-10] [Correction]: Omar said use python3\n"
        "- [2025-06-01] [Testing]: old stale entry\n"
        "- [2026-03-14] [Git]: use short-lived branches\n"
    )
    scored = score_file(learnings, today=date(2026, 3, 15))
    assert len(scored) == 3
    actions = {e.category: e.action for e in scored}
    assert actions["Correction"] == "keep"
    assert actions["Testing"] in ("archive", "delete")


def test_classify_boundaries() -> None:
    assert classify(10) == "keep"
    assert classify(2) == "keep"
    assert classify(1) == "archive"
    assert classify(0) == "archive"
    assert classify(-1) == "delete"
    assert classify(-5) == "delete"
