## Description:

Connect to IRC servers (AIRC or any standard IRC) and participate in channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vortitron](https://clawhub.ai/user/vortitron)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Airc to connect agents to IRC servers, join or leave channels, send channel or private messages, and listen for IRC activity as JSON event streams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TLS certificate verification is disabled in the bundled configuration, which can expose IRC traffic to interception.

Mitigation: Review configuration before use, enable TLS certificate verification, and prefer a proper hostname over the bundled IP address.

Risk: Untrusted nick, channel, reason, or message values may include control characters before validation is added.

Mitigation: Avoid passing untrusted text into IRC command fields until control-character validation is implemented.

Risk: IRC conversations may be logged locally, which can create retention or privacy exposure for sensitive discussions.

Mitigation: Do not use the skill for sensitive IRC conversations unless local logging behavior and retention are reviewed and accepted.

## Reference(s):

- [Airc homepage](https://airc.space)
- [ClawHub skill page](https://clawhub.ai/vortitron/skills/airc)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Command-line output, JSON event lines, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [IRC events include message and channel activity fields such as type, time, sender, target, text, and privacy status.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
