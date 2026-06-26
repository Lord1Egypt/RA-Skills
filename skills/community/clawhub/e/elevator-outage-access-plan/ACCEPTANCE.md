# Acceptance Criteria - Elevator Outage Access Plan

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow produces an immediate safety check, outage snapshot, access needs roster, temporary route plan, delivery and visitor instructions, communication card, coordination tracker, and restoration follow-up.
- [x] The skill stays within access coordination and does not provide elevator maintenance, repair, override, troubleshooting, legal, medical, or disability-rights advice.
- [x] The safety boundary directs trapped persons, unsafe stair use, injury, distress, fire, smoke, or power hazards to emergency services or official building emergency contacts.
- [x] The skill uses minimal personal information in rosters and public notices.
- [x] No CJK characters are present.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Clean Scan Evidence

- [x] Secrets scan: no API keys, tokens, passwords, or credentials found.
- [x] Executable scan: no scripts, binaries, or executable code present.
- [x] Network scan: no outbound calls, fetch, or API endpoints.
- [x] File audit: only SKILL.md, skill.json, and ACCEPTANCE.md; no temp, logs, or build artifacts.
- [x] Language audit: English only; no CJK or mixed-script content.
- [x] Claims audit: all gate check claims verifiable against file contents.

## Install-First Success Path

- **Input:** User says "Elevator is out in our building. Help me make an access plan."
- **Steps:**
  1. Agent reads SKILL.md, checks immediate safety (anyone trapped or unable to use stairs), and confirms outage facts.
  2. Agent asks for affected people and floors, available alternatives, delivery needs, and contact assignments.
  3. Agent builds the access needs roster, temporary route options, delivery instructions, communication card, and coordination tracker.
- **Output:** A complete Elevator Outage Access Plan with immediate safety check, outage snapshot, access needs roster, temporary routes, delivery and visitor instructions, communication card, and restoration follow-up — all with emergency services prioritization and no elevator repair advice.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-11
- Status: Ready for cross-review and test.
