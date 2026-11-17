#!/usr/bin/env python3
"""
Regression test for scripts/ledger.py. Stdlib only, no test framework
required -- run it directly:

    python3 examples/stress_test.py

Generates 200 random expenses (mixed split types, several participant
subsets) across 5 people and checks two invariants that must always hold
no matter what split types or amounts show up:

  1. Net balances sum to *exactly* zero in integer minor units (not
     "close to zero" -- see references/settlement-algorithm.md for why
     this matters).
  2. `settle` never proposes more than `members - 1` payments.

Exits non-zero on any failure, so it's CI-friendly.
"""

import json
import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "..", "scripts", "ledger.py")
NAMES = ["Alice", "Bob", "Priya", "Dev", "Sara"]
N_EXPENSES = 200
SEED = 42


def run(data_dir, *args):
    result = subprocess.run(
        [sys.executable, LEDGER, "--data-dir", data_dir, *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"FAILED: {args}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def main():
    # Throwaway ledger directory, cleaned up automatically on exit.
    with tempfile.TemporaryDirectory(prefix="fairsplit-stress-") as data_dir:
        check(data_dir)


def check(data_dir):
    run(data_dir, "init", "--group", "Stress", "--currency", "USD",
        "--members", ",".join(NAMES))

    random.seed(SEED)
    for _ in range(N_EXPENSES):
        payer = random.choice(NAMES)
        amount = round(random.uniform(1, 999), 2)
        participants = random.sample(NAMES, random.randint(1, len(NAMES)))
        split = random.choice(["equal", "shares", "percent"])

        args = ["add", "--group", "Stress", "--payer", payer,
                "--amount", str(amount),
                "--participants", ",".join(participants),
                "--split", split]

        if split in ("shares", "percent"):
            weights = [random.randint(1, 5) for _ in participants]
            detail = ",".join(f"{p}:{w}" for p, w in zip(participants, weights))
            args += ["--detail", detail]

        run(data_dir, *args)

    with open(os.path.join(data_dir, "stress.json")) as fh:
        state = json.load(fh)

    net = {m: 0 for m in state["members"]}
    for expense in state["expenses"]:
        net[expense["payer"]] += expense["amount_minor"]
        for person, minor in expense["shares_minor"].items():
            net[person] -= minor

    total_drift = sum(net.values())
    assert total_drift == 0, f"balances do not sum to zero: drift={total_drift}"

    settle_output = run(data_dir, "settle", "--group", "Stress")
    n_payments = settle_output.count("pays")
    max_expected = len(NAMES) - 1
    assert n_payments <= max_expected, (
        f"settlement used {n_payments} payments, expected at most {max_expected}"
    )

    print(f"OK: {N_EXPENSES} random expenses across {len(NAMES)} people")
    print("OK: balances sum to exactly zero (integer minor units)")
    print(f"OK: settlement used {n_payments} payments (<= {max_expected})")


if __name__ == "__main__":
    main()
