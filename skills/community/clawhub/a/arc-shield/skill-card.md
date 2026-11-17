## Description:

Output sanitization for agent responses - prevents accidental secret leaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to scan, redact, report on, or block outbound agent messages that may contain secrets, tokens, credentials, or PII before they are sent to external channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised leak-prevention controls are unreliable and may expose secrets during scanning or reporting.

Mitigation: Treat the skill as experimental, avoid routing real secrets through report mode, and verify strict and redaction behavior before using it on external messages.

Risk: Pattern and entropy scanning can miss new secret formats or produce false positives.

Mitigation: Maintain custom patterns, run the included tests after changes, and keep agent-side instructions that prevent secrets from being emitted in the first place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arc-claw-bot/skills/arc-shield)
- [README](artifact/README.md)
- [Quick reference](artifact/QUICKREF.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text streams, stderr reports, JSON reports, and Markdown guidance with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can pass through, redact, report on, or block output; Python-based scanning adds entropy checks.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
