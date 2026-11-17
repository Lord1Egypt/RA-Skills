#!/usr/bin/env python3
"""Regression tests for security-sensitive skill dependency constraints."""

import json
from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parent.parent
REQUIREMENTS_PATH = SKILL_DIR / "requirements.txt"
SKILL_PATH = SKILL_DIR / "SKILL.md"
SAFE_CRYPTOGRAPHY_REQUIREMENT = "cryptography>=50.0.0,<51"


class RequirementsTests(unittest.TestCase):
    def test_cryptography_range_starts_at_fully_patched_release(self) -> None:
        cryptography_requirements = [
            line.strip()
            for line in REQUIREMENTS_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("cryptography")
        ]

        self.assertEqual(cryptography_requirements, [SAFE_CRYPTOGRAPHY_REQUIREMENT])

    def test_openclaw_installer_uses_same_safe_range(self) -> None:
        metadata_line = next(
            line
            for line in SKILL_PATH.read_text(encoding="utf-8").splitlines()
            if line.startswith("metadata: ")
        )
        metadata = json.loads(metadata_line.removeprefix("metadata: "))
        installers = metadata["openclaw"]["install"]
        pip_installer = next(item for item in installers if item["id"] == "pip-cryptography")

        self.assertEqual(pip_installer["packages"], [SAFE_CRYPTOGRAPHY_REQUIREMENT])


if __name__ == "__main__":
    unittest.main()
