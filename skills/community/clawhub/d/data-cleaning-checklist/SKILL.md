---
name: data-cleaning-checklist
version: 1.0.0
description: Clean a dataset before analysis: schema check, nulls, duplicates, outliers, and unit consistency, with every fix logged. Use before trusting any CSV, export, or scraped dataset.
---

# Data Cleaning Checklist

## Overview

Analyses fail quietly on dirty data. This checklist runs the same inspections in the same order every time, and — critically — logs every change made, so results can be reproduced and challenged.

## When to use

Before analyzing, merging, publishing, or training on any dataset.

## Workflow

1. **Schema check** — columns, types, and encodings match the documentation; surprises here invalidate everything downstream
2. **Null audit** — per column: how many missing, and is missing meaningful or an error?
3. **Duplicate pass** — exact duplicates and near-duplicates on the natural key; decide and log the rule
4. **Range and unit check** — values within plausible ranges; units consistent (the classic: cents vs dollars, wei vs ether, seconds vs milliseconds)
5. **Outlier review** — extremes are inspected, not silently dropped; each removal needs a written reason
6. **Write the cleaning log** — every transformation, count affected, and the rule applied

## Guardrails

- Never overwrite the raw file — clean into a new artifact
- Never drop outliers to make results cleaner
- If provenance is unknown, say so in every downstream use

## Output format

A cleaned dataset plus a cleaning log: checks run, issues found, transformations applied with counts.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
