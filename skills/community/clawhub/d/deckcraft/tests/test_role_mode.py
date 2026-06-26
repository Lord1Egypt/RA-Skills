#!/usr/bin/env python3
"""Tests for role_mode parameter (v6.0+)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile

from engine import DeckEngine


class TestRoleModeSingle(unittest.TestCase):
    """Default single mode should work exactly as before."""

    def test_default_is_single(self):
        eng = DeckEngine(theme_name="business", canvas="16:9")
        self.assertEqual(eng.role_mode, "single")

    def test_explicit_single(self):
        eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="single")
        self.assertEqual(eng.role_mode, "single")

    def test_single_cover_and_save(self):
        eng = DeckEngine(theme_name="business", canvas="16:9")
        eng.cover(title="Test", subtitle="Sub")
        self.assertEqual(eng.slide_count, 1)
        with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
            path = f.name
        try:
            eng.save(path)
            self.assertTrue(os.path.isfile(path))
        finally:
            os.unlink(path)

    def test_single_strategist_plan_raises(self):
        """single mode should NOT allow strategist_plan."""
        eng = DeckEngine(theme_name="business", canvas="16:9")
        with self.assertRaises(RuntimeError):
            eng.strategist_plan({"title": "test"})

    def test_single_execute_plan_raises(self):
        """single mode should NOT allow execute_plan."""
        eng = DeckEngine(theme_name="business", canvas="16:9")
        with self.assertRaises(RuntimeError):
            eng.execute_plan({"content_plan": [{"type": "cover", "title": "X"}]})


class TestRoleModeMulti(unittest.TestCase):
    """Multi mode should provide strategist + executor API."""

    def test_multi_init(self):
        eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")
        self.assertEqual(eng.role_mode, "multi")

    def test_strategist_plan_returns_template(self):
        eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")
        plan = eng.strategist_plan({"title": "Test Brief"})
        self.assertIsInstance(plan, dict)
        self.assertIn("meta", plan)
        self.assertIn("strategy", plan)
        self.assertEqual(plan["meta"]["source_brief"], "Test Brief")

    def test_strategist_plan_validates_brief_type(self):
        eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")
        with self.assertRaises(TypeError):
            eng.strategist_plan("not a dict")

    def test_execute_plan_generates_slides(self):
        eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")
        plan = {
            "content_plan": [
                {"type": "cover", "title": "Hello", "subtitle": "World"},
                {"type": "content", "title": "Slide 2", "bullets": ["Point 1"]},
                {"type": "closing", "title": "Bye"},
            ]
        }
        result = eng.execute_plan(plan)
        self.assertIs(result, eng)  # returns self for chaining
        self.assertEqual(eng.slide_count, 3)

    def test_execute_plan_empty_raises(self):
        eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")
        with self.assertRaises(TypeError):
            eng.execute_plan({"content_plan": []})

    def test_execute_plan_unknown_type_warns(self):
        import warnings
        eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")
        plan = {
            "content_plan": [
                {"type": "cover", "title": "Hello"},
                {"type": "nonexistent_type", "title": "Skip me"},
                {"type": "closing", "title": "Bye"},
            ]
        }
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            eng.execute_plan(plan)
            # Should warn about unknown type but not crash
            warn_msgs = [str(x.message) for x in w]
            self.assertTrue(any("nonexistent_type" in m for m in warn_msgs))
        self.assertEqual(eng.slide_count, 2)  # cover + closing only


class TestRoleModeInvalid(unittest.TestCase):
    """Invalid role_mode should raise ValueError."""

    def test_invalid_role_mode(self):
        with self.assertRaises(ValueError):
            DeckEngine(theme_name="business", canvas="16:9", role_mode="team")


if __name__ == "__main__":
    unittest.main()
