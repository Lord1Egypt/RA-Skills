from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from axiotic_experiments.backends import (
    REMOTE_BOOTSTRAP,
    encode_ssh_request,
    runpod_command,
    runpod_mapping,
    ssh_command,
    ssh_payload,
    write_runpod_adapter_spec,
)
from axiotic_experiments.environment import build_runtime_environment
from axiotic_experiments.machines import MachineProfile
from axiotic_experiments.spec import ExperimentSpec

from .fixtures import spec_mapping


class BackendTests(unittest.TestCase):
    def test_ssh_secrets_are_in_stdin_payload_not_command(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping())
        profile = MachineProfile(
            name="worker",
            transport="ssh",
            target="worker",
            workspace_root="~/Work/repos",
            checkout_root="~/.runs",
        )
        credentials = {
            "WANDB_API_KEY": "wandb-runtime-value",
            "HF_TOKEN": "hub-runtime-value",
            "GITHUB_TOKEN": "github-runtime-value",
        }
        runtime_env = build_runtime_environment(
            spec,
            core=spec.core_manifest(),
            bundle_uri="https://example.test/bundle",
            artifact_index={"nodes": []},
        )

        command = ssh_command(profile)
        payload = ssh_payload(
            spec,
            profile,
            runtime_env=runtime_env,
            credentials=credentials,
        )

        rendered_command = " ".join(command)
        self.assertNotIn("wandb-runtime-value", rendered_command)
        self.assertNotIn("hub-runtime-value", rendered_command)
        self.assertNotIn("github-runtime-value", rendered_command)
        self.assertEqual(payload["env"]["WANDB_API_KEY"], "wandb-runtime-value")
        self.assertEqual(payload["workdir"], "~/Work/repos/repo")

    def test_remote_bootstrap_enforces_online_wandb_and_commit(self) -> None:
        self.assertIn('WANDB_MODE", "").lower() != "online"', REMOTE_BOOTSTRAP)
        self.assertIn('rev-parse", "HEAD"', REMOTE_BOOTSTRAP)
        self.assertIn("source commit mismatch", REMOTE_BOOTSTRAP)
        self.assertIn("SIGTERM", REMOTE_BOOTSTRAP)
        self.assertIn("source archive checksum mismatch", REMOTE_BOOTSTRAP)

    def test_ssh_request_frames_header_before_archive(self) -> None:
        request = encode_ssh_request({"run_id": "one"}, b"archive")
        header_size = int.from_bytes(request[:8], "big")
        header = request[8 : 8 + header_size]

        self.assertEqual(header, b'{"run_id":"one"}')
        self.assertEqual(request[8 + header_size :], b"archive")

    def test_runpod_mapping_matches_control_plane_contract(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping(machine="runpod"))

        mapping = runpod_mapping(spec)

        self.assertEqual(mapping["capacity"]["gpu_type_ids"], ["NVIDIA L4"])
        self.assertEqual(mapping["wandb"]["mode"], "online")
        self.assertEqual(mapping["github"]["branch"], "experiments")

    def test_runpod_adapter_serializes_as_toml(self) -> None:
        spec = ExperimentSpec.from_mapping(spec_mapping(machine="runpod"))
        with tempfile.TemporaryDirectory() as directory:
            path = write_runpod_adapter_spec(
                spec,
                Path(directory) / "adapter.toml",
            )
            text = path.read_text()

        self.assertIn("[capacity]", text)
        self.assertIn('image = "org/worker@sha256:', text)

    def test_runpod_dry_command_does_not_require_installed_delegate(self) -> None:
        with (
            patch("axiotic_experiments.backends.shutil.which", return_value=None),
            patch.object(Path, "is_file", return_value=False),
        ):
            command = runpod_command(
                Path("adapter.toml"),
                Path("bundle"),
                "project",
                execute=False,
            )

        self.assertEqual(command[0], "runpod-capacity")
        self.assertEqual(command[-1], "project")
        self.assertNotIn("--execute", command)


if __name__ == "__main__":
    unittest.main()
