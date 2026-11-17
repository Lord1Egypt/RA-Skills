## Description:

Buzz helps agents install, run, and manage a real-time news aggregator with Discord and Telegram push notifications for Jin10, BlockBeats, RSS, X KOLs, Polymarket, and OpenNews sources via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxcnny930](https://clawhub.ai/user/zxcnny930)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Buzz to configure and operate a local real-time news-alert service that aggregates market, crypto, RSS, X KOL, and AI-filtered news sources and pushes alerts to Discord or Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release relies on mutable remote code and should be reviewed before execution.

Mitigation: Review the upstream project before running the setup commands and install only if that review is acceptable.

Risk: An unauthenticated or broadly exposed dashboard can expose stored tokens and configuration control.

Mitigation: Set dashboard.password before startup and keep port 3848 bound or firewalled to localhost or private trusted hosts.

Risk: config.json can contain Discord, Telegram, AI, and 6551 credentials.

Mitigation: Treat config.json as sensitive, keep it out of version control, and avoid placing credentials in shared logs or shell history.

## Reference(s):

- [Buzz ClawHub skill page](https://clawhub.ai/zxcnny930/skills/buzz)
- [zxcnny930 publisher profile](https://clawhub.ai/user/zxcnny930)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST API examples, configuration update guidance, and local service management steps.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
