# Dark Factory Operations

## Quick Start

```bash
# 1. Validate your specification
python /home/ubuntu/skills/dark-factory/scripts/specification_validator.py my_spec.json

# 2. Run behavioral tests only (optional pre-check)
python /home/ubuntu/skills/dark-factory/scripts/behavioral_test_engine.py my_spec.json

# 3. Run the full dark factory
python /home/ubuntu/skills/dark-factory/scripts/orchestrator.py my_spec.json

# 4. Review the outcome report
cat my_spec_outcome_report.json | python3 -m json.tool
```

## Detailed Workflow

### Step 1 — Prepare the Specification

Obtain a `specification.json` from `intent-engineering` or write one manually following `specification_schema.json`. The specification must include at minimum: `specification_id`, `title`, `description`, `behavioral_scenarios` (at least one), and `success_criteria.test_pass_rate`.

### Step 2 — Validate

Always run the validator before the orchestrator. Validation is fast (< 1 second) and catches structural errors that would cause the orchestrator to fail mid-run.

```bash
python specification_validator.py my_spec.json
# Exit code 0 = passed, 1 = failed
```

### Step 3 — Run Behavioral Tests (Optional Pre-check)

Running the behavioral test engine independently lets you verify that your scenarios are testable before committing to the full orchestration run.

```bash
python behavioral_test_engine.py my_spec.json --output pre_check_report.json
```

### Step 4 — Run the Full Orchestrator

```bash
python orchestrator.py my_spec.json --output-dir ./output/
```

The orchestrator runs all five stages in sequence and writes the outcome report to `<spec-name>_outcome_report.json`. Exit code 0 = success, 1 = partial or failed.

### Step 5 — Review the Outcome Report

The outcome report contains:
- `status` — `success`, `partial`, or `failed`
- `performance_metrics` — pass rates for all three test stages
- `generated_code` — the AI-generated implementation files
- `test_results` — detailed results for behavioral, unit, and integration tests
- `edge_cases` — failed scenarios to feed into the feedback-loop
- `cryptographic_signature` — SHA-256 digest proving report integrity

### Step 6 — Feed into Feedback Loop

Pass the outcome report and original specification to `feedback-loop` for analysis and improvement:

```bash
python /home/ubuntu/skills/feedback-loop/scripts/feedback_loop_orchestrator.py \
  --spec my_spec.json \
  --outcome my_spec_outcome_report.json
```

Or use the unified-orchestrator to run all three stages at once.

## Monitoring

Track these metrics across runs to understand the health of your dark factory:

| Metric | Target | Action if Below Target |
| :--- | :--- | :--- |
| Specification Validation Pass Rate | > 95% | Review specification quality, add more detail to scenarios |
| Behavioral Test Pass Rate | > 95% | Review failed scenarios, clarify expected outputs |
| Unit Test Pass Rate | > 90% | Review generated code, check for ambiguous scenarios |
| Integration Test Pass Rate | > 90% | Verify dependencies are registered in skill_registry.json |
| Overall Execution Success Rate | > 90% | Review full outcome report for root cause |
| Average Execution Time | < 5 minutes | Check for slow integration dependencies |

## Troubleshooting

**Validation fails with "Missing required field"** — check that your specification includes all required top-level fields. Run `specification_validator.py` and fix each reported error before proceeding.

**Behavioral pass rate is 0%** — this usually means the specification has no `behavioral_scenarios` or they are malformed. Verify the JSON structure against `specification_schema.json`.

**Orchestrator exits with code 1** — check the outcome report `status` field. If `partial`, the pass rate was between 70–90%. If `failed`, it was below 70%. Review `edge_cases` and `failures` in the report.

**Integration tests all fail** — the mock integration test engine tests against registered dependencies. Ensure all dependencies are listed in `specification.dependencies` and registered in `skill_registry.json`.

## Advanced Operations

### Running with Custom Output Directory

```bash
python orchestrator.py my_spec.json --output-dir /path/to/output/
```

### Validating Multiple Specifications

```bash
for spec in specs/*.json; do
  echo "Validating: $spec"
  python specification_validator.py "$spec" && echo "PASS" || echo "FAIL"
done
```

### CI/CD Integration

```yaml
# Example GitHub Actions step
- name: Validate Specification
  run: python /home/ubuntu/skills/dark-factory/scripts/specification_validator.py spec.json

- name: Run Behavioral Tests
  run: python /home/ubuntu/skills/dark-factory/scripts/behavioral_test_engine.py spec.json

- name: Run Dark Factory
  run: python /home/ubuntu/skills/dark-factory/scripts/orchestrator.py spec.json --output-dir ./artifacts/
```

### Verifying Report Integrity

The outcome report includes a SHA-256 digest of its own content (excluding the signature field). To verify:

```python
import json, hashlib

report = json.load(open("outcome_report.json"))
sig = report.pop("cryptographic_signature")
content = json.dumps(report, sort_keys=True, separators=(",", ":"))
digest = hashlib.sha256(content.encode()).hexdigest()
print("VALID" if digest == sig["digest"] else "TAMPERED")
```
