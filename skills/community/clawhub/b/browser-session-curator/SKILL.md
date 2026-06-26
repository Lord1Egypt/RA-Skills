---
name: browser-session-curator
description: Turn an overwhelming set of tabs, bookmarks, and snippets into a structured
  session digest with tasks, reading queue, and archive plan.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Browser Session Curator

## Purpose

Turn an overwhelming set of tabs, bookmarks, and snippets into a structured session digest with tasks, reading queue, and archive plan.

## Trigger phrases

- 整理浏览器标签页
- tab dump
- session digest
- 书签归档
- 浏览器会话整理

## Ask for these inputs

- tab titles/URLs/notes
- session goal
- time budget
- archive rules
- project tags

## Workflow

1. Cluster tabs by task, reading, waiting, and archive.
2. Identify likely duplicates and stale tabs.
3. Produce a short execution plan for the next 30–60 minutes.
4. Export a digest with tags and follow-up actions.
5. Prefer lightweight action over cataloging everything forever.

## Output contract

- session digest
- reading queue
- archive list
- next-hour action plan

## Files in this skill

- Script: `{baseDir}/scripts/session_digest.py`
- Resource: `{baseDir}/resources/session_tags.yaml`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 整理浏览器标签页
- tab dump
- session digest

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/session_digest.py`.
- Bundled resource is local and referenced by the instructions: `resources/session_tags.yaml`.
