# Classification Guide

## Purpose
Reduce classification drift between agents by using a repeatable pre-share process.

## Default rule
When uncertain, downgrade classification rather than widening visibility.

## Quick interpretation
- `private`: local-only, never commit
- `sealed`: summary-only reference, no sensitive body content
- `shared-team`: approved team-visible collaboration content
- `public-repo`: approved broadly visible repo content

## Common decision rule
If the exact content is not required for someone else to act, prefer `sealed` or `private` over a broader level.

## Reminder
Classification is not complete until the checklist in `assets/classification-checklist.md` has been answered.
