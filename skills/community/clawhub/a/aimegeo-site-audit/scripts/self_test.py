#!/usr/bin/env python3
"""Regression tests for the local HTML snapshot inventory."""
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_html as audit

class SnapshotInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "page.html").write_text('<title>Fixture</title><meta name="robots" content="noindex"><h1>Heading</h1><a href="/next">Next</a>')
        (self.root / "input.json").write_text(json.dumps({"schema_version":1,"dataset_kind":"synthetic_fixture","pages":[{"url":"https://sample.test/","html":"page.html","http_status":200}]}))
    def tearDown(self): self.temp.cleanup()
    def test_extract_reports_facts_without_assessment(self):
        result = audit.audit(self.root / "input.json")
        self.assertEqual(result["status"], "complete")
        page = result["pages"][0]
        self.assertEqual(page["signals"]["titles"], ["Fixture"])
        self.assertEqual(page["signals"]["noindex_directives"], [{"name":"robots","content":"noindex"}])
        self.assertNotIn("findings", result)
        self.assertNotIn("priority", page)
    def test_unavailable_record_is_not_described_as_zero_findings(self):
        record=json.loads((self.root/"input.json").read_text())
        record["pages"].append({"url":"https://sample.test/missing","state":"fetch_failed","reason":"Fixture only"})
        (self.root/"input.json").write_text(json.dumps(record))
        result=audit.audit(self.root/"input.json")
        self.assertEqual(result["summary"]["not_verified_pages"],1)
        self.assertEqual(result["pages"][1]["reason_code"],"fetch_failed")
    def test_page_cap_and_duplicate_are_explicit(self):
        data=json.loads((self.root/"input.json").read_text())
        data["pages"]*=2; (self.root/"input.json").write_text(json.dumps(data))
        result=audit.audit(self.root/"input.json",max_pages=1)
        self.assertEqual(result["pages"][1]["state"],"skipped")
        self.assertEqual(result["pages"][1]["reason_code"],"duplicate_url")
    def test_html_path_cannot_escape_input_directory(self):
        data=json.loads((self.root/"input.json").read_text()); data["pages"][0]["html"]="../outside.html"
        (self.root/"input.json").write_text(json.dumps(data))
        with self.assertRaises(ValueError): audit.load_input(self.root/"input.json")
    def test_output_refuses_overwrite_and_exports_raw_snapshot_fields(self):
        result=audit.audit(self.root/"input.json"); out=self.root/"out"
        audit.write_outputs(result,out)
        csv_text=(out/"页面观察.csv").read_text(encoding="utf-8-sig")
        self.assertIn("noindex",csv_text)
        self.assertNotIn("priority",csv_text)
        with self.assertRaises(ValueError): audit.write_outputs(result,out)

if __name__ == "__main__": unittest.main()
