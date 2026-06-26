import os
import stat
import subprocess
import tempfile
import textwrap
import unittest


SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "bin"))
REVIEW_PR = os.path.join(BIN_DIR, "review-pr.sh")
DEV_RELAY = os.path.join(BIN_DIR, "dev-relay.sh")


def _write_executable(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)


class ReviewCustomPromptContractTests(unittest.TestCase):
    def test_custom_prompt_keeps_review_output_contract(self):
        with tempfile.TemporaryDirectory() as td:
            fake_bin = os.path.join(td, "bin")
            repo_dir = os.path.join(td, "repo")
            capture_stdin = os.path.join(td, "prompt.txt")
            capture_args = os.path.join(td, "args.txt")
            os.makedirs(fake_bin, exist_ok=True)
            os.makedirs(repo_dir, exist_ok=True)

            _write_executable(
                os.path.join(fake_bin, "gh"),
                textwrap.dedent(
                    """\
                    #!/bin/sh
                    if [ "$1" = "pr" ] && [ "$2" = "view" ]; then
                      cat <<'JSON'
                    {"title":"T","body":"","headRefName":"feature","baseRefName":"main","additions":1,"deletions":0}
                    JSON
                      exit 0
                    fi
                    if [ "$1" = "pr" ] && [ "$2" = "comment" ]; then
                      exit 0
                    fi
                    if [ "$1" = "repo" ] && [ "$2" = "clone" ]; then
                      exit 0
                    fi
                    exit 0
                    """
                ),
            )
            _write_executable(
                os.path.join(fake_bin, "git"),
                "#!/bin/sh\nexit 0\n",
            )
            _write_executable(
                os.path.join(fake_bin, "bash"),
                textwrap.dedent(
                    """\
                    #!/bin/sh
                    if [ "${1-}" = "$TARGET_DEV_RELAY" ]; then
                      printf '%s\\n' "$@" > "$CAPTURE_ARGS"
                      cat > "$CAPTURE_STDIN"
                      exit 0
                    fi
                    exec /bin/bash "$@"
                    """
                ),
            )

            env = dict(os.environ)
            env["PATH"] = fake_bin + os.pathsep + env.get("PATH", "")
            env["TARGET_DEV_RELAY"] = DEV_RELAY
            env["CAPTURE_STDIN"] = capture_stdin
            env["CAPTURE_ARGS"] = capture_args
            env["CODEFLOW_ENFORCE_GUARD"] = "false"

            proc = subprocess.run(
                [
                    "/bin/bash",
                    REVIEW_PR,
                    "-w",
                    repo_dir,
                    "-p",
                    "Focus on security vulnerabilities",
                    "-c",
                    "https://github.com/owner/repo/pull/123",
                ],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            with open(capture_stdin, "r", encoding="utf-8") as f:
                prompt = f.read()

            self.assertIn("Focus on security vulnerabilities", prompt)
            self.assertIn("Write your final review to /tmp/pr-review-123.md", prompt)
            self.assertIn("Done: PR #123 review complete", prompt)


if __name__ == "__main__":
    unittest.main()
