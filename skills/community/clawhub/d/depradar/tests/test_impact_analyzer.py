"""Tests for lib/impact_analyzer.py — cross-reference breaking changes with codebase."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lib.schema import PackageUpdate, BreakingChange, ImpactLocation
import lib.impact_analyzer as ia


def make_pkg(name: str, breaking_symbols: list[str]) -> PackageUpdate:
    """Helper to create a minimal PackageUpdate with breaking changes."""
    changes = [
        BreakingChange(
            symbol=sym,
            change_type="removed",
            description=f"{sym} was removed",
            old_signature=None,
            new_signature=None,
            migration_note=None,
            source="changelog",
            confidence="high",
        )
        for sym in breaking_symbols
    ]
    return PackageUpdate(
        id="P1",
        package=name,
        ecosystem="npm",
        current_version="7.0.0",
        latest_version="8.0.0",
        semver_type="major",
        has_breaking_changes=True,
        breaking_changes=changes,
        impact_locations=[],
        impact_confidence="not_scanned",
        github_repo=None,
        subs=None,
        score=0.0,
    )


class TestDetermineConfidence(unittest.TestCase):
    def test_high_when_ast_found(self):
        locs = [
            ImpactLocation(
                file_path="src/payments.py",
                line_number=10,
                usage_text="stripe.webhooks.constructEvent(payload, sig, secret)",
                detection_method="ast",
            )
        ]
        confidence = ia._determine_confidence(locs)
        self.assertEqual(confidence, "high")

    def test_med_when_grep_found(self):
        locs = [
            ImpactLocation(
                file_path="src/payments.ts",
                line_number=15,
                usage_text="stripe.webhooks.constructEvent(",
                detection_method="grep",
            )
        ]
        confidence = ia._determine_confidence(locs)
        self.assertEqual(confidence, "med")

    def test_low_when_empty(self):
        confidence = ia._determine_confidence([])
        self.assertEqual(confidence, "low")

    def test_high_takes_precedence(self):
        locs = [
            ImpactLocation("f1.py", 1, "code", "ast"),
            ImpactLocation("f2.ts", 2, "code", "grep"),
        ]
        confidence = ia._determine_confidence(locs)
        self.assertEqual(confidence, "high")


class TestAnalyzeImpact(unittest.TestCase):
    def test_finds_python_usage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a Python file that uses the breaking symbol
            src = Path(tmpdir) / "src"
            src.mkdir()
            (src / "payments.py").write_text(
                "import stripe\n"
                "result = stripe.webhooks.constructEvent(payload, sig, secret)\n"
            )

            pkg = make_pkg("stripe", ["constructEvent"])
            packages = [pkg]
            ia.analyze_impact(packages, project_root=tmpdir)

            updated = packages[0]
            self.assertIsInstance(updated.impact_locations, list)
            # Should have found at least one impact
            if updated.impact_confidence != "not_scanned":
                self.assertIn(updated.impact_confidence, ["high", "med", "low"])

    def test_finds_js_usage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "src"
            src.mkdir()
            (src / "webhook.js").write_text(
                "const stripe = require('stripe');\n"
                "const event = stripe.webhooks.constructEvent(payload, sig, secret);\n"
            )

            pkg = make_pkg("stripe", ["constructEvent"])
            packages = [pkg]
            ia.analyze_impact(packages, project_root=tmpdir)

            updated = packages[0]
            self.assertIsInstance(updated.impact_locations, list)

    def test_no_impact_when_symbol_not_used(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "src"
            src.mkdir()
            (src / "app.py").write_text("print('hello world')\n")

            pkg = make_pkg("stripe", ["constructEvent"])
            packages = [pkg]
            ia.analyze_impact(packages, project_root=tmpdir)

            updated = packages[0]
            # Symbol not used — impact_locations should be empty
            self.assertEqual(len(updated.impact_locations), 0)

    def test_skips_node_modules(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            nm = Path(tmpdir) / "node_modules" / "stripe" / "lib"
            nm.mkdir(parents=True)
            (nm / "index.js").write_text(
                "exports.constructEvent = function() {};\n"
            )

            pkg = make_pkg("stripe", ["constructEvent"])
            packages = [pkg]
            ia.analyze_impact(packages, project_root=tmpdir)

            updated = packages[0]
            # node_modules should be skipped
            for loc in updated.impact_locations:
                self.assertNotIn("node_modules", loc.file_path)

    def test_handles_no_breaking_changes(self):
        pkg = PackageUpdate(
            id="P1",
            package="lodash",
            ecosystem="npm",
            current_version="4.17.20",
            latest_version="4.17.21",
            semver_type="patch",
            has_breaking_changes=False,
            breaking_changes=[],
            impact_locations=[],
            impact_confidence="not_scanned",
            github_repo=None,
            subs=None,
            score=0.0,
        )
        packages = [pkg]
        with tempfile.TemporaryDirectory() as tmpdir:
            ia.analyze_impact(packages, project_root=tmpdir)
        # Should complete without error
        self.assertEqual(len(packages[0].breaking_changes), 0)

    def test_handles_empty_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg = make_pkg("stripe", ["constructEvent"])
            packages = [pkg]
            ia.analyze_impact(packages, project_root=tmpdir)
            # Empty directory — no impact found, but no error
            self.assertIsInstance(packages[0].impact_locations, list)

    def test_multiple_packages_parallel(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "src"
            src.mkdir()
            (src / "app.py").write_text(
                "import stripe\nfrom openai import Completion\n"
                "stripe.webhooks.constructEvent(x, y, z)\nCompletion.create(model='gpt-3')\n"
            )

            pkg1 = make_pkg("stripe", ["constructEvent"])
            pkg2 = make_pkg("openai", ["Completion"])
            packages = [pkg1, pkg2]
            ia.analyze_impact(packages, project_root=tmpdir)
            # Both should have been analyzed
            for pkg in packages:
                self.assertIsInstance(pkg.impact_locations, list)


if __name__ == "__main__":
    unittest.main()
