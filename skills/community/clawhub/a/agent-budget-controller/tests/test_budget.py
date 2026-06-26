#!/usr/bin/env python3
"""Basic integration tests for budget CLI."""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import BudgetConfig
from lib.tracker import UsageTracker
from lib.pricing import PricingTable
from lib.reporter import BudgetReporter
from lib.alerts import BudgetAlerts


def test_full_workflow():
    """Test complete workflow: set -> log -> status -> check."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir)
        
        print("🧪 Testing full workflow...")
        
        # 1. Config: Set limits
        print("  1. Setting limits...")
        config = BudgetConfig(data_dir)
        config.set_global_limit("daily", 5.00)
        config.set_agent_limit("test-agent", "daily", 2.00)
        
        assert config.get_global_limit("daily") == 5.00
        assert config.get_agent_limit("test-agent", "daily") == 2.00
        print("     ✅ Limits set")
        
        # 2. Pricing: Calculate cost
        print("  2. Calculating cost...")
        pricing = PricingTable(data_dir)
        cost1 = pricing.get_cost("gpt-4o", 1000, 500)
        cost2 = pricing.get_cost("claude-sonnet-4-5", 2000, 800)
        
        assert cost1 > 0
        assert cost2 > 0
        print(f"     ✅ Cost calculated: ${cost1:.4f}, ${cost2:.4f}")
        
        # 3. Tracker: Log usage
        print("  3. Logging usage...")
        tracker = UsageTracker(data_dir)
        tracker.log_usage("test-agent", "gpt-4o", 1000, 500, cost1)
        tracker.log_usage("test-agent", "claude-sonnet-4-5", 2000, 800, cost2)
        
        daily_usage = tracker.get_period_usage("daily", agent="test-agent")
        assert abs(daily_usage - (cost1 + cost2)) < 0.0001
        print(f"     ✅ Usage logged: ${daily_usage:.4f}")
        
        # 4. Reporter: Generate status
        print("  4. Generating status...")
        reporter = BudgetReporter(tracker, config)
        status = reporter.generate_status_report(agent="test-agent")
        
        assert "test-agent" in status
        assert "daily" in status.lower()
        print("     ✅ Status generated")
        
        # 5. Check limits
        print("  5. Checking limits...")
        results = reporter.check_limits(agent="test-agent")
        
        # Should be OK (under $2 limit)
        assert results["daily"] == True
        print("     ✅ Limits checked (OK)")
        
        # 6. Test alert levels
        print("  6. Testing alerts...")
        level_ok, pct_ok = BudgetAlerts.get_alert_level(1.0, 5.0)  # 20%
        level_warn, pct_warn = BudgetAlerts.get_alert_level(3.6, 5.0)  # 72%
        level_crit, pct_crit = BudgetAlerts.get_alert_level(4.6, 5.0)  # 92%
        level_exc, pct_exc = BudgetAlerts.get_alert_level(5.5, 5.0)  # 110%
        
        assert level_ok == "ok"
        assert level_warn == "warning"
        assert level_crit == "critical"
        assert level_exc == "exceeded"
        print("     ✅ Alert levels correct")
        
        print("\n✅ All tests passed!")


def test_pricing_fuzzy_match():
    """Test fuzzy model name matching."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir)
        
        print("🧪 Testing fuzzy model matching...")
        
        pricing = PricingTable(data_dir)
        
        # Test with full version strings
        cost1 = pricing.get_cost("anthropic/claude-sonnet-4-20250514", 1000, 500)
        cost2 = pricing.get_cost("openai/gpt-4o-2024-11-20", 1000, 500)
        
        assert cost1 > 0
        assert cost2 > 0
        print("  ✅ Fuzzy matching works")


def test_usage_log_persistence():
    """Test that usage log persists across instances."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir)
        
        print("🧪 Testing usage log persistence...")
        
        # Write with first instance
        tracker1 = UsageTracker(data_dir)
        tracker1.log_usage("agent1", "model1", 100, 50, 0.01)
        
        # Read with second instance
        tracker2 = UsageTracker(data_dir)
        records = tracker2.get_usage()
        
        assert len(records) == 1
        assert records[0]["agent"] == "agent1"
        print("  ✅ Log persists")


if __name__ == '__main__':
    test_full_workflow()
    print()
    test_pricing_fuzzy_match()
    print()
    test_usage_log_persistence()
    print("\n🎉 All tests passed!")
