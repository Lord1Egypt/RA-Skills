"""Tests for CertainLogic Smart Router."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from smart_router import SmartRouter


class TestProfileDetection:
    """Test automatic profile detection from queries."""

    def test_detects_coding(self):
        router = SmartRouter()
        tier, conf, reason = router.classify("Write a Python function")
        assert "coding" in reason.lower()

    def test_detects_research(self):
        router = SmartRouter()
        tier, conf, reason = router.classify("Analyze the impact of climate change")
        assert "research" in reason.lower()

    def test_detects_marketing(self):
        router = SmartRouter()
        tier, conf, reason = router.classify("Write a blog post about AI tools")
        assert "marketing" in reason.lower()

    def test_falls_back_to_general(self):
        router = SmartRouter()
        tier, conf, reason = router.classify("Hello, how are you?")
        assert "general" in reason.lower()


class TestTierSelection:
    """Test model tier selection."""

    def test_simple_query_to_cheap(self):
        router = SmartRouter()
        result = router.route("What is Python?")
        assert result["model_tier"] in ["cheap", "default"]

    def test_complex_query_to_powerful(self):
        router = SmartRouter()
        result = router.route("Design a system architecture for distributed computing")
        assert result["model_tier"] in ["default", "powerful"]

    def test_forced_cheap(self):
        router = SmartRouter()
        result = router.route("Complex architecture design", force_cheap=True)
        assert result["model_tier"] == "cheap"
        assert result["override"] is True

    def test_forced_powerful(self):
        router = SmartRouter()
        result = router.route("Simple print statement", force_powerful=True)
        assert result["model_tier"] == "powerful"
        assert result["override"] is True


class TestHonesty:
    """Ensure no false claims in output."""

    def test_no_magic_claims(self):
        router = SmartRouter()
        result = router.route("Any query")
        assert "AI" not in result["reasoning"]
        assert "learned" not in result["reasoning"].lower()

    def test_confidence_present(self):
        router = SmartRouter()
        result = router.route("Test query")
        assert isinstance(result["confidence"], float)
        assert 0.0 <= result["confidence"] <= 1.0

    def test_explicit_override_flag(self):
        router = SmartRouter()
        normal = router.route("query")
        forced = router.route("query", force_cheap=True)
        assert normal["override"] is False
        assert forced["override"] is True


class TestEdgeCases:
    """Edge case handling."""

    def test_empty_string(self):
        router = SmartRouter()
        result = router.route("")
        assert result["model_tier"] in ["cheap", "default", "powerful"]

    def test_very_long_query(self):
        router = SmartRouter()
        long_query = "code " * 1000
        result = router.route(long_query)
        assert result["model_tier"] in ["cheap", "default", "powerful"]

    def test_special_characters(self):
        router = SmartRouter()
        result = router.route("function() { return $$$; }")
        assert "model_tier" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
