## Description:

Auto Responder helps agents automatically reply to messages in configured topics using keyword, exclusion, template, and cooldown rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunaviva211-sketch](https://clawhub.ai/user/lunaviva211-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Auto Responder to configure autonomous replies for group topics, including keyword matching, exclusions, response templates, cooldowns, and hook or heartbeat integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic replies may be sent in unsuitable topics or too frequently if matching rules, templates, mention requirements, or rate limits are too broad.

Mitigation: Confirm the configured topics, keywords, exclusions, response templates, mention requirement, cooldowns, and rate limits for each agent before enabling the skill.

Risk: The local response cache may retain message-derived metadata used to prevent duplicate replies.

Mitigation: Periodically inspect or clear the cache, and enable the skill only where this metadata retention is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lunaviva211-sketch/skills/auto-responder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include topic rules, keywords, response templates, cooldown settings, and hook or heartbeat integration steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
