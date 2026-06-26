# agent-cost-eval-kit — Before/After Input Examples

This file shows what "good enough" input looks like for the eval agent cost change skill.
Copy, modify, and paste into your agent conversation.

## Minimal Useful Input

The minimum viable before/after evaluation:

```
Change made: reduced retry count from 3 to 1 on the summarization sub-agent
Before: 3 retries on timeout, average 4.2k tokens/run, occasional 3x billing on slow turns
After: 1 retry, average 3.8k tokens/run, timeout failure rate up from 2% to 7%
Observed result: cost down ~10%, but timeout failures noticeably higher on long documents
```

## Good Input with Numbers

```
Change made: switched research sub-agent from MiniMax-M2.7 to MiniMax-M2.5
Before:
  - model: MiniMax-M2.7
  - avg tokens/run: 12,400
  - avg cost/run: $0.34
  - success rate: 98%
  - avg latency: 4.2s
  - quality: 4.1/5 avg reviewer score (last 20 runs)

After:
  - model: MiniMax-M2.5
  - avg tokens/run: 11,100
  - avg cost/run: $0.19
  - success rate: 95%
  - avg latency: 2.8s
  - quality: 3.8/5 avg reviewer score (last 20 runs)

Task type: research synthesis on structured data
Risk class: Medium
Observed quality issue: 3 reviewer flags for incomplete citations on complex queries
Human notes: acceptable for internal reports, not for client-facing deliverables
```

## Minimal Input for Low-Risk Task

```
Change made: changed daily digest job from every 4h to every 8h
Before: ran 6x/day, 1.2k tokens/run
After: ran 3x/day, 1.1k tokens/run
Observed result: same coverage, ~50% token reduction on this job
```

## High-Risk Workflow — Requires Human Review

```
Change made: downgraded coding sub-agent from claude-sonnet-4 to claude-haiku
Before:
  - model: claude-sonnet-4
  - bug escape rate: 3%
  - review comment density: 0.4 comment/file
  - avg cost/file: $0.82

After:
  - model: claude-haiku
  - bug escape rate: 11%
  - review comment density: 1.2 comment/file
  - avg cost/file: $0.09

Task type: code review on production Python
Risk class: High
Observed quality issue: significant increase in bug escape rate and review burden
Human notes: this should not be kept for production code without explicit approval
```

## Narrowing Example — Keep for Low Risk Only

```
Change made: changed fallback model from MiniMax-M2.7 to MiniMax-M2.5 on all routes
Before: fallback always to M2.7
After: fallback to M2.5 for summarization,保留了 M2.7 for reasoning tasks

Result: overall cost down 18%, BUT reasoning task failures up from 1% to 9%

Decision pattern from eval:
  - summarization tasks: Keep Change (Low risk, quality held)
  - reasoning tasks: Revert Change (Medium risk, failures unacceptable)
  - narrow: only apply M2.5 fallback to Low-risk, non-reasoning tasks
```
