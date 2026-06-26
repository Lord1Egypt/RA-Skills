# Prompt — Model Selection

## Purpose

A reusable decision prompt to pick the **cheapest Claude model that meets the quality bar** for a given task, avoiding overspending on Opus when Haiku or Sonnet would do.

## Reusable template

```
You are choosing a Claude model for a task. Default to the cheapest tier and
escalate only if quality is insufficient.

Task: {{task_description}}
Volume: {{requests_per_day}} requests/day
Latency sensitivity: {{latency_need}}   # low | medium | high
Quality bar: {{quality_bar}}            # e.g. "must extract fields with >98% accuracy"
Budget sensitivity: {{budget_need}}     # low | medium | high

Rules:
- Start at claude-haiku-4-5 (cheapest, fastest).
- Escalate to claude-sonnet-4-6 only if Haiku fails the quality bar on a sample.
- Escalate to claude-opus-4-8 only for hard reasoning/coding where Sonnet fails.
- Prefer Haiku for high volume or high latency sensitivity.
- Always set max_tokens to the smallest value that fits the expected output.

Output: the chosen model, max_tokens suggestion, and a one-line justification.
```

## Variables

| Variable | Meaning |
|----------|---------|
| `{{task_description}}` | What the model must do. |
| `{{requests_per_day}}` | Expected volume (drives cost). |
| `{{latency_need}}` | How fast responses must be. |
| `{{quality_bar}}` | Concrete acceptance criterion. |
| `{{budget_need}}` | How cost-sensitive the use case is. |

## Example (filled)

```
Task: Classify support tickets into 5 categories.
Volume: 50000 requests/day
Latency sensitivity: high
Quality bar: >95% category accuracy on a 200-item sample
Budget sensitivity: high
```

Expected decision: **claude-haiku-4-5**, `max_tokens: 16`, justification: high volume + simple classification + tight budget; validate accuracy on the sample before scaling.

## Bad

> "Use claude-opus-4-8 for everything to be safe."

Wastes money — Opus is the most expensive tier; a classifier needs Haiku.

## Good

> "Start with Haiku; measure accuracy on a 200-item sample; escalate to Sonnet only if it misses the 95% bar. Set max_tokens to 16 (single label)."

Cheapest viable choice with a concrete escalation rule and a tight output cap.
