from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
import signal
import struct
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomli_w

from .machines import MachineProfile
from .spec import ExperimentSpec


class BackendError(RuntimeError):
    pass


REMOTE_BOOTSTRAP = r"""
import hashlib
import io
import json
import os
import pathlib
import shutil
import signal
import struct
import subprocess
import sys
import tarfile

stream = sys.stdin.buffer
header_size = struct.unpack("!Q", stream.read(8))[0]
payload = json.loads(stream.read(header_size))
archive = stream.read()
env = os.environ.copy()
env.update(payload["env"])
if env.get("WANDB_MODE", "").lower() != "online":
    raise SystemExit("W&B must be online")
if env.get("WANDB_DISABLED", "").lower() in {"1", "true", "yes"}:
    raise SystemExit("W&B cannot be disabled")

if payload["source_sync"] == "archive":
    if hashlib.sha256(archive).hexdigest() != payload["archive_sha256"]:
        raise SystemExit("source archive checksum mismatch")
    workdir = pathlib.Path(payload["checkout"]).expanduser()
    if workdir.name != "source" or workdir.parent.name != payload["run_id"]:
        raise SystemExit("unsafe source archive checkout path")
    incoming = workdir.with_name("source.incoming-" + str(os.getpid()))
    if incoming.exists():
        shutil.rmtree(incoming)
    incoming.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as bundle:
        for member in bundle.getmembers():
            path = pathlib.PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise SystemExit("unsafe source archive member")
            if member.issym() or member.islnk():
                raise SystemExit("source archive links are not supported")
        bundle.extractall(incoming)
    (incoming / ".axiotic-source-commit").write_text(payload["commit"] + "\n")
    if workdir.exists():
        shutil.rmtree(workdir)
    incoming.replace(workdir)
elif payload["source_sync"] == "git":
    workdir = pathlib.Path(payload["checkout"]).expanduser()
    workdir.parent.mkdir(parents=True, exist_ok=True)
    if not (workdir / ".git").exists():
        subprocess.run(
            ["git", "clone", "--no-checkout", payload["clone_url"], str(workdir)],
            check=True,
        )
    subprocess.run(
        ["git", "-C", str(workdir), "fetch", "--depth=1", "origin", payload["commit"]],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(workdir), "checkout", "--detach", payload["commit"]],
        check=True,
    )
else:
    workdir = pathlib.Path(payload["workdir"]).expanduser()

if payload["source_sync"] == "archive":
    head = (workdir / ".axiotic-source-commit").read_text().strip()
else:
    head = subprocess.run(
        ["git", "-C", str(workdir), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
if head != payload["commit"]:
    raise SystemExit(
        "source commit mismatch: expected "
        + payload["commit"]
        + ", observed "
        + head
    )

process = subprocess.Popen(
    payload["command"],
    cwd=workdir,
    env=env,
    start_new_session=True,
)
try:
    returncode = process.wait(timeout=payload["timeout_seconds"])
except subprocess.TimeoutExpired:
    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
    raise SystemExit(124)
raise SystemExit(returncode)
""".strip()


@dataclass(frozen=True)
class LaunchResult:
    returncode: int
    compute_uri: str
    elapsed_seconds: float


def _git_head(path: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise BackendError(completed.stderr.strip() or f"not a Git checkout: {path}")
    return completed.stdout.strip()


def _prepare_local_source(spec: ExperimentSpec, profile: MachineProfile) -> Path:
    if spec.execution.source_sync == "verify":
        workdir = profile.source_path(spec.source.repo_dir)
    else:
        workdir = Path(profile.remote_checkout(spec.run.id)).expanduser()
        if not (workdir / ".git").is_dir():
            workdir.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", "--no-checkout", spec.source.clone_url, str(workdir)],
                check=True,
            )
        subprocess.run(
            [
                "git",
                "-C",
                str(workdir),
                "fetch",
                "--depth=1",
                "origin",
                spec.source.commit,
            ],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(workdir), "checkout", "--detach", spec.source.commit],
            check=True,
        )
    observed = _git_head(workdir)
    if observed != spec.source.commit:
        raise BackendError(
            "source commit mismatch: "
            f"expected {spec.source.commit}, observed {observed}"
        )
    return workdir


def launch_local(
    spec: ExperimentSpec,
    profile: MachineProfile,
    *,
    runtime_env: dict[str, str],
    credentials: dict[str, str],
) -> LaunchResult:
    workdir = _prepare_local_source(spec, profile)
    env = os.environ.copy()
    env.update(runtime_env)
    env.update(credentials)
    started = time.monotonic()
    process = subprocess.Popen(
        list(spec.run.command),
        cwd=workdir,
        env=env,
        start_new_session=True,
    )
    try:
        returncode = process.wait(timeout=spec.execution.max_hours * 3600)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        returncode = 124
    elapsed = time.monotonic() - started
    return LaunchResult(
        returncode=returncode,
        compute_uri=f"machine://local/run/{spec.run.id}",
        elapsed_seconds=elapsed,
    )


def ssh_payload(
    spec: ExperimentSpec,
    profile: MachineProfile,
    *,
    runtime_env: dict[str, str],
    credentials: dict[str, str],
) -> dict[str, Any]:
    return {
        "run_id": spec.run.id,
        "command": list(spec.run.command),
        "env": {**runtime_env, **credentials},
        "timeout_seconds": spec.execution.max_hours * 3600,
        "source_sync": spec.execution.source_sync,
        "clone_url": spec.source.clone_url,
        "commit": spec.source.commit,
        "workdir": profile.source_path_text(spec.source.repo_dir),
        "checkout": profile.remote_checkout(spec.run.id),
        "archive_sha256": None,
    }


def source_archive(spec: ExperimentSpec, profile: MachineProfile) -> bytes:
    source = profile.source_path(spec.source.repo_dir)
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(source),
            "archive",
            "--format=tar.gz",
            spec.source.commit,
        ],
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        raise BackendError(
            completed.stderr.decode(errors="replace").strip()
            or f"could not archive {spec.source.commit} from {source}"
        )
    return completed.stdout


def encode_ssh_request(payload: dict[str, Any], archive: bytes = b"") -> bytes:
    header = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return struct.pack("!Q", len(header)) + header + archive


def ssh_command(profile: MachineProfile) -> list[str]:
    if profile.transport != "ssh" or profile.target is None:
        raise BackendError("SSH backend requires an SSH machine profile")
    remote_command = "python3 -c " + shlex.quote(REMOTE_BOOTSTRAP)
    return ["ssh", profile.target, remote_command]


def launch_ssh(
    spec: ExperimentSpec,
    profile: MachineProfile,
    *,
    runtime_env: dict[str, str],
    credentials: dict[str, str],
) -> LaunchResult:
    payload = ssh_payload(
        spec,
        profile,
        runtime_env=runtime_env,
        credentials=credentials,
    )
    archive = b""
    if spec.execution.source_sync == "archive":
        archive = source_archive(spec, profile)
        payload["archive_sha256"] = hashlib.sha256(archive).hexdigest()
    started = time.monotonic()
    completed = subprocess.run(
        ssh_command(profile),
        input=encode_ssh_request(payload, archive),
        check=False,
    )
    elapsed = time.monotonic() - started
    return LaunchResult(
        returncode=completed.returncode,
        compute_uri=f"ssh://{profile.target}/run/{spec.run.id}",
        elapsed_seconds=elapsed,
    )


def runpod_mapping(spec: ExperimentSpec) -> dict[str, Any]:
    if spec.runpod is None:
        raise BackendError("RunPod backend requires [runpod]")
    return {
        "run": {
            "id": spec.run.id,
            "name": spec.run.name,
            "command": list(spec.run.command),
            "image": spec.runpod.image,
            "seed": spec.run.seed,
            "phase": spec.run.phase,
            "variant": spec.run.variant,
            "modality": spec.run.modality,
            "dataset": spec.run.dataset,
            "reason": spec.run.reason,
            "notes": spec.run.notes,
        },
        "capacity": {
            "gpu_type_ids": list(spec.resources.gpu_type_ids),
            "gpu_count": spec.resources.gpus,
            "max_hours": spec.execution.max_hours,
            "max_cost_usd": spec.runpod.max_cost_usd,
            "minimum_balance_reserve_usd": (spec.runpod.minimum_balance_reserve_usd),
            "cloud_type": spec.runpod.cloud_type,
            "interruptible": spec.runpod.interruptible,
            "container_disk_gb": spec.runpod.container_disk_gb,
            "volume_gb": spec.runpod.volume_gb,
            "volume_mount_path": spec.runpod.volume_mount_path,
            "ports": list(spec.runpod.ports),
            **(
                {"container_registry_auth_id": (spec.runpod.container_registry_auth_id)}
                if spec.runpod.container_registry_auth_id
                else {}
            ),
        },
        "wandb": {
            "entity": spec.wandb.entity,
            "project": spec.wandb.project,
            "mode": "online",
        },
        "huggingface": {
            "repo_id": spec.huggingface.checkpoint_repo,
            "repo_type": "model",
            "checkpoint_prefix": spec.huggingface.checkpoint_prefix,
            "dataset_repo_id": spec.huggingface.dataset_repo,
            "dataset_prefix": spec.huggingface.dataset_prefix,
            "revision": spec.huggingface.revision,
            "dataset_revision": spec.huggingface.dataset_revision,
        },
        "github": {
            "repo": spec.github.repo,
            "branch": spec.github.results_branch,
            "results_prefix": spec.github.results_prefix,
        },
        "source": {
            "repo_url": spec.source.repo_url,
            "branch": spec.source.branch,
            "commit": spec.source.commit,
        },
    }


def write_runpod_adapter_spec(spec: ExperimentSpec, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(tomli_w.dumps(runpod_mapping(spec)).encode("utf-8"))
    return path


def runpod_command(
    spec_path: Path,
    bundle_dir: Path,
    butler_project: str,
    *,
    execute: bool,
) -> list[str]:
    executable = shutil.which("runpod-capacity")
    if executable is None:
        fallback = Path(os.environ.get("RUNPOD_CAPACITY_CLI", ""))
        if not fallback.is_file():
            if execute:
                raise BackendError("runpod-capacity executable not found")
            command = ["runpod-capacity"]
        else:
            command = ["python3", str(fallback)]
    else:
        command = [executable]
    command.extend(
        [
            "launch",
            str(spec_path),
            "--output",
            str(bundle_dir),
            "--butler-project",
            butler_project,
        ]
    )
    if execute:
        command.append("--execute")
    return command
