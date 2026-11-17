import tempfile
import unittest
from pathlib import Path

from scripts.idempotency import (
    IdempotencyConflict,
    IdempotencyStore,
    replay_response,
)


class IdempotencyStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "idempotency.json"
        self.store = IdempotencyStore(self.path)

    def tearDown(self):
        self.temp_dir.cleanup()

    @staticmethod
    def order(**overrides):
        command = {
            "cmd": "order",
            "exchange": "CFFEX",
            "instrument": "IF2505",
            "direction": "buy",
            "offset": "open",
            "price_type": "limit",
            "price": 3850.0,
            "volume": 1,
        }
        command.update(overrides)
        return command

    def test_same_derived_request_replays_after_completion(self):
        command = self.order()
        key, record = self.store.begin(command)
        self.assertIsNone(record)
        response = {"ok": True, "order_ref": "000000000001", "ret": 0}
        self.store.complete(key, response)

        replay_key, replay_record = self.store.begin(dict(command))
        self.assertEqual(replay_key, key)
        self.assertEqual(replay_response(replay_key, replay_record), {
            **response,
            "idempotent_replay": True,
            "idempotency_key": key,
        })

    def test_explicit_key_conflict_is_rejected(self):
        first = self.order(idempotency_key="ticket-1")
        self.store.begin(first)
        with self.assertRaises(IdempotencyConflict):
            self.store.begin(self.order(volume=2, idempotency_key="ticket-1"))

    def test_pending_record_is_not_retried(self):
        command = self.order(idempotency_key="ticket-2")
        key, record = self.store.begin(command)
        self.assertIsNone(record)
        _, replay_record = self.store.begin(command)
        response = replay_response(key, replay_record)
        self.assertFalse(response["ok"])
        self.assertTrue(response["idempotent_replay"])
        self.assertIn("状态未知", response["error"])

    def test_records_survive_store_reload(self):
        command = self.order(idempotency_key="ticket-3")
        key, _ = self.store.begin(command)
        self.store.complete(key, {"ok": False, "ret": -3})

        reloaded = IdempotencyStore(self.path)
        replay_key, record = reloaded.begin(command)
        self.assertEqual(replay_key, key)
        self.assertEqual(record["response"], {"ok": False, "ret": -3})

    def test_subscription_order_is_canonicalised(self):
        first = {
            "cmd": "subscribe",
            "instruments": "IF2505, rb2510",
        }
        second = {
            "cmd": "subscribe",
            "instruments": "rb2510,IF2505",
        }
        key, _ = self.store.begin(first)
        self.store.complete(key, {"ok": True, "ret": 0})
        replay_key, record = self.store.begin(second)
        self.assertEqual(replay_key, key)
        self.assertEqual(record["status"], "completed")

    def test_corrupt_journal_fails_closed(self):
        self.path.write_text('{"version": 1, "records": []}', encoding="utf-8")
        with self.assertRaises(RuntimeError):
            IdempotencyStore(self.path)


if __name__ == "__main__":
    unittest.main()
