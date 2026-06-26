#!/usr/bin/env python3
"""Basic regression checks for flight and transport entrypoints."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FLIGHT_SCRIPT = ROOT / "scripts" / "domestic_flight_public_service.py"
TRANSPORT_SCRIPT = ROOT / "scripts" / "transport_service.py"
FLIGHT_SAMPLE = ROOT / "assets" / "sample-public-state.json"
TRAIN_QUERY_SAMPLE = ROOT / "assets" / "sample-train-query.json"
TRAIN_PRICE_SAMPLE = ROOT / "assets" / "sample-train-price.json"


def run_command(script: Path, *args: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(script), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    payload = run_command(
        FLIGHT_SCRIPT,
        "search",
        "--from",
        "北京首都",
        "--to",
        "上海",
        "--date",
        "2026-03-20",
        "--sample-state",
        str(FLIGHT_SAMPLE),
        "--limit",
        "1",
        "--sort-by",
        "price",
    )
    assert payload["trip_type"] == "one-way"
    assert payload["outbound"]["route"]["from"]["code"] == "PEK"
    assert payload["outbound"]["route"]["to"]["code"] == "SHA"
    assert payload["outbound"]["count"] == 1
    assert payload["outbound"]["flights"][0]["ticket_price"] == 700
    assert payload["outbound"]["flights"][0]["flight_no"] == "MU5100"

    round_trip = run_command(
        FLIGHT_SCRIPT,
        "search",
        "--from",
        "北京首都",
        "--to",
        "上海",
        "--date",
        "2026-03-20",
        "--return-date",
        "2026-03-22",
        "--sample-state",
        str(FLIGHT_SAMPLE),
        "--return-sample-state",
        str(FLIGHT_SAMPLE),
        "--limit",
        "1",
        "--direct-only",
    )
    assert round_trip["trip_type"] == "round-trip"
    assert round_trip["return"]["route"]["from"]["code"] == "SHA"
    assert round_trip["return"]["route"]["to"]["code"] == "PEK"
    assert round_trip["return"]["count"] == 1

    transport_flight_payload = run_command(
        TRANSPORT_SCRIPT,
        "search",
        "--mode",
        "flight",
        "--from",
        "北京首都",
        "--to",
        "上海",
        "--date",
        "2026-03-20",
        "--sample-state",
        str(FLIGHT_SAMPLE),
        "--limit",
        "1",
    )
    assert transport_flight_payload["mode"] == "flight"
    assert transport_flight_payload["trip_type"] == "one-way"
    assert transport_flight_payload["outbound"]["options"][0]["flight_no"] == "MU5100"

    transport_train_payload = run_command(
        TRANSPORT_SCRIPT,
        "search",
        "--mode",
        "train",
        "--from",
        "BJP",
        "--to",
        "SHH",
        "--date",
        "2026-03-20",
        "--seat-type",
        "second_class",
        "--sample-train-query",
        str(TRAIN_QUERY_SAMPLE),
        "--sample-train-price",
        str(TRAIN_PRICE_SAMPLE),
        "--limit",
        "1",
    )
    assert transport_train_payload["mode"] == "train"
    assert transport_train_payload["outbound"]["count"] == 1
    assert transport_train_payload["outbound"]["options"][0]["train_no"] == "G1"
    assert transport_train_payload["outbound"]["options"][0]["ticket_price"] == 662.0
    assert transport_train_payload["outbound"]["options"][0]["seat_availability"]["second_class"] == "有"
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
