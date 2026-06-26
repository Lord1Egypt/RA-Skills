import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from guardlib import preflight_report


class PowerShellRiskTests(unittest.TestCase):
    def setUp(self):
        self.cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.allowed_roots = [self.cwd]

    def report(self, command):
        return preflight_report(command, self.cwd, self.allowed_roots)

    def test_remove_item_recurse_force_wildcard_is_critical(self):
        report = self.report(r"Remove-Item -Path .\dist\* -Recurse -Force")
        self.assertEqual(report["risk"], "critical")
        self.assertTrue(report["need_approval"])
        self.assertIn("remove-item -Recurse expands the scope beyond a single item", report["reasons"])
        self.assertIn("remove-item -Force bypasses normal PowerShell safety checks", report["reasons"])
        self.assertTrue(any(item["type"] == "wildcard-target" for item in report["path_findings"]))

    def test_literalpath_avoids_wildcard_finding(self):
        report = self.report(r"Remove-Item -LiteralPath .\[cache] -Recurse")
        self.assertEqual(report["risk"], "critical")
        self.assertIn("remove-item -LiteralPath narrows matching by disabling wildcard expansion", report["reasons"])
        self.assertFalse(any(item["type"] == "wildcard-target" for item in report["path_findings"]))

    def test_copy_item_tracks_destination_without_destructive_label(self):
        report = self.report(r"Copy-Item -Path .\src\config.json -Destination .\backup\config.json")
        self.assertEqual(report["risk"], "medium")
        self.assertIn("write", report["categories"])
        self.assertNotIn("destructive", report["categories"])
        resolved = {item["raw"] for item in report["path_findings"]}
        self.assertEqual(resolved, set())
        self.assertIn("copy-item -Path may expand wildcards in PowerShell", report["reasons"])

    def test_move_item_force_is_high(self):
        report = self.report(r"Move-Item .\build .\archive -Force")
        self.assertEqual(report["risk"], "high")
        self.assertIn("destructive", report["categories"])
        self.assertIn("move-item -Force bypasses normal PowerShell safety checks", report["reasons"])

    def test_content_writes_are_medium(self):
        for command, reason in [
            (r"Set-Content -Path .\appsettings.json -Value test", "set-content can overwrite local file content"),
            (r"Out-File -LiteralPath .\logs\app[1].txt -InputObject hi", "out-file -LiteralPath narrows matching by disabling wildcard expansion"),
            (r"Clear-Content -Path .\notes.txt", "clear-content can overwrite local file content"),
        ]:
            with self.subTest(command=command):
                report = self.report(command)
                self.assertEqual(report["risk"], "medium")
                self.assertIn("write", report["categories"])
                self.assertIn(reason, report["reasons"])


if __name__ == "__main__":
    unittest.main()
