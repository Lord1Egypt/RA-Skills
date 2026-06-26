import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from totp_common import generate_totp, normalize_seed  # noqa: E402


class TotpCommonTests(unittest.TestCase):
    def test_normalize_seed_rejects_invalid_value(self) -> None:
        with self.assertRaises(ValueError):
            normalize_seed("not-base32")

    def test_rfc_style_vector(self) -> None:
        seed = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
        code, expires_in = generate_totp(seed, digits=8, for_time=59)
        self.assertEqual(code, "94287082")
        self.assertEqual(expires_in, 1)


if __name__ == "__main__":
    unittest.main()
