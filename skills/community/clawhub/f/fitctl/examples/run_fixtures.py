#!/usr/bin/env python3
"""Run public fitctl fixture decisions: success, rejection, missing evidence.

Replay evidence only — fixtures are recorded artifacts from fitctl v0.8.0
(commit 1ec8777d69525b6037fa2654d084cddcf61e3c62), not observations of this host.

Usage: python3 run_fixtures.py [--out DIR] [--cache-dir DIR]
  --out DIR  also write each validation report JSON under DIR (optional)
  --cache-dir DIR  external input cache (default: .cache/fitctl-skill)

The first run downloads pinned public inputs from GitHub; cached inputs work
offline. Download and integrity failures are operational errors, not verdicts.

Exit status: 0 if all five cases produced their expected verdict family,
1 on an operational error (invalid input, missing fixture). A rejecting or
indeterminate verdict is a valid report, not an error. Covers all four
verdict values: fit, fit_with_degradation, unfit, indeterminate.
"""
import argparse
import pathlib
import sys

sys.dont_write_bytecode = True
from _public_inputs import public_inputs

try:
    import fitctl
except ImportError:
    sys.exit("operational error: fitctl python bindings not installed "
             "(python3 -m pip install --only-binary=:all: fitctl==0.1.1)")

# Fixture timestamps: host_state/linux-bare-metal-like-fresh-v1 was collected
# 2025-04-21T14:37:19Z. Case 3 evaluates 30 s later so the state is fresh.
AT_LIVE = "2025-04-21T14:37:49Z"
AT_PAST = "2026-09-28T12:00:00Z"


def load(path):
    return fitctl.Artifact.from_json(path.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=pathlib.Path, default=None)
    ap.add_argument("--cache-dir", type=pathlib.Path, default=pathlib.Path(".cache/fitctl-skill"))
    args = ap.parse_args()
    try:
        inputs = public_inputs(args.cache_dir)
    except (OSError, ValueError) as error:
        ap.exit(1, f"operational error: public example inputs: {error}\n")
    policy_path = inputs / "policy" / "general_compute_default.v1.json"
    survey_corpus = inputs / "fixtures" / "host_survey"
    state_corpus = inputs / "fixtures" / "host_state"
    profiles = inputs / "service_profiles"
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)

    policy = fitctl.Policy.from_json(policy_path.read_text(encoding="utf-8"))
    survey = fitctl.replay_survey(str(survey_corpus), "linux-bare-metal-like-v1")
    contract = fitctl.derive_contract(survey, policy, at=AT_PAST)

    cases = []

    # Case 1 — expected fit: general compute, contract_only.
    profile = load(profiles / "general_compute_contract_only.v2.json")
    report = fitctl.validate(contract, profile, at=AT_PAST)
    cases.append(("success-fit", report, {"fit"}, "general_compute_contract_only.v2"))

    # Case 2 — expected rejection: gpu_required against a no-accelerator fixture.
    profile = load(profiles / "gpu_required_contract_only.v2.json")
    report = fitctl.validate(contract, profile, at=AT_PAST)
    cases.append(("rejection-unfit", report, {"unfit"}, "gpu_required_contract_only.v2"))

    # Case 2b — expected degradation: GPU-preferred-with-fallback vs no-GPU host.
    profile = load(profiles / "gpu_preferred_with_general_compute_fallback_contract_only.v2.json")
    report = fitctl.validate(contract, profile, at=AT_PAST)
    cases.append(("degradation-fallback", report, {"fit_with_degradation"},
                  "gpu_preferred_with_general_compute_fallback_contract_only.v2"))

    # Case 3 — missing evidence: state_required with no state supplied.
    profile = load(profiles / "cpu_small_state_required.v2.json")
    report = fitctl.validate(contract, profile, at=AT_PAST, mode="state_required")
    cases.append(("missing-evidence", report, {"indeterminate"},
                  "cpu_small_state_required.v2 (no state)"))

    # Case 3b — fresh state supplied at a timestamp 30 s after collection.
    state = fitctl.replay_state(str(state_corpus), "linux-bare-metal-like-fresh-v1")
    contract_fresh = fitctl.derive_contract(survey, policy, at=AT_LIVE)
    report_fresh = fitctl.validate(
        contract_fresh, profile, at=AT_LIVE, state=state,
        mode="state_required", max_state_age_seconds=60)
    cases.append(("state-fresh", report_fresh, {"fit", "fit_with_degradation"},
                  "cpu_small_state_required.v2 (fresh state)"))

    ok = True
    for name, report, expected, profile_name in cases:
        verdict = report.verdict
        reason = report.primary_reason_code
        mark = "PASS" if verdict in expected else "FAIL"
        ok = ok and verdict in expected
        print(f"{mark}  {name}: verdict={verdict} reason={reason} "
              f"profile={profile_name}")
        if args.out:
            out = args.out / f"fixture-{name}.validation.json"
            out.write_text(report.to_json(), encoding="utf-8")
            print(f"      saved {out}")

    print(f"python bindings {fitctl.__version__} (core {fitctl.core_version}); "
          f"inputs from public fitctl v0.8.0 cached at {inputs} — replay evidence only")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
