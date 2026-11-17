## Description:

This skill gives an agent a long-term memory workflow for recording interactions, checking deliverables against user requirements, and reflecting on past corrections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webray1983](https://clawhub.ai/user/webray1983)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to keep task memory, compare deliverables to original requests before responding, and run on-demand double-check reviews when a user asks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store conversation summaries, requirements, corrections, preferences, and sensitive details in shared plaintext memory files.

Mitigation: Use it only when persistent memory is intended, and add consent, review, deletion, redaction, and per-project storage controls before using it with confidential or regulated data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webray1983/skills/double-check-it)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plaintext memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the shell script is used, it writes memory records, indexes, and reflections as plaintext files in the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
