from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from axiotic_experiments.results import append_metric, replay_metrics
from axiotic_experiments.runtime import EnvironmentRun
from axiotic_experiments.spec import ExperimentSpec
from axiotic_experiments.telemetry import open_run

from .fixtures import spec_mapping


class RecordingSink:
    def __init__(self) -> None:
        self.rows: list[tuple[int, dict[str, object]]] = []

    def log(self, metrics: dict[str, object], *, step: int) -> None:
        self.rows.append((step, metrics))


class FakeConfig(dict):
    def update(self, value, *, allow_val_change=False):
        self.allow_val_change = allow_val_change
        return super().update(value)


class FakeRun:
    def __init__(self) -> None:
        self.config = FakeConfig()
        self.tags: tuple[str, ...] = ()
        self.notes = ""
        self.summary: dict[str, object] = {}
        self.logged: list[tuple[int, dict[str, object]]] = []
        self.finished: list[int] = []
        self.url = "https://wandb.test/run"

    def log(self, metrics, *, step):
        self.logged.append((step, metrics))

    def finish(self, *, exit_code=0):
        self.finished.append(exit_code)


class FakeWandb:
    def __init__(self) -> None:
        self.run = FakeRun()
        self.kwargs: dict[str, object] = {}

    def init(self, **kwargs):
        self.kwargs = kwargs
        return self.run


class FakeResultStore:
    def __init__(self) -> None:
        self.calls: list[tuple[Path, str]] = []

    def upload_bundle(self, bundle: Path, *, run_id: str) -> str:
        self.calls.append((bundle, run_id))
        return "result-commit"


class ResultTests(unittest.TestCase):
    def test_metrics_round_trip_preserves_steps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metrics.jsonl"
            append_metric(path, step=4, metrics={"loss": 2.0})
            append_metric(path, step=9, metrics={"loss": 1.0})
            sink = RecordingSink()

            result = replay_metrics(path, sink)

        self.assertEqual(result, {"records": 2, "first_step": 4, "last_step": 9})
        self.assertEqual([step for step, _ in sink.rows], [4, 9])

    def test_replay_rejects_regressing_steps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metrics.jsonl"
            path.write_text(
                '{"step":2,"metrics":{"loss":2}}\n{"step":1,"metrics":{"loss":1}}\n'
            )
            with self.assertRaisesRegex(ValueError, "regress"):
                replay_metrics(path, RecordingSink())


class TelemetryTests(unittest.TestCase):
    def test_open_run_sets_deterministic_resume_and_provenance(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping())
        fake = FakeWandb()
        with patch.dict(
            os.environ,
            {"WANDB_API_KEY": "runtime-value", "WANDB_MODE": "online"},
            clear=False,
        ):
            run = open_run(
                spec,
                core=spec.core_manifest(),
                wandb_module=fake,
            )

        self.assertIs(run, fake.run)
        self.assertEqual(fake.kwargs["id"], spec.run.id)
        self.assertEqual(fake.kwargs["resume"], "allow")
        self.assertEqual(fake.kwargs["mode"], "online")
        self.assertEqual(run.config["commit"], spec.source.commit)
        self.assertIn("variant:model", run.tags)
        self.assertTrue(run.config.allow_val_change)

    def test_environment_run_mirrors_metric_and_marks_failure(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping())
        fake = FakeWandb()
        index = {"schema_version": "1.0", "nodes": []}
        with tempfile.TemporaryDirectory() as directory:
            metrics = Path(directory) / "metrics.jsonl"
            environment = {
                "WANDB_API_KEY": "runtime-value",
                "WANDB_MODE": "online",
                "WANDB_ENTITY": spec.wandb.entity,
                "WANDB_PROJECT": spec.wandb.project,
                "AXIOTIC_RUN_ID": spec.run.id,
                "AXIOTIC_RUN_CORE_JSON": json.dumps(spec.core_manifest()),
                "AXIOTIC_ARTIFACT_INDEX_JSON": json.dumps(index),
            }
            with (
                patch.dict(os.environ, environment, clear=False),
                self.assertRaisesRegex(RuntimeError, "boom"),
                EnvironmentRun(
                    metrics_path=metrics,
                    wandb_module=fake,
                    publish_results=False,
                ) as run,
            ):
                run.log({"loss": 1.0}, step=3)
                raise RuntimeError("boom")
            row = json.loads(metrics.read_text())

        self.assertEqual(row["step"], 3)
        self.assertEqual(fake.run.finished, [1])

    def test_environment_run_publishes_bundle_on_success(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping())
        fake_wandb = FakeWandb()
        fake_store = FakeResultStore()
        index = {"schema_version": "1.0", "nodes": []}
        with tempfile.TemporaryDirectory() as directory:
            metrics = Path(directory) / "metrics.jsonl"
            environment = {
                "WANDB_API_KEY": "runtime-value",
                "WANDB_MODE": "online",
                "WANDB_ENTITY": spec.wandb.entity,
                "WANDB_PROJECT": spec.wandb.project,
                "AXIOTIC_RUN_ID": spec.run.id,
                "AXIOTIC_RUN_CORE_JSON": json.dumps(spec.core_manifest()),
                "AXIOTIC_ARTIFACT_INDEX_JSON": json.dumps(index),
            }
            with (
                patch.dict(os.environ, environment, clear=False),
                EnvironmentRun(
                    metrics_path=metrics,
                    wandb_module=fake_wandb,
                    result_store=fake_store,
                ) as run,
            ):
                run.log({"accuracy": 1.0}, step=1)

        self.assertEqual(len(fake_store.calls), 1)
        self.assertEqual(fake_store.calls[0][1], spec.run.id)
        self.assertEqual(
            fake_wandb.run.summary["github_results_commit"], "result-commit"
        )
        self.assertEqual(fake_wandb.run.finished, [0])


if __name__ == "__main__":
    unittest.main()
