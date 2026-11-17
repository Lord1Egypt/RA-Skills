import json
import secrets
import shutil
import stat
import unittest
from pathlib import Path
from unittest import mock

from config import resolve_user_paths, write_user_config
from onboarding import (
    archive_identity_for_rotation,
    generate_replacement_user_id,
    main,
    reset_identity_config,
)


class OnboardingRotationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state_dir = Path("/tmp") / f"ahs-onboarding-test-{secrets.token_hex(8)}"
        self.paths = resolve_user_paths(self.state_dir)
        self.paths["secrets_dir"].mkdir(mode=0o700, parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.state_dir, ignore_errors=True)

    def write_v5_identity(self) -> dict:
        config = {
            "user_id": "ahs_previous_identity",
            "protocol_version": 5,
            "onboarding_fingerprint": "old-fingerprint",
            "storage": "sqlite",
            "last_fetch_at": "2026-08-09T22:20:00+00:00",
            "last_fetch_status": "ok",
        }
        write_user_config(config, self.state_dir)
        artifacts = {
            self.paths["config_dir"] / "signing_public_key_v5.pem": b"old-signing-public",
            self.paths["secrets_dir"] / "signing_private_key_v5.pem": b"old-signing-private",
            self.paths["config_dir"] / "encryption_public_key_v5.pem": b"old-encryption-public",
            self.paths["secrets_dir"] / "encryption_private_key_v5.pem": b"old-encryption-private",
            self.paths["config_dir"] / "registration-qr.json": b'{"fingerprint":"old-fingerprint"}\n',
        }
        for path, contents in artifacts.items():
            path.write_bytes(contents)
        return config

    def test_rotation_backup_preserves_complete_identity_privately(self) -> None:
        existing_config = self.write_v5_identity()

        backup_dir = archive_identity_for_rotation(
            self.paths,
            existing_config,
            "ahs_replacement_identity",
        )

        self.assertIsNotNone(backup_dir)
        assert backup_dir is not None
        self.assertEqual(stat.S_IMODE(backup_dir.stat().st_mode), 0o700)
        manifest = json.loads((backup_dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["previous_user_id"], "ahs_previous_identity")
        self.assertEqual(manifest["replacement_user_id"], "ahs_replacement_identity")
        self.assertEqual(manifest["previous_protocol_version"], 5)
        self.assertEqual(
            (backup_dir / "config/secrets/signing_private_key_v5.pem").read_bytes(),
            b"old-signing-private",
        )
        for archived_file in manifest["files"]:
            archived_path = backup_dir / archived_file["path"]
            self.assertEqual(stat.S_IMODE(archived_path.stat().st_mode), 0o600)

    def test_rotation_backup_aborts_when_existing_v5_identity_is_incomplete(self) -> None:
        existing_config = self.write_v5_identity()
        (self.paths["secrets_dir"] / "encryption_private_key_v5.pem").unlink()

        with self.assertRaisesRegex(RuntimeError, "existing identity is incomplete"):
            archive_identity_for_rotation(
                self.paths,
                existing_config,
                "ahs_replacement_identity",
            )

        backup_root = self.paths["config_dir"] / "key-backups"
        self.assertFalse(backup_root.exists())

    def test_rotation_user_id_can_never_reuse_previous_identity(self) -> None:
        with mock.patch(
            "onboarding.generate_user_id",
            side_effect=["ahs_previous_identity", "ahs_replacement_identity"],
        ):
            replacement = generate_replacement_user_id("ahs_previous_identity")

        self.assertEqual(replacement, "ahs_replacement_identity")

    def test_rotation_config_removes_identity_status_and_key_fields(self) -> None:
        reset = reset_identity_config(
            {
                "user_id": "ahs_previous_identity",
                "signing_public_key_base64": "old-key",
                "onboarding_fingerprint": "old-fingerprint",
                "last_fetch_attempt_at": "attempt",
                "last_fetch_success_at": "success",
                "last_unlink_status": "error",
                "last_validation_raw_days": 7,
                "storage": "json",
                "sqlite_path": "/private/state/health.db",
            }
        )

        self.assertEqual(reset, {"storage": "json", "sqlite_path": "/private/state/health.db"})

    def test_rotate_end_to_end_archives_identity_and_activates_new_user_id(self) -> None:
        with mock.patch("onboarding.render_qr_via_supabase", return_value=None), mock.patch(
            "sys.argv",
            ["onboarding.py", "--state-dir", str(self.state_dir)],
        ), mock.patch("sys.stdout"):
            self.assertEqual(main(), 0)

        initial_config = json.loads(self.paths["primary_config_path"].read_text(encoding="utf-8"))
        initial_user_id = initial_config["user_id"]
        initial_signing_private_key = (
            self.paths["secrets_dir"] / "signing_private_key_v5.pem"
        ).read_bytes()

        with mock.patch("onboarding.render_qr_via_supabase", return_value=None), mock.patch(
            "sys.argv",
            ["onboarding.py", "--state-dir", str(self.state_dir), "--rotate"],
        ), mock.patch("sys.stdout"):
            self.assertEqual(main(), 0)

        rotated_config = json.loads(self.paths["primary_config_path"].read_text(encoding="utf-8"))
        self.assertNotEqual(rotated_config["user_id"], initial_user_id)
        self.assertNotEqual(
            (self.paths["secrets_dir"] / "signing_private_key_v5.pem").read_bytes(),
            initial_signing_private_key,
        )
        backup_dir = Path(rotated_config["last_rotation_backup_path"])
        manifest = json.loads((backup_dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["previous_user_id"], initial_user_id)
        self.assertEqual(manifest["replacement_user_id"], rotated_config["user_id"])
        self.assertEqual(
            (backup_dir / "config/secrets/signing_private_key_v5.pem").read_bytes(),
            initial_signing_private_key,
        )

    def test_rotate_uses_same_new_identity_semantics_for_v4(self) -> None:
        with mock.patch("onboarding.render_qr_via_supabase", return_value=None), mock.patch(
            "sys.argv",
            ["onboarding.py", "--state-dir", str(self.state_dir), "--protocol", "v4"],
        ), mock.patch("sys.stdout"):
            self.assertEqual(main(), 0)

        initial_config = json.loads(self.paths["primary_config_path"].read_text(encoding="utf-8"))
        initial_private_key = (self.paths["secrets_dir"] / "private_key.pem").read_bytes()

        with mock.patch("onboarding.render_qr_via_supabase", return_value=None), mock.patch(
            "sys.argv",
            [
                "onboarding.py",
                "--state-dir",
                str(self.state_dir),
                "--protocol",
                "v4",
                "--rotate",
            ],
        ), mock.patch("sys.stdout"):
            self.assertEqual(main(), 0)

        rotated_config = json.loads(self.paths["primary_config_path"].read_text(encoding="utf-8"))
        self.assertNotEqual(rotated_config["user_id"], initial_config["user_id"])
        backup_dir = Path(rotated_config["last_rotation_backup_path"])
        self.assertEqual(
            (backup_dir / "config/secrets/private_key.pem").read_bytes(),
            initial_private_key,
        )


if __name__ == "__main__":
    unittest.main()
