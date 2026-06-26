# Acceptance Criteria - Event Ticket Help Sheet

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow captures ticket details, collects screenshots or proof items, identifies contact paths, builds an arrival plan, and creates a help sheet.
- [x] The deliverable includes ticket facts, contact paths, proof bundle, arrival plan, support message, on-site script, and decision tree.
- [x] The safety boundary allows legitimate support paths only and rejects fake receipts, altered tickets, duplicate codes, or bypass advice.
- [x] No CJK characters are present.

## Clean Scan Evidence

- [x] Secrets scan: no API keys, tokens, passwords, or credentials found.
- [x] Executable scan: no scripts, binaries, or executable code present.
- [x] Network scan: no outbound calls, fetch, or API endpoints.
- [x] File audit: only SKILL.md, skill.json, and ACCEPTANCE.md; no temp, logs, or build artifacts.
- [x] Language audit: English only; no CJK or mixed-script content.
- [x] Claims audit: all gate check claims verifiable against file contents.

## Install-First Success Path

- **Input:** User says "My concert ticket QR code is not showing and the show is tonight. Make me an action sheet."
- **Steps:**
  1. Agent reads SKILL.md and captures ticket facts (event, venue, source, format, issue, time remaining).
  2. Agent builds the Proof Bundle Checklist, identifies legitimate Contact Paths, and drafts a Copy-Ready Support Message.
  3. Agent creates the Arrival Plan with timing buffers and the At-the-Gate Script.
  4. Agent maps the If-This-Happens decision tree and the Do-Not-Do list.
- **Output:** A complete Event Ticket Help Sheet with ticket snapshot, proof bundle, contact paths, support message, arrival plan, gate script, decision tree, and safety reminders — document-only, no ticket system access.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: Golden Bean / code
- Date: 2026-05-10
- Status: Ready for cross-review and test.
