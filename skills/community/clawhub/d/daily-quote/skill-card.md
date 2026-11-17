## Description:

Daily curated quote from philosophers, leaders, and thinkers - with author context and why it resonates today. Bilingual EN/CN shareable visual card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate a daily bilingual inspirational quote card with author context, a short explanation, and shareable visual presentation. Users can also opt into morning and evening push prompts through supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional push system can create persistent morning and evening scheduled messages through external channels.

Mitigation: Enable push only when recurring delivery is intended, confirm the selected channel and recipient, and verify the jobs can be removed.

Risk: Per-user push settings are stored by the helper scripts.

Mitigation: Review where user settings are stored before enabling push and remove stored settings when disabling recurring delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiajiaoy/skills/daily-quote)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with generated single-file HTML and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a shareable bilingual quote card and optional recurring push configuration.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
