"""Static invariants for the injection measurement gate."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
BASELINE = ROOT / "references" / "baseline-20261109.json"
MANIFEST = ROOT / "manifest.json"


def frontmatter(text: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise AssertionError("SKILL.md frontmatter missing")
    return dict(re.findall(r"^([A-Za-z_]+):\s*(.+)$", match.group(1), re.M))


class InjectionGateTests(unittest.TestCase):
    def test_description_and_body_budget(self):
        text = SKILL.read_text(encoding="utf-8")
        fields = frontmatter(text)
        self.assertLessEqual(len(fields["description"]), 45, fields["description"])
        self.assertLessEqual(len(text.encode("utf-8")), 8192)

    def test_baseline_reconciles_and_text_blocks_fit(self):
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
        blocks = {item["id"]: item for item in data["blocks"]}
        self.assertEqual(sum(item["bytes"] for item in data["blocks"]), data["sum_bytes"])
        text_total = data["sum_bytes"] - blocks["mcp"]["bytes"]
        self.assertLessEqual(text_total, data["gate_bytes"], text_total)

    def test_manifest_declares_gate_and_version(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        fields = frontmatter(SKILL.read_text(encoding="utf-8"))
        self.assertEqual(data["version"], fields["version"])
        self.assertEqual(data["release"]["version"], fields["version"])
        self.assertTrue(data["injectionGate"]["enabled"])
        self.assertEqual(data["injectionGate"]["descriptionMaxChars"], 45)
        self.assertEqual(data["injectionGate"]["skillMaxBytes"], 8192)
        self.assertEqual(data["injectionGate"]["textGateBytes"], 57344)

    def test_gate_files_are_publishable(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        listed = set(data["publishableFiles"])
        for rel in (
            "docs/injection-measurement.md",
            "references/baseline-20261109.json",
            "references/budgets.md",
            "references/mcp-measure.md",
            "scripts/measure_prompt.py",
            "scripts/injection_state.py",
            "scripts/self_test.py",
        ):
            self.assertIn(rel, listed)


if __name__ == "__main__":
    unittest.main()
