from __future__ import annotations

import argparse
import contextlib
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .backends import (
    BackendError,
    launch_local,
    launch_ssh,
    runpod_command,
    ssh_command,
    ssh_payload,
    write_runpod_adapter_spec,
)
from .credentials import CredentialError, redact, resolve_credentials
from .environment import build_runtime_environment
from .github_store import GitHubApiResultStore, GitHubResultStore
from .governance import Butler, ButlerError
from .hf_store import HuggingFaceCheckpointStore, HuggingFaceDatasetStore
from .machines import MachineError, MachineProfile, MachineRegistry
from .manifest import sha256_json, validate_sealed_graph, write_bundle, write_json
from .provenance import build_graph
from .results import replay_metrics
from .spec import ExperimentSpec, SpecError
from .telemetry import (
    WandbConfigurationError,
    birth_run,
    finish_run,
    open_run,
)


class CliError(RuntimeError):
    pass


def _json(value: Any) -> None:
    print(json.dumps(redact(value), indent=2, sort_keys=True))


def _machines_path(value: Path | None) -> Path:
    if value is not None:
        return value.expanduser().absolute()
    configured = os.environ.get("AXIOTIC_MACHINES_FILE")
    if configured:
        return Path(configured).expanduser().absolute()
    cwd = Path("machines.toml").absolute()
    if cwd.is_file():
        return cwd
    source = Path(__file__).resolve().parents[2] / "machines.toml"
    if source.is_file():
        return source
    raise CliError("machines.toml not found; pass --machines")


def _load(
    spec_path: Path,
    machines_path: Path | None,
) -> tuple[ExperimentSpec, MachineProfile, MachineRegistry]:
    spec = ExperimentSpec.load(spec_path)
    registry = MachineRegistry.load(_machines_path(machines_path))
    profile = registry.resolve(spec.execution.machine)
    if spec.execution.machine == "runpod" and profile.transport != "runpod":
        raise CliError("machine 'runpod' must resolve to the RunPod transport")
    return spec, profile, registry


def _bundle_uri(spec: ExperimentSpec) -> str:
    return (
        f"https://github.com/{spec.github.repo}/tree/"
        f"{spec.github.results_branch}/{spec.github.results_prefix.strip('/')}/"
        f"{spec.run.id}"
    )


def _launch_plan(
    spec: ExperimentSpec,
    profile: MachineProfile,
    runtime_env: dict[str, str],
) -> dict[str, Any]:
    if profile.transport == "local":
        execution = {
            "transport": "local",
            "workdir": str(profile.source_path(spec.source.repo_dir)),
            "command": list(spec.run.command),
        }
    elif profile.transport == "ssh":
        execution = {
            "transport": "ssh",
            "target": profile.target,
            "workdir": profile.source_path_text(spec.source.repo_dir),
            "checkout": profile.remote_checkout(spec.run.id),
            "source_sync": spec.execution.source_sync,
            "command": list(spec.run.command),
            "secret_transport": "encrypted-ssh-stdin-memory-only",
        }
    else:
        execution = {
            "transport": "runpod",
            "gpu_type_ids": list(spec.resources.gpu_type_ids),
            "image": spec.runpod.image if spec.runpod else None,
            "delegates_to": "runpod-capacity",
        }
    return {
        "schema_version": "1.0",
        "run_id": spec.run.id,
        "machine": profile.name,
        "execution": execution,
        "resources": {
            "gpus": spec.resources.gpus,
            "cpus": spec.resources.cpus,
            "memory_gb": spec.resources.memory_gb,
            "max_hours": spec.execution.max_hours,
        },
        "runtime_environment": runtime_env,
        "required_credentials": [
            "WANDB_API_KEY",
            "HF_TOKEN",
            "GITHUB_TOKEN",
            *(["RUNPOD_API_KEY"] if profile.transport == "runpod" else []),
        ],
        "credentials_embedded": False,
    }


def _plan(
    spec: ExperimentSpec,
    profile: MachineProfile,
    output: Path,
) -> dict[str, Any]:
    core = spec.core_manifest()
    bundle_uri = _bundle_uri(spec)
    graph = build_graph(
        spec,
        profile,
        core_sha256=sha256_json(core),
    )
    planned_index = graph.seal()
    runtime_env = build_runtime_environment(
        spec,
        core=core,
        bundle_uri=bundle_uri,
        artifact_index=planned_index,
    )
    launch_plan = _launch_plan(spec, profile, runtime_env)
    hashes = write_bundle(output, core, graph, launch_plan=launch_plan)
    runpod_spec: str | None = None
    if profile.transport == "runpod":
        adapter = write_runpod_adapter_spec(spec, output / "runpod-adapter.toml")
        runpod_spec = str(adapter)
    return {
        "valid": True,
        "dry_run": True,
        "run_id": spec.run.id,
        "machine": profile.name,
        "transport": profile.transport,
        "bundle": str(output.absolute()),
        "bundle_uri": bundle_uri,
        "core_sha256": hashes.core_sha256,
        "index_sha256": hashes.index_sha256,
        "runpod_adapter_spec": runpod_spec,
    }


def _cmd_validate(args: argparse.Namespace) -> int:
    spec, profile, registry = _load(args.spec, args.machines)
    _json(
        {
            "valid": True,
            "run_id": spec.run.id,
            "machine": profile.name,
            "transport": profile.transport,
            "machines": sorted(registry.profiles),
        }
    )
    return 0


def _cmd_plan(args: argparse.Namespace) -> int:
    spec, profile, _ = _load(args.spec, args.machines)
    _json(_plan(spec, profile, args.output))
    return 0


def _rewrite_observed_index(
    spec: ExperimentSpec,
    profile: MachineProfile,
    bundle: Path,
    *,
    compute_uri: str,
    hf_revision: str | None = None,
    hf_dataset_revision: str | None = None,
    github_commit: str | None = None,
) -> dict[str, Any]:
    core = json.loads((bundle / "run-core.json").read_text())
    index = build_graph(
        spec,
        profile,
        core_sha256=sha256_json(core),
        compute_uri=compute_uri,
        hf_revision=hf_revision,
        hf_dataset_revision=hf_dataset_revision,
        github_commit=github_commit,
    ).seal()
    validate_sealed_graph(index)
    write_json(bundle / "artifact-index.json", index)
    return index


def _cmd_launch(args: argparse.Namespace) -> int:
    spec, profile, _ = _load(args.spec, args.machines)
    plan = _plan(spec, profile, args.output)
    if not args.execute:
        if profile.transport == "ssh":
            core = spec.core_manifest()
            runtime_env = build_runtime_environment(
                spec,
                core=core,
                bundle_uri=_bundle_uri(spec),
                artifact_index=json.loads(
                    (args.output / "artifact-index.json").read_text()
                ),
            )
            preview_payload = ssh_payload(
                spec,
                profile,
                runtime_env=runtime_env,
                credentials={
                    "WANDB_API_KEY": "[runtime]",
                    "HF_TOKEN": "[runtime]",
                    "GITHUB_TOKEN": "[runtime]",
                },
            )
            plan["ssh_command"] = ssh_command(profile)
            plan["ssh_payload"] = preview_payload
        elif profile.transport == "runpod":
            plan["delegate_command"] = runpod_command(
                args.output / "runpod-adapter.toml",
                args.output / "runpod",
                args.butler_project,
                execute=False,
            )
        _json(plan)
        return 0

    if profile.transport == "runpod":
        command = runpod_command(
            args.output / "runpod-adapter.toml",
            args.output / "runpod",
            args.butler_project,
            execute=True,
        )
        completed = subprocess.run(command, check=False)
        return completed.returncode

    credentials = resolve_credentials(profile)
    requested_gpu_hours = spec.resources.gpus * spec.execution.max_hours
    butler = Butler()
    reservation = None
    if requested_gpu_hours:
        reservation = butler.gpu_reserve(
            project=args.butler_project,
            job=spec.run.id,
            gpus=spec.resources.gpus,
            hours=spec.execution.max_hours,
            estimated_cost=spec.resources.estimated_cost,
            currency=spec.resources.currency,
            disk_gb=spec.resources.disk_gb,
        )

    core = spec.core_manifest()
    started = time.monotonic()
    result = None
    launch_attempted = False
    launch_error: BaseException | None = None
    try:
        bundle_uri = _bundle_uri(spec)
        runtime_env = build_runtime_environment(
            spec,
            core=core,
            bundle_uri=bundle_uri,
            artifact_index=json.loads(
                (args.output / "artifact-index.json").read_text()
            ),
        )
        birth_run(
            spec,
            core=core,
            machine=profile.name,
            bundle_uri=bundle_uri,
        )
        launch_attempted = True
        if profile.transport == "local":
            result = launch_local(
                spec,
                profile,
                runtime_env=runtime_env,
                credentials=credentials,
            )
        elif profile.transport == "ssh":
            result = launch_ssh(
                spec,
                profile,
                runtime_env=runtime_env,
                credentials=credentials,
            )
        else:
            raise CliError(f"unsupported transport: {profile.transport}")
        _rewrite_observed_index(
            spec,
            profile,
            args.output,
            compute_uri=result.compute_uri,
        )
        result_store = GitHubApiResultStore(
            repo=spec.github.repo,
            branch=spec.github.results_branch,
            results_prefix=spec.github.results_prefix,
            token=credentials["GITHUB_TOKEN"],
        )
        core_commit = result_store.upload_file(
            args.output / "run-core.json",
            run_id=spec.run.id,
        )
        final_index = _rewrite_observed_index(
            spec,
            profile,
            args.output,
            compute_uri=result.compute_uri,
            github_commit=core_commit,
        )
        index_commit = result_store.upload_file(
            args.output / "artifact-index.json",
            run_id=spec.run.id,
        )
        finish_run(
            spec,
            core=core,
            exit_code=result.returncode,
            compute_uri=result.compute_uri,
            elapsed_seconds=result.elapsed_seconds,
        )
        _json(
            {
                "run_id": spec.run.id,
                "returncode": result.returncode,
                "compute_uri": result.compute_uri,
                "elapsed_seconds": result.elapsed_seconds,
                "github_bundle_commit": core_commit,
                "github_index_commit": index_commit,
                "index_sha256": sha256_json(final_index),
            }
        )
        return result.returncode
    except BaseException as exc:
        launch_error = exc
        elapsed = time.monotonic() - started
        with contextlib.suppress(Exception):
            finish_run(
                spec,
                core=core,
                exit_code=1,
                compute_uri=f"{profile.transport}://{profile.name}/failed/{spec.run.id}",
                elapsed_seconds=elapsed,
            )
        raise
    finally:
        elapsed = (
            result.elapsed_seconds if result is not None else time.monotonic() - started
        )
        if reservation is not None:
            actual_gpu_hours = (
                spec.resources.gpus * elapsed / 3600 if launch_attempted else 0.0
            )
            actual_cost = spec.resources.estimated_cost if launch_attempted else 0.0
            outcome = (
                "failed"
                if launch_error is not None or result is None or result.returncode != 0
                else "completed"
            )
            try:
                butler.gpu_reconcile(
                    project=args.butler_project,
                    reservation_id=reservation.reservation_id,
                    actual_gpu_hours=actual_gpu_hours,
                    actual_cost=actual_cost,
                    outcome=outcome,
                    note=(
                        "cost charged at conservative pre-launch estimate"
                        if launch_attempted and actual_cost is not None
                        else ""
                    ),
                )
            except ButlerError:
                if launch_error is None:
                    raise


def _doctor_local(profile: MachineProfile) -> dict[str, Any]:
    return {
        "machine": profile.name,
        "transport": profile.transport,
        "reachable": True,
        "hostname": socket.gethostname(),
        "python3": shutil.which("python3"),
        "git": shutil.which("git"),
        "nvidia_smi": shutil.which("nvidia-smi"),
    }


_REMOTE_DOCTOR = (
    "import json,platform,shutil,socket;"
    "print(json.dumps({'reachable':True,'hostname':socket.gethostname(),"
    "'platform':platform.platform(),'python3':shutil.which('python3'),"
    "'git':shutil.which('git'),'nvidia_smi':shutil.which('nvidia-smi')}))"
)


def _doctor_profile(profile: MachineProfile) -> dict[str, Any]:
    if profile.transport == "local":
        return _doctor_local(profile)
    if profile.transport == "runpod":
        return {
            "machine": profile.name,
            "transport": profile.transport,
            "reachable": shutil.which("runpod-capacity") is not None
            or Path(os.environ.get("RUNPOD_CAPACITY_CLI", "")).is_file(),
        }
    completed = subprocess.run(
        ["ssh", profile.target or "", "python3 -c " + repr(_REMOTE_DOCTOR)],
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if completed.returncode:
        return {
            "machine": profile.name,
            "transport": profile.transport,
            "target": profile.target,
            "reachable": False,
            "error": completed.stderr.strip() or f"SSH exited {completed.returncode}",
        }
    payload = json.loads(completed.stdout)
    return {
        "machine": profile.name,
        "transport": profile.transport,
        "target": profile.target,
        **payload,
    }


def _cmd_doctor(args: argparse.Namespace) -> int:
    registry = MachineRegistry.load(_machines_path(args.machines))
    names = args.machine or sorted(registry.profiles)
    results = [_doctor_profile(registry.resolve(name)) for name in names]
    _json({"machines": results, "healthy": all(item["reachable"] for item in results)})
    return 0 if all(item["reachable"] for item in results) else 1


def _checkpoint_store(spec: ExperimentSpec) -> HuggingFaceCheckpointStore:
    return HuggingFaceCheckpointStore(
        repo_id=spec.huggingface.checkpoint_repo,
        checkpoint_prefix=spec.huggingface.checkpoint_prefix,
        revision=spec.huggingface.revision,
        token=os.environ.get("HF_TOKEN"),
    )


def _dataset_store(spec: ExperimentSpec) -> HuggingFaceDatasetStore:
    return HuggingFaceDatasetStore(
        repo_id=spec.huggingface.dataset_repo,
        snapshot_prefix=spec.huggingface.dataset_prefix,
        revision=spec.huggingface.dataset_revision,
        token=os.environ.get("HF_TOKEN"),
    )


def _cmd_checkpoint_upload(args: argparse.Namespace) -> int:
    spec, _, _ = _load(args.spec, args.machines)
    uploaded = _checkpoint_store(spec).upload(
        args.checkpoint,
        run_id=spec.run.id,
        step=args.step,
        provenance_path=args.index,
    )
    _json(uploaded.__dict__)
    return 0


def _cmd_checkpoint_fetch(args: argparse.Namespace) -> int:
    spec, _, _ = _load(args.spec, args.machines)
    resolved = _checkpoint_store(spec).download_latest(
        run_id=spec.run.id,
        local_dir=args.output,
    )
    _json(
        {
            **resolved.__dict__,
            "path": str(resolved.path),
            "resume_from_checkpoint": str(resolved.path),
        }
    )
    return 0


def _cmd_dataset_upload(args: argparse.Namespace) -> int:
    spec, _, _ = _load(args.spec, args.machines)
    uploaded = _dataset_store(spec).upload(
        args.snapshot,
        run_id=spec.run.id,
        provenance_path=args.index,
    )
    _json(uploaded.__dict__)
    return 0


class _WandbSink:
    def __init__(self, run: Any):
        self.run = run

    def log(self, metrics: dict[str, Any], *, step: int) -> None:
        self.run.log(metrics, step=step)


def _cmd_results_replay(args: argparse.Namespace) -> int:
    spec, _, _ = _load(args.spec, args.machines)
    run = open_run(spec, core=spec.core_manifest())
    try:
        result = replay_metrics(args.metrics, _WandbSink(run))
    finally:
        run.finish(exit_code=0)
    _json(result)
    return 0


def _cmd_publish_results(args: argparse.Namespace) -> int:
    spec, _, _ = _load(args.spec, args.machines)
    if not args.execute:
        _json(
            {
                "dry_run": True,
                "run_id": spec.run.id,
                "repo": spec.github.repo,
                "branch": spec.github.results_branch,
                "bundle": str(args.bundle),
            }
        )
        return 0
    if args.repo_dir:
        store = GitHubResultStore(
            repo_dir=args.repo_dir,
            results_prefix=spec.github.results_prefix,
        )
        destination = store.stage(args.bundle, run_id=spec.run.id)
        commit = store.commit_and_push(
            run_id=spec.run.id,
            branch=spec.github.results_branch,
        )
        _json({"destination": str(destination), "commit": commit})
        return 0
    token = os.environ.get("GITHUB_TOKEN", "")
    store = GitHubApiResultStore(
        repo=spec.github.repo,
        branch=spec.github.results_branch,
        results_prefix=spec.github.results_prefix,
        token=token,
    )
    commit = store.upload_bundle(args.bundle, run_id=spec.run.id)
    _json({"commit": commit})
    return 0


def _cmd_reconcile(args: argparse.Namespace) -> int:
    spec, profile, _ = _load(args.spec, args.machines)
    index = _rewrite_observed_index(
        spec,
        profile,
        args.bundle,
        compute_uri=args.compute_uri,
        hf_revision=args.hf_revision,
        hf_dataset_revision=args.hf_dataset_revision,
        github_commit=args.github_commit,
    )
    _json(
        {
            "run_id": spec.run.id,
            "index": str(args.bundle / "artifact-index.json"),
            "index_sha256": sha256_json(index),
            "nodes": len(index["nodes"]),
            "links_per_node": len(index["nodes"]) - 1,
        }
    )
    return 0


def _cmd_propagate_index(args: argparse.Namespace) -> int:
    spec, _, _ = _load(args.spec, args.machines)
    index = json.loads(args.index.read_text())
    validate_sealed_graph(index)
    if not args.execute:
        _json(
            {
                "dry_run": True,
                "run_id": spec.run.id,
                "index_sha256": sha256_json(index),
                "targets": ["huggingface-model", "huggingface-dataset", "wandb"],
            }
        )
        return 0
    checkpoint = _checkpoint_store(spec).publish_index(
        args.index,
        run_id=spec.run.id,
    )
    dataset = _dataset_store(spec).publish_index(args.index, run_id=spec.run.id)
    run = open_run(spec, core=spec.core_manifest())
    try:
        wandb_node = next(node for node in index["nodes"] if node["id"] == "wandb-run")
        run.summary["provenance_core_sha256"] = index["core_sha256"]
        run.summary["provenance_index_sha256"] = sha256_json(index)
        run.summary["artifact_links"] = wandb_node["links"]
    finally:
        run.finish(exit_code=0)
    _json(
        {
            "checkpoint_index": checkpoint.__dict__,
            "dataset_index": dataset.__dict__,
            "wandb": "updated",
        }
    )
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="axexp")
    sub = root.add_subparsers(dest="command", required=True)

    def with_spec(name: str) -> argparse.ArgumentParser:
        command = sub.add_parser(name)
        command.add_argument("spec", type=Path)
        command.add_argument("--machines", type=Path)
        return command

    with_spec("validate")

    plan = with_spec("plan")
    plan.add_argument("--output", type=Path, required=True)

    launch = with_spec("launch")
    launch.add_argument("--output", type=Path, required=True)
    launch.add_argument("--butler-project", required=True)
    launch.add_argument("--execute", action="store_true")

    doctor = sub.add_parser("doctor")
    doctor.add_argument("--machines", type=Path)
    doctor.add_argument("--machine", action="append")

    checkpoint_upload = with_spec("checkpoint-upload")
    checkpoint_upload.add_argument("checkpoint", type=Path)
    checkpoint_upload.add_argument("--step", type=int, required=True)
    checkpoint_upload.add_argument("--index", type=Path, required=True)

    checkpoint_fetch = with_spec("checkpoint-fetch")
    checkpoint_fetch.add_argument("--output", type=Path, required=True)

    dataset_upload = with_spec("dataset-upload")
    dataset_upload.add_argument("snapshot", type=Path)
    dataset_upload.add_argument("--index", type=Path, required=True)

    replay = with_spec("results-replay")
    replay.add_argument("--metrics", type=Path, required=True)

    publish = with_spec("publish-results")
    publish.add_argument("--bundle", type=Path, required=True)
    publish.add_argument("--repo-dir", type=Path)
    publish.add_argument("--execute", action="store_true")

    reconcile = with_spec("reconcile")
    reconcile.add_argument("--bundle", type=Path, required=True)
    reconcile.add_argument("--compute-uri", required=True)
    reconcile.add_argument("--hf-revision")
    reconcile.add_argument("--hf-dataset-revision")
    reconcile.add_argument("--github-commit")

    propagate = with_spec("propagate-index")
    propagate.add_argument("--index", type=Path, required=True)
    propagate.add_argument("--execute", action="store_true")

    return root


_COMMANDS = {
    "validate": _cmd_validate,
    "plan": _cmd_plan,
    "launch": _cmd_launch,
    "doctor": _cmd_doctor,
    "checkpoint-upload": _cmd_checkpoint_upload,
    "checkpoint-fetch": _cmd_checkpoint_fetch,
    "dataset-upload": _cmd_dataset_upload,
    "results-replay": _cmd_results_replay,
    "publish-results": _cmd_publish_results,
    "reconcile": _cmd_reconcile,
    "propagate-index": _cmd_propagate_index,
}


def run(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return _COMMANDS[args.command](args)


def main() -> None:
    try:
        raise SystemExit(run())
    except (
        BackendError,
        ButlerError,
        CliError,
        CredentialError,
        MachineError,
        SpecError,
        WandbConfigurationError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
