## Description:

OpenClaw documentation expert with config references, errata tracking, search scripts, and decision tree navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallvainian](https://clawhub.ai/user/sallvainian)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to answer OpenClaw setup, troubleshooting, and configuration questions with local references, errata checks, and document search commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled examples may include concrete account IDs, phone numbers, or ready-to-paste settings that are not safe defaults for every environment.

Mitigation: Replace identifiers with verified local values and audit snippets before applying them.

Risk: The skill may suggest elevated execution or an upstream pipe-to-bash installer.

Mitigation: Disable elevated execution unless strictly needed and independently verify installer contents before running them.

Risk: The authoritative security scan marked the release as suspicious because some scripts and examples need review before installation.

Mitigation: Install only after reviewing bundled scripts, snippets, and security guidance for the target environment.

## Reference(s):

- [Clawdocs Improved release page](https://clawhub.ai/sallvainian/skills/clawdocs-improved)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Agents configuration reference](artifact/references/agents.md)
- [Channels configuration reference](artifact/references/channels.md)
- [Gateway configuration reference](artifact/references/gateway.md)
- [Tools configuration reference](artifact/references/tools.md)
- [Session and messages configuration reference](artifact/references/session-messages.md)
- [Environment providers reference](artifact/references/environment-providers.md)
- [OpenClaw docs errata](artifact/snippets/errata.md)
- [Validated OpenClaw config snippets](artifact/snippets/validated-configs.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with configuration snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cite local reference files and OpenClaw documentation URLs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
