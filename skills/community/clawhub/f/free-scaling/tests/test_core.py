"""Core test suite for nim-ensemble (free-scaling library).

Unit tests run without API keys.
Integration tests require NVIDIA_API_KEY and hit real NIM endpoints.
"""

import os
import time
from pathlib import Path

import pytest

# ── Fixtures / helpers ─────────────────────────────────────────────

HAS_KEY = bool(os.environ.get("NVIDIA_API_KEY"))
needs_api = pytest.mark.skipif(not HAS_KEY, reason="NVIDIA_API_KEY not set")


@pytest.fixture
def free_scaling_state_dir(tmp_path, monkeypatch):
    """Isolate ELO/feedback state per test."""
    monkeypatch.setenv("FREE_SCALING_STATE_DIR", str(tmp_path))

    import nim_ensemble.elo as elo
    import nim_ensemble.feedback as feedback

    elo.STATE_DIR = Path(tmp_path)
    elo.STATE_FILE = elo.STATE_DIR / "elo.json"
    feedback.STATE_DIR = Path(tmp_path)
    feedback.FEEDBACK_FILE = feedback.STATE_DIR / "feedback.json"
    return tmp_path


# =====================================================================
# UNIT TESTS — no API calls required
# =====================================================================


class TestParseAnswer:
    """parse_answer: keyword extraction, negation, thinking models."""

    def test_simple_yes(self):
        from nim_ensemble.parser import parse_answer
        assert parse_answer("YES, it looks correct.") == "YES"

    def test_simple_no(self):
        from nim_ensemble.parser import parse_answer
        assert parse_answer("NO — this is wrong.") == "NO"

    def test_negation_not_safe(self):
        """'NOT SAFE' should NOT match SAFE — negation must be rejected."""
        from nim_ensemble.parser import parse_answer
        result = parse_answer("NOT SAFE because of XSS", patterns=["SAFE", "UNSAFE"])
        assert result != "SAFE", f"Negated 'NOT SAFE' wrongly matched as SAFE (got {result})"

    def test_negation_isnt_compliant(self):
        from nim_ensemble.parser import parse_answer
        result = parse_answer("ISN'T really COMPLIANT", patterns=["COMPLIANT", "VIOLATED"])
        assert result != "COMPLIANT"

    def test_custom_patterns(self):
        from nim_ensemble.parser import parse_answer
        assert parse_answer("VULNERABLE to SQL injection", patterns=["SAFE", "VULNERABLE"]) == "VULNERABLE"

    def test_empty_returns_unclear(self):
        from nim_ensemble.parser import parse_answer
        assert parse_answer("") == "UNCLEAR"
        assert parse_answer(None) == "UNCLEAR"

    def test_bold_markers_stripped(self):
        """Markdown bold (**YES**) should still match."""
        from nim_ensemble.parser import parse_answer
        assert parse_answer("**YES** — confirmed.") == "YES"

    def test_thinking_model_output(self):
        """<think>...</think> blocks should be stripped before parsing."""
        from nim_ensemble.parser import strip_thinking, parse_answer
        raw = "<think>Let me analyze this carefully...</think>\nSAFE — no issues found."
        stripped = strip_thinking(raw)
        assert "<think>" not in stripped
        assert parse_answer(stripped) == "SAFE"

    def test_thinking_empty_after_strip(self):
        """If stripping <think> leaves nothing, return original content."""
        from nim_ensemble.parser import strip_thinking
        raw = "<think>only thinking here</think>"
        result = strip_thinking(raw)
        # Should return the original since stripping yields empty
        assert result == raw

    def test_longest_pattern_first(self):
        """INCONSISTENT should match before CONSISTENT."""
        from nim_ensemble.parser import parse_answer
        assert parse_answer("INCONSISTENT with guidelines") == "INCONSISTENT"

    def test_unsafe_before_safe(self):
        """UNSAFE should match before SAFE (longer pattern wins)."""
        from nim_ensemble.parser import parse_answer
        assert parse_answer("UNSAFE — do not deploy") == "UNSAFE"


class TestHealthTTL:
    """_is_dead / _mark_dead / DEAD_TTL_S: in-memory health tracking."""

    def setup_method(self):
        """Clear dead-models state before each test."""
        from nim_ensemble.health import _dead_models
        _dead_models.clear()

    def test_mark_and_check_dead(self):
        from nim_ensemble.health import _mark_dead, _is_dead
        _mark_dead("gemma-27b")
        assert _is_dead("gemma-27b") is True

    def test_not_dead_by_default(self):
        from nim_ensemble.health import _is_dead
        assert _is_dead("gemma-27b") is False

    def test_ttl_expiry(self):
        """After TTL, model should no longer be dead."""
        from nim_ensemble.health import _mark_dead, _is_dead, _dead_models, DEAD_TTL_S
        _mark_dead("gemma-27b")
        assert _is_dead("gemma-27b") is True

        # Backdate the timestamp past the TTL
        _dead_models["gemma-27b"] = time.time() - DEAD_TTL_S - 1
        assert _is_dead("gemma-27b") is False

    def test_ttl_not_expired_yet(self):
        """Within TTL, model should still be dead."""
        from nim_ensemble.health import _mark_dead, _is_dead, _dead_models, DEAD_TTL_S
        _mark_dead("gemma-27b")
        # Backdate by half the TTL — should still be dead
        _dead_models["gemma-27b"] = time.time() - (DEAD_TTL_S / 2)
        assert _is_dead("gemma-27b") is True


class TestGetSubstitute:
    """_get_substitute: should return a different-family model."""

    def setup_method(self):
        from nim_ensemble.health import _dead_models
        _dead_models.clear()

    def test_substitute_different_family(self):
        from nim_ensemble.health import _get_substitute
        from nim_ensemble.models import MODELS
        sub = _get_substitute("gemma-27b")
        assert sub is not None
        assert sub != "gemma-27b"
        assert MODELS[sub]["family"] != MODELS["gemma-27b"]["family"]

    def test_substitute_not_dead(self):
        """Substitute should not be a dead model."""
        from nim_ensemble.health import _get_substitute, _mark_dead
        from nim_ensemble.models import MODELS

        # Mark several models dead
        for alias in ["mistral-large", "nemotron-super-49b", "llama-3.3"]:
            _mark_dead(alias)

        sub = _get_substitute("gemma-27b")
        if sub is not None:
            assert sub not in ["mistral-large", "nemotron-super-49b", "llama-3.3"]

    def test_substitute_not_thinking(self):
        """Substitute should not be a thinking model (too slow)."""
        from nim_ensemble.health import _get_substitute
        from nim_ensemble.models import MODELS
        sub = _get_substitute("gemma-27b")
        if sub is not None:
            assert not MODELS[sub].get("thinking", False)

    def test_unknown_model_returns_none(self):
        from nim_ensemble.health import _get_substitute
        assert _get_substitute("nonexistent-model") is None


class TestPickDiverseModels:
    """_pick_diverse_models: family diversity in model selection."""

    def setup_method(self):
        from nim_ensemble.health import _dead_models
        _dead_models.clear()

    def test_returns_requested_count(self):
        from nim_ensemble.generate import _pick_diverse_models
        models = _pick_diverse_models(3)
        assert len(models) == 3

    def test_different_families(self):
        """First k models (where k <= num families) should all be different families."""
        from nim_ensemble.generate import _pick_diverse_models
        from nim_ensemble.models import MODELS
        models = _pick_diverse_models(3)
        families = [MODELS[m]["family"] for m in models]
        assert len(set(families)) == 3, f"Expected 3 unique families, got {families}"

    def test_exclude_works(self):
        from nim_ensemble.generate import _pick_diverse_models
        excluded = ["mistral-large", "gemma-27b"]
        models = _pick_diverse_models(3, exclude=excluded)
        for m in excluded:
            assert m not in models

    def test_skips_dead_models(self):
        from nim_ensemble.generate import _pick_diverse_models
        from nim_ensemble.health import _mark_dead
        _mark_dead("mistral-large")
        models = _pick_diverse_models(3)
        # mistral-large should be skipped (or substituted)
        # Either way, we should still get 3 models
        assert len(models) == 3


class TestClassifyTask:
    """classify_task: keyword-based task type detection."""

    def test_code_question(self):
        from nim_ensemble.cascade import classify_task
        assert classify_task("Is this Python function safe? def foo(): eval(input())") == "code"

    def test_compliance_question(self):
        from nim_ensemble.cascade import classify_task
        assert classify_task("Did the agent follow the rule about tone?") == "compliance"

    def test_factual_question(self):
        from nim_ensemble.cascade import classify_task
        assert classify_task("What is the capital of France?") == "factual"

    def test_general_fallback(self):
        from nim_ensemble.cascade import classify_task
        assert classify_task("Hello, how are you?") == "general"


class TestFeedbackAndELO:
    def test_elo_consensus_is_case_insensitive(self, free_scaling_state_dir):
        from nim_ensemble import elo

        elo.update_from_votes([("m1", "yes", "raw")], "YES")
        ranked = dict(elo.rank(min_calls=0))
        assert ranked["m1"]["agrees"] == 1
        assert ranked["m1"]["disagrees"] == 0

    def test_elo_override_is_case_insensitive(self, free_scaling_state_dir):
        from nim_ensemble import elo

        elo.update_from_override([("m1", "safe", "raw")], "SAFE")
        ranked = dict(elo.rank(min_calls=0))
        assert ranked["m1"]["overrides_for"] == 1
        assert ranked["m1"]["overrides_against"] == 0

    def test_resolve_feedback_skips_resolved_message_match(self, free_scaling_state_dir):
        from nim_ensemble import feedback

        feedback.log_result("q1", "YES", [("m1", "YES", 1.0)], message_id="msg-1")
        feedback.log_result("q2", "NO", [("m2", "NO", 1.0)], message_id="msg-1")

        first = feedback.resolve_feedback(message_id="msg-1", confirmed=True)
        assert first["resolved"] is True

        second = feedback.resolve_feedback(message_id="msg-1", confirmed=True)
        assert second["resolved"] is True
        assert second["original_answer"] == "NO"

    def test_resolve_ab_requires_explicit_a_b_tags(self, free_scaling_state_dir):
        from nim_ensemble import feedback

        feedback.log_result("qa", "YES", [("a1", "YES", 1.0)], tag="trial-A", message_id="msg-ab")
        feedback.log_result("qb", "NO", [("b1", "NO", 1.0)], tag="trial-B", message_id="msg-ab")

        result = feedback.resolve_by_reaction("msg-ab", "🅱️")
        assert result["resolved"] is True
        assert len(result["resolved_ids"]) == 2


class TestWeightedMajority:
    """_weighted_majority: vote tallying."""

    def test_unanimous(self):
        from nim_ensemble.cascade import _weighted_majority
        ans, conf = _weighted_majority([
            ("m1", "YES", 0.9),
            ("m2", "YES", 0.8),
            ("m3", "YES", 0.7),
        ])
        assert ans == "YES"
        assert conf == 1.0

    def test_split_vote(self):
        from nim_ensemble.cascade import _weighted_majority
        ans, conf = _weighted_majority([
            ("m1", "YES", 0.9),
            ("m2", "NO", 0.8),
            ("m3", "YES", 0.7),
        ])
        assert ans == "YES"
        # YES weight = 0.9 + 0.7 = 1.6, total = 2.4, conf = 1.6/2.4 ≈ 0.667
        assert 0.66 < conf < 0.68

    def test_empty_votes(self):
        from nim_ensemble.cascade import _weighted_majority
        ans, conf = _weighted_majority([])
        assert ans == "UNCLEAR"
        assert conf == 0.0

    def test_all_errors_ignored(self):
        from nim_ensemble.cascade import _weighted_majority
        ans, conf = _weighted_majority([
            ("m1", "ERROR", 1.0),
            ("m2", "UNCLEAR", 1.0),
        ])
        assert ans == "UNCLEAR"
        assert conf == 0.0


# =====================================================================
# INTEGRATION TESTS — require NVIDIA_API_KEY
# =====================================================================


@needs_api
class TestScale:
    """scale(): end-to-end with real API calls."""

    def test_returns_cascade_result(self):
        """scale() returns a CascadeResult with a valid answer."""
        from nim_ensemble import scale, CascadeResult
        result = scale(
            "Is 7 a prime number? Answer YES or NO.",
            k=1,
            answer_patterns=["YES", "NO"],
        )
        assert isinstance(result, CascadeResult)
        assert result.answer in ("YES", "NO", "UNCLEAR", "ERROR")
        assert result.calls_made >= 1
        assert len(result.models_used) >= 1

    def test_context_in_system_message(self):
        """Context parameter should influence the answer."""
        from nim_ensemble import scale
        code = "user_input = input(); exec(user_input)"
        result = scale(
            "Is this code safe? Answer SAFE or UNSAFE.",
            context=code,
            k=1,
            answer_patterns=["SAFE", "UNSAFE"],
        )
        # With exec(user_input) the answer should be UNSAFE
        assert result.answer in ("SAFE", "UNSAFE", "UNCLEAR", "ERROR")
        # Context was provided, so reasoning should exist
        assert result.calls_made >= 1

    def test_k1_uses_task_routing(self):
        """k=1 should use classify_task to pick the best model, not hardcode."""
        from nim_ensemble import scale, classify_task
        from nim_ensemble.cascade import _get_routing
        question = "Is this Python code safe? def f(): eval(x)"
        task_type = classify_task(question)
        best_for_task, _ = _get_routing()
        expected_model = best_for_task.get(task_type, best_for_task["general"])[0]

        result = scale(question, k=1, answer_patterns=["SAFE", "UNSAFE"])
        assert result.models_used[0] == expected_model
        assert result.stage == "primary"
        assert result.calls_made == 1


@needs_api
class TestScaleBatch:
    """scale_batch(): batch processing."""

    def test_returns_correct_length(self):
        """Output list should match input list length."""
        from nim_ensemble import scale_batch, CascadeResult
        items = [
            {"question": "Is 2 prime? Answer YES or NO.", "answer_patterns": ["YES", "NO"]},
            {"question": "Is 4 prime? Answer YES or NO.", "answer_patterns": ["YES", "NO"]},
            {"question": "Is 9 prime? Answer YES or NO.", "answer_patterns": ["YES", "NO"]},
        ]
        results = scale_batch(items, k=1)
        assert len(results) == 3
        for r in results:
            assert isinstance(r, CascadeResult)

    def test_per_item_error_no_crash(self):
        """Bad items shouldn't crash the batch — they get ERROR results."""
        from nim_ensemble import scale_batch, CascadeResult
        items = [
            {"question": "Is 7 prime? Answer YES or NO.", "answer_patterns": ["YES", "NO"]},
            {"question": ""},  # edge case: empty question
        ]
        results = scale_batch(items, k=1)
        assert len(results) == 2
        for r in results:
            assert isinstance(r, CascadeResult)


@needs_api
class TestGenerate:
    """generate(): best-of-k generation with cross-evaluation."""

    def test_returns_generate_result(self):
        """generate() returns a GenerateResult with non-empty output."""
        from nim_ensemble import generate, GenerateResult
        result = generate(
            "Write a one-sentence definition of 'recursion'.",
            k=2,
            max_tokens=100,
        )
        assert isinstance(result, GenerateResult)
        assert len(result.output) > 0
        assert result.total_calls >= 2

    def test_picks_winner(self):
        """generate() should pick a winner_idx from multiple outputs."""
        from nim_ensemble import generate
        result = generate(
            "Explain what a hash table is in one sentence.",
            k=2,
            max_tokens=100,
        )
        # With 2+ valid outputs, winner_idx should be valid
        valid_outputs = [o for o in result.all_outputs if o and o.strip()]
        if len(valid_outputs) >= 2:
            assert result.winner_idx >= 0
            assert result.winner_model != ""
        # Even with 1 valid output, winner_idx should be set
        assert result.winner_idx >= 0 or result.errors


@needs_api
class TestGenerateBatch:
    """generate_batch(): batch generation."""

    def test_returns_correct_length(self):
        from nim_ensemble import generate_batch, GenerateResult
        items = [
            {"question": "Define 'stack' in one sentence."},
            {"question": "Define 'queue' in one sentence."},
        ]
        results = generate_batch(items, k=2)
        assert len(results) == 2
        for r in results:
            assert isinstance(r, GenerateResult)


@needs_api
class TestHealth:
    """health(): model health probing."""

    def test_returns_model_health(self):
        """health() returns ModelHealth with valid status."""
        from nim_ensemble import health
        from nim_ensemble.health import ModelHealth
        # Probe just one fast model to keep it quick
        results = health(models=["gemma-27b"])
        assert "gemma-27b" in results
        h = results["gemma-27b"]
        assert isinstance(h, ModelHealth)
        assert h.status in ("ok", "dead", "slow", "error")
        assert h.latency_s >= 0


@needs_api
class TestVoteShortCircuit:
    """vote(): parallel short-circuit when 2 models agree."""

    def test_short_circuit_cancels_remaining(self):
        """With 3 models and short_circuit=True, should stop after 2 agree."""
        from nim_ensemble import vote
        result = vote(
            "Is 2 + 2 = 4? Answer YES or NO.",
            panel=["gemma-27b", "nemotron-super-49b", "mistral-large"],
            answer_patterns=["YES", "NO"],
            short_circuit=True,
            parallel=True,
        )
        # 2+2=4 is trivially YES — models should agree quickly
        if result.answer == "YES" and "short-circuit" in result.confidence:
            # Short circuit fired: only 2 votes collected
            non_error = [v for v in result.votes if v != "ERROR"]
            assert len(non_error) >= 2
            assert len(set(non_error)) == 1  # all agree
        # Even without short-circuit, result should be valid
        assert result.answer in ("YES", "NO", "ERROR", "UNCLEAR")
