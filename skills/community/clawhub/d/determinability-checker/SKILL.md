---
name: determinability-checker
version: 2.0.0
description: Check target determinability on a bounded finite configuration set.
---

# determinability-checker

Use only when the user requests this specific operation. Review SECURITY.md before running the service.

## Determinability behavior

Accepts 1–128 uniquely named configurations and at most 32 evidence fields. Every requested field must exist; absent fields are errors, not shared null observations. Observation/target values must be finite JSON scalars. Boolean and numeric values remain distinct. Decision-table keys are canonical JSON representations (`"true"`, `"1"`, or an encoded JSON string); decode keys with JSON parsing.

The checker runs in a worker thread and bounds conflict edges to 8,128. Evidence cover selection is a greedy heuristic; the legacy method name `find_minimal_evidence_cover` does not mean global optimality. `can_proceed` states determinability over the submitted finite dataset only; it is not execution permission, factual correctness or a safety guarantee.

## Setup

Work from the package directory containing `skill/` and `requirements.txt`. Install locked dependencies with `pip install --require-hashes -r requirements.txt`, provision the documented authentication configuration, and run on 127.0.0.1. This package never starts a daemon or changes another runtime automatically.
