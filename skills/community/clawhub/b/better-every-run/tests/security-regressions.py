import json
import subprocess
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "scripts/ber.js"
class PromotionRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "project"
        self.root.mkdir()
        self.target = self.root / "SKILL.md"
        self.target.write_text("# Skill\n")
        self.run_cli("remember", "--note", "Use concise output for task summaries.", "--scope", "skill")
        self.store = self.root / ".better-every-run/lessons.jsonl"
        self.lesson = json.loads(self.store.read_text().strip())
        self.id = self.lesson["id"]
    def run_cli(self, *args, ok=True):
        result = subprocess.run(["node", str(CLI), *args], cwd=self.root, capture_output=True, text=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result
    def write_lesson(self, **changes):
        self.lesson = json.loads(self.store.read_text().strip())
        self.lesson.update(changes)
        self.store.write_text(json.dumps(self.lesson) + "\n")
    def card(self):
        self.run_cli("card", self.id, "--to", "skill", "--target", "SKILL.md")
    def test_rejected_states_and_expiry_fail_without_writes(self):
        self.card()
        for status in ["proposed", "rejected", "quarantined", "superseded", "promoted"]:
            with self.subTest(status=status):
                self.write_lesson(status=status)
                self.run_cli("promote", self.id, "--to", "skill", "--target", "SKILL.md", ok=False)
                self.run_cli("eval-fixture", self.id, "--target", "evals/case.json", ok=False)
                self.assertEqual(self.target.read_text(), "# Skill\n")
                self.assertFalse((self.root / "evals/case.json").exists())
        self.write_lesson(status="accepted", expiresAt="2000-01-01")
        self.run_cli("promote", self.id, "--to", "skill", "--target", "SKILL.md", ok=False)
    def test_lesson_changed_after_card_fails(self):
        self.card()
        self.write_lesson(text="Use long output for task summaries.")
        self.run_cli("promote", self.id, "--to", "skill", "--target", "SKILL.md", ok=False)
        self.assertEqual(self.target.read_text(), "# Skill\n")
    def test_symlink_file_and_parent_fail(self):
        external = Path(self.tmp.name) / "outside"
        external.mkdir()
        file = external / "rules.md"
        file.write_text("unchanged")
        self.target.unlink()
        self.target.symlink_to(file)
        self.run_cli("card", self.id, "--to", "skill", "--target", "SKILL.md", ok=False)
        (self.root / "evals").symlink_to(external, target_is_directory=True)
        self.run_cli("eval-fixture", self.id, "--target", "evals/new.json", ok=False)
        self.assertEqual(file.read_text(), "unchanged")
        self.assertFalse((external / "new.json").exists())
    def test_target_replaced_by_symlink_after_card_fails(self):
        self.card()
        external = Path(self.tmp.name) / "outside.md"
        external.write_text(self.target.read_text())
        self.target.unlink()
        self.target.symlink_to(external)
        self.run_cli("promote", self.id, "--to", "skill", "--target", "SKILL.md", ok=False)
        self.assertEqual(external.read_text(), "# Skill\n")
if __name__ == "__main__":
    unittest.main()
