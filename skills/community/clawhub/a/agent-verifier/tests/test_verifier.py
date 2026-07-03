"""Tests for agent-verifier."""
import json
import tempfile
from pathlib import Path

import pytest

from agent_verifier import Verifier


@pytest.fixture
def redlist_path(tmp_path):
    p = tmp_path / "redlist.txt"
    p.write_text(
        "ProjectAtlas\n"
        "ClientA-Holdings\n"
        "regex:£\\d{2,3}[Kk]\\b\n"
    )
    return p


def test_pass_when_clean_and_no_llm():
    v = Verifier(weekend_block_days=())  # no LLM, no redlist, no weekend
    r = v.verify(
        subject="hello",
        body="this is a clean draft",
        recipient="someone@example.com",
    )
    assert r.verdict == "PASS"
    assert r.can_send is True


def test_redlist_blocks(redlist_path):
    v = Verifier(redlist_path=redlist_path, weekend_block_days=())
    r = v.verify(
        subject="ProjectAtlas update",
        body="hi there",
        recipient="ceo@example.com",
    )
    assert r.verdict == "BLOCK"
    assert r.can_send is False
    assert any(c.axis == "redlist" and c.severity == "BLOCK" for c in r.checks)


def test_redlist_recipient_match_allows(redlist_path):
    """Term in body but recipient is the related party — should not block."""
    v = Verifier(redlist_path=redlist_path, weekend_block_days=())
    r = v.verify(
        subject="ClientA-Holdings update",
        body="hi there",
        recipient="ops@clienta-holdings.com",
    )
    assert any(c.axis == "redlist" and c.severity == "PASS" for c in r.checks)


def test_redlist_regex_match(redlist_path):
    v = Verifier(redlist_path=redlist_path, weekend_block_days=())
    r = v.verify(
        subject="re: the £500K pilot",
        body="all good",
        recipient="someone@example.com",
    )
    assert r.verdict == "BLOCK"


def test_weekend_block_when_today_is_weekend():
    """We can't time-travel, so just assert the calendar axis exists."""
    v = Verifier(weekend_block_days=("Monday", "Tuesday", "Wednesday",
                                     "Thursday", "Friday", "Saturday", "Sunday"))
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert any(c.axis == "calendar" and c.severity == "BLOCK" for c in r.checks)


def test_weekend_disabled():
    v = Verifier(weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert any(c.axis == "calendar" and c.severity == "PASS" for c in r.checks)


def test_llm_pass():
    fake_llm = lambda _prompt: json.dumps({
        "atomic_claims": [
            {"claim": "we ship X", "status": "verified", "reason": "stated in draft"},
        ],
        "confidential": {"severity": "PASS", "reason": "clean"},
        "clarity": {"severity": "PASS", "reason": "clear ask"},
        "could_not_verify": "",
        "needs_from_user": "",
    })
    v = Verifier(llm=fake_llm, weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert r.verdict == "PASS"
    assert len(r.claims) == 1
    assert r.claims[0].status == "verified"


def test_llm_block_propagates():
    fake_llm = lambda _prompt: json.dumps({
        "atomic_claims": [],
        "confidential": {"severity": "BLOCK", "reason": "leaked client name"},
        "clarity": {"severity": "PASS", "reason": "ok"},
    })
    v = Verifier(llm=fake_llm, weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert r.verdict == "BLOCK"
    assert r.can_send is False


def test_failed_atomic_claim_blocks():
    """v0.2 — any failed claim escalates the LLM axis to BLOCK."""
    fake_llm = lambda _prompt: json.dumps({
        "atomic_claims": [
            {"claim": "Anthropic shipped Opus 9", "status": "failed",
             "reason": "no such model exists"},
            {"claim": "we offer a 15-min call", "status": "verified",
             "reason": "stated in draft"},
        ],
        "confidential": {"severity": "PASS", "reason": "ok"},
        "clarity": {"severity": "PASS", "reason": "ok"},
    })
    v = Verifier(llm=fake_llm, weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert r.verdict == "BLOCK"
    assert any(c.status == "failed" for c in r.claims)


def test_unverifiable_atomic_claim_warns():
    """v0.2 — unverifiable claims escalate PASS to WARN, never to BLOCK alone."""
    fake_llm = lambda _prompt: json.dumps({
        "atomic_claims": [
            {"claim": "we helped 3 LAs", "status": "unverifiable",
             "reason": "no public evidence in the draft"},
        ],
        "confidential": {"severity": "PASS", "reason": "ok"},
        "clarity": {"severity": "PASS", "reason": "ok"},
    })
    v = Verifier(llm=fake_llm, weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert r.verdict == "WARN"


def test_flywheel_fields_threaded_through():
    """v0.2 — could_not_verify + needs_from_user surface in the result."""
    fake_llm = lambda _prompt: json.dumps({
        "atomic_claims": [],
        "confidential": {"severity": "PASS", "reason": "ok"},
        "clarity": {"severity": "PASS", "reason": "ok"},
        "could_not_verify": "Whether this council has actually published an AI strategy.",
        "needs_from_user": "Add a CRM hook so the verifier can look up prior contact.",
    })
    v = Verifier(llm=fake_llm, weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert "council" in r.could_not_verify
    assert "CRM" in r.needs_from_user
    d = r.to_dict()
    assert d["could_not_verify"] == r.could_not_verify
    assert d["needs_from_user"] == r.needs_from_user
    assert d["claims"]["total"] == 0


def test_legacy_v0_1_payload_handled_gracefully():
    """v0.1 callers may have shipped without atomic_claims — we degrade quietly."""
    fake_llm = lambda _prompt: json.dumps({
        "confidential": {"severity": "PASS", "reason": "ok"},
        "clarity": {"severity": "PASS", "reason": "ok"},
        # no atomic_claims, no flywheel fields
    })
    v = Verifier(llm=fake_llm, weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert r.verdict == "PASS"
    assert r.claims == []
    assert r.could_not_verify == ""
    assert r.needs_from_user == ""


def test_llm_non_json_defaults_to_warn():
    fake_llm = lambda _prompt: "I'm sorry, I can't help with that"
    v = Verifier(llm=fake_llm, weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert r.verdict == "WARN"  # llm axis defaults to WARN, no BLOCK present


def test_llm_exception_defaults_to_warn():
    def boom(_prompt):
        raise RuntimeError("rate limited")
    v = Verifier(llm=boom, weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    assert r.verdict == "WARN"


def test_style_check_warns():
    style = lambda text: ["americanism: 'organize'"] if "organize" in text else []
    v = Verifier(style_check=style, weekend_block_days=())
    r = v.verify(subject="organize a call", body="ok", recipient="x@y.com")
    assert r.verdict == "WARN"


def test_to_dict_serialisable():
    v = Verifier(weekend_block_days=())
    r = v.verify(subject="hi", body="ok", recipient="x@y.com")
    d = r.to_dict()
    assert json.dumps(d)  # round-trips
    assert d["verdict"] in ("PASS", "WARN", "BLOCK")
    assert isinstance(d["checks"], list)
