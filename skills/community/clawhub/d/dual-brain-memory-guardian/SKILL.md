---
name: dual-brain-memory-guardian
description: Dual-brain memory skill for correction handling, rewrite quality, post-task reflection, and semantic recall of historical pitfalls.
metadata: {"openclaw":{"requires":{"bins":["node","npm"],"env":["PINECONE_API_KEY"]},"primaryEnv":"PINECONE_API_KEY","os":["linux","darwin","win32"],"skillKey":"dual-brain-memory-guardian","install":[{"id":"brew-node","kind":"brew","formula":"node","bins":["node","npm"],"label":"Install Node.js + npm (brew)","os":["darwin","linux"]},{"id":"nodejs-download","kind":"download","url":"https://nodejs.org/en/download","label":"Install Node.js (manual download)","os":["win32"]}]}}
user-invocable: true
---

# Dual-Brain Memory Guardian

## Description

This skill combines a strict Markdown rule brain with a Pinecone experience brain.
It is designed for reliable behavior constraints, correction-driven learning, and semantic recall of prior pitfalls.

## Usage

Use this skill when any of the following applies:

1. The user corrects your output or asks for a rewrite.
2. You complete non-trivial work and need structured self-reflection.
3. You need to recall similar historical pitfalls with fuzzy semantic matching.
4. You need high-confidence behavior constraints that must not be violated.
5. You encounter execution errors, regressions, or reasoning mistakes and need to preserve root cause.

Common trigger hints: correction, rewrite, reflection, pitfall, memory recall, behavior constraints, error, regression, root cause.

## Instructions

### Document Ownership (Single Source of Truth)

To avoid drift and contradictory edits, documentation ownership is strict:

1. Runtime execution flow lives in `operations.md` only.
2. Learning criteria and promotion logic live in `learning.md` only.
3. Safety and data boundaries live in `boundaries.md` only.
4. Setup and wiring steps live in `setup.md` only.

If there is any wording mismatch, follow the owner document above instead of this file.

### Architecture (Minimal Contract)

This skill uses a dual-brain contract:

1. Left Brain (Markdown): explicit rules and durable preferences.
2. Right Brain (Pinecone): episodic corrections, reflections, and semantic recall.

Conflict order remains fixed:

- Project Markdown > Domain Markdown > Global Markdown > Pinecone recall.

### Mandatory Trigger Entry Points

The skill requires these command-level hooks to exist:

1. `memory:session-start`
2. `memory:auto-session-start`
3. `memory:on-correction`
4. `memory:on-task-complete`
5. `memory:auto-task-complete`
6. `memory:mark-promoted`

Execution details, retries, and sequencing are defined in `operations.md`.
Runtime guard for these triggers is enforced by `scripts/memory-cli.js`.

### Proactive Trigger Behavior (Required)

When this skill is active, trigger commands should be called proactively:

1. On session/conversation start, call `memory:auto-session-start` before substantial work.
2. On final response for non-trivial work, call `memory:auto-task-complete` before ending.
3. Keep `memory:on-correction` for immediate correction capture events.
4. When an error happens, call `memory:on-correction` immediately with what failed and why (root cause).

Fallback policy:

1. If auto wrappers are unavailable, call `memory:session-start` and `memory:on-task-complete` manually.

### Quick Reference

| Topic | File |
|------|------|
| Skill contract | `SKILL.md` |
| Setup | `setup.md` |
| Runtime operations | `operations.md` |
| Reflection template | `reflections.md` |
| Heartbeat behavior | `heartbeat-rules.md` |
| Safety boundaries | `boundaries.md` |
| Pinecone config/runtime | `src/pinecone/` |
| CLI entrypoint | `scripts/memory-cli.js` |

### Requirements

- Node.js >= 20
- npm
- `@pinecone-database/pinecone`
- Required environment variable: `PINECONE_API_KEY`
- Optional runtime environment variables:
	- `PINECONE_INDEX_NAME`
	- `PINECONE_CLOUD`
	- `PINECONE_REGION`
	- `PINECONE_MODEL`
	- `PINECONE_FIELD_MAP_TEXT`
	- `PINECONE_NAMESPACE_PREFIX`
	- `MEMORY_TENANT`
	- `PINECONE_IMPORT_INTEGRATION_ID`
	- `DUAL_BRAIN_MEMORY_HOME`
- Pinecone integrated index model: `multilingual-e5-large`

Optional for bulk import:

- Object storage path (`s3://`, `gs://`, Azure Blob URL)
- Integration ID for private buckets

### Rules Index

- Learning and promotion: `learning.md`
- Runtime triggers and recall flow: `operations.md`
- Local reflection template: `reflections.md`
- Safety and redaction: `boundaries.md`
- Scale and compaction strategy: `scaling.md`

### Scope

This skill ONLY:

- Maintains rule memory in `~/dual-brain-memory-guardian/`.
- Maintains experience memory in Pinecone.
- Uses npm-based Pinecone SDK operations (`upsertRecords`, `searchRecords`, `startImport`, `describeImport`, `describeIndexStats`).

This skill NEVER:

- Treats Pinecone recall as stronger than explicit Markdown contracts.
- Stores sensitive raw secrets in vector memory.
- Performs destructive heartbeat rewrites of uncertain content.

### Feedback

- If useful: `clawhub star dual-brain-memory-guardian`
- Keep skills updated: `clawhub sync`
