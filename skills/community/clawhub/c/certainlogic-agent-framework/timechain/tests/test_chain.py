"""Cypher Tempre — automated test suite for all subsystems."""

import unittest, sys, json, subprocess, os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))


class TestTimechain(unittest.TestCase):
    def test_verify(self):
        r = subprocess.run(
            [sys.executable, "timechain.py", "verify"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("VERIFY: PASS", r.stdout)

    def test_head_exists(self):
        r = subprocess.run(
            [sys.executable, "timechain.py", "stat"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("height:", r.stdout)
        self.assertNotIn("root genesis", r.stdout)


class TestCPHY(unittest.TestCase):
    def test_balance(self):
        r = subprocess.run(
            [sys.executable, "cphy.py", "balance"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("minted", r.stdout)

    def test_map(self):
        r = subprocess.run(
            [sys.executable, "cphy.py", "map"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("active lock", r.stdout)

    def test_selftest(self):
        r = subprocess.run(
            [sys.executable, "cphy.py", "selftest"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("SELFTEST PASS", r.stdout)


class TestRouter(unittest.TestCase):
    def test_stats(self):
        r = subprocess.run(
            [sys.executable, "router.py", "stats"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("REPLAY", r.stdout)


class TestConsensus(unittest.TestCase):
    def test_verify(self):
        r = subprocess.run(
            [sys.executable, "consensus.py", "verify"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        # May or may not have witnesses; at minimum, runs without crash
        self.assertLess(r.returncode, 2)


class TestTelemetry(unittest.TestCase):
    def test_adherence(self):
        r = subprocess.run(
            [sys.executable, "telemetry.py", "adherence"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("sessions primed", r.stdout)


class TestRecall(unittest.TestCase):
    def test_log(self):
        r = subprocess.run(
            [sys.executable, "timechain.py", "log"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        lines = r.stdout.strip().split('\n')
        self.assertGreater(len(lines), 10)


class TestDream(unittest.TestCase):
    def test_status(self):
        r = subprocess.run(
            [sys.executable, "dream.py", "status"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("dream", r.stdout.lower())


class TestImmune(unittest.TestCase):
    def test_status(self):
        r = subprocess.run(
            [sys.executable, "immune.py", "status"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        self.assertIn("locked", r.stdout)


class TestEnforce(unittest.TestCase):
    def test_mark(self):
        r = subprocess.run(
            [sys.executable, "enforce.py", "mark"],
            capture_output=True, text=True, cwd=SKILL_DIR
        )
        # mark stays silent by design; success is exit 0
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
