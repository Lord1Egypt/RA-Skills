import pytest
from cost_tracker import CostRecord, CostTracker


class TestCostTracker:
    def test_initial_state(self):
        tracker = CostTracker(budget_limit=50.0)
        assert tracker.total_cost == 0.0
        assert tracker.over_budget is False
        assert tracker.iteration_count == 0

    def test_add_record(self):
        tracker = CostTracker(budget_limit=50.0)
        record = CostRecord(iteration=1, cost_usd=10.0, duration_seconds=60.0, decision="keep")
        new_tracker = tracker.add(record)
        assert new_tracker.total_cost == 10.0
        assert new_tracker.iteration_count == 1
        # Original is unchanged (immutable)
        assert tracker.total_cost == 0.0

    def test_over_budget(self):
        tracker = CostTracker(budget_limit=20.0)
        r1 = CostRecord(iteration=1, cost_usd=15.0, duration_seconds=60.0, decision="keep")
        r2 = CostRecord(iteration=2, cost_usd=10.0, duration_seconds=60.0, decision="keep")
        tracker = tracker.add(r1).add(r2)
        assert tracker.over_budget is True
        assert tracker.total_cost == 25.0

    def test_summary(self):
        tracker = CostTracker(budget_limit=50.0)
        r = CostRecord(iteration=1, cost_usd=5.0, duration_seconds=30.0, decision="keep")
        tracker = tracker.add(r)
        s = tracker.summary()
        assert s["total_cost_usd"] == 5.0
        assert s["iterations"] == 1
        assert s["over_budget"] is False
