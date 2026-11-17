## Description:

Use Clawrma for web fetch, web search, screenshots, snapshots, and inference, or as a fallback when built-in tools are not configured, blocked, or expensive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tnchr](https://clawhub.ai/user/tnchr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Clawrma to perform web retrieval, search, screenshot capture, structured snapshots, and CLI-backed inference when native tools are unavailable, blocked, rate-limited, unreliable, or too costly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web content, prompts, URLs, and screenshots may be routed through an unpinned third-party CLI without clear privacy, scoping, or integrity controls.

Mitigation: Review the Clawrma npm package and GitHub source before installing, prefer pinned versions, and require explicit approval before routing sensitive content to the CLI.

Risk: Sensitive data could be exposed if the skill is used with private sites, authenticated pages, internal URLs, secrets in query strings, proprietary prompts, or sensitive screenshots.

Mitigation: Avoid those inputs unless the user has approved the data path and is comfortable sending the data through Clawrma.

## Reference(s):

- [Clawrma GitHub repository](https://github.com/clawrma/clawrma)
- [Clawrma npm package](https://www.npmjs.com/package/clawrma)
- [Clawrma ClawHub skill page](https://clawhub.ai/tnchr/skills/clawrma)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; Clawrma CLI commands may return JSON, plain text, or screenshot file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill routes selected web, screenshot, snapshot, and inference tasks through the Clawrma CLI.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
