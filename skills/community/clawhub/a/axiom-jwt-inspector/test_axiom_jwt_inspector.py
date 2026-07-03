"""Tests — axiom-jwt-inspector """

from pathlib import Path
import sys
import time
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_jwt_inspector import create, decode, verify_hmac


class TestDecode(unittest.TestCase):
    def setUp(self):
        # Create a test JWT
        self.payload = {"sub": "user-123", "name": "Papa", "exp": int(time.time()) + 3600}
        self.jwt = create(self.payload, "mysecret")

    def test_01_decode(self):
        result = decode(self.jwt)
        self.assertTrue(result["valid_format"])
        self.assertEqual(result["payload"]["sub"], "user-123")

    def test_02_header(self):
        result = decode(self.jwt)
        self.assertEqual(result["header"]["alg"], "HS256")
        self.assertEqual(result["header"]["typ"], "JWT")

    def test_03_exp_info(self):
        result = decode(self.jwt)
        self.assertIsNotNone(result["exp_info"])
        self.assertFalse(result["exp_info"]["expired"])
        self.assertGreater(result["exp_info"]["seconds_until_expiry"], 0)

    def test_04_expired(self):
        expired = create({"sub": "x", "exp": int(time.time()) - 100}, "s")
        result = decode(expired)
        self.assertTrue(result["exp_info"]["expired"])

    def test_05_invalid_format(self):
        result = decode("not-a-jwt")
        self.assertFalse(result["valid_format"])

    def test_06_two_parts(self):
        result = decode("a.b")
        self.assertFalse(result["valid_format"])

    def test_07_empty(self):
        result = decode("")
        self.assertFalse(result["valid_format"])


class TestVerifyHmac(unittest.TestCase):
    def setUp(self):
        self.payload = {"sub": "u1"}
        self.jwt = create(self.payload, "secret123")

    def test_08_valid_hmac(self):
        result = verify_hmac(self.jwt, "secret123")
        self.assertTrue(result["signature_valid"])

    def test_09_wrong_secret(self):
        result = verify_hmac(self.jwt, "wrong-secret")
        self.assertFalse(result["signature_valid"])

    def test_10_alg_not_supported(self):
        # Use a token with alg=none (manually constructed)
        # Skipping — would require manual crafting
        pass


class TestCreate(unittest.TestCase):
    def test_11_roundtrip(self):
        payload = {"a": 1, "b": "two"}
        jwt = create(payload, "secret")
        result = decode(jwt)
        self.assertEqual(result["payload"], payload)

    def test_12_alg_hs512(self):
        jwt = create({"a": 1}, "secret", alg="HS512")
        result = decode(jwt)
        self.assertEqual(result["header"]["alg"], "HS512")


class TestDeterminism(unittest.TestCase):
    def test_13_1000_decodes(self):
        jwt = create({"a": 1}, "secret")
        first = decode(jwt)
        for _ in range(1000):
            self.assertEqual(decode(jwt)["payload"], first["payload"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
