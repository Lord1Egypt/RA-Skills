from __future__ import annotations

import re
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class SpecError(ValueError):
    """Raised when an experiment specification violates a hard invariant."""


_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{2,127}$")
_COMMIT = re.compile(r"^[0-9a-fA-F]{7,64}$")
_SECRET_KEY = re.compile(r"(?:TOKEN|PASSWORD|SECRET|API_KEY|PRIVATE_KEY)$")
_SECRET_VALUE = (
    re.compile(r"\brpa_[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
)


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name)
    if not isinstance(value, Mapping):
        raise SpecError(f"missing [{name}] section")
    return value


def _optional_section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name, {})
    if not isinstance(value, Mapping):
        raise SpecError(f"[{name}] must be a table")
    return value


def _required(raw: Mapping[str, Any], field: str, section: str) -> Any:
    value = raw.get(field)
    if value is None or value == "" or value == []:
        raise SpecError(f"missing [{section}].{field}")
    return value


def _string_tuple(
    raw: Mapping[str, Any],
    field: str,
    section: str,
    *,
    required: bool = False,
) -> tuple[str, ...]:
    value = _required(raw, field, section) if required else raw.get(field, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SpecError(f"[{section}].{field} must be an array of strings")
    return tuple(value)


@dataclass(frozen=True)
class RunSpec:
    id: str
    name: str
    command: tuple[str, ...]
    seed: int
    phase: str
    variant: str
    modality: str
    dataset: str
    reason: str
    notes: str

    @property
    def tags(self) -> tuple[str, ...]:
        return (
            f"phase:{self.phase}",
            f"variant:{self.variant}",
            f"modality:{self.modality}",
            f"dataset:{self.dataset}",
            f"seed:{self.seed}",
        )


@dataclass(frozen=True)
class ExecutionSpec:
    machine: str
    max_hours: float
    public_env: dict[str, str]
    source_sync: str


@dataclass(frozen=True)
class ResourceSpec:
    gpus: int
    cpus: int
    memory_gb: int
    gpu_type_ids: tuple[str, ...]
    estimated_cost: float | None
    currency: str
    disk_gb: int


@dataclass(frozen=True)
class WandbSpec:
    entity: str
    project: str
    mode: str


@dataclass(frozen=True)
class HuggingFaceSpec:
    checkpoint_repo: str
    dataset_repo: str
    checkpoint_prefix: str
    dataset_prefix: str
    revision: str
    dataset_revision: str


@dataclass(frozen=True)
class GitHubSpec:
    repo: str
    results_branch: str
    results_prefix: str


@dataclass(frozen=True)
class SourceSpec:
    repo_url: str
    clone_url: str
    repo_dir: str
    branch: str
    commit: str

    @property
    def commit_url(self) -> str:
        return f"{self.repo_url.rstrip('/')}/commit/{self.commit}"


@dataclass(frozen=True)
class RunPodSpec:
    image: str
    max_cost_usd: float
    minimum_balance_reserve_usd: float
    cloud_type: str
    interruptible: bool
    container_disk_gb: int
    volume_gb: int
    volume_mount_path: str
    ports: tuple[str, ...]
    container_registry_auth_id: str | None


@dataclass(frozen=True)
class ExperimentSpec:
    run: RunSpec
    execution: ExecutionSpec
    resources: ResourceSpec
    wandb: WandbSpec
    huggingface: HuggingFaceSpec
    github: GitHubSpec
    source: SourceSpec
    runpod: RunPodSpec | None

    @classmethod
    def load(cls, path: str | Path) -> ExperimentSpec:
        with Path(path).open("rb") as handle:
            return cls.from_mapping(tomllib.load(handle))

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> ExperimentSpec:
        run = _section(raw, "run")
        execution = _section(raw, "execution")
        resources = _section(raw, "resources")
        wandb = _section(raw, "wandb")
        huggingface = _section(raw, "huggingface")
        github = _section(raw, "github")
        source = _section(raw, "source")
        runpod = _optional_section(raw, "runpod")

        run_id = str(_required(run, "id", "run"))
        if not _RUN_ID.fullmatch(run_id):
            raise SpecError(
                "[run].id must be 3-128 characters using letters, digits, "
                "'.', '_' or '-'"
            )
        command = _string_tuple(run, "command", "run", required=True)
        if not command:
            raise SpecError("[run].command must not be empty")

        max_hours = float(_required(execution, "max_hours", "execution"))
        if max_hours <= 0:
            raise SpecError("[execution].max_hours must be positive")
        source_sync = str(execution.get("source_sync", "verify")).lower()
        if source_sync not in {"verify", "git", "archive"}:
            raise SpecError(
                "[execution].source_sync must be 'verify', 'git', or 'archive'"
            )
        public_env_raw = execution.get("env", {})
        if not isinstance(public_env_raw, Mapping) or not all(
            isinstance(key, str) and isinstance(value, (str, int, float, bool))
            for key, value in public_env_raw.items()
        ):
            raise SpecError("[execution].env must contain scalar public values")
        public_env = {key: str(value) for key, value in public_env_raw.items()}
        for key, value in public_env.items():
            if _SECRET_KEY.search(key.upper()):
                raise SpecError(
                    f"[execution].env cannot contain credential-like key {key!r}"
                )
            if any(pattern.search(value) for pattern in _SECRET_VALUE):
                raise SpecError(
                    f"[execution].env contains credential-like material in {key!r}"
                )

        gpus = int(resources.get("gpus", 0))
        cpus = int(resources.get("cpus", 1))
        memory_gb = int(resources.get("memory_gb", 1))
        if gpus < 0 or cpus <= 0 or memory_gb <= 0:
            raise SpecError("[resources] values must be positive (gpus may be zero)")
        gpu_type_ids = _string_tuple(resources, "gpu_type_ids", "resources")
        estimated_cost_raw = resources.get("estimated_cost")
        estimated_cost = (
            None if estimated_cost_raw is None else float(estimated_cost_raw)
        )
        if estimated_cost is not None and estimated_cost < 0:
            raise SpecError("[resources].estimated_cost must be non-negative")
        currency = str(resources.get("currency", "GBP")).strip().upper()
        if not re.fullmatch(r"[A-Z]{3}", currency):
            raise SpecError("[resources].currency must be a three-letter code")
        disk_gb = int(resources.get("disk_gb", 0))
        if disk_gb < 0:
            raise SpecError("[resources].disk_gb must be non-negative")

        mode = str(_required(wandb, "mode", "wandb")).lower()
        if mode != "online":
            raise SpecError("W&B mode must be online")

        commit = str(_required(source, "commit", "source"))
        if not _COMMIT.fullmatch(commit):
            raise SpecError("[source].commit must be a 7-64 character Git SHA")
        repo_url = str(_required(source, "repo_url", "source"))
        clone_url = str(source.get("clone_url", repo_url))

        machine = str(_required(execution, "machine", "execution"))
        parsed_runpod: RunPodSpec | None = None
        if machine == "runpod":
            if not runpod:
                raise SpecError("machine 'runpod' requires a [runpod] section")
            if gpus <= 0:
                raise SpecError("RunPod execution requires at least one GPU")
            if not gpu_type_ids:
                raise SpecError("RunPod execution requires [resources].gpu_type_ids")
            max_cost = float(_required(runpod, "max_cost_usd", "runpod"))
            if max_cost <= 0:
                raise SpecError("[runpod].max_cost_usd must be positive")
            cloud_type = str(runpod.get("cloud_type", "SECURE")).upper()
            if cloud_type not in {"SECURE", "COMMUNITY"}:
                raise SpecError("[runpod].cloud_type must be SECURE or COMMUNITY")
            parsed_runpod = RunPodSpec(
                image=str(_required(runpod, "image", "runpod")),
                max_cost_usd=max_cost,
                minimum_balance_reserve_usd=float(
                    runpod.get("minimum_balance_reserve_usd", 0.0)
                ),
                cloud_type=cloud_type,
                interruptible=bool(runpod.get("interruptible", False)),
                container_disk_gb=int(runpod.get("container_disk_gb", 50)),
                volume_gb=int(runpod.get("volume_gb", 20)),
                volume_mount_path=str(runpod.get("volume_mount_path", "/workspace")),
                ports=_string_tuple(runpod, "ports", "runpod"),
                container_registry_auth_id=(
                    str(runpod["container_registry_auth_id"])
                    if runpod.get("container_registry_auth_id")
                    else None
                ),
            )

        return cls(
            run=RunSpec(
                id=run_id,
                name=str(_required(run, "name", "run")),
                command=command,
                seed=int(_required(run, "seed", "run")),
                phase=str(_required(run, "phase", "run")),
                variant=str(_required(run, "variant", "run")),
                modality=str(_required(run, "modality", "run")),
                dataset=str(_required(run, "dataset", "run")),
                reason=str(_required(run, "reason", "run")),
                notes=str(_required(run, "notes", "run")),
            ),
            execution=ExecutionSpec(
                machine=machine,
                max_hours=max_hours,
                public_env=public_env,
                source_sync=source_sync,
            ),
            resources=ResourceSpec(
                gpus=gpus,
                cpus=cpus,
                memory_gb=memory_gb,
                gpu_type_ids=gpu_type_ids,
                estimated_cost=estimated_cost,
                currency=currency,
                disk_gb=disk_gb,
            ),
            wandb=WandbSpec(
                entity=str(_required(wandb, "entity", "wandb")),
                project=str(_required(wandb, "project", "wandb")),
                mode=mode,
            ),
            huggingface=HuggingFaceSpec(
                checkpoint_repo=str(
                    _required(huggingface, "checkpoint_repo", "huggingface")
                ),
                dataset_repo=str(_required(huggingface, "dataset_repo", "huggingface")),
                checkpoint_prefix=str(
                    huggingface.get("checkpoint_prefix", "checkpoints")
                ),
                dataset_prefix=str(huggingface.get("dataset_prefix", "snapshots")),
                revision=str(huggingface.get("revision", "main")),
                dataset_revision=str(huggingface.get("dataset_revision", "main")),
            ),
            github=GitHubSpec(
                repo=str(_required(github, "repo", "github")),
                results_branch=str(_required(github, "results_branch", "github")),
                results_prefix=str(github.get("results_prefix", "experiments/results")),
            ),
            source=SourceSpec(
                repo_url=repo_url,
                clone_url=clone_url,
                repo_dir=str(_required(source, "repo_dir", "source")),
                branch=str(_required(source, "branch", "source")),
                commit=commit,
            ),
            runpod=parsed_runpod,
        )

    def core_manifest(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "run_id": self.run.id,
            "run": {
                "name": self.run.name,
                "command": list(self.run.command),
                "seed": self.run.seed,
                "phase": self.run.phase,
                "variant": self.run.variant,
                "modality": self.run.modality,
                "dataset": self.run.dataset,
                "reason": self.run.reason,
                "notes": self.run.notes,
                "tags": list(self.run.tags),
            },
            "execution": {
                "machine": self.execution.machine,
                "max_hours": self.execution.max_hours,
                "source_sync": self.execution.source_sync,
                "public_env": self.execution.public_env,
            },
            "resources": {
                "gpus": self.resources.gpus,
                "cpus": self.resources.cpus,
                "memory_gb": self.resources.memory_gb,
                "gpu_type_ids": list(self.resources.gpu_type_ids),
                "estimated_cost": self.resources.estimated_cost,
                "currency": self.resources.currency,
                "disk_gb": self.resources.disk_gb,
            },
            "wandb": {
                "entity": self.wandb.entity,
                "project": self.wandb.project,
                "mode": "online",
                "run_id": self.run.id,
                "resume": "allow",
            },
            "huggingface": {
                "checkpoint_repo": self.huggingface.checkpoint_repo,
                "checkpoint_prefix": self.huggingface.checkpoint_prefix,
                "revision": self.huggingface.revision,
                "dataset_repo": self.huggingface.dataset_repo,
                "dataset_prefix": self.huggingface.dataset_prefix,
                "dataset_revision": self.huggingface.dataset_revision,
            },
            "github": {
                "repo": self.github.repo,
                "results_branch": self.github.results_branch,
                "results_prefix": self.github.results_prefix,
            },
            "source": {
                "repo_url": self.source.repo_url,
                "clone_url": self.source.clone_url,
                "repo_dir": self.source.repo_dir,
                "branch": self.source.branch,
                "commit": self.source.commit,
                "commit_url": self.source.commit_url,
            },
        }
