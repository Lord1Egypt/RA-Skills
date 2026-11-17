from __future__ import annotations

import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from axiotic_experiments.governance import Butler, ButlerError

FAKE_BUTLER = """
import json
import pathlib
import sys

log = pathlib.Path(__file__).with_suffix(".jsonl")
with log.open("a") as handle:
    handle.write(json.dumps(sys.argv[1:]) + "\\n")

command = sys.argv[1]
def value(flag):
    return sys.argv[sys.argv.index(flag) + 1]

if command == "gpu-reserve":
    job = value("--reservation-id")
    print(json.dumps({
        "verdict": "reserved",
        "reservation": {"reservation_id": job},
    }))
elif command == "gpu-reconcile":
    print(json.dumps({"verdict": "reconciled"}))
else:
    print(json.dumps({"verdict": "invalid", "reason": "unexpected command"}))
    raise SystemExit(1)
"""


class ButlerGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.cli = Path(self.temp.name) / "fake_butler.py"
        self.cli.write_text(textwrap.dedent(FAKE_BUTLER))
        self.butler = Butler(cli=self.cli)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def calls(self) -> list[list[str]]:
        log = self.cli.with_suffix(".jsonl")
        return [json.loads(line) for line in log.read_text().splitlines()]

    def test_reserve_uses_run_id_as_idempotency_key_and_carries_all_dimensions(
        self,
    ) -> None:
        reservation = self.butler.gpu_reserve(
            project="test-project",
            job="run-42",
            gpus=2,
            hours=6,
            estimated_cost=24,
            currency="GBP",
            disk_gb=200,
        )
        call = self.calls()[0]
        self.assertEqual(reservation.reservation_id, "run-42")
        self.assertEqual(call[0], "gpu-reserve")
        self.assertEqual(call[call.index("--reservation-id") + 1], "run-42")
        self.assertEqual(call[call.index("--estimated-cost") + 1], "24")
        self.assertEqual(call[call.index("--disk-gb") + 1], "200")

    def test_reconcile_is_job_linked_and_records_non_negative_actual(self) -> None:
        self.butler.gpu_reconcile(
            project="test-project",
            reservation_id="run-42",
            actual_gpu_hours=7.5,
            actual_cost=20,
            outcome="failed",
        )
        call = self.calls()[0]
        self.assertEqual(call[0], "gpu-reconcile")
        self.assertEqual(call[call.index("--reservation-id") + 1], "run-42")
        self.assertEqual(call[call.index("--actual-gpu-hours") + 1], "7.5")
        self.assertEqual(call[call.index("--retained-disk-gb") + 1], "0")
        self.assertNotIn("gpu-log", call)

    def test_wrong_reservation_identity_fails_closed(self) -> None:
        self.cli.write_text(
            "import json; print(json.dumps({'verdict':'reserved', "
            "'reservation':{'reservation_id':'wrong'}}))"
        )
        with self.assertRaisesRegex(ButlerError, "wrong reservation identity"):
            self.butler.gpu_reserve(project="test-project", job="run-42", gpus=1, hours=1)


if __name__ == "__main__":
    unittest.main()
