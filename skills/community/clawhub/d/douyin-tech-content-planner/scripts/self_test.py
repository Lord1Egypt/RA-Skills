from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_plan import PlanError, load_json, validate

ROOT = Path(__file__).resolve().parents[1]


class PlannerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.facts = load_json(ROOT / "examples" / "facts.json")
        self.plan = load_json(ROOT / "examples" / "plan.json")

    def test_example_passes_and_is_marked_hypothetical(self) -> None:
        self.assertTrue(self.facts["example_is_hypothetical"])
        validate(self.facts, self.plan)

    def test_unknown_fact_reference_is_rejected(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["beats"][0]["fact_ids"] = ["MISSING"]
        with self.assertRaisesRegex(PlanError, "unknown fact id"):
            validate(self.facts, plan)

    def test_unverified_fact_cannot_be_used_in_a_beat(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["beats"][0]["fact_ids"] = ["F3"]
        with self.assertRaisesRegex(PlanError, "unverified fact"):
            validate(self.facts, plan)

    def test_opening_evidence_must_be_within_first_12_seconds(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["opening_evidence"]["seconds"] = 13
        with self.assertRaisesRegex(PlanError, "between 0 and 12"):
            validate(self.facts, plan)

    def test_invalid_status_type_returns_a_validation_error(self) -> None:
        facts = copy.deepcopy(self.facts)
        facts["facts"][0]["status"] = []
        with self.assertRaisesRegex(PlanError, "status must be verified or unverified"):
            validate(facts, self.plan)


if __name__ == "__main__":
    unittest.main()
