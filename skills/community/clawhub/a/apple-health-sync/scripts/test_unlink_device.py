import unittest

from unlink_device import record_unlink_failure, record_unlink_success


class UnlinkDeviceStateTests(unittest.TestCase):
    def test_unlink_failure_preserves_last_success_timestamp(self) -> None:
        state = {
            "last_unlink_at": "2026-08-09T22:20:00+00:00",
            "last_unlink_success_at": "2026-08-09T22:20:00+00:00",
        }

        record_unlink_failure(state, "2026-08-11T08:00:00+00:00", "HTTP 401")

        self.assertEqual(state["last_unlink_attempt_at"], "2026-08-11T08:00:00+00:00")
        self.assertEqual(state["last_unlink_success_at"], "2026-08-09T22:20:00+00:00")
        self.assertEqual(state["last_unlink_at"], "2026-08-09T22:20:00+00:00")
        self.assertEqual(state["last_unlink_status"], "error")

    def test_unlink_failure_discards_legacy_attempt_timestamp_without_known_success(self) -> None:
        state = {
            "last_unlink_at": "2026-08-11T07:00:00+00:00",
            "last_unlink_status": "error",
        }

        record_unlink_failure(state, "2026-08-11T08:00:00+00:00", "HTTP 401")

        self.assertNotIn("last_unlink_at", state)
        self.assertNotIn("last_unlink_success_at", state)
        self.assertEqual(state["last_unlink_attempt_at"], "2026-08-11T08:00:00+00:00")

    def test_unlink_success_updates_attempt_and_success_timestamps(self) -> None:
        state = {"last_unlink_error": "old failure"}

        record_unlink_success(
            state,
            "2026-08-11T08:00:00+00:00",
            "2026-08-11T08:00:02+00:00",
        )

        self.assertEqual(state["last_unlink_attempt_at"], "2026-08-11T08:00:00+00:00")
        self.assertEqual(state["last_unlink_success_at"], "2026-08-11T08:00:02+00:00")
        self.assertEqual(state["last_unlink_at"], "2026-08-11T08:00:02+00:00")
        self.assertEqual(state["last_unlink_status"], "ok")
        self.assertNotIn("last_unlink_error", state)


if __name__ == "__main__":
    unittest.main()
