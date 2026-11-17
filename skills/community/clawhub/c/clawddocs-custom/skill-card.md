## Description:

Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terkinvasil](https://clawhub.ai/user/terkinvasil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support teams use this skill to navigate Clawdbot documentation, locate setup and troubleshooting pages, and produce configuration guidance with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scripts are lightweight examples rather than complete fetch, search, or index tooling.

Mitigation: Treat script output as a starting point and verify documentation results against the live Clawdbot documentation before relying on them.

Risk: Copied configuration snippets can expose provider tokens or bind the gateway to a broad network interface.

Mitigation: Review all copied configuration before use, keep secrets in environment variables, and prefer local-only gateway binding unless remote access is intentional and protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terkinvasil/skills/clawddocs-custom)
- [Clawdbot documentation](https://docs.clawd.bot/)
- [Clawdbot Discord provider documentation](https://docs.clawd.bot/providers/discord)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cite Clawdbot documentation URLs when answering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
