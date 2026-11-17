## Description:

Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to navigate Clawdbot documentation, find relevant setup or troubleshooting pages, and assemble common provider, gateway, automation, and agent configuration snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts are stubs and may not deliver the full documentation-search behavior described by the skill.

Mitigation: Validate script output against the live Clawdbot documentation before relying on it for setup, troubleshooting, or change tracking.

Risk: Configuration examples include provider tokens, WhatsApp session paths, and a gateway bind address that could expose services if copied without review.

Mitigation: Keep provider tokens secret, protect session files, and bind gateways to localhost unless remote access is intentional and protected.

## Reference(s):

- [Clawddocs Zc on ClawHub](https://clawhub.ai/lean-zhouchao/skills/clawddocs-zc)
- [Clawdbot Documentation](https://docs.clawd.bot/)
- [Clawdbot Discord Provider Documentation](https://docs.clawd.bot/providers/discord)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cite Clawdbot documentation URLs and propose commands for the bundled helper scripts.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
