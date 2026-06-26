import os
import stat
import subprocess
import tempfile
import unittest


SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "bin"))
REVIEW_PR = os.path.join(BIN_DIR, "review-pr.sh")
PARALLEL = os.path.join(BIN_DIR, "parallel-tasks.sh")


def _write_executable(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)


class ReviewParallelGuardPrecheckTests(unittest.TestCase):
    def test_review_blocks_before_running_gh_or_git(self):
        with tempfile.TemporaryDirectory() as td:
            fake_bin = os.path.join(td, "bin")
            gh_called = os.path.join(td, "gh.called")
            git_called = os.path.join(td, "git.called")
            os.makedirs(fake_bin, exist_ok=True)

            _write_executable(
                os.path.join(fake_bin, "gh"),
                f"#!/bin/sh\n: > {gh_called}\nexit 99\n",
            )
            _write_executable(
                os.path.join(fake_bin, "git"),
                f"#!/bin/sh\n: > {git_called}\nexit 99\n",
            )

            env = dict(os.environ)
            env["PATH"] = fake_bin + os.pathsep + env.get("PATH", "")
            env["XDG_STATE_HOME"] = td
            env["HOME"] = td
            env["OPENCLAW_SESSION_KEY"] = "acct:discord:thread:blocked"
            env["OPENCLAW_SESSION"] = env["OPENCLAW_SESSION_KEY"]

            proc = subprocess.run(
                ["/bin/bash", REVIEW_PR, "https://github.com/owner/repo/pull/123"],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 42, proc.stderr + proc.stdout)
            self.assertIn("Codeflow guard blocked this run", proc.stderr)
            self.assertFalse(os.path.exists(gh_called))
            self.assertFalse(os.path.exists(git_called))

    def test_parallel_blocks_before_start_summary(self):
        with tempfile.TemporaryDirectory() as td:
            tasks_file = os.path.join(td, "tasks.txt")
            with open(tasks_file, "w", encoding="utf-8") as f:
                f.write("~/repo | do the thing\n")

            env = dict(os.environ)
            env["XDG_STATE_HOME"] = td
            env["HOME"] = td
            env["OPENCLAW_SESSION_KEY"] = "acct:discord:thread:blocked"
            env["OPENCLAW_SESSION"] = env["OPENCLAW_SESSION_KEY"]

            proc = subprocess.run(
                ["/bin/bash", PARALLEL, tasks_file],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 42, proc.stderr + proc.stdout)
            self.assertIn("Codeflow guard blocked this run", proc.stderr)
            self.assertNotIn("Parallel Session Started", proc.stdout)


if __name__ == "__main__":
    unittest.main()
