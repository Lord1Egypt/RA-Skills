from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class HuggingFaceStoreError(RuntimeError):
    pass


@dataclass(frozen=True)
class UploadedArtifact:
    repo_id: str
    repo_type: str
    revision: str
    path_in_repo: str
    uri: str


@dataclass(frozen=True)
class ResolvedCheckpoint:
    path: Path
    step: int
    revision: str
    path_in_repo: str


def _repo_uri(repo_id: str, repo_type: str) -> str:
    prefix = "datasets/" if repo_type == "dataset" else ""
    return f"https://huggingface.co/{prefix}{repo_id}"


class HuggingFaceCheckpointStore:
    def __init__(
        self,
        *,
        repo_id: str,
        checkpoint_prefix: str,
        revision: str = "main",
        token: str | None = None,
        api: Any | None = None,
        hf_hub_download: Callable[..., str] | None = None,
        snapshot_download: Callable[..., str] | None = None,
    ):
        self.repo_id = repo_id
        self.checkpoint_prefix = checkpoint_prefix.strip("/")
        self.revision = revision
        self.token = token
        if api is None or hf_hub_download is None or snapshot_download is None:
            try:
                from huggingface_hub import HfApi
                from huggingface_hub import hf_hub_download as sdk_hf_hub_download
                from huggingface_hub import snapshot_download as sdk_snapshot_download
            except ImportError as exc:
                raise HuggingFaceStoreError(
                    "install the 'huggingface-hub' package"
                ) from exc
            api = api or HfApi(token=token)
            hf_hub_download = hf_hub_download or sdk_hf_hub_download
            snapshot_download = snapshot_download or sdk_snapshot_download
        self.api = api
        self.hf_hub_download = hf_hub_download
        self.snapshot_download = snapshot_download

    def upload(
        self,
        checkpoint_dir: Path,
        *,
        run_id: str,
        step: int,
        provenance_path: Path,
    ) -> UploadedArtifact:
        if not checkpoint_dir.is_dir():
            raise HuggingFaceStoreError(
                f"checkpoint directory not found: {checkpoint_dir}"
            )
        if not provenance_path.is_file():
            raise HuggingFaceStoreError(
                f"provenance index not found: {provenance_path}"
            )
        path_in_repo = f"{self.checkpoint_prefix}/{run_id}/step-{step}"
        folder_commit = self.api.upload_folder(
            repo_id=self.repo_id,
            repo_type="model",
            revision=self.revision,
            folder_path=str(checkpoint_dir),
            path_in_repo=path_in_repo,
            commit_message=f"[{run_id}] checkpoint step {step}",
        )
        provenance_commit = self.api.upload_file(
            repo_id=self.repo_id,
            repo_type="model",
            revision=self.revision,
            path_or_fileobj=str(provenance_path),
            path_in_repo=f"{path_in_repo}/artifact-index.json",
            commit_message=f"[{run_id}] checkpoint provenance step {step}",
        )
        checkpoint_revision = str(
            getattr(provenance_commit, "oid", None)
            or getattr(folder_commit, "oid", self.revision)
        )
        pointer = json.dumps(
            {
                "schema_version": "1.0",
                "run_id": run_id,
                "step": step,
                "path": path_in_repo,
                "revision": checkpoint_revision,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        pointer_commit = self.api.upload_file(
            repo_id=self.repo_id,
            repo_type="model",
            revision=self.revision,
            path_or_fileobj=pointer,
            path_in_repo=f"{self.checkpoint_prefix}/{run_id}/latest.json",
            commit_message=f"[{run_id}] point latest checkpoint to step {step}",
        )
        final_revision = str(getattr(pointer_commit, "oid", checkpoint_revision))
        return UploadedArtifact(
            repo_id=self.repo_id,
            repo_type="model",
            revision=final_revision,
            path_in_repo=path_in_repo,
            uri=(
                f"{_repo_uri(self.repo_id, 'model')}/tree/"
                f"{final_revision}/{path_in_repo}"
            ),
        )

    def download_latest(
        self,
        *,
        run_id: str,
        local_dir: Path,
    ) -> ResolvedCheckpoint:
        pointer_name = f"{self.checkpoint_prefix}/{run_id}/latest.json"
        pointer_path = self.hf_hub_download(
            repo_id=self.repo_id,
            repo_type="model",
            revision=self.revision,
            filename=pointer_name,
            token=self.token,
        )
        pointer = json.loads(Path(pointer_path).read_text())
        revision = str(pointer["revision"])
        path_in_repo = str(pointer["path"])
        self.snapshot_download(
            repo_id=self.repo_id,
            repo_type="model",
            revision=revision,
            local_dir=str(local_dir),
            allow_patterns=[f"{path_in_repo}/**"],
            token=self.token,
        )
        resolved = local_dir / path_in_repo
        if not resolved.is_dir():
            raise HuggingFaceStoreError(
                f"download completed without checkpoint directory: {resolved}"
            )
        return ResolvedCheckpoint(
            path=resolved,
            step=int(pointer["step"]),
            revision=revision,
            path_in_repo=path_in_repo,
        )

    def publish_index(self, provenance_path: Path, *, run_id: str) -> UploadedArtifact:
        return _publish_index(
            self.api,
            provenance_path=provenance_path,
            run_id=run_id,
            repo_id=self.repo_id,
            repo_type="model",
            revision=self.revision,
        )


class HuggingFaceDatasetStore:
    def __init__(
        self,
        *,
        repo_id: str,
        snapshot_prefix: str,
        revision: str = "main",
        token: str | None = None,
        api: Any | None = None,
    ):
        self.repo_id = repo_id
        self.snapshot_prefix = snapshot_prefix.strip("/")
        self.revision = revision
        if api is None:
            try:
                from huggingface_hub import HfApi
            except ImportError as exc:
                raise HuggingFaceStoreError(
                    "install the 'huggingface-hub' package"
                ) from exc
            api = HfApi(token=token)
        self.api = api

    def upload(
        self,
        snapshot_dir: Path,
        *,
        run_id: str,
        provenance_path: Path,
    ) -> UploadedArtifact:
        if not snapshot_dir.is_dir():
            raise HuggingFaceStoreError(f"dataset snapshot not found: {snapshot_dir}")
        if not provenance_path.is_file():
            raise HuggingFaceStoreError(
                f"provenance index not found: {provenance_path}"
            )
        path_in_repo = f"{self.snapshot_prefix}/{run_id}"
        folder_commit = self.api.upload_folder(
            repo_id=self.repo_id,
            repo_type="dataset",
            revision=self.revision,
            folder_path=str(snapshot_dir),
            path_in_repo=path_in_repo,
            commit_message=f"[{run_id}] publish dataset snapshot",
        )
        provenance_commit = self.api.upload_file(
            repo_id=self.repo_id,
            repo_type="dataset",
            revision=self.revision,
            path_or_fileobj=str(provenance_path),
            path_in_repo=f"{path_in_repo}/artifact-index.json",
            commit_message=f"[{run_id}] publish dataset provenance",
        )
        final_revision = str(
            getattr(provenance_commit, "oid", None)
            or getattr(folder_commit, "oid", self.revision)
        )
        return UploadedArtifact(
            repo_id=self.repo_id,
            repo_type="dataset",
            revision=final_revision,
            path_in_repo=path_in_repo,
            uri=(
                f"{_repo_uri(self.repo_id, 'dataset')}/tree/"
                f"{final_revision}/{path_in_repo}"
            ),
        )

    def publish_index(self, provenance_path: Path, *, run_id: str) -> UploadedArtifact:
        return _publish_index(
            self.api,
            provenance_path=provenance_path,
            run_id=run_id,
            repo_id=self.repo_id,
            repo_type="dataset",
            revision=self.revision,
        )


def _publish_index(
    api: Any,
    *,
    provenance_path: Path,
    run_id: str,
    repo_id: str,
    repo_type: str,
    revision: str,
) -> UploadedArtifact:
    if not provenance_path.is_file():
        raise HuggingFaceStoreError(f"provenance index not found: {provenance_path}")
    path_in_repo = f"provenance/{run_id}/artifact-index.json"
    commit = api.upload_file(
        repo_id=repo_id,
        repo_type=repo_type,
        revision=revision,
        path_or_fileobj=str(provenance_path),
        path_in_repo=path_in_repo,
        commit_message=f"[{run_id}] publish final provenance index",
    )
    final_revision = str(getattr(commit, "oid", revision))
    return UploadedArtifact(
        repo_id=repo_id,
        repo_type=repo_type,
        revision=final_revision,
        path_in_repo=path_in_repo,
        uri=f"{_repo_uri(repo_id, repo_type)}/blob/{final_revision}/{path_in_repo}",
    )
