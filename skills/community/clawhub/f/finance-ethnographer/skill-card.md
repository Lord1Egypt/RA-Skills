## Description:

Observes local OpenClaw session transcripts for finance-related usage patterns, generates daily finance UX reports, and redacts PII before review without automatic external sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dflam1](https://clawhub.ai/user/dflam1)

### License/Terms of Use:


## Use Case:

Developers, researchers, and product teams use this skill to study finance-related user workflows in local OpenClaw sessions, summarize recurring finance topics and UX signals, and review redacted daily insight reports before sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring local jobs read broad OpenClaw session transcripts and persist finance-related notes, quotes, reports, and identifiers.

Mitigation: Review cron entries, collected files, retention expectations, and removal steps before installation and during operation.

Risk: Sensitive excerpts may be stored in local reports before redaction is applied or verified.

Mitigation: Review only redacted report files for sharing, validate redaction quality, and keep non-redacted originals local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dflam1/skills/finance-ethnographer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSONL observation logs, and concise guidance with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local observation logs and redacted report files; evidence states that nothing is transmitted automatically.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
