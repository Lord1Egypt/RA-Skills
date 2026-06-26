# Acceptance Criteria - Claim Evidence Timeline Builder

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow collects events, sorts by time, attaches proof, marks gaps, separates facts from interpretation, and writes a concise summary.
- [x] The skill uses only user-provided events and proof and does not invent evidence.
- [x] The skill avoids legal advice and does not predict claim outcomes.
- [x] No CJK characters are present.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, YAML frontmatter with name/description/version/tags | ✅ |
| skill.json | Valid JSON, version 1.0.1, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "My laptop broke three months after the warranty repair. I have the original receipt, two repair emails, and a chat log with support. Build a timeline so I can send it to the retailer."
2. **Steps:** The skill guides the assistant to: (a) clarify the audience and desired outcome, (b) collect events from user-provided info with dates, (c) sort events chronologically, (d) attach proof IDs to each event, (e) separate facts from user interpretation, (f) mark gaps and missing evidence, (g) write a concise factual summary, (h) deliver the full timeline artifact.
3. **Output:** A claim evidence timeline with timeline purpose statement, chronological timeline table with proof IDs, proof index, gaps and follow-up list, fact-vs-interpretation notes, concise summary, and submission checklist.

Expected first-run outcome: The user receives a clear, chronologically sorted timeline with proof attachments and gap markers — ready to submit or review, using only user-provided facts, with no legal advice or invented evidence.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: Golden Bean / code
- Date: 2026-05-10
- Status: Ready for cross-review and test.
