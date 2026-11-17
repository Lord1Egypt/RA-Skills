import tempfile
import unittest
from pathlib import Path

from scripts.accounts import AccountLease, AccountRegistry
from scripts.demo_client import DemoAccountClient


class AccountIsolationTests(unittest.TestCase):
    def test_example_registry_has_isolated_paths(self):
        registry = AccountRegistry(Path(__file__).parents[1] / "accounts.example.json")
        paths = [registry.resolve(account_id) for account_id in "ABCDE"]
        self.assertEqual([item.account_id for item in paths], list("ABCDE"))
        self.assertEqual(len({item.root for item in paths}), 5)
        self.assertEqual(len({item.state_file for item in paths}), 5)
        self.assertEqual([item.daemon_port for item in paths], [17771, 17772, 17773, 17774, 17775])

    def test_write_example_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "accounts.json"
            registry = AccountRegistry(target)
            first = registry.write_example()
            before = target.read_bytes()
            second = registry.write_example()
            self.assertEqual(first, second)
            self.assertEqual(before, target.read_bytes())

    def test_duplicate_real_account_lease_is_rejected(self):
        first = AccountLease("smoke-broker-test", "smoke-user-test")
        second = AccountLease("smoke-broker-test", "smoke-user-test")
        first.acquire()
        try:
            with self.assertRaisesRegex(RuntimeError, "已有一个交易实例"):
                second.acquire()
        finally:
            first.release()


class DemoManagementTests(unittest.TestCase):
    def test_demo_order_replays_by_explicit_key(self):
        client = DemoAccountClient()
        prepared = client.prepare_order(
            "A", exchange="SHFE", instrument="al2610", direction="buy",
            offset="open", volume=1, price_type="limit", price=20840,
        )
        first = client.submit_prepared_order("A", prepared["confirmation_token"], "test-key")
        second = client.submit_prepared_order("A", prepared["confirmation_token"], "test-key")
        self.assertEqual(first["order_ref"], second["order_ref"])
        self.assertTrue(second["idempotent_replay"])


if __name__ == "__main__":
    unittest.main()
