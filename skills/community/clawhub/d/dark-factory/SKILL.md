---
name: dark-factory
description: Autonomously executes validated specifications from intent-engineering to produce provable, cryptographically signed outcome reports. Use when you need to: validate a specification for clarity and completeness, run behavioral tests against a mock environment, generate code autonomously, execute unit and integration tests, or produce a signed outcome report ready for feedback-loop analysis. Can be used standalone or as Stage 2 in the unified-orchestrator pipeline.
---

# Dark Factory

## Overview

The dark factory is the **execution engine** of the three-skill pipeline. It takes a structured specification produced by `intent-engineering`, validates it, runs behavioral tests, generates code, executes tests, and produces a cryptographically signed **Provable Outcome Report** — all autonomously.

| Role | Description |
| :--- | :--- |
| **The "How"** | Executes the "Why" defined by intent-engineering |
| **Input** | `specification.json` from intent-engineering |
| **Output** | `outcome_report.json` — signed, verifiable, ready for feedback-loop |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Agent (Orchestrator)                       │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ intent-          │  │ dark-factory     │  │ feedback-loop    │
│ engineering      │  │                  │  │                  │
│ (The "Why")      │  │ (The "How")      │  │ (The "Learn")    │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Shared Data     │
                    │  Contracts       │
                    └──────────────────┘
```

## Workflow

### Step 1 — Validate the Specification

```bash
python /home/ubuntu/skills/dark-factory/scripts/specification_validator.py my_spec.json
```

Checks required fields, validates structure, ensures behavioral scenarios are complete, and provides warnings.

### Step 2 — Run Behavioral Tests

```bash
python /home/ubuntu/skills/dark-factory/scripts/behavioral_test_engine.py my_spec.json
```

Executes all behavioral scenarios against a mock environment, calculates pass rates, and generates a test report.

### Step 3 — Run the Full Dark Factory

```bash
python /home/ubuntu/skills/dark-factory/scripts/orchestrator.py my_spec.json
```

The orchestrator runs the complete workflow in sequence:
1. Load and validate the specification
2. Execute behavioral tests
3. Generate code (AI agent integration point)
4. Execute unit and integration tests
5. Generate the signed outcome report

Output: `<spec-name>_outcome_report.json`

## Data Contracts

### Input — Specification from intent-engineering

```json
{
  "specification_id": "spec-12345678",
  "title": "Feature Name",
  "description": "What should be built",
  "behavioral_scenarios": [
    {
      "scenario": "Description",
      "input": {},
      "expected_output": {}
    }
  ],
  "success_criteria": {
    "test_pass_rate": 0.95
  }
}
```

### Output — Provable Outcome Report

```json
{
  "report_id": "report-12345678",
  "specification_id": "spec-12345678",
  "status": "success",
  "generated_code": {},
  "test_results": {},
  "security_evidence": {},
  "cryptographic_signature": {}
}
```

## Key Features

The dark factory provides four core capabilities. **Specification-Driven Development** ensures all execution is grounded in a validated, human-readable specification before any code is generated. **Behavioral Validation** runs all scenarios against a mock environment first, catching ambiguities early. **Autonomous Execution** coordinates code generation, unit testing, integration testing, and deployment without human intervention. **Provable Outcomes** produce a cryptographically signed report that can be independently verified and fed into the feedback-loop for continuous improvement.

## Key Metrics

| Metric | Target |
| :--- | :--- |
| Specification Validation Pass Rate | > 95% |
| Behavioral Test Pass Rate | > 95% |
| Execution Success Rate | > 90% |
| Average Execution Time | < 5 minutes |
| Evidence Verification Rate | 100% |

## Use Cases

**Autonomous Skill Development** — define a specification in intent-engineering, run the dark factory to build the skill autonomously, then verify with feedback-loop.

**Specification-Driven Testing** — validate and test a specification before committing to implementation using `specification_validator.py` and `behavioral_test_engine.py` independently.

**Continuous Integration** — integrate into CI/CD pipelines by running the validator and orchestrator as pipeline steps.

## Resources

| Path | Purpose |
| :--- | :--- |
| `scripts/specification_validator.py` | Validates specification structure and completeness |
| `scripts/behavioral_test_engine.py` | Executes behavioral scenarios against mock environment |
| `scripts/orchestrator.py` | Full workflow orchestrator — main entry point |
| `references/specification_schema.json` | JSON Schema defining valid specification format |
| `references/outcome_report_schema.json` | JSON Schema defining outcome report format |
| `references/triad_integration.md` | Complete three-skill ecosystem architecture |
| `references/behavioral_testing_guide.md` | How to write effective behavioral tests |
| `references/dark_factory_operations.md` | Operational procedures, monitoring, troubleshooting |
