# Acceptance - AI Output Failure Triage

## Required Files

- `SKILL.md`
- `skill.json`
- `ACCEPTANCE.md`

## Metadata Checks

- Version is `1.0.0`.
- License is `MIT-0`.
- Language is `en`.
- `hasExecutableCode` is `false`.
- `requires_api` is `false`.
- `no_network` is `true`.
- `no_credentials` is `true`.
- Skill type is prompt-flow or equivalent document-only prompt workflow.

## Content Checks

- Explains when to use the skill.
- Captures original goal, prompt, failed output, and user dissatisfaction.
- Classifies likely failure causes.
- Produces a missing context checklist.
- Rewrites the task with role, objective, inputs, constraints, output format, verification, and uncertainty behavior.
- Adds an acceptance test.
- Produces a safer retry prompt and go/no-go recommendation.
- Warns that the next answer is not guaranteed correct.
- Requires verification for factual, medical, legal, financial, safety-critical, and high-stakes outputs.
- Avoids encouraging users to share confidential data.

## Negative Checks

- No executable code.
- No API or network dependency.
- No credential collection.
- No claim that AI output is authoritative.
- No CJK characters.

## Clean Scan Evidence

- [x] No secrets, tokens, passwords, API keys, or private keys.
- [x] No executable code, scripts, package.json, or build artifacts.
- [x] No network calls, outbound requests, or external API dependencies.
- [x] No credential handling or environment-variable leakage.
- [x] No binary files, compiled code, or platform-specific executables.
- [x] No temp files, logs, .DS_Store, or editor artifacts.
- [x] Document-only, prompt-only, no execution required.
- [x] Language content is English with no CJK-dominant paragraphs.

## Install-First Success Path

**Input:** User provides an AI output that failed (original goal, prompt, failed response, what went wrong, audience, stakes, and constraints).

**Steps:**
1. Read the skill metadata and verify document-only, prompt-only safety.
2. Review the workflow: capture original goal/prompt/output, classify failure reasons, identify missing context, rewrite task framing, add acceptance test, recommend retry/switch/gather/manual, produce reusable next prompt.
3. Ask for any missing required inputs (original prompt, failed output, constraints, audience, stakes).
4. Produce the AI Output Failure Triage Report with all 7 required sections.

**Output:** A complete triage report with original task snapshot, likely failure causes, missing context checklist, improved task framing, acceptance test, safer retry prompt, and go/no-go recommendation — ready for immediate use with no additional tools, files, or network access.
