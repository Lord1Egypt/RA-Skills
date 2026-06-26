---
name: downloads-command-center
description: Organize the Downloads folder into a clean, searchable command center
  by file type, project, date, and action state.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Downloads Command Center

## Purpose

Organize the Downloads folder into a clean, searchable command center by file type, project, date, and action state.

## Trigger phrases

- 整理下载文件夹
- 清理 Downloads
- organize my downloads
- rename recent files
- 把下载内容分类

## Ask for these inputs

- Downloads folder path
- organization preference by type/project/date
- whether to move duplicates to quarantine
- optional keep rules

## Workflow

1. Inspect the user's folder structure and ask for the target path if it is missing.
2. Propose a safe organization plan before moving files in bulk.
3. Use the helper script to generate a preview manifest and rename plan.
4. Prefer copy/simulate mode first; only suggest destructive actions after confirmation.
5. Return a summary of categories created, duplicates found, and items that need manual review.

## Output contract

- folder plan
- rename/move preview
- duplicate report
- cleanup checklist

## Files in this skill

- Script: `{baseDir}/scripts/organize_downloads.py`
- Resource: `{baseDir}/resources/rules.sample.json`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 整理下载文件夹
- 清理 Downloads
- organize my downloads

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/organize_downloads.py`.
- Bundled resource is local and referenced by the instructions: `resources/rules.sample.json`.
