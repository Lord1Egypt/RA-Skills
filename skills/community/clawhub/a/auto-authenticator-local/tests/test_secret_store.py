import pathlib
import sys
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import secret_store  # noqa: E402


class SecretStoreTests(unittest.TestCase):
    def test_backend_name_uses_macos_fallback_when_keyring_missing(self) -> None:
        with mock.patch.object(secret_store, "keyring", None):
            with mock.patch("platform.system", return_value="Darwin"):
                self.assertEqual(secret_store.backend_name(), "macos-security-cli")

    def test_backend_name_requires_secure_backend_on_other_platforms(self) -> None:
        with mock.patch.object(secret_store, "keyring", None):
            with mock.patch("platform.system", return_value="Linux"):
                with self.assertRaises(RuntimeError):
                    secret_store.backend_name()


if __name__ == "__main__":
    unittest.main()
