"""Fail-closed execution policy unit tests."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

POLICY_PATH = Path(__file__).resolve().parents[1] / "scripts" / "policy.py"
SPEC = importlib.util.spec_from_file_location("api_to_typemcp_policy", POLICY_PATH)
assert SPEC is not None and SPEC.loader is not None
policy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(policy)


class PolicyTests(unittest.TestCase):
    def test_classifies_known_methods_and_denies_unknown_methods(self) -> None:
        self.assertEqual(policy.classify_method("GET"), "read")
        self.assertEqual(policy.classify_method("HEAD"), "read")
        self.assertEqual(policy.classify_method("OPTIONS"), "read")
        self.assertEqual(policy.classify_method("POST"), "protected-write")
        self.assertEqual(policy.classify_method("DELETE"), "protected-write")
        self.assertEqual(policy.classify_method("CONNECT"), "deny")

    def test_protected_write_grants_only_one_exact_known_identifier(self) -> None:
        known = {"createPet", "deletePet"}
        self.assertTrue(policy.is_protected_operation_allowed("createPet", "createPet", known))

        for value in (None, "", "*", "create*", "createPet,createPet", "missing", "createPet,missing", " createPet"):
            with self.subTest(value=value):
                self.assertFalse(policy.is_protected_operation_allowed("createPet", value, known))


if __name__ == "__main__":
    unittest.main()
