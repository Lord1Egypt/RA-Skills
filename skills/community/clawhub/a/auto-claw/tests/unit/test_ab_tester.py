"""
Unit tests for src/ab_tester.py — A/B Testing Engine
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import ab_tester as ab


class TestABTesterModule:
    """Smoke tests for ab_tester module."""

    def test_abtester_class_exists(self):
        """ABTester class is importable."""
        assert hasattr(ab, 'ABTester')

    def test_abtest_dataclass_exists(self):
        """ABTest and ABTestResult dataclasses exist."""
        assert hasattr(ab, 'ABTest')
        assert hasattr(ab, 'ABTestResult')

    def test_abvariant_dataclass_exists(self):
        """ABVariant dataclass exists."""
        assert hasattr(ab, 'ABVariant')

    def test_tester_instantiable(self):
        """ABTester can be instantiated."""
        t = ab.ABTester()
        assert t is not None

    def test_has_add_variant_method(self):
        """Has add_variant method."""
        t = ab.ABTester()
        assert callable(getattr(t, 'add_variant', None))

    def test_has_create_test_method(self):
        """Has create_test method."""
        t = ab.ABTester()
        assert callable(getattr(t, 'create_test', None))

    def test_has_record_visitor_method(self):
        """Has record_visitor method."""
        t = ab.ABTester()
        assert callable(getattr(t, 'record_visitor', None))

    def test_has_record_conversion_method(self):
        """Has record_conversion method."""
        t = ab.ABTester()
        assert callable(getattr(t, 'record_conversion', None))

    def test_has_analyze_test_method(self):
        """Has analyze_test method."""
        t = ab.ABTester()
        assert callable(getattr(t, 'analyze_test', None))

    def test_abtest_result_fields(self):
        """ABTestResult has expected fields."""
        r = ab.ABTestResult(
            test_id="test-001",
            test_name="Test 1",
            status="running",
            winner="control",
            confidence=0.95,
            lift=0.5,
            recommendation="keep_testing",
            duration_days=7,
        )
        assert r.confidence == 0.95
        assert r.lift == 0.5
        assert r.winner == "control"

    def test_abtest_fields(self):
        """ABTest dataclass has expected fields."""
        v = ab.ABVariant(id="control", name="Control", traffic_split=50.0)
        t = ab.ABTest(
            test_id="test-001",
            name="Test 1",
            url="https://example.com",
            test_element="button",
            variants=[v],
            goal_type="click",
            goal_selector="button",
            status="running",
        )
        assert t.test_id == "test-001"
        assert t.status == "running"

    def test_abvariant_fields(self):
        """ABVariant dataclass has expected fields."""
        v = ab.ABVariant(
            id="control",
            name="Control",
            traffic_split=50.0,
            visitors=1000,
            conversions=50,
            headline="Control",
            description="Original",
            cta_text="Click",
            cta_color="blue",
        )
        assert v.id == "control"
        assert v.visitors == 1000
