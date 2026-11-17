## Description:

Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigertamvip](https://clawhub.ai/user/tigertamvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support agents use this skill to find Clawdbot documentation, choose the right documentation category, retrieve relevant pages, and provide configuration guidance for Clawdbot features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration examples can expose credentials, session folders, or unauthenticated network services if copied directly into production.

Mitigation: Keep real tokens out of commits, protect WhatsApp session folders, and use localhost binding or add authentication, TLS, and firewall controls before exposing a gateway.

Risk: The included shell scripts are minimal documentation shortcuts and may not return complete or current documentation content.

Mitigation: Verify generated answers and configuration guidance against the official Clawdbot documentation before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tigertamvip/skills/clawddocs-1)
- [Clawdbot documentation](https://docs.clawd.bot/)
- [Clawdbot Discord provider documentation](https://docs.clawd.bot/providers/discord)
- [Common Config Snippets](snippets/common-configs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source documentation links and JSON configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package metadata reports 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
