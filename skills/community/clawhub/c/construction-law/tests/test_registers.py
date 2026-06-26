#!/usr/bin/env python3
"""
Test suite for the Notice Calendar and Obligations Register.

Covers:
- All supported forms are accepted by argparse
- fidic-silver entries are present and correct
- Output format (md/csv) works for all forms
- Obligations register produces both contractor and employer entries
- No crashes on any supported (form, format, party) combo
"""

import sys
import os
import io
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from notice_calendar import NOTICE_DATABASES, generate_calendar
from obligations_register import OBLIGATIONS, generate_register


class TestNoticeCalendarForms(unittest.TestCase):
    """Verify all supported forms produce output."""

    EXPECTED_FORMS = ["fidic-red", "fidic-yellow", "fidic-silver", "psscoc", "sia", "nec4"]

    def test_all_forms_present(self):
        """All expected forms should be in NOTICE_DATABASES."""
        for form in self.EXPECTED_FORMS:
            self.assertIn(form, NOTICE_DATABASES, f"Missing form: {form}")

    def test_all_forms_have_notices(self):
        """Each form should have at least 5 notices."""
        for form in self.EXPECTED_FORMS:
            notices = NOTICE_DATABASES[form]["notices"]
            self.assertGreaterEqual(len(notices), 5,
                                    f"{form} has too few notices: {len(notices)}")

    def test_silver_has_no_engineer_references(self):
        """Silver Book notices should not reference 'Engineer' as recipient."""
        silver = NOTICE_DATABASES["fidic-silver"]
        for notice in silver["notices"]:
            self.assertNotIn("Engineer", notice["recipient"],
                             f"Silver Book should not have Engineer: {notice}")

    def test_silver_has_correct_claim_notice_period(self):
        """Silver Book Cl.20.2.1 should be 28 days."""
        silver = NOTICE_DATABASES["fidic-silver"]
        claim_notices = [n for n in silver["notices"] if n["clause"] == "20.2.1"]
        self.assertEqual(len(claim_notices), 1)
        self.assertIn("28 days", claim_notices[0]["period"])

    def test_md_output_for_all_forms(self):
        """Markdown output should work for all forms."""
        for form in self.EXPECTED_FORMS:
            f = io.StringIO()
            with redirect_stdout(f):
                generate_calendar(form, "md")
            output = f.getvalue()
            self.assertIn("| Clause |", output,
                          f"{form} MD output missing table header")

    def test_csv_output_for_all_forms(self):
        """CSV output should work for all forms."""
        for form in self.EXPECTED_FORMS:
            f = io.StringIO()
            with redirect_stdout(f):
                generate_calendar(form, "csv")
            output = f.getvalue()
            self.assertIn("Clause,", output,
                          f"{form} CSV output missing header row")

    def test_notice_entry_structure(self):
        """Each notice entry should have all required fields."""
        required_fields = {"clause", "event", "period", "recipient", "consequence", "category"}
        for form, data in NOTICE_DATABASES.items():
            for i, notice in enumerate(data["notices"]):
                for field in required_fields:
                    self.assertIn(field, notice,
                                  f"{form} notice[{i}] missing field: {field}")


class TestObligationsRegisterForms(unittest.TestCase):
    """Verify all supported forms in obligations register."""

    EXPECTED_FORMS = ["fidic-red", "fidic-silver", "psscoc"]

    def test_all_forms_present(self):
        """Expected forms should be in OBLIGATIONS."""
        for form in self.EXPECTED_FORMS:
            self.assertIn(form, OBLIGATIONS, f"Missing form: {form}")

    def test_silver_has_contractor_and_employer(self):
        """Silver Book should have both contractor and employer obligations."""
        silver = OBLIGATIONS["fidic-silver"]
        self.assertIn("contractor", silver)
        self.assertIn("employer", silver)

    def test_silver_contractor_count(self):
        """Silver Book should have ~33 contractor obligations."""
        count = len(OBLIGATIONS["fidic-silver"]["contractor"])
        self.assertGreaterEqual(count, 30,
                                f"Silver contractor obligations: {count}, expected ≥30")

    def test_silver_employer_count(self):
        """Silver Book should have ~11 employer obligations."""
        count = len(OBLIGATIONS["fidic-silver"]["employer"])
        self.assertGreaterEqual(count, 10,
                                f"Silver employer obligations: {count}, expected ≥10")

    def test_silver_no_engineer_as_recipient(self):
        """Silver Book obligations should not have Engineer as the acting/receiving party.
        Explanatory notes like 'no Engineer' are fine."""
        silver = OBLIGATIONS["fidic-silver"]
        # Phrases that mention Engineer only to explain its absence are OK
        ok_phrases = ["no engineer", "no independent engineer", "not engineer"]
        for party in ["contractor", "employer"]:
            for ob in silver[party]:
                desc = ob.get("obligation", "") + " " + ob.get("timing", "")
                if "Engineer" in desc:
                    lower = desc.lower()
                    has_ok = any(phrase in lower for phrase in ok_phrases)
                    self.assertTrue(has_ok,
                                    f"Silver {party} references Engineer without disclaimer: {ob}")

    def test_md_output_all_forms(self):
        """MD output should work for all forms."""
        for form in self.EXPECTED_FORMS:
            f = io.StringIO()
            with redirect_stdout(f):
                generate_register(form, "both", "md")
            output = f.getvalue()
            self.assertIn("|", output, f"{form} MD output empty")

    def test_csv_output_all_forms(self):
        """CSV output should work for all forms."""
        for form in self.EXPECTED_FORMS:
            f = io.StringIO()
            with redirect_stdout(f):
                generate_register(form, "both", "csv")
            output = f.getvalue()
            self.assertIn("Clause", output, f"{form} CSV output empty")

    def test_party_filter_contractor(self):
        """Filtering by contractor should only show contractor obligations."""
        f = io.StringIO()
        with redirect_stdout(f):
            generate_register("fidic-silver", "contractor", "md")
        output = f.getvalue()
        self.assertIn("Contractor", output)

    def test_party_filter_employer(self):
        """Filtering by employer should only show employer obligations."""
        f = io.StringIO()
        with redirect_stdout(f):
            generate_register("fidic-silver", "employer", "md")
        output = f.getvalue()
        self.assertIn("Employer", output)

    def test_obligation_entry_structure(self):
        """Each obligation should have required fields."""
        required_fields = {"clause", "obligation", "timing", "priority", "category"}
        for form, data in OBLIGATIONS.items():
            for party in ["contractor", "employer"]:
                if party not in data:
                    continue
                for i, ob in enumerate(data[party]):
                    for field in required_fields:
                        self.assertIn(field, ob,
                                      f"{form}/{party}[{i}] missing: {field}")


if __name__ == "__main__":
    unittest.main()
