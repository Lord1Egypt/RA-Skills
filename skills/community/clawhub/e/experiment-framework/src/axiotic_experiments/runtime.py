from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from types import TracebackType
from typing import Any, Self

from .github_store import GitHubApiResultStore
from .hf_store import HuggingFaceCheckpointStore, HuggingFaceDatasetStore
from .manifest import write_json
from .results import append_metric
from .telemetry import WandbConfigurationError, _require_online, _wandb_module


class RuntimeConfigurationError(RuntimeError):
    pass


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeConfigurationError(f"missing runtime environment: {name}")
    return value


class EnvironmentRun:
    """Machine-neutral trainer integration built entirely from dispatcher env."""

    def __init__(
        self,
        *,
        metrics_path: Path | None = None,
        wandb_module: Any | None = None,
        result_store: Any | None = None,
        publish_results: bool = True,
    ):
        self.run_id = _required("AXIOTIC_RUN_ID")
        self.core = json.loads(_required("AXIOTIC_RUN_CORE_JSON"))
        self.index = json.loads(_required("AXIOTIC_ARTIFACT_INDEX_JSON"))
        default_root = Path.home() / ".axiotic-experiments" / "runs" / self.run_id
        self.metrics_path = metrics_path or default_root / "metrics.jsonl"
        self.bundle_dir = self.metrics_path.parent
        self.wandb_module = wandb_module
        self.result_store = result_store
        self.publish_results = publish_results
        self.run: Any | None = None
        self._tempdir: tempfile.TemporaryDirectory[str] | None = None

    def __enter__(self) -> Self:
        _require_online()
        self.bundle_dir.mkdir(parents=True, exist_ok=True)
        write_json(self.bundle_dir / "run-core.json", self.core)
        write_json(self.bundle_dir / "artifact-index.json", self.index)
        self.metrics_path.touch(exist_ok=True)
        wandb = _wandb_module(self.wandb_module)
        run = self.core["run"]
        source = self.core["source"]
        self.run = wandb.init(
            entity=_required("WANDB_ENTITY"),
            project=_required("WANDB_PROJECT"),
            id=self.run_id,
            name=os.environ.get("WANDB_NAME", run["name"]),
            notes=run["notes"],
            tags=run["tags"],
            job_type=run["phase"],
            resume="allow",
            mode="online",
            config=self.core,
        )
        self.run.config.update(
            {
                "axiotic_phase": run["phase"],
                "axiotic_variant": run["variant"],
                "axiotic_modality": run["modality"],
                "axiotic_dataset": run["dataset"],
                "axiotic_reason": run["reason"],
                "repo_url": source["repo_url"],
                "branch": source["branch"],
                "commit": source["commit"],
                "commit_url": source["commit_url"],
                "seed": run["seed"],
            },
            allow_val_change=True,
        )
        self.run.tags = tuple(
            sorted(set(tuple(self.run.tags or ()) + tuple(run["tags"])))
        )
        self.run.notes = run["notes"]
        return self

    def log(self, metrics: dict[str, Any], *, step: int) -> None:
        if self.run is None:
            raise WandbConfigurationError("experiment run is not open")
        append_metric(self.metrics_path, step=step, metrics=metrics)
        self.run.log(metrics, step=step)

    def _index_path(self) -> Path:
        if self._tempdir is None:
            self._tempdir = tempfile.TemporaryDirectory(prefix=f"axexp-{self.run_id}-")
        path = Path(self._tempdir.name) / "artifact-index.json"
        path.write_text(
            json.dumps(self.index, sort_keys=True, separators=(",", ":")) + "\n"
        )
        return path

    def checkpoint(self, directory: Path, *, step: int) -> dict[str, Any]:
        token = _required("HF_TOKEN")
        hf = self.core["huggingface"]
        uploaded = HuggingFaceCheckpointStore(
            repo_id=hf["checkpoint_repo"],
            checkpoint_prefix=hf["checkpoint_prefix"],
            revision=hf["revision"],
            token=token,
        ).upload(
            directory,
            run_id=self.run_id,
            step=step,
            provenance_path=self._index_path(),
        )
        if self.run is not None:
            self.run.summary["latest_checkpoint_uri"] = uploaded.uri
            self.run.summary["latest_checkpoint_step"] = step
        return uploaded.__dict__

    def dataset_snapshot(self, directory: Path) -> dict[str, Any]:
        token = _required("HF_TOKEN")
        hf = self.core["huggingface"]
        uploaded = HuggingFaceDatasetStore(
            repo_id=hf["dataset_repo"],
            snapshot_prefix=hf["dataset_prefix"],
            revision=hf["dataset_revision"],
            token=token,
        ).upload(
            directory,
            run_id=self.run_id,
            provenance_path=self._index_path(),
        )
        if self.run is not None:
            self.run.summary["dataset_snapshot_uri"] = uploaded.uri
        return uploaded.__dict__

    def _publish_results(self) -> str | None:
        if not self.publish_results:
            return None
        store = self.result_store
        if store is None:
            github = self.core["github"]
            store = GitHubApiResultStore(
                repo=github["repo"],
                branch=github["results_branch"],
                results_prefix=github["results_prefix"],
                token=_required("GITHUB_TOKEN"),
            )
        return str(store.upload_bundle(self.bundle_dir, run_id=self.run_id))

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        publish_error: BaseException | None = None
        published_commit: str | None = None
        try:
            published_commit = self._publish_results()
        except BaseException as error:
            publish_error = error
        if self.run is not None:
            if published_commit:
                self.run.summary["github_results_commit"] = published_commit
            if publish_error is not None:
                self.run.summary["github_results_error"] = str(publish_error)
            self.run.finish(
                exit_code=1 if exc_type is not None or publish_error is not None else 0
            )
            self.run = None
        if self._tempdir is not None:
            self._tempdir.cleanup()
            self._tempdir = None
        if publish_error is not None and exc_type is None:
            raise publish_error
