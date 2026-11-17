## Description:

Test B helps OpenClaw agents prepare for context compaction by scanning conversation and tool-output history, extracting important details to memory files, and producing a pre-compact checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill before OpenClaw context compaction to preserve key facts, decisions, errors, user preferences, and task progress in memory files and to review a checklist before compression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save summarized conversation and tool-output details into persistent memory files, including sensitive data if present.

Mitigation: Use it only in sessions where persistent memory is acceptable, and review or redact tokens, passwords, private keys, personal data, internal hostnames, and confidential configuration before entries are written.

Risk: The extraction workflow may preserve more detail than is necessary for task continuity.

Mitigation: Limit saved entries to facts, decisions, errors, preferences, and task progress that are needed after compaction, then review the pre-compact checklist before confirming compression.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wavmson/skills/compact-test-b)
- [Publisher profile](https://clawhub.ai/user/wavmson)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown checklist and appended memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append summarized task details to memory/YYYY-MM-DD.md after reviewing conversation and tool output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
