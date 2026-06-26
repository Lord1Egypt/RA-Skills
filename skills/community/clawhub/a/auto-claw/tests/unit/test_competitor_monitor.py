"""
Unit tests for src/competitor_monitor.py — Competitor Monitoring Engine
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import competitor_monitor as cm


class TestCompetitorMonitorModule:
    """Smoke tests for competitor_monitor module."""

    def test_monitor_class_exists(self):
        """CompetitorMonitor class exists."""
        assert hasattr(cm, 'CompetitorMonitor')

    def test_monitor_instantiable(self):
        """CompetitorMonitor can be instantiated."""
        m = cm.CompetitorMonitor()
        assert m is not None

    def test_has_fetch_method(self):
        """Has fetch_competitor method."""
        m = cm.CompetitorMonitor()
        assert callable(getattr(m, 'fetch_competitor', None))

    def test_has_detect_changes_method(self):
        """Has detect_changes method."""
        m = cm.CompetitorMonitor()
        assert callable(getattr(m, 'detect_changes', None))

    def test_has_monitor_all_method(self):
        """Has monitor_all method."""
        m = cm.CompetitorMonitor()
        assert callable(getattr(m, 'monitor_all', None))

    def test_has_compare_with_us_method(self):
        """Has compare_with_us method."""
        m = cm.CompetitorMonitor()
        assert callable(getattr(m, 'compare_with_us', None))

    def test_has_generate_alerts_method(self):
        """Has generate_alerts method."""
        m = cm.CompetitorMonitor()
        assert callable(getattr(m, 'generate_alerts', None))

    def test_competitors_is_dict(self):
        """competitors is a dict."""
        m = cm.CompetitorMonitor()
        assert isinstance(m.competitors, dict)
