from __future__ import annotations

from typing import Any


def spec_mapping(*, machine: str = "local") -> dict[str, Any]:
    value: dict[str, Any] = {
        "run": {
            "id": "phase-model_seed0",
            "name": "Test run",
            "command": ["python3", "train.py"],
            "seed": 0,
            "phase": "phase",
            "variant": "model",
            "modality": "text",
            "dataset": "fixture-v1",
            "reason": "Verify framework behavior.",
            "notes": "Fixture run.",
        },
        "execution": {
            "machine": machine,
            "max_hours": 1.5,
            "source_sync": "git" if machine != "local" else "verify",
            "env": {"PYTHONUNBUFFERED": "1"},
        },
        "resources": {
            "gpus": 1 if machine == "runpod" else 0,
            "cpus": 2,
            "memory_gb": 4,
            "gpu_type_ids": ["NVIDIA L4"] if machine == "runpod" else [],
        },
        "wandb": {
            "entity": "entity",
            "project": "project",
            "mode": "online",
        },
        "huggingface": {
            "checkpoint_repo": "org/checkpoints",
            "dataset_repo": "org/datasets",
            "checkpoint_prefix": "checkpoints",
            "dataset_prefix": "snapshots",
            "revision": "main",
            "dataset_revision": "main",
        },
        "github": {
            "repo": "org/repo",
            "results_branch": "experiments",
            "results_prefix": "experiments/results",
        },
        "source": {
            "repo_url": "https://github.com/org/repo",
            "clone_url": "git@github.com:org/repo.git",
            "repo_dir": "repo",
            "branch": "main",
            "commit": "0123456789abcdef0123456789abcdef01234567",
        },
    }
    if machine == "runpod":
        value["runpod"] = {
            "image": "org/worker@sha256:" + ("a" * 64),
            "max_cost_usd": 10,
            "minimum_balance_reserve_usd": 1,
            "cloud_type": "SECURE",
            "interruptible": False,
        }
    return value
