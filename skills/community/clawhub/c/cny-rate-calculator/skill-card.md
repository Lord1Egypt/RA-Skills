## Description:

Fetches Bank of Taiwan CNY exchange rates, calculates tiered Prairie Grasslands pricing, and sends scheduled notifications through configured messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[9starmax](https://clawhub.ai/user/9starmax)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to monitor Bank of Taiwan CNY exchange rates, calculate tiered prices, and deliver recurring exchange-rate notifications to selected channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores notification targets, reads OpenClaw messaging configuration, and can create recurring outbound messaging jobs.

Mitigation: Review configured channels before enabling the skill, avoid untrusted webhook URLs, and use least-privilege bot or gateway tokens.

Risk: Scheduled notifications include under-disclosed automatic behavior and an extra shortened-link message.

Mitigation: Inspect scheduled message content before deployment and remove or disable the shortened-link message if it is not wanted.

## Reference(s):

- [Bank of Taiwan Exchange Rates](https://rate.bot.com.tw/xrt)
- [Prairie Grasslands CNY Calculator Reference](https://78lion.com/CNY.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-like notification text, JSON channel status, and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured notification channels and schedule settings; can send outbound messages through supported chat, gateway, and webhook channels.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
