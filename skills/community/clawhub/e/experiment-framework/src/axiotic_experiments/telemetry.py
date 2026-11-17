from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .results import append_metric
from .run_context import RunContextMetadata, attach_run_context
from .spec import ExperimentSpec


class WandbConfigurationError(RuntimeError):
    pass


def _wandb_module(module: Any | None = None) -> Any:
    if module is not None:
        return module
    try:
        import wandb
    except ImportError as exc:
        raise WandbConfigurationError("install the 'wandb' package") from exc
    return wandb


def _require_online() -> None:
    mode = os.environ.get("WANDB_MODE", "online").lower()
    disabled = os.environ.get("WANDB_DISABLED", "").lower() in {"1", "true", "yes"}
    if mode != "online" or disabled:
        raise WandbConfigurationError("W&B must be enabled in online mode")
    if not os.environ.get("WANDB_API_KEY"):
        raise WandbConfigurationError("WANDB_API_KEY is required")


def open_run(
    spec: ExperimentSpec,
    *,
    core: dict[str, Any],
    wandb_module: Any | None = None,
) -> Any:
    _require_online()
    wandb = _wandb_module(wandb_module)
    os.environ["WANDB_MODE"] = "online"
    run = wandb.init(
        entity=spec.wandb.entity,
        project=spec.wandb.project,
        id=spec.run.id,
        name=spec.run.name,
        notes=spec.run.notes,
        tags=list(spec.run.tags),
        job_type=spec.run.phase,
        resume="allow",
        mode="online",
        config=core,
    )
    attach_run_context(run, RunContextMetadata.from_spec(spec))
    return run


def birth_run(
    spec: ExperimentSpec,
    *,
    core: dict[str, Any],
    machine: str,
    bundle_uri: str,
    wandb_module: Any | None = None,
) -> str:
    run = open_run(spec, core=core, wandb_module=wandb_module)
    try:
        run.summary["axiotic_dispatch_machine"] = machine
        run.summary["axiotic_bundle_uri"] = bundle_uri
        run.summary["axiotic_lifecycle"] = "dispatched"
        return str(run.url)
    finally:
        run.finish(exit_code=0)


def finish_run(
    spec: ExperimentSpec,
    *,
    core: dict[str, Any],
    exit_code: int,
    compute_uri: str,
    elapsed_seconds: float,
    wandb_module: Any | None = None,
) -> None:
    run = open_run(spec, core=core, wandb_module=wandb_module)
    try:
        run.summary["axiotic_compute_uri"] = compute_uri
        run.summary["axiotic_elapsed_seconds"] = elapsed_seconds
        run.summary["axiotic_lifecycle"] = "completed" if exit_code == 0 else "failed"
    finally:
        run.finish(exit_code=exit_code)


class ExperimentRun:
    """Trainer-side W&B and replayable-metrics context."""

    def __init__(
        self,
        spec: ExperimentSpec,
        *,
        metrics_path: Path,
        core: dict[str, Any] | None = None,
        wandb_module: Any | None = None,
    ):
        self.spec = spec
        self.metrics_path = metrics_path
        self.core = core or spec.core_manifest()
        self.wandb_module = wandb_module
        self.run: Any | None = None

    def __enter__(self) -> ExperimentRun:
        self.run = open_run(
            self.spec,
            core=self.core,
            wandb_module=self.wandb_module,
        )
        return self

    def log(self, metrics: dict[str, Any], *, step: int) -> None:
        if self.run is None:
            raise WandbConfigurationError("experiment run is not open")
        append_metric(self.metrics_path, step=step, metrics=metrics)
        self.run.log(metrics, step=step)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object,
    ) -> None:
        if self.run is not None:
            self.run.finish(exit_code=1 if exc_type is not None else 0)
            self.run = None
