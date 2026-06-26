# MinerU Public Benchmark

This page turns the repository's version-controlled sample runs into a public benchmark story.

## Scope

- Product: `MinerU`
- Model sample: `gpt-4.1-mini`
- Baseline run: [`data/runs/sample-run/summary.json`](../data/runs/sample-run/summary.json)
- Follow-up runs: [`repair-t7-run`](../data/runs/repair-t7-run/summary.json) and [`repair-t14-run`](../data/runs/repair-t14-run/summary.json)

## What changed

| Run | Mention | Positive | Capability | Ecosystem |
|---|---:|---:|---:|---:|
| Baseline | 80.00% | 70.00% | 100.00% | 50.00% |
| T+7 | 85.00% | 75.00% | 100.00% | 75.00% |
| T+14 | 90.00% | 82.00% | 100.00% | 100.00% |

## Delta from baseline

| Metric | Baseline -> T+7 | Baseline -> T+14 |
|---|---:|---:|
| Mention rate | +5.00 pts | +10.00 pts |
| Positive mention rate | +5.00 pts | +12.00 pts |
| Capability accuracy | +0.00 pts | +0.00 pts |
| Ecosystem accuracy | +25.00 pts | +50.00 pts |

## What the sample run says

1. MinerU already had strong capability understanding in the baseline sample.
2. The largest upside came from ecosystem clarity, which moved from `50%` to `100%` by T+14.
3. The repair backlog also shrank: the baseline sample had `outdated` and `negative_eval` issues, T+7 had one remaining `negative_eval`, and T+14 had no repair candidates left in the sample summary.

## Why this matters

For developer tools, LLM visibility often breaks at the point where a model has heard of the project but does not know when to recommend it, what integrations it belongs to, or whether it is still current. This sample benchmark makes that pattern visible.

## Public artifacts

- Baseline weekly report: [`data/runs/sample-run/weekly_report.md`](../data/runs/sample-run/weekly_report.md)
- T+14 weekly report: [`data/runs/repair-t14-run/weekly_report.md`](../data/runs/repair-t14-run/weekly_report.md)
- Before/after chart: [`assets/mineru-before-after.svg`](../assets/mineru-before-after.svg)

## Interpretation note

This is a **public repository sample benchmark**, not a third-party certified benchmark. Its value is that every metric and artifact is version-controlled and reproducible inside the repo.
