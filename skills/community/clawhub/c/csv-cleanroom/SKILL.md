---
name: csv-cleanroom
description: Profile messy CSV files, standardize columns, detect data quality issues,
  and produce a reproducible cleanup plan.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# CSV Cleanroom

## Purpose

Profile messy CSV files, standardize columns, detect data quality issues, and produce a reproducible cleanup plan.

## Trigger phrases

- 清洗 CSV
- profile this dataset
- 数据质量检查
- 列名规范化
- build a cleanup plan

## Ask for these inputs

- CSV file or schema
- target schema if available
- known bad values
- dedupe rules
- date/currency locale

## Workflow

1. Profile the CSV: row count, nulls, duplicates, type mismatches, and outliers.
2. Normalize headers and map to the target schema.
3. Generate a step-by-step cleanup plan and optional transformed output.
4. Document irreversible operations before applying them.
5. Return a quality score and remediation checklist.

## Output contract

- profile report
- normalized schema
- cleanup plan
- quality scorecard

## Files in this skill

- Script: `{baseDir}/scripts/csv_cleanroom.py`
- Resource: `{baseDir}/resources/data_quality_checklist.md`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 清洗 CSV
- profile this dataset
- 数据质量检查

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/csv_cleanroom.py`.
- Bundled resource is local and referenced by the instructions: `resources/data_quality_checklist.md`.
