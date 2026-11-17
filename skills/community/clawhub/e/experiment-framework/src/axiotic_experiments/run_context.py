from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .spec import ExperimentSpec


@dataclass(frozen=True)
class RunContextMetadata:
    phase: str
    variant: str
    modality: str
    dataset: str
    reason: str
    notes: str
    repo_url: str
    branch: str
    commit: str
    commit_url: str
    seed: int
    tags: tuple[str, ...]

    @classmethod
    def from_spec(cls, spec: ExperimentSpec) -> RunContextMetadata:
        return cls(
            phase=spec.run.phase,
            variant=spec.run.variant,
            modality=spec.run.modality,
            dataset=spec.run.dataset,
            reason=spec.run.reason,
            notes=spec.run.notes,
            repo_url=spec.source.repo_url,
            branch=spec.source.branch,
            commit=spec.source.commit,
            commit_url=spec.source.commit_url,
            seed=spec.run.seed,
            tags=spec.run.tags,
        )

    def config(self) -> dict[str, Any]:
        return {
            "axiotic_phase": self.phase,
            "axiotic_variant": self.variant,
            "axiotic_modality": self.modality,
            "axiotic_dataset": self.dataset,
            "axiotic_reason": self.reason,
            "repo_url": self.repo_url,
            "branch": self.branch,
            "commit": self.commit,
            "commit_url": self.commit_url,
            "seed": self.seed,
        }


def attach_run_context(run: Any, context: RunContextMetadata) -> None:
    """Refresh metadata on both new and resumed W&B runs."""

    run.config.update(context.config(), allow_val_change=True)
    run.tags = tuple(sorted(set(tuple(run.tags or ()) + context.tags)))
    run.notes = context.notes
