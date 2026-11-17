# FK-Bench v2 · Forklift Embodied Intelligence Benchmark

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](#-quickstart)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-success.svg)](.github/workflows/ci.yml)
[![Dataset](https://img.shields.io/badge/dataset-500_items-orange.svg)](data/v2.0/)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen.svg)](CHANGELOG.md)
[![Cite](https://img.shields.io/badge/cite-CITATION.cff-lightgrey.svg)](CITATION.cff)

> **FK-Bench v2** (Forklift Embodied Intelligence Benchmark v2) is a
> **multimodal embodied-AI evaluation suite** for counterbalance forklift
> scenarios. It ships **500** items spanning **6 evaluation modules** and
> **7 industrial scenes**, with a **three-layer automatic scoring engine**
> and a **physics / safety static validator** out of the box.

[中文 README](README.md) | [Quickstart](docs/quickstart.md) |
[Schema](docs/schema.md) | [Scoring](docs/scoring.md) |
[Modules](docs/modules.md)

---

## ✨ Highlights

- **Combinatorial 500-item dataset** — fully reproducible from seed `42`,
  spanning MOD-1 through MOD-6.
- **Seven industrial scenes** — `S1_HIGH_BAY`, `S2_BLOCK`, `S3_DOCK`,
  `S4_LINE_SIDE`, `S5_VNA`, `S6_OUTDOOR`, `S7_MIXED`.
- **Three difficulty tiers** — `basic` / `intermediate` / `edge`
  (200 / 225 / 75 items).
- **15-action DSL** — `NAVIGATE`, `LIFT`, `LOWER`, `TILT_FORWARD`,
  `TILT_BACK`, `SIDESHIFT`, `CLAMP`, `RELEASE`, `ROTATE_CARGO`,
  `FORK_ADJUST`, `TRAVERSE`, `HORN`, `EMERGENCY_STOP`, `RAISE_ALARM`,
  `ASK_CLARIFICATION`.
- **Static validator** — physics (overload, derated capacity, centre of
  gravity) + safety (red lines mapped to GB/T 43756, ISO 3691-1,
  ISO 23308, TSG 11) + JSON Schema checks.
- **Three-layer scoring engine** — red-line veto + LCS sequence
  similarity (weight 0.4) + parameter IoU (weight 0.6), final score 0–100.
- **Domain knowledge base** — standards, physics, attachments, scenes,
  slang, sensor anomalies, and ≥15 traceable reference URLs.
- **End-to-end demo** — `examples/run_demo.py` runs the full pipeline
  offline in seconds.

## 📦 Repository layout

```
forklift-benchmark-v2/
├── README.md               # Chinese (main) README
├── README.en.md            # English README
├── LICENSE                 # Apache-2.0
├── CONTRIBUTING.md         # Contribution guide
├── CHANGELOG.md            # Version history
├── CITATION.cff            # Citation metadata
├── pyproject.toml          # pip install -e .
├── requirements.txt        # Runtime deps
├── requirements-dev.txt    # Dev deps
├── .gitignore              # Python defaults
├── .github/
│   └── workflows/ci.yml    # GitHub Actions: lint + pytest + build
├── docs/
│   ├── quickstart.md       # Quickstart
│   ├── schema.md           # Data schema
│   ├── scoring.md          # Scoring formula
│   └── modules.md          # Module reference
├── examples/
│   └── run_demo.py         # End-to-end demo (standalone)
├── forklift_benchmark/     # Top-level Python package (with CLI)
│   ├── __init__.py
│   ├── cli.py
│   └── py.typed
├── dsl/                    # Action DSL & Pydantic schema
├── generator/              # Combinatorial generator
├── validator/              # Physics / safety / schema validator
├── scorer/                 # Three-layer scoring engine
├── tests/                  # pytest tests
├── data/
│   └── v2.0/               # 500 JSON items + index.json
└── knowledge/              # Domain knowledge (standards, physics,
                            # attachments, scenes, slang, sensors, refs)
```

## 🚀 Quickstart

```bash
git clone https://github.com/forklift-benchmark/forklift-benchmark-v2.git
cd forklift-benchmark-v2
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"

# Run the end-to-end demo (offline, 5 mini-items)
python examples/run_demo.py

# Run the full test suite
pytest -v
```

See [`docs/quickstart.md`](docs/quickstart.md) for the complete walk-through.

## 📊 Module & scene distribution

| Module | Name                                | Items | basic | intermediate | edge |
|--------|-------------------------------------|-------|-------|--------------|------|
| MOD-1  | Navigation & Path Planning          | 80    | 32    | 36           | 12   |
| MOD-2  | Load Handling & Fork Operations     | 100   | 40    | 45           | 15   |
| MOD-3  | Attachment Awareness                | 100   | 40    | 45           | 15   |
| MOD-4  | Safety & Red-Line Compliance        | 90    | 36    | 40           | 14   |
| MOD-5  | Site Topology Reasoning             | 80    | 32    | 36           | 12   |
| MOD-6  | Sensor Anomaly Robustness           | 50    | 20    | 22           | 8    |

Scene distribution: `S1=80 / S2=80 / S3=75 / S4=85 / S5=65 / S6=60 / S7=55`.

> **MOD-4 red lines.** All 90 MOD-4 items **must** trigger a
> `SAFETY_ABORT` decision (`EMERGENCY_STOP`, `RAISE_ALARM`, or
> `ASK_CLARIFICATION`). Any plan that fails to abort is hard-vetoed to
> `0` on that item.

## 🔬 Scoring formula

```
score = 100 · red_line · (0.4 · lcs + 0.6 · iou)
```

* `red_line ∈ {0, 1}` — a one-strike veto on MOD-4 or hard
  physical / regulatory violations.
* `lcs` — longest common subsequence ratio between the predicted and
  gold action sequences, lightly adjusted by the Jaccard overlap.
* `iou` — per-key tolerance score on shared numeric parameters, with
  a 10 % tolerance band per parameter.

See [`docs/scoring.md`](docs/scoring.md) for the full reference.

## 🤝 Contributing

Issues, pull requests, and dataset additions are all welcome. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the workflow and coding
conventions.

## 📚 Citation

If this benchmark is useful in your work, please cite it as:

```bibtex
@misc{fkbenchv2,
  title   = {FK-Bench v2: A 500-Item Multimodal Benchmark for Embodied Forklift Agents},
  year    = {2026},
  version = {2.0.0},
  url     = {https://github.com/forklift-benchmark/forklift-benchmark-v2},
  note    = {Apache-2.0 License}
}
```

You can also use the [`CITATION.cff`](CITATION.cff) file at the repo
root — GitHub will render a "Cite this repository" button automatically.

## 📄 License

Released under the [Apache License 2.0](LICENSE). © 2026 Forklift
Embodied Intelligence Benchmark Authors.
