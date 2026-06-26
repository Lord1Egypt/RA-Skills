# Acceptance Criteria - Daycare Waitlist Status Board

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow produces a privacy note, waitlist status board, licensing and policy board, priority notes, follow-up messages, decision checklist, and open questions.
- [x] The skill requires verification of licensing, policies, fees, enrollment terms, and availability through official provider or regulator sources.
- [x] The skill avoids unnecessary private child details in shared artifacts.
- [x] No CJK characters are present.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-11
- Status: Ready for cross-review and test.

## Clean Scan Evidence

- [x] Secrets scan: no API keys, tokens, passwords, or credentials found.
- [x] Executable scan: no scripts, binaries, or executable code present.
- [x] Network scan: no outbound calls, fetch, or API endpoints.
- [x] File audit: only SKILL.md, skill.json, and ACCEPTANCE.md; no temp, logs, or build artifacts.
- [x] Language audit: English only; no CJK or mixed-script content.
- [x] Claims audit: all gate check claims verifiable against file contents.

## Install-First Success Path

- **Input:** User says "Organize our daycare waitlist status across three preschools into one board."
- **Steps:**
  1. Agent reads SKILL.md, asks for program names, application dates, waitlist status, tour notes, follow-up history, and user priorities.
  2. Agent builds the Waitlist Status Board, Licensing and Policy Verification Board, Priority Fit Notes, and draft follow-up messages.
  3. Agent produces a privacy note, decision-ready checklist, and open questions list — with private child details omitted from any shareable version.
- **Output:** A privacy-conscious daycare waitlist status board with provider comparisons, licensing check reminders, policy questions, availability signals, follow-up message templates, and a decision checklist — all verified against user-supplied data only, with no childcare or safety advice.
