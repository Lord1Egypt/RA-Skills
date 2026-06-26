# Acceptance Criteria - Allergy Season Room Routine

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow supports pick room, note triggers, choose low-effort actions, schedule cadence, and print routine card.
- [x] The output includes daily, weekly, and high-pollen-day actions.
- [x] The skill avoids diagnosis, medication advice, treatment changes, and medical certainty.
- [x] The safety boundary routes breathing trouble, wheezing, swelling, chest tightness, severe reactions, and rapidly worsening symptoms to urgent local care.
- [x] No CJK characters are present.

## Clean Scan Evidence

- [x] No executable code, scripts, package files, or install hooks.
- [x] No API endpoints, network calls, or external service dependencies.
- [x] No credentials, tokens, passwords, or private keys.
- [x] No secrets, environment variables, or configuration secrets.
- [x] No CJK characters; English/ASCII only.
- [x] No executable or network behavior; document-only skill.
- [x] No hidden files, temp files, or log files.
- [x] File count is exactly 3: SKILL.md, skill.json, ACCEPTANCE.md.

## Install-First Success Path

**Input:** User wants to reduce indoor allergy discomfort in one room during allergy season.

**Steps:**
1. Agent starts with safety: advises urgent medical care for breathing trouble, wheezing, swelling, or severe reactions.
2. Agent asks for room, symptoms, suspected triggers, available tools, and effort level.
3. Agent maps likely irritant paths (windows, clothes, pets, bedding, vents).
4. Agent selects low-effort actions and sorts them into daily, weekly, and high-pollen-day cadences.
5. Agent produces a printable room routine card with checkboxes and a safety note.

**Output:** A printable Allergy Season Room Routine card with daily/weekly/high-pollen-day actions, a two-minute version, cadence plan, and safety note.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-10
- Status: Ready for cross-review and test.
