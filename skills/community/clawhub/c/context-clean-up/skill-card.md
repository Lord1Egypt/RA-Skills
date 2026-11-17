## Description:

Context Clean Up helps agents audit bloated prompt context and produce a ranked, reversible cleanup plan without applying changes automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phenomenoner](https://clawhub.ai/user/phenomenoner)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to identify prompt-context bloat, inspect ranked offenders, and plan low-risk cleanup with rollback and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audit reports may include private OpenClaw session history or reasoning snippets.

Mitigation: Treat JSON reports as sensitive and inspect or redact them before sharing.

Risk: Out-of-band notification guidance can send data outside the main transcript.

Mitigation: Use out-of-band delivery only after approving the destination and the data that will leave the transcript.

Risk: Cleanup proposals can remove useful context or change automation behavior if applied without review.

Mitigation: Apply only explicit, reversible changes with backups, rollback notes, and new-session verification.

## Reference(s):

- [Context Clean Up on ClawHub](https://clawhub.ai/phenomenoner/skills/context-clean-up)
- [Out-of-band delivery](artifact/references/out-of-band-delivery.md)
- [Cron noise checklist](artifact/references/cron-noise-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, JSON]

**Output Format:** [Markdown guidance with optional JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit-only; no automatic deletions or unattended configuration edits.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
