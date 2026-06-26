# Sciverse API Public Benchmark

This page shows a public benchmark snapshot for a scientific API / agent-workflow product.

## Scope

- Product: `Sciverse API`
- Sample run: [`data/runs/sciverse-sample-run/summary.json`](../data/runs/sciverse-sample-run/summary.json)
- Report: [`data/runs/sciverse-sample-run/weekly_report.md`](../data/runs/sciverse-sample-run/weekly_report.md)

## Core metrics

| Metric | Score |
|---|---:|
| Mention rate | 77.27% |
| Positive mention rate | 63.64% |
| Capability accuracy | 100.00% |
| Ecosystem accuracy | 83.33% |

## Funnel-stage slices

| Funnel stage | Mention | Positive | Capability | Ecosystem |
|---|---:|---:|---:|---:|
| Awareness | 75.00% | 75.00% | NA | NA |
| Selection | 75.00% | 75.00% | 100.00% | NA |
| Integration | 100.00% | 50.00% | NA | 100.00% |
| Activation | 75.00% | 25.00% | NA | NA |
| Agent | 75.00% | 75.00% | NA | 75.00% |

## What stands out

1. Capability understanding is already strong in the public sample.
2. The weakest stage is `activation`, where positive mention rate drops to `25%`.
3. Integration and agent scenarios are viable, but still exposed to positioning drift and friction.

## Top repair candidates

| Query ID | Repair type |
|---|---|
| `ecosystem-002` | `competitor_insert` |
| `competitor-002` | `weak_positioning` |
| `negative-001` | `integration_friction` |
| `negative-002` | `negative_eval` |

## Why this matters

This is a useful public example because scientific APIs often lose adoption in the handoff between discovery and activation. A model can know the API exists, yet still fail to give a confident next step for integration or agent use.

## Interpretation note

This page is a **public benchmark snapshot built from version-controlled sample artifacts**. It is intended to show how to evaluate a scientific API in the open, not to claim market leadership.
