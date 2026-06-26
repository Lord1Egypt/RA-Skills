# Acceptance Checklist - AI Work Session Planner

## Metadata

- Slug: `ai-work-session-planner`
- Version: `1.0.0`
- License: `MIT-0`
- Language: English
- Executable code: none

## Acceptance Criteria

- Provides a clear trigger for messy work goals that need a focused 60 to 120 minute session.
- Uses a prompt-only workflow from goal capture through input listing, time splitting, checkpoints, AI role definition, and done-state definition.
- Produces a timed work plan with required inputs, assumptions, checkpoints, AI prompts, done-state, and fallback plan.
- Flags missing inputs, blockers, and assumptions instead of pretending the plan has complete context.
- Keeps the scope realistic for the available time and reduces scope when needed.
- Marks where human judgment, factual review, approvals, or sensitive decision review are required.
- Avoids credential collection and does not require APIs, network access, package files, code execution, or executable files.

## Manual Review Notes

Pass if the skill can be used entirely as a prompt-flow and returns a realistic focused-session plan that helps the user start, check progress, and finish with a clear done-state.

## Clean Scan Evidence

- [x] No executable code, scripts, or binary files in the skill directory.
- [x] No API keys, tokens, passwords, secrets, or credentials present.
- [x] No network, API, or external service dependencies declared.
- [x] All content in English, ASCII-safe, no CJK or non-ASCII characters.
- [x] No PII, private data, or sensitive identifiers embedded.
- [x] Directory contains exactly 3 files: SKILL.md, skill.json, ACCEPTANCE.md.
- [x] No hidden files, temp files, logs, or build artifacts.
- [x] skill.json is valid JSON with document-only metadata.
