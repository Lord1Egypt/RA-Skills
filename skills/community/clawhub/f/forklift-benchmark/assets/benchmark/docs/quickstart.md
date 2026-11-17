# Quickstart

This guide walks you through installing FK-Bench v2, generating the 500-item
dataset, validating it, and scoring a mock prediction. It assumes a Unix-like
shell; on Windows, replace `source .venv/bin/activate` with
`.venv\Scripts\activate`.

## 1. Prerequisites

- Python 3.9, 3.10, 3.11, or 3.12.
- `git`.
- ~150 MB of free disk space (the dataset and PyPI cache).

## 2. Install

```bash
git clone https://github.com/forklift-benchmark/forklift-benchmark-v2.git
cd forklift-benchmark-v2
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
```

This installs the runtime dependencies (`pydantic`, `PyYAML`) plus the
dev extras (`pytest`, `pytest-cov`, `ruff`).

## 3. Generate the dataset (optional)

A pre-generated dataset ships in `data/v2.0/`. If you want to regenerate
it from the templates:

```bash
python -m generator.run --total 500 --seed 42 --output data/v2.0
```

The seed is fixed at 42 to guarantee bit-exact reproducibility.

## 4. Run the static validator

```bash
python -m validator.run --dataset data/v2.0 --report validator_report.json
```

A clean run reports a pass-rate of ≥ 95 %. The report is also written to
`validator_report.json` for downstream tooling.

## 5. Score a prediction

A "prediction" is a JSON file shaped like a list of `Item` objects whose
`prediction` field has been filled in by your model. The repo ships a
mock predictor in `examples/run_demo.py` so you can see the expected
shape:

```bash
python examples/run_demo.py
```

It will:

1. Generate 5 mini-items using the combinatorial template.
2. Call a mock predictor that returns a plausible action plan.
3. Run the three-layer scorer (red-line veto + LCS + parameter IoU).
4. Write a Markdown report to `examples/demo_report.md`.

## 6. Run the test suite

```bash
pytest -v
```

The suite is the source of truth for the validator and scorer contracts.
It must pass on every supported Python version before any release.

## 7. Where to go next

- `docs/schema.md` — the canonical Pydantic models for `Item`,
  `ActionPlan`, `EvalMetrics`, etc.
- `docs/scoring.md` — the three-layer scoring formula and edge cases.
- `docs/modules.md` — the six evaluation modules and their red-line
  conditions.
- `knowledge/` — domain background (standards, physics, attachments,
  scenes, slang, sensor anomalies, references).

## 8. Troubleshooting

- **`ModuleNotFoundError: dsl`** — install the package in editable mode
  with `pip install -e .` so the `dsl/`, `generator/`, `validator/`, and
  `scorer/` subpackages are importable.
- **`pydantic` validation errors** — your data is from an older draft of
  the schema. Re-run the generator with `--seed 42` to obtain the v2
  shapes.
- **The validator rejects a plan that "looks fine"** — double-check the
  load centre of gravity and the derated capacity curve. The red-line
  rules in `MOD-4` are intentionally strict; they cite specific clauses
  of GB/T 43756, ISO 3691-1, and TSG 11.
