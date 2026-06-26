# Demo Folder — Tutorial Recording Assets

Files in this folder support the v2.5.0 YouTube tutorial recording.

## Files

- **`matter.json`** — sample Matter Intake input for Demo 1 (FIDIC Red 1999, Singapore, Contractor, late site access, EOT + additional payment)
- **`run-demos.sh`** — orchestrator that runs the three demos with pauses between each, ready for live screen recording

## Usage

From the skill root (`skills/construction-law/`):

```bash
bash demo/run-demos.sh
```

Press Enter between each demo to advance. Each demo clears the screen so the recording stays clean.

## Standalone commands (if you prefer to run them individually)

```bash
# Demo 1 — Matter Intake (FIDIC Red EOT, late site access)
python3 scripts/intake.py --file demo/matter.json

# Demo 2 — FIDIC Comparator (risk allocation: Red vs Yellow vs Silver)
python3 scripts/construction_law.py compare --forms red,yellow,silver --topic risk

# Demo 2b — Export claims comparison to CSV
python3 scripts/construction_law.py compare --forms red,silver --topic claims --format csv --output comparison.csv

# Demo 3 — SOP Act timeline (Payment Claim 30 Jun 2026)
python3 scripts/sop_calculator.py --claim-date 2026-06-30
```

## Note

These demo artefacts are excluded from the published skill via `.gitignore` / publish manifest if needed — they're recording aids, not user-facing skill assets.
