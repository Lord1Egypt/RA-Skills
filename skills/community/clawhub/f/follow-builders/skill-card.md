## Description:

AI builders digest — monitors top AI builders on X and YouTube podcasts, remixes their content into digestible summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zarazhangrui](https://clawhub.ai/user/zarazhangrui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to receive daily or weekly AI builder digests from curated X/Twitter and YouTube podcast sources. The skill also guides setup for delivery preferences, language, scheduling, and optional Telegram or email delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create recurring jobs for unattended digest delivery.

Mitigation: Review any cron or OpenClaw scheduled job before enabling automatic delivery, and prefer on-demand stdout delivery when unattended delivery is not needed.

Risk: Telegram or email delivery can store delivery credentials locally.

Mitigation: Restrict permissions on ~/.follow-builders, protect Telegram and Resend tokens, and rotate credentials if they may have been exposed.

Risk: Mutable digest prompts can change after installation without a new package review.

Mitigation: Review prompt files and centrally fetched prompt content before relying on summaries for important decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zarazhangrui/skills/follow-builders)
- [Publisher profile](https://clawhub.ai/user/zarazhangrui)
- [README](README.md)
- [Sample digest output](examples/sample-digest.md)
- [Configuration schema](config/config-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest text with setup guidance, inline shell commands, and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can deliver on demand in chat/stdout or through configured Telegram/email delivery; supports English, Chinese, and bilingual digests.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
