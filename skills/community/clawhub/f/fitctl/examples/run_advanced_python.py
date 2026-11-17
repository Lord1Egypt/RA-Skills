#!/usr/bin/env python3
"""Replayable Python advanced operations: batch comparison, redaction,
semantic identity, and operational-error shape.

Uses pinned public fixtures (replay evidence, no live collection). Run with
the same interpreter that imports fitctl 0.1.1+:

  <fitctl-py> run_advanced_python.py [--out DIR] [--cache-dir DIR]

The first run downloads inputs from GitHub into .cache/fitctl-skill (or the
specified external cache). A verified cache works offline.

Exit 0 when every check hits its expected outcome; 1 otherwise.
"""
import argparse
import pathlib
import sys

sys.dont_write_bytecode = True
from _public_inputs import public_inputs
import fitctl

AT = "2026-09-28T12:00:00Z"   # replay example timestamp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=pathlib.Path, default=None)
    ap.add_argument("--cache-dir", type=pathlib.Path, default=pathlib.Path(".cache/fitctl-skill"))
    args = ap.parse_args()
    try:
        inputs = public_inputs(args.cache_dir)
    except (OSError, ValueError) as error:
        ap.exit(1, f"operational error: public example inputs: {error}\n")
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)

    policy = fitctl.Policy.from_json(
        (inputs / "policy" / "general_compute_default.v1.json").read_text(encoding="utf-8"))
    survey = fitctl.replay_survey(str(inputs / "fixtures" / "host_survey"),
                                  "linux-bare-metal-like-v1")
    contract = fitctl.derive_contract(survey, policy, at=AT)
    profiles = [fitctl.Artifact.from_json(
        (inputs / "service_profiles" / name).read_text(encoding="utf-8"))
        for name in ("general_compute_contract_only.v2.json",
                     "gpu_required_contract_only.v2.json")]

    ok = True

    # Batch: one contract x two profiles -> fit + unfit rows, CSV export.
    batch = fitctl.classify_batch([contract], profiles, at=AT)
    rows = [(r["verdict"], r["primary_reason_code"]) for r in batch.rows]
    expect = [("fit", "requirements_satisfied"), ("unfit", "capability_unknown")]
    good = rows == expect
    ok &= good
    print(f"{'PASS' if good else 'FAIL'}  classify_batch rows: {rows}")
    csv_text = batch.export_csv("rows_csv")
    good = csv_text.startswith("row_id,host_alias,")
    ok &= good
    print(f"{'PASS' if good else 'FAIL'}  rows_csv header present ({len(csv_text)} bytes)")

    # Redaction: external profile changes identity, replaces source/correlation.
    survey_d = survey.to_dict()["envelope"]["provenance"]
    redacted = survey.redact("external", at=AT)
    rd = redacted.to_dict()
    prov = rd["envelope"]["provenance"]
    good = (redacted.artifact_id == prov["correlation_id"]
            and prov.get("source") != survey_d.get("source")
            and redacted.semantic_hash() != survey.semantic_hash())
    ok &= good
    print(f"{'PASS' if good else 'FAIL'}  redact(external): id={redacted.artifact_id[:20]}... "
          f"source={prov.get('source')}")

    # Semantic identity is stable across serialization roundtrips.
    h = survey.semantic_hash()
    good = h == fitctl.Artifact.from_json(survey.to_json()).semantic_hash()
    ok &= good
    print(f"{'PASS' if good else 'FAIL'}  semantic_hash stable ({h[:16]}...)")

    # Operational error shape: malformed JSON -> DecodeError with reason_code.
    try:
        fitctl.Artifact.from_json("{not json")
        print("FAIL  expected DecodeError")
        ok = False
    except fitctl.DecodeError as e:
        print(f"PASS  DecodeError reason_code={e.reason_code} checkpoint={e.checkpoint_id}")

    if args.out:
        args.out.joinpath("advanced-batch.json").write_text(batch.to_json(), encoding="utf-8")
        args.out.joinpath("advanced-batch.csv").write_text(csv_text, encoding="utf-8")
        args.out.joinpath("advanced-redacted.survey.json").write_text(
            redacted.to_json(), encoding="utf-8")
    print(f"inputs from public fitctl v0.8.0 cached at {inputs} — replay evidence only")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
