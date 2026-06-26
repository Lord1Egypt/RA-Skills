"""End-to-end tests for scripts/score-calendar-event.py.

Cases drawn from the worked-examples table in
references/event-suitability.md. The script is deterministic + side-
effect-free, so these double as a contract test against the rubric.
"""
import json, pathlib, subprocess

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCORE_SCRIPT = REPO_ROOT / "scripts" / "score-calendar-event.py"


def score(event: dict) -> dict:
    r = subprocess.run(
        ["python3", str(SCORE_SCRIPT)],
        input=json.dumps(event),
        capture_output=True, text=True,
        timeout=10,
    )
    assert r.returncode == 0, f"scorer failed: {r.stderr}"
    return json.loads(r.stdout)


def test_wedding_smart_casual_travel_multi_day_premium():
    """Sonoma wedding, smart casual, 3 days, travel: 4+3+1+1+0 = 9 → premium."""
    out = score({
        "title":          "Sarah & Tom wedding",
        "description":    "smart casual",
        "duration_days":  3,
        "is_travel":      True,
        "event_location": "Sonoma",
        "home_metro":     "SF",
    })
    assert out["score"] == 9
    assert out["action"] == "premium"


def test_medical_appointment_hard_veto():
    """Annual physical → -10 hard veto, regardless of other dimensions."""
    out = score({
        "title":       "Annual physical with Dr. Lee",
        "description": "",
    })
    assert out["score"] == -10
    assert out["action"] == "skip"
    assert "hard-veto" in out["reason"]


def test_therapy_hard_veto():
    """Therapy session → hard veto."""
    out = score({"title": "Therapy with Dr. Jones"})
    assert out["score"] == -10
    assert out["action"] == "skip"


def test_one_on_one_meeting_skip():
    """1:1 with Jamie → 0, skip."""
    out = score({"title": "1:1 with Jamie", "description": ""})
    assert out["score"] == 0
    assert out["action"] == "skip"


def test_focus_block_skip():
    """Focus / TODO blocks should not trigger lookbooks."""
    out = score({"title": "Block: focus", "description": ""})
    assert out["score"] == 0
    assert out["action"] == "skip"


def test_paris_vacation_editorial():
    """Multi-day travel with no explicit dress code: 3+2+1+1+0 = 7 → editorial."""
    out = score({
        "title":          "Paris vacation",
        "description":    "",
        "duration_days":  6,
        "is_travel":      True,
        "event_location": "Paris",
        "home_metro":     "SF",
    })
    assert out["score"] == 7
    assert out["action"] == "editorial"


def test_friday_dinner_smart_casual_below_threshold():
    """Friday dinner — Bestia, smart casual, 0 days, local: 2+3+0+0+0 = 5 → skip."""
    out = score({
        "title":         "Friday dinner — Bestia",
        "description":   "smart casual",
        "duration_days": 0,
    })
    assert out["score"] == 5
    assert out["action"] == "skip"


def test_concert_local_below_threshold():
    """Concert at local venue: 2+2+0+0+0 = 4 → skip."""
    out = score({
        "title":       "Tycho · Greek Theater",
        "description": "rooftop",
    })
    assert out["score"] <= 5
    assert out["action"] == "skip"


def test_customer_opt_in_pushes_borderline_to_soft():
    """A score-3 event becomes 5 with +2 customer signal — still skip on score 5."""
    out = score({
        "title": "Coffee with Pat",
        "customer_opt_in_for_this_event": True,
    })
    # Coffee/meeting weight 0 + signal 2 = 2 → skip
    assert out["action"] == "skip"


def test_returned_breakdown_includes_all_dimensions():
    """Schema check: every result has the 5 weight dimensions."""
    out = score({"title": "Sarah's wedding", "duration_days": 2, "is_travel": True})
    breakdown = out["breakdown"]
    for k in ("type", "dress_code", "duration", "location", "signal"):
        assert k in breakdown


def test_empty_input_scores_zero():
    """Empty event → 0 → skip (don't crash, don't auto-fire)."""
    r = subprocess.run(
        ["python3", str(SCORE_SCRIPT)],
        input="",
        capture_output=True, text=True,
        timeout=10,
    )
    assert r.returncode == 0
    out = json.loads(r.stdout)
    assert out["score"] == 0
    assert out["action"] == "skip"
