import base64
import os
import secrets
import stat
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from sync_cryptography import (
    decrypt_legacy_rsa_chunked_payload,
    decrypt_v5_payload,
    encrypt_v5_payload,
    generate_legacy_rsa_keys,
    generate_v5_keys,
    read_legacy_rsa_block_size,
    sign_legacy_challenge,
    x25519_public_key_base64_from_private_key,
)


class SyncCryptographyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime_dir = Path("/tmp") / f"ahs-crypto-test-{secrets.token_hex(8)}"
        self.runtime_dir.mkdir(mode=0o700)

    def tearDown(self) -> None:
        for path in self.runtime_dir.iterdir():
            path.unlink(missing_ok=True)
        self.runtime_dir.rmdir()

    def legacy_paths(self) -> tuple[Path, Path]:
        return self.runtime_dir / "private.pem", self.runtime_dir / "public.pem"

    def test_legacy_key_generation_signing_and_permissions(self) -> None:
        private_path, public_path = self.legacy_paths()

        status = generate_legacy_rsa_keys(private_path, public_path, rotate=False)

        self.assertEqual(status, "generated")
        self.assertEqual(stat.S_IMODE(private_path.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(public_path.stat().st_mode), 0o644)

        challenge = "legacy-challenge"
        signature = base64.b64decode(sign_legacy_challenge(private_path, challenge, "RSA-2048"))
        public_key = serialization.load_pem_public_key(public_path.read_bytes())
        public_key.verify(signature, challenge.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())

    def test_legacy_chunked_decryption_stays_compatible(self) -> None:
        private_path, public_path = self.legacy_paths()
        generate_legacy_rsa_keys(private_path, public_path, rotate=False)
        public_key = serialization.load_pem_public_key(public_path.read_bytes())
        plaintext = (b"private-health-payload-" * 15) + b"done"
        encrypted_chunks = []
        for offset in range(0, len(plaintext), 128):
            encrypted_chunks.append(
                public_key.encrypt(
                    plaintext[offset : offset + 128],
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )
            )

        decrypted = decrypt_legacy_rsa_chunked_payload(
            private_path,
            base64.b64encode(b"".join(encrypted_chunks)).decode("ascii"),
            read_legacy_rsa_block_size(private_path),
        )

        self.assertEqual(decrypted, plaintext)

    def test_legacy_rotation_behavior_is_preserved(self) -> None:
        private_path, public_path = self.legacy_paths()
        generate_legacy_rsa_keys(private_path, public_path, rotate=False)
        original_private_key = private_path.read_bytes()
        os.chmod(private_path, 0o644)

        self.assertEqual(generate_legacy_rsa_keys(private_path, public_path, rotate=False), "existing")
        self.assertEqual(stat.S_IMODE(private_path.stat().st_mode), 0o600)
        self.assertEqual(private_path.read_bytes(), original_private_key)
        self.assertEqual(generate_legacy_rsa_keys(private_path, public_path, rotate=True), "generated")
        self.assertNotEqual(private_path.read_bytes(), original_private_key)

    def test_v5_encryption_round_trip(self) -> None:
        signing_private = self.runtime_dir / "signing-private.pem"
        signing_public = self.runtime_dir / "signing-public.pem"
        encryption_private = self.runtime_dir / "encryption-private.pem"
        encryption_public = self.runtime_dir / "encryption-public.pem"
        generate_v5_keys(
            signing_private,
            signing_public,
            encryption_private,
            encryption_public,
            rotate=False,
        )
        encryption_public_base64 = x25519_public_key_base64_from_private_key(encryption_private)
        plaintext = b'{"2026-07-20":{"activity":{"steps":1234}}}'
        encrypted = encrypt_v5_payload(plaintext, "ahs_test", "recent", encryption_public_base64)

        decrypted, aad = decrypt_v5_payload(
            encrypted,
            encryption_private,
            encryption_public_base64,
            "ahs_test",
            "recent",
            max_ciphertext_bytes=4096,
            max_plaintext_bytes=4096,
        )

        self.assertEqual(decrypted, plaintext)
        self.assertEqual(aad, {"scope": "recent", "user_id": "ahs_test"})


if __name__ == "__main__":
    unittest.main()
