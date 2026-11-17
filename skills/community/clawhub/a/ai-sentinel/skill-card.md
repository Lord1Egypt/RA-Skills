## Description:

AI Sentinel helps OpenClaw developers install and configure the ai-sentinel plugin for prompt injection detection, local or Pro classification, and dashboard reporting with explicit confirmation before configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amandiwakar](https://clawhub.ai/user/amandiwakar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add prompt-injection screening to agent messages, tool calls, and tool results. It supports local Community scanning and Pro reporting or cloud scanning when the operator explicitly consents to external transmission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a third-party gateway plugin that can inspect agent messages, tool calls, and tool results.

Mitigation: Review the npm package provenance before installation and use a pinned package version such as ai-sentinel@0.2.1 when supported.

Risk: Pro mode can transmit scan results and, depending on configuration, raw message content to an external API.

Mitigation: Use Community mode for local-only scanning, or require explicit consent and keep telemetry configured without raw input unless content transmission is acceptable.

Risk: Pro mode requires an API key and writes local configuration files.

Mitigation: Store the API key only in an ignored local .env file and require user confirmation before updating .env, .gitignore, or OpenClaw plugin configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amandiwakar/skills/ai-sentinel)
- [AI Sentinel homepage](https://zetro.ai)
- [ai-sentinel npm package](https://www.npmjs.com/package/ai-sentinel)
- [AI Sentinel dashboard](https://app.zetro.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw setup guidance and proposes configuration or environment-file changes only after explicit user confirmation.]

## Skill Version(s):

0.2.2 (source: server release evidence and changelog, released 2026-08-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
