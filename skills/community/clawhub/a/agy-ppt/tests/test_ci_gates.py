#!/usr/bin/env python3
"""Deterministic tests for CI quality gates, negative validation, and frozen contract guards.

Verifies:
1. README bilingual parity and relative link checker (positive and negative cases).
2. Repository hygiene, private path, and credential checker (positive and negative cases).
3. Frozen contract modification detector and maintainer approval label policy.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

# Add scripts/ci to sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]
CI_SCRIPTS = REPO_ROOT / "scripts" / "ci"

import sys
if str(CI_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CI_SCRIPTS))

import check_readme_parity as rmp
import check_repository_hygiene as rh
import check_frozen_contracts as fc


class TestReadmeParityGate(unittest.TestCase):
    def test_authoritative_readmes_pass_parity(self) -> None:
        """The committed repository READMEs must pass parity and link validation."""
        success, errors = rmp.run_readme_parity_checks(REPO_ROOT)
        self.assertTrue(success, f"Committed READMEs failed parity check: {errors}")
        self.assertEqual(len(errors), 0)

    def test_missing_readme_fails(self) -> None:
        """Missing README file fails cleanly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            success, errors = rmp.run_readme_parity_checks(tmp_root)
            self.assertFalse(success)
            self.assertTrue(any("does not exist" in e for e in errors))

    def test_broken_relative_link_fails(self) -> None:
        """Referencing a non-existent local file triggers broken link failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            zh = tmp_root / "README.md"
            en = tmp_root / "README_en.md"

            zh.write_text(
                "# Title\n\n[EN](README_en.md)\n\n[Broken Link](non_existent_doc.md)\n",
                encoding="utf-8",
            )
            en.write_text(
                "# Title\n\n[ZH](README.md)\n",
                encoding="utf-8",
            )

            errors = rmp.check_readme_links(zh, tmp_root)
            self.assertTrue(any("non_existent_doc.md" in err.target for err in errors))

    def test_broken_anchor_link_fails(self) -> None:
        """Referencing an anchor that does not exist triggers link failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            zh = tmp_root / "README.md"
            zh.write_text(
                "# Title\n\n[Bad Anchor](#does-not-exist)\n",
                encoding="utf-8",
            )
            errors = rmp.check_readme_links(zh, tmp_root)
            self.assertTrue(any("does-not-exist" in err.error for err in errors))

    def test_missing_section_parity_detected(self) -> None:
        """A required semantic section missing from one language fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            zh = tmp_root / "README.md"
            en = tmp_root / "README_en.md"

            zh.write_text("# Title\n\n## 安裝\n\nContent\n", encoding="utf-8")
            en.write_text("# Title\n\nNo installation section here\n", encoding="utf-8")

            errors = rmp.check_semantic_parity(zh, en)
            self.assertTrue(any("Installation" in err for err in errors))


class TestRepositoryHygieneGate(unittest.TestCase):
    def test_authoritative_repository_passes_hygiene(self) -> None:
        """The committed repository must pass all hygiene, path, and credential audits."""
        success, errors = rh.run_hygiene_checks(REPO_ROOT)
        self.assertTrue(success, f"Authoritative repository failed hygiene check: {errors}")
        self.assertEqual(len(errors), 0)

    def test_prohibited_artifact_detected(self) -> None:
        """Prohibited file names are caught."""
        samples = [
            ".env",
            "production.env",
            "foo/bar/__pycache__/module.cpython-311.pyc",
            "download.part",
            "rfc2119.txt",
            "NIST.AI.600-1.pdf",
            "deck.pptx",
            "slide_1.png",
        ]
        errors = rh.check_prohibited_artifacts(samples)
        self.assertEqual(len(errors), len(samples))

    def test_private_path_rejection(self) -> None:
        """A private filesystem path in a non-allowlisted file triggers violation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            dirty_file = tmp_root / "module.py"
            dirty_file.write_text(
                'CACHE_PATH = "/Users/sujunmin/sensitive_data/cache"\n',
                encoding="utf-8",
            )
            errors = rh.check_private_paths(tmp_root, ["module.py"])
            self.assertEqual(len(errors), 1)
            self.assertIn("/Users/sujunmin", errors[0])

    def test_credential_leak_rejection(self) -> None:
        """Private key header is detected and rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            key_file = tmp_root / "secret.pem"
            key_file.write_text(
                "REDACTED-SECRET\n",
                encoding="utf-8",
            )
            errors = rh.check_credential_hygiene(tmp_root, ["secret.pem"])
            self.assertEqual(len(errors), 1)
            self.assertIn("Private key header", errors[0])


class TestFrozenContractGuard(unittest.TestCase):
    def test_all_frozen_files_exist(self) -> None:
        """All designated Phase 12 and Phase 13 production files exist."""
        missing = fc.verify_frozen_files_exist(REPO_ROOT)
        self.assertEqual(missing, [], f"Missing frozen files: {missing}")

    def test_clean_change_list_passes(self) -> None:
        """Changes touching only non-frozen files pass cleanly."""
        changed = ["README.md", "docs/new_doc.md", "tests/test_foo.py"]
        passed, touched, is_approved = fc.check_frozen_modifications(changed, [])
        self.assertTrue(passed)
        self.assertEqual(touched, [])
        self.assertFalse(is_approved)

    def test_unapproved_phase12_change_fails(self) -> None:
        """Modifying a Phase 12 file without maintainer approval label fails."""
        changed = ["skills/agy-ppt/scripts/source_grounding.py", "README.md"]
        passed, touched, is_approved = fc.check_frozen_modifications(changed, ["documentation"])
        self.assertFalse(passed)
        self.assertEqual(touched, ["skills/agy-ppt/scripts/source_grounding.py"])
        self.assertFalse(is_approved)

    def test_unapproved_phase13_change_fails(self) -> None:
        """Modifying a Phase 13 file without maintainer approval label fails."""
        changed = ["skills/agy-ppt/scripts/source_ingestion.py"]
        passed, touched, is_approved = fc.check_frozen_modifications(changed, [])
        self.assertFalse(passed)
        self.assertEqual(touched, ["skills/agy-ppt/scripts/source_ingestion.py"])
        self.assertFalse(is_approved)

    def test_approved_frozen_change_passes_with_notice(self) -> None:
        """Modifying a frozen file WITH maintainer approval label passes."""
        changed = ["skills/agy-ppt/scripts/source_grounding.py"]
        labels = ["bug", fc.APPROVAL_LABEL]
        passed, touched, is_approved = fc.check_frozen_modifications(changed, labels)
        self.assertTrue(passed)
        self.assertEqual(touched, ["skills/agy-ppt/scripts/source_grounding.py"])
        self.assertTrue(is_approved)


if __name__ == "__main__":
    unittest.main(verbosity=2)
