# Spanish Ham Demo Validation Result

## Commands Run

```bash
python3 scripts/validate_orchestrator_contracts.py
python3 scripts/smoke_test_full_report.py
python3 scripts/validate_demo_run.py
```

## Results

| Check | Status | Notes |
|---|---|---|
| Orchestrator contracts | passed | registry exists, relative paths start with `../`, routing and missing-output rules passed |
| Full report smoke test | passed | original `final_report.md` smoke test still passes |
| Spanish Ham demo run | passed | required directories, JSON files, client report, mock disclaimer and retest plan are present |

## Raw Output

### validate_orchestrator_contracts.py

```json
{
  "status": "passed",
  "errors": [],
  "warnings": [],
  "checks": [
    "registry exists",
    "relative_path starts with ../",
    "gap matrix can produce content task plan",
    "industry routing selects expected platform Skills",
    "missing downstream output is partial/failed",
    "customer delivery report contains full required sections",
    "summary-only output is rejected"
  ]
}
```

### smoke_test_full_report.py

```text
smoke test passed
```

### validate_demo_run.py

```json
{
  "status": "passed",
  "errors": [],
  "warnings": [],
  "run_dir": "/Users/wanglujie/Documents/Skills/powermatrix-geo-growth-orchestrator/runs/spanish_ham_demo"
}
```
