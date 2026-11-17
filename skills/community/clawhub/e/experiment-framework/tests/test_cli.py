from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from axiotic_experiments.cli import run
from axiotic_experiments.manifest import validate_sealed_graph

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_validates_each_tracked_backend_example(self) -> None:
        for name in (
            "local-smoke.toml",
            "worker-smoke.toml",
            "worker2-smoke.toml",
            "runpod-smoke.toml",
        ):
            with self.subTest(name=name), redirect_stdout(StringIO()):
                code = run(
                    [
                        "validate",
                        str(ROOT / "examples" / name),
                        "--machines",
                        str(ROOT / "machines.toml"),
                    ]
                )
            self.assertEqual(code, 0)

    def test_plan_writes_complete_redacted_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bundle"
            stream = StringIO()
            with redirect_stdout(stream):
                code = run(
                    [
                        "plan",
                        str(ROOT / "examples/local-smoke.toml"),
                        "--machines",
                        str(ROOT / "machines.toml"),
                        "--output",
                        str(output),
                    ]
                )
            response = json.loads(stream.getvalue())
            index = json.loads((output / "artifact-index.json").read_text())
            launch = json.loads((output / "launch-plan.json").read_text())

        self.assertEqual(code, 0)
        self.assertTrue(response["dry_run"])
        self.assertFalse(launch["credentials_embedded"])
        self.assertNotIn("WANDB_API_KEY", launch["runtime_environment"])
        validate_sealed_graph(index)

    def test_ssh_launch_without_execute_is_a_redacted_preview(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bundle"
            stream = StringIO()
            with redirect_stdout(stream):
                code = run(
                    [
                        "launch",
                        str(ROOT / "examples/worker-smoke.toml"),
                        "--machines",
                        str(ROOT / "machines.toml"),
                        "--output",
                        str(output),
                        "--butler-project",
                        "fixture",
                    ]
                )
            response = json.loads(stream.getvalue())

        self.assertEqual(code, 0)
        self.assertTrue(response["dry_run"])
        self.assertEqual(
            response["ssh_payload"]["env"]["WANDB_API_KEY"],
            "[redacted]",
        )
        self.assertNotIn(
            "runtime",
            " ".join(response["ssh_command"]),
        )

    def test_runpod_dry_launch_writes_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bundle"
            stream = StringIO()
            with redirect_stdout(stream):
                code = run(
                    [
                        "launch",
                        str(ROOT / "examples/runpod-smoke.toml"),
                        "--machines",
                        str(ROOT / "machines.toml"),
                        "--output",
                        str(output),
                        "--butler-project",
                        "fixture",
                    ]
                )
            response = json.loads(stream.getvalue())
            adapter_exists = (output / "runpod-adapter.toml").is_file()

        self.assertEqual(code, 0)
        self.assertTrue(adapter_exists)
        self.assertNotIn("--execute", response["delegate_command"])


if __name__ == "__main__":
    unittest.main()
