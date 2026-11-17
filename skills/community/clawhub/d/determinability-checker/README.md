# determinability-checker 2.0.0 — repair candidate

## Determinability behavior

Accepts 1–128 uniquely named configurations and at most 32 evidence fields. Every requested field must exist; absent fields are errors, not shared null observations. Observation/target values must be finite JSON scalars. Boolean and numeric values remain distinct. Decision-table keys are canonical JSON representations (`"true"`, `"1"`, or an encoded JSON string); decode keys with JSON parsing.

The checker runs in a worker thread and bounds conflict edges to 8,128. Evidence cover selection is a greedy heuristic; the legacy method name `find_minimal_evidence_cover` does not mean global optimality. `can_proceed` states determinability over the submitted finite dataset only; it is not execution permission, factual correctness or a safety guarantee.

See [SECURITY.md](SECURITY.md) for configuration, signing, migration and installation.
