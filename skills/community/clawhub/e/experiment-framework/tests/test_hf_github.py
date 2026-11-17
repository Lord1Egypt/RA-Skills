from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from axiotic_experiments.github_store import (
    GitHubStoreError,
    assert_no_secret_material,
)
from axiotic_experiments.hf_store import HuggingFaceCheckpointStore


class FakeApi:
    def __init__(self) -> None:
        self.uploads: list[tuple[str, str]] = []
        self.counter = 0

    def upload_folder(self, **kwargs):
        self.counter += 1
        self.uploads.append(("folder", kwargs["path_in_repo"]))
        return SimpleNamespace(oid=f"folder-{self.counter}")

    def upload_file(self, **kwargs):
        self.counter += 1
        self.uploads.append(("file", kwargs["path_in_repo"]))
        return SimpleNamespace(oid=f"file-{self.counter}")


class StoreTests(unittest.TestCase):
    def test_checkpoint_upload_advances_pinned_latest_pointer(self) -> None:
        api = FakeApi()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "checkpoint"
            checkpoint.mkdir()
            (checkpoint / "state.json").write_text("{}")
            provenance = root / "artifact-index.json"
            provenance.write_text('{"nodes":[]}')
            store = HuggingFaceCheckpointStore(
                repo_id="org/model",
                checkpoint_prefix="checkpoints",
                api=api,
                hf_hub_download=lambda **_: "",
                snapshot_download=lambda **_: "",
            )

            uploaded = store.upload(
                checkpoint,
                run_id="run-1",
                step=12,
                provenance_path=provenance,
            )

        self.assertEqual(uploaded.revision, "file-3")
        self.assertIn(
            ("file", "checkpoints/run-1/latest.json"),
            api.uploads,
        )

    def test_secret_scanner_accepts_public_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "run-core.json").write_text(json.dumps({"run_id": "safe"}))
            assert_no_secret_material(root)

    def test_secret_scanner_rejects_token_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bad.txt").write_text("hf_" + ("x" * 30))
            with self.assertRaises(GitHubStoreError):
                assert_no_secret_material(root)


if __name__ == "__main__":
    unittest.main()
