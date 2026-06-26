import json
import os
import subprocess
import unittest


SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PARSER = os.path.join(SCRIPT_DIR, "parse-stream.py")


def _run_parser(events: list[dict]) -> list[dict]:
    env = dict(os.environ)
    env["PLATFORM"] = "test"
    env["CODEFLOW_SAFE_MODE"] = "false"
    env["CODEFLOW_OUTPUT_MODE"] = "minimal"
    env.pop("RELAY_DIR", None)

    proc = subprocess.run(
        ["python3", PARSER],
        input="".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events),
        capture_output=True,
        text=True,
        env=env,
    )
    if proc.returncode != 0:
        raise AssertionError(proc.stderr)

    out: list[dict] = []
    for line in proc.stdout.splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


class ClaudeToolUseIdCorrelationTests(unittest.TestCase):
    def test_failure_uses_matching_tool_use_id_instead_of_last_tool(self):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "id": "tool-write", "name": "Write", "input": {"file_path": "a.txt", "content": "x"}},
                        {"type": "tool_use", "id": "tool-bash", "name": "Bash", "input": {"command": "echo ok"}},
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "tool-write",
                            "is_error": True,
                            "content": [{"type": "text", "text": "permission denied"}],
                        }
                    ]
                },
            },
        ]

        out = _run_parser(events)
        text = "\n".join((item.get("text") or "") for item in out if item.get("op") == "post")
        self.assertIn("Write failed", text)
        self.assertNotIn("Bash failed", text)


if __name__ == "__main__":
    unittest.main()
