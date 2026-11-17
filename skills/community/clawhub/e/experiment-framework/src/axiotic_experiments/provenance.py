from __future__ import annotations

from .machines import MachineProfile
from .manifest import ArtifactNode, ProvenanceGraph
from .spec import ExperimentSpec


def _compute_uri(
    spec: ExperimentSpec,
    profile: MachineProfile,
    observed_uri: str | None,
) -> str:
    if observed_uri:
        return observed_uri
    if profile.transport == "local":
        return f"machine://local/planned/{spec.run.id}"
    if profile.transport == "ssh":
        return f"ssh://{profile.target}/planned/{spec.run.id}"
    return f"runpod://planned/{spec.run.id}"


def build_graph(
    spec: ExperimentSpec,
    profile: MachineProfile,
    *,
    core_sha256: str,
    compute_uri: str | None = None,
    hf_revision: str | None = None,
    hf_dataset_revision: str | None = None,
    github_commit: str | None = None,
) -> ProvenanceGraph:
    run_id = spec.run.id
    result_path = f"{spec.github.results_prefix.rstrip('/')}/{run_id}"
    git_ref = github_commit or spec.github.results_branch
    hf_ref = hf_revision or spec.huggingface.revision
    dataset_ref = hf_dataset_revision or spec.huggingface.dataset_revision
    checkpoint_path = (
        f"{spec.huggingface.checkpoint_prefix.rstrip('/')}/{run_id}/latest.json"
    )
    github_base = f"https://github.com/{spec.github.repo}"
    github_result_base = f"{github_base}/blob/{git_ref}/{result_path}"

    graph = ProvenanceGraph(run_id=run_id, core_sha256=core_sha256)
    graph.add(
        ArtifactNode(
            "compute-job",
            "compute",
            _compute_uri(spec, profile, compute_uri),
            metadata={
                "machine": profile.name,
                "transport": profile.transport,
                "state": "observed" if compute_uri else "planned",
            },
        )
    )
    graph.add(
        ArtifactNode(
            "wandb-run",
            "telemetry",
            f"https://wandb.ai/{spec.wandb.entity}/{spec.wandb.project}/runs/{run_id}",
            metadata={"mode": "online", "resume": "allow"},
        )
    )
    checkpoint_base = f"https://huggingface.co/{spec.huggingface.checkpoint_repo}"
    graph.add(
        ArtifactNode(
            "hf-checkpoint",
            "checkpoint",
            f"{checkpoint_base}/tree/{hf_ref}/{checkpoint_path.rsplit('/', 1)[0]}",
            metadata={
                "latest_pointer": (
                    f"{checkpoint_base}/blob/{hf_ref}/{checkpoint_path}"
                ),
                "revision": hf_ref,
            },
        )
    )
    graph.add(
        ArtifactNode(
            "hf-dataset",
            "dataset",
            (
                "https://huggingface.co/datasets/"
                f"{spec.huggingface.dataset_repo}/tree/{dataset_ref}/"
                f"{spec.huggingface.dataset_prefix.strip('/')}/{run_id}"
            ),
            metadata={
                "source_dataset": spec.run.dataset,
                "revision": dataset_ref,
            },
        )
    )
    graph.add(
        ArtifactNode(
            "github-source",
            "source",
            spec.source.commit_url,
            sha256=spec.source.commit,
            metadata={"branch": spec.source.branch},
        )
    )
    graph.add(
        ArtifactNode(
            "github-results",
            "results",
            github_result_base,
            sha256=github_commit,
            metadata={"branch": spec.github.results_branch},
        )
    )
    graph.add(
        ArtifactNode(
            "run-config",
            "configuration",
            f"{github_result_base}/run-core.json",
            sha256=core_sha256,
        )
    )
    graph.add(
        ArtifactNode(
            "metrics-mirror",
            "metrics",
            f"{github_result_base}/metrics.jsonl",
        )
    )
    return graph
