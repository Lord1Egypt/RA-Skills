## Description:

Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for Clawdbot features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kendrick-lu](https://clawhub.ai/user/kendrick-lu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer Clawdbot setup, configuration, troubleshooting, automation, provider, and deployment questions with links to the relevant documentation and reusable config snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may copy bot token examples into shared files, prompts, or logs.

Mitigation: Keep real tokens in environment variables or secret stores and avoid pasting live credentials into generated snippets or transcripts.

Risk: The gateway example binds to 0.0.0.0, which may expose a service beyond the local machine.

Mitigation: Use remote binding only when intended and pair it with authentication, TLS, and firewall controls.

Risk: The helper scripts are lightweight examples and may not provide a complete working documentation search system.

Mitigation: Treat script output as navigation aid text and verify final answers against the referenced Clawdbot documentation.

## Reference(s):

- [Clawddocs.Bak ClawHub release page](https://clawhub.ai/kendrick-lu/skills/clawddocs-bak)
- [Common Config Snippets](snippets/common-configs.md)
- [Clawdbot Discord provider documentation](https://docs.clawd.bot/providers/discord)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cite Clawdbot documentation URLs and suggest local helper scripts; full-text index use requires qmd.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
