import subprocess
import sys
import unittest
from pathlib import Path


class ReviewHelperTests(unittest.TestCase):
    def test_review_pack_contains_sections(self):
        base = Path(__file__).parent
        result = subprocess.run(
            [
                sys.executable,
                str(base / "scripts" / "review_helper.py"),
                "--pr-json",
                str(base / "fixtures" / "pull-request-sample.json"),
                "--checks-json",
                str(base / "fixtures" / "check-runs-sample.json"),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertIn("## Overview", result.stdout)
        self.assertIn("## Failing Checks", result.stdout)
        self.assertIn("ui regression", result.stdout)
        self.assertIn("pending checks remain", result.stdout)


if __name__ == "__main__":
    unittest.main()
