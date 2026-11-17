import secrets
import stat
import unittest
from pathlib import Path

from fetch_health_data import (
    DROP_VALUE,
    MAX_HEART_RATE_SAMPLES_PER_WORKOUT,
    MAX_WORKOUT_ROUTE_POINTS_PER_WORKOUT,
    merge_scope_payloads,
    record_fetch_failure,
    record_fetch_success,
    sanitize_decrypted_payload,
    sanitize_workout_heart_rate_samples,
    sanitize_workout_route_points,
    write_ndjson,
    write_sqlite,
)


class FetchHealthDataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime_dir = Path("/tmp") / f"ahs-fetch-test-{secrets.token_hex(8)}"
        self.runtime_dir.mkdir(mode=0o700)

    def tearDown(self) -> None:
        for path in self.runtime_dir.iterdir():
            path.unlink(missing_ok=True)
        self.runtime_dir.rmdir()

    def test_sanitizer_keeps_more_than_512_workout_heart_rate_samples(self) -> None:
        samples = [
            {
                "start_offset_ms": index * 5_000,
                "end_offset_ms": (index + 1) * 5_000,
                "bpm": 120.5,
            }
            for index in range(600)
        ]
        payload = {
            "2026-07-20": {
                "workouts": [
                    {
                        "heart_rate": {"avg_bpm": 120.5, "samples": len(samples)},
                        "heart_rate_samples": samples,
                    }
                ]
            }
        }

        sanitized, metrics = sanitize_decrypted_payload(payload)

        stored_samples = sanitized["2026-07-20"]["workouts"][0]["heart_rate_samples"]
        self.assertEqual(len(stored_samples), 600)
        self.assertEqual(metrics["stored_days"], 1)
        self.assertEqual(metrics["dropped_days"], 0)

    def test_sanitizer_rejects_entire_malformed_heart_rate_series(self) -> None:
        payload = {
            "2026-07-20": {
                "workouts": [
                    {
                        "duration_seconds": 60,
                        "heart_rate_samples": [
                            {"start_offset_ms": 0, "end_offset_ms": 5_000, "bpm": 110},
                            {"start_offset_ms": 5_000, "end_offset_ms": 4_000, "bpm": 115},
                        ],
                    }
                ]
            }
        }

        sanitized, _ = sanitize_decrypted_payload(payload)

        workout = sanitized["2026-07-20"]["workouts"][0]
        self.assertNotIn("heart_rate_samples", workout)
        self.assertEqual(workout["duration_seconds"], 60)

    def test_sanitizer_rejects_entire_oversized_heart_rate_series(self) -> None:
        valid_sample = {"start_offset_ms": 0, "end_offset_ms": 5_000, "bpm": 110}
        samples = [valid_sample] * (MAX_HEART_RATE_SAMPLES_PER_WORKOUT + 1)

        sanitized = sanitize_workout_heart_rate_samples(samples)

        self.assertIs(sanitized, DROP_VALUE)

    def test_sanitizer_keeps_detailed_time_pace_and_more_than_512_route_points(self) -> None:
        route_points = [
            {
                "timestamp_offset_ms": index * 1_000,
                "latitude": 50.0 + index / 1_000_000,
                "longitude": 8.0 + index / 1_000_000,
                "altitude_meters": 120.5,
                "horizontal_accuracy_meters": 3.0,
                "speed_meters_per_second": 3.5,
                "course_degrees": 180.0,
            }
            for index in range(600)
        ]
        speed_samples = [
            {
                "source": "running",
                "start_offset_ms": index * 5_000,
                "end_offset_ms": (index + 1) * 5_000,
                "speed_meters_per_second": 3.5,
                "pace_seconds_per_kilometer": 285.71,
            }
            for index in range(600)
        ]
        payload = {
            "2026-08-06": {
                "workouts": [
                    {
                        "duration_seconds": 3_000,
                        "workout_timing": {
                            "elapsed_duration_ms": 3_060_000,
                            "active_duration_ms": 3_000_000,
                            "paused_duration_ms": 60_000,
                        },
                        "workout_events": [
                            {"type": "lap", "start_offset_ms": 0, "end_offset_ms": 300_000}
                        ],
                        "workout_activities": [
                            {
                                "activity_type": "running",
                                "start_offset_ms": 0,
                                "end_offset_ms": 3_060_000,
                                "active_duration_ms": 3_000_000,
                            }
                        ],
                        "speed_samples": speed_samples,
                        "distance_intervals": [
                            {
                                "source": "walking_running",
                                "start_offset_ms": 0,
                                "end_offset_ms": 300_000,
                                "duration_ms": 300_000,
                                "distance_meters": 1_000.0,
                                "speed_meters_per_second": 3.333,
                                "pace_seconds_per_kilometer": 300.0,
                            }
                        ],
                        "route_points": route_points,
                    }
                ]
            }
        }

        sanitized, metrics = sanitize_decrypted_payload(payload)
        workout = sanitized["2026-08-06"]["workouts"][0]

        self.assertEqual(len(workout["speed_samples"]), 600)
        self.assertEqual(len(workout["route_points"]), 600)
        self.assertEqual(workout["workout_events"][0]["type"], "lap")
        self.assertEqual(workout["workout_timing"]["paused_duration_ms"], 60_000)
        self.assertNotIn("workout_activities", workout)
        self.assertEqual(metrics["stored_days"], 1)

    def test_sanitizer_rejects_entire_malformed_route_series(self) -> None:
        payload = {
            "2026-08-06": {
                "workouts": [
                    {
                        "duration_seconds": 60,
                        "route_points": [
                            {"timestamp_offset_ms": 0, "latitude": 50.0, "longitude": 8.0},
                            {"timestamp_offset_ms": 1_000, "latitude": 95.0, "longitude": 8.0},
                        ],
                    }
                ]
            }
        }

        sanitized, _ = sanitize_decrypted_payload(payload)

        workout = sanitized["2026-08-06"]["workouts"][0]
        self.assertNotIn("route_points", workout)
        self.assertEqual(workout["duration_seconds"], 60)

    def test_sanitizer_rejects_entire_malformed_speed_series(self) -> None:
        payload = {
            "2026-08-06": {
                "workouts": [
                    {
                        "duration_seconds": 60,
                        "speed_samples": [
                            {
                                "source": "running",
                                "start_offset_ms": 0,
                                "end_offset_ms": 5_000,
                                "speed_meters_per_second": 3.5,
                                "pace_seconds_per_kilometer": 285.71,
                            },
                            {
                                "source": "running",
                                "start_offset_ms": 10_000,
                                "end_offset_ms": 5_000,
                                "speed_meters_per_second": 3.5,
                                "pace_seconds_per_kilometer": 285.71,
                            },
                        ],
                    }
                ]
            }
        }

        sanitized, _ = sanitize_decrypted_payload(payload)

        workout = sanitized["2026-08-06"]["workouts"][0]
        self.assertNotIn("speed_samples", workout)
        self.assertEqual(workout["duration_seconds"], 60)

    def test_sanitizer_rejects_entire_oversized_route_series(self) -> None:
        valid_point = {"timestamp_offset_ms": 0, "latitude": 50.0, "longitude": 8.0}
        points = [valid_point] * (MAX_WORKOUT_ROUTE_POINTS_PER_WORKOUT + 1)

        sanitized = sanitize_workout_route_points(points)

        self.assertIs(sanitized, DROP_VALUE)

    def test_recent_scope_overlays_history_per_day_category(self) -> None:
        history = {
            "2026-07-20": {
                "sleep": {"total_hours": 8},
                "workouts": [{"heart_rate": {"avg_bpm": 100}}],
            }
        }
        recent_workouts = [
            {
                "heart_rate": {"avg_bpm": 120},
                "heart_rate_samples": [
                    {"start_offset_ms": 0, "end_offset_ms": 5_000, "bpm": 120}
                ],
            }
        ]
        recent = {
            "2026-07-20": {
                "activity": {"steps": 1000},
                "workouts": recent_workouts,
            }
        }

        merged = merge_scope_payloads({}, history, recent)

        self.assertEqual(merged["2026-07-20"]["sleep"], {"total_hours": 8})
        self.assertEqual(merged["2026-07-20"]["activity"], {"steps": 1000})
        self.assertEqual(merged["2026-07-20"]["workouts"], recent_workouts)

    def test_sqlite_storage_is_private(self) -> None:
        sqlite_path = self.runtime_dir / "health.db"

        write_sqlite(
            sqlite_path,
            "ahs_private",
            "2026-07-20T00:00:00+00:00",
            {"2026-07-20": {"activity": {"steps": 1000}}},
        )

        self.assertEqual(stat.S_IMODE(sqlite_path.stat().st_mode), 0o600)

    def test_ndjson_storage_is_private(self) -> None:
        json_path = self.runtime_dir / "health.ndjson"

        write_ndjson(json_path, {"user_id": "ahs_private", "payload": {}})

        self.assertEqual(stat.S_IMODE(json_path.stat().st_mode), 0o600)

    def test_fetch_failure_preserves_last_success_timestamp(self) -> None:
        state = {
            "last_fetch_at": "2026-08-09T22:20:00+00:00",
            "last_fetch_success_at": "2026-08-09T22:20:00+00:00",
        }

        record_fetch_failure(state, "2026-08-11T08:00:00+00:00", "HTTP 401")

        self.assertEqual(state["last_fetch_attempt_at"], "2026-08-11T08:00:00+00:00")
        self.assertEqual(state["last_fetch_success_at"], "2026-08-09T22:20:00+00:00")
        self.assertEqual(state["last_fetch_at"], "2026-08-09T22:20:00+00:00")
        self.assertEqual(state["last_fetch_status"], "error")

    def test_fetch_failure_discards_legacy_attempt_timestamp_without_known_success(self) -> None:
        state = {
            "last_fetch_at": "2026-08-11T07:00:00+00:00",
            "last_fetch_status": "error",
        }

        record_fetch_failure(state, "2026-08-11T08:00:00+00:00", "HTTP 401")

        self.assertNotIn("last_fetch_at", state)
        self.assertNotIn("last_fetch_success_at", state)
        self.assertEqual(state["last_fetch_attempt_at"], "2026-08-11T08:00:00+00:00")

    def test_fetch_success_updates_attempt_and_success_timestamps(self) -> None:
        state = {"last_fetch_error": "old failure"}

        record_fetch_success(
            state,
            "2026-08-11T08:00:00+00:00",
            "2026-08-11T08:00:02+00:00",
            2,
            {"raw_days": 7, "stored_days": 6, "dropped_days": 1},
        )

        self.assertEqual(state["last_fetch_attempt_at"], "2026-08-11T08:00:00+00:00")
        self.assertEqual(state["last_fetch_success_at"], "2026-08-11T08:00:02+00:00")
        self.assertEqual(state["last_fetch_at"], "2026-08-11T08:00:02+00:00")
        self.assertEqual(state["last_fetch_status"], "ok")
        self.assertNotIn("last_fetch_error", state)


if __name__ == "__main__":
    unittest.main()
