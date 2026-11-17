---
name: agent-cost-guard
description: Audit agent cost, Curator and background work; cap it.
category: agents
tags: [cost, curator, background-work, tokens, guardrail, audit]
allowed-tools: []
permissions:
  scheme: none
  hosts: []
  file_read: none
  file_write: none
  environment: none
  secrets: none
  shell: none
---

# Agent Cost Guard (read-only audit guide)

This package contains **documentation and reference tables only**. It ships no code, makes no network call, reads
no file, touches no key material and cannot move money. Everything below is a checklist you run with the tools you
already have on your own machine.

## What is in this package
- `SKILL.md` - this checklist (Steps 1-7).
- `references/prices-reference.md` - provider price table for the models you are most likely to be paying for;
  used by Step 4.
- `references/case-study.md` - the reported community case behind the inheritance trap and the two checks that
  catch it; used by Steps 2 and 3.
- `agents/openai.yaml` - catalog metadata (display name and short description) for the skill directory.

## When to use it
- Someone asks "what is my agent costing me?" and the answer is not obvious.
- You run an agent with background work: automatic skill curation, background review, compression, approval
  prompts, title generation.
- Cost appeared without new usage, or a scheduled job silently stopped.

## Step 1 - Find the background work
List every scheduled job and classify each one: **uses a model** (costs money) or **pure script** (free).
Then look for work that is NOT a scheduled job at all: curator runs, background review, compression and approval
steps. Those live in your agent's usage records, not in the job list, and they are where the money hides.
Ask for the token totals broken down **by task**, not just by day.

## Step 2 - Check which model each background task uses (the inheritance trap)
Background work usually **inherits the primary model unless the operator sets it explicitly**. So a top-tier
reasoning model as your main model silently becomes the model of your housekeeping too, several times a day, and
it never appears in the scheduled-job log.
Verify it: pull the usage records grouped by (task, model). If the expensive model shows up on a background task
you never configured, that is the inheritance trap, not a mystery.

## Step 3 - Count tokens per task per day
From the same usage records, compute: tokens per day, per model, per task. Watch for a single background task
that outweighs all interactive use. A reported community case ran hundreds of iterations in a day (about 353
million tokens in 20 hours) because curation kept re-triggering itself on a top-tier model. The full write-up,
with the two checks that reproduce the mechanism on your own data, is in `references/case-study.md`.

## Step 4 - Price it
Price table to start from: `references/prices-reference.md` (October 2026 figures, for estimation only - your
provider is the authority, and prices move).
Agents normally record **tokens, not money**, so price it yourself: tokens x provider price per million, split
input and output.
- Check whether your provider has **peak / off-peak** pricing, and compute both.
- Check **cache-hit** pricing: on some providers a cached input token costs a fraction of a fresh one, so an
  unstable prompt prefix quietly turns cheap cache hits into full-price misses.
- If you cannot price a model, say "not computable" instead of inventing a number.
- Two things you usually cannot verify from the machine: the provider's own bill, and whether the numbers your
  agent recorded match it. State that as a limit, do not paper over it.

## Step 5 - Cap it (each item needs the owner's approval, and each has a restore step)
| Lever | Why | Restore |
|---|---|---|
| Give background work its own cheaper model | the same pass can cost many times less | set it back |
| Keep curation on a long interval, keep automatic rewriting off unless you accept the cost | every pass re-reads the whole skill tree | restore the old interval |
| Lower the agent turn cap and the API retry count | bounds a runaway loop instead of letting it multiply | restore the old numbers |
| Pause one job that keeps failing | a failing paid job accumulates retries | resume the job |
| Pin critical skills so automation cannot move them | automated curation can restructure your skills | unpin |
| Provider-side spend cap | the only limit an agent cannot exceed | the owner changes it |
| Never edit the agent's core code | an update overwrites your fix and you lose the audit path | configure instead |

## Step 6 - Alert and brake
- Send alerts from a **script**, not from the model: if the model or the account breaks, the alert must still
  arrive. Two independent paths beat one.
- Distinguish **"the job failed"** from **"the job did not run"**: the first has an attempt and an error, the
  second means the scheduler or the account is dead. A message that conflates them sends the owner hunting the
  wrong fault.
- Brake in tiers - pause one job, then pause curation, then stop new work globally - and always print the
  restore command next to the brake. Never brake silently.
- De-duplicate: one alert per state per window, plus one "recovered" message.

## Step 7 - Report to the human (five short parts)
1. What you found, in plain language.
2. What you changed with their approval, and how to undo each change.
3. One risk that was prevented, with evidence they can re-check.
4. How they verify it themselves (three or four short commands).
5. What you could NOT guarantee. This part is not optional.

Weekly summary: tokens over seven days, the largest task, how many alerts fired, which changes were approved.

## Optional: the paid machine path
A **separate artifact** - an x402 endpoint - returns a risk-ranked assessment of a configuration when you POST
your own numbers to it. It is deliberately not part of this package: this package stays read-only so it can never
move money or read key material. If you want it, discover the endpoint and read its price from the machine path
(the HTTP 402 challenge), never from prose.

## Hard limits
- Do not edit the agent's core code. Configure, pause, cap.
- Do not copy credentials anywhere; never print a secret value in a report.
- Do not promise "prevents 100 percent" or any number you cannot demonstrate.
