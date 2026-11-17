## Description:

Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to navigate Clawdbot documentation, locate relevant setup or troubleshooting pages, and prepare configuration snippets for supported providers, gateway settings, automation, tools, platforms, and install workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gateway configuration snippet binds to 0.0.0.0, which can expose the service beyond localhost if copied directly.

Mitigation: Change the bind address to 127.0.0.1 unless remote access is intentional and protected by authentication, TLS, and network restrictions.

Risk: The included scripts are lightweight documentation helpers with placeholder behavior, so users may overestimate search, cache, or version-tracking completeness.

Mitigation: Treat script output as navigation assistance and verify important setup or troubleshooting details against the Clawdbot documentation.

## Reference(s):

- [Clawddocs Local on ClawHub](https://clawhub.ai/netanel-abergel/skills/clawddocs-local)
- [Clawdbot documentation](https://docs.clawd.bot/)
- [Discord provider documentation](https://docs.clawd.bot/providers/discord)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should cite relevant Clawdbot documentation URLs when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
