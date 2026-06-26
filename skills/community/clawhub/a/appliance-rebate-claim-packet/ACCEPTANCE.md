# Acceptance Criteria - Appliance Rebate Claim Packet

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow is limited to a paperwork checklist and claim packet.
- [x] The workflow requires current program rules and deadlines to be verified before submission.
- [x] The output includes a rebate snapshot, rule and deadline check, document checklist, form field prep, assembly order, proof plan, gap script, tracking log, and open questions.
- [x] The safety boundary prohibits full payment numbers, fabricated documents, guaranteed approval, and submission on the user's behalf.
- [x] No CJK characters are present.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, YAML frontmatter with name/description | ✅ |
| skill.json | Valid JSON, version 1.0.1, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "I just bought a new Energy Star refrigerator from Home Depot. Help me build a rebate claim packet for my utility company's appliance rebate program — I have the receipt and model number ready."
2. **Steps:** The skill guides the assistant to: (a) identify the rebate program sponsor and rules, (b) capture appliance facts (model, purchase date, retailer) while redacting payment details, (c) build a document checklist matching each program requirement to a document or photo proof, (d) prep form fields with evidence sources, (e) assemble the packet with a submission order and file naming plan, (f) run a deadline check with follow-up dates, (g) create a submission proof plan and claim tracking log.
3. **Output:** A complete rebate claim packet with rebate snapshot, rule and deadline check table, document checklist, form field prep, packet assembly order, submission proof plan, missing-items contact script, claim tracking log, and open questions — all with payment data redacted and deadlines highlighted.

Expected first-run outcome: The user receives a paperwork-ready claim packet they can use to submit a rebate with all required documents organized, deadlines tracked, and payment details safely redacted.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-11
- Status: Ready for cross-review and test.
