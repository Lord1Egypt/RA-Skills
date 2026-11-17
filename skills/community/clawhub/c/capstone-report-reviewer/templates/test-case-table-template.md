# Test Case Table Template (Chapter 5)

Fill during debugging — it doubles as your debug log and your report material.

## Per-function test table

| Case ID | Function | Input condition | Expected result | Measured result | Verdict | Notes |
|------|------|----------|----------|----------|------|------|
| T-01 | [FILL IN] | | | | PASS/FAIL | |
| T-02 | | | | | | |
| T-03 | | | | | | |

## Stability test record

| Item | Value |
|------|------|
| Continuous run duration | e.g. 8 h |
| Sampling interval | e.g. 10 min |
| Samples collected | |
| Drift statistics | max / mean / stddev |
| Failures/reboots during run | |

## Error analysis skeleton

| Metric | Spec | Measured | Deviation | Source of error |
|------|------|------|------|------|
| [FILL IN] | | | | e.g. sensor accuracy / ADC quantization / environmental interference |

Rules:
- Multi-condition coverage required: at least normal, boundary, and one adversarial case per function
- A single success screenshot is not a test — examiners will ask for repeated runs
- Every FAIL followed by a fix note is *good* material: it proves the work is yours
