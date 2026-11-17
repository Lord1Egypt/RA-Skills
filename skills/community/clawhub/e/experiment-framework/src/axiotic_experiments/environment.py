from __future__ import annotations

import json
from typing import Any

from .spec import ExperimentSpec


def build_runtime_environment(
    spec: ExperimentSpec,
    *,
    core: dict[str, Any],
    bundle_uri: str,
    artifact_index: dict[str, Any] | None = None,
) -> dict[str, str]:
    env = {
        **spec.execution.public_env,
        "WANDB_ENTITY": spec.wandb.entity,
        "WANDB_PROJECT": spec.wandb.project,
        "WANDB_MODE": "online",
        "WANDB_RUN_ID": spec.run.id,
        "WANDB_NAME": spec.run.name,
        "WANDB_RESUME": "allow",
        "WANDB_NOTES": spec.run.notes,
        "WANDB_TAGS": ",".join(spec.run.tags),
        "HF_REPO_ID": spec.huggingface.checkpoint_repo,
        "HF_REVISION": spec.huggingface.revision,
        "HF_DATASET_REPO_ID": spec.huggingface.dataset_repo,
        "HF_DATASET_REVISION": spec.huggingface.dataset_revision,
        "GITHUB_RESULTS_REPO": spec.github.repo,
        "GITHUB_RESULTS_BRANCH": spec.github.results_branch,
        "AXIOTIC_RUN_ID": spec.run.id,
        "AXIOTIC_RUN_NAME": spec.run.name,
        "AXIOTIC_RUN_CORE_JSON": json.dumps(
            core,
            sort_keys=True,
            separators=(",", ":"),
        ),
        **(
            {
                "AXIOTIC_ARTIFACT_INDEX_JSON": json.dumps(
                    artifact_index,
                    sort_keys=True,
                    separators=(",", ":"),
                )
            }
            if artifact_index is not None
            else {}
        ),
        "AXIOTIC_BUNDLE_URI": bundle_uri,
        "AXIOTIC_RESUME_POLICY": "huggingface-latest",
        "AXIOTIC_SOURCE_COMMIT": spec.source.commit,
        "AXIOTIC_MAX_HOURS": str(spec.execution.max_hours),
        "AXIOTIC_GPU_COUNT": str(spec.resources.gpus),
        "AXIOTIC_SEED": str(spec.run.seed),
        "AXIOTIC_PHASE": spec.run.phase,
        "AXIOTIC_VARIANT": spec.run.variant,
        "AXIOTIC_MODALITY": spec.run.modality,
        "AXIOTIC_DATASET": spec.run.dataset,
        "AXIOTIC_REASON": spec.run.reason,
        "AXIOTIC_NOTES": spec.run.notes,
    }
    if env.get("WANDB_DISABLED", "").lower() in {"1", "true", "yes"}:
        raise ValueError("W&B cannot be disabled")
    return env
