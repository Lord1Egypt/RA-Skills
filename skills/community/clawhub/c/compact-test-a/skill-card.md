## Description:

Smart Compact helps OpenClaw agents scan conversation and tool-output context before compaction, extract important details into memory files, and produce a checklist before optional compaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill before context compaction to preserve important tool-output details, decisions, paths, and troubleshooting notes in local memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save broad conversation and tool-output details into durable local memory files.

Mitigation: Require explicit approval before memory writes and redact tokens, passwords, cookies, private keys, authorization headers, connection strings, personal data, and raw sensitive tool output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wavmson/skills/compact-test-a)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown checklist with optional appended local memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append selected conversation facts to memory/YYYY-MM-DD.md; sensitive data handling should be reviewed before deployment.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
