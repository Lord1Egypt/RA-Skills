import os
import subprocess
import unittest


SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "bin"))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
CODEFLOW = os.path.join(ROOT_DIR, "codeflow")
DEV_RELAY = os.path.join(BIN_DIR, "dev-relay.sh")
LIB = os.path.join(BIN_DIR, "lib.sh")


class CliHelpAndAgentDetectionTests(unittest.TestCase):
    def test_public_help_contracts_return_usage(self):
        cases = [
            (["/bin/bash", CODEFLOW, "run", "--help"], "dev-relay.sh [options] -- <command>"),
            (["/bin/bash", CODEFLOW, "review", "--help"], "review-pr.sh [options] <pr_url>"),
            (["/bin/bash", CODEFLOW, "parallel", "--help"], "parallel-tasks.sh [options] <tasks-file>"),
            (["/bin/bash", CODEFLOW, "control", "--help"], "--session-key"),
            (["/bin/bash", CODEFLOW, "resume", "--help"], "codeflow resume [run-flags] <relay_dir>"),
            (["/bin/bash", CODEFLOW, "enforcer", "--help"], "codeflow enforcer install [--restart]"),
            (["/bin/bash", DEV_RELAY, "--help"], "dev-relay.sh [options] -- <command>"),
        ]

        for cmd, needle in cases:
            with self.subTest(cmd=cmd):
                proc = subprocess.run(cmd, capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
                self.assertIn(needle, proc.stdout)

    def test_agent_detection_uses_command_not_display_name(self):
        proc = subprocess.run(
            [
                "bash",
                "-c",
                f'source "{LIB}"; codeflow_detect_agent_command "$1"',
                "--",
                "/usr/local/bin/codex",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), "Codex\tfalse\ttrue")


if __name__ == "__main__":
    unittest.main()
