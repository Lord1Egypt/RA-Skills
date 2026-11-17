## Description:

Smart context compaction for OpenClaw agents that scans tool outputs, extracts valuable information into memory files, and generates a pre-compact checklist before running /compact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill before context compaction to identify large tool outputs, preserve important facts, and produce a pre-compact checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive conversation details, credentials, private endpoints, personal information, customer data, or tool output could be written to memory files.

Mitigation: Review and redact extracted details before any memory append, and use the skill only when persistent memory is acceptable.

Risk: Broad conversation and tool-output details may be persisted without a clear opt-out gate.

Mitigation: Ask for explicit confirmation before writing memory and store only the details needed to preserve task continuity.

## Reference(s):

- [Compact Guard on ClawHub](https://clawhub.ai/wavmson/skills/compact-guard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown checklist and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append extracted context to memory/YYYY-MM-DD.md when persistent memory is appropriate.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
