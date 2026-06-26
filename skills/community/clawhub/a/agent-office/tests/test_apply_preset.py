import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "apply_preset.py"
SPEC = importlib.util.spec_from_file_location("apply_preset_module", MODULE_PATH)
apply_preset = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(apply_preset)


class ApplyPresetTests(unittest.TestCase):
    def test_aliases_resolve_to_expected_slug(self):
        self.assertEqual(apply_preset.resolve_preset_name("出版公司"), "publishing-company")
        self.assertEqual(apply_preset.resolve_preset_name("编程公司"), "coding-company")

    def test_load_preset_has_workers(self):
        publishing = apply_preset.load_preset("出版公司")
        coding = apply_preset.load_preset("coding-company")
        self.assertEqual(publishing["slug"], "publishing-company")
        self.assertEqual(coding["slug"], "coding-company")
        self.assertGreaterEqual(len(publishing["workers"]), 4)
        self.assertGreaterEqual(len(coding["workers"]), 5)

    def test_dry_run_returns_planned_workers(self):
        results = apply_preset.apply_preset("出版公司", dry_run=True)
        self.assertTrue(results)
        self.assertTrue(all(item["status"] == "planned" for item in results))


if __name__ == "__main__":
    unittest.main()
