## Description:

Helps developers compare coding assistant platforms, follow registration guidance, and configure API keys for supported tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get registration, pricing, setup, status-check, and credential-rotation guidance for common coding assistant platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be stored in a local .openclaw/.env file with weak local safeguards.

Mitigation: Prefer a dedicated secret manager or OS keychain; if local storage is used, protect .openclaw/.env and ensure it is ignored by version control.

Risk: Entering real API keys through agent or command workflows can expose secrets in transcripts, shell history, logs, or command arguments.

Mitigation: Avoid passing keys on the command line, verify outputs show only masked key previews, and rotate keys after suspected exposure.

Risk: Provider registration, install, and pricing guidance can become outdated.

Mitigation: Confirm npm install commands, pricing, and registration steps against linked official provider documentation before purchase or deployment.

## Reference(s):

- [GitHub Copilot reference](references/github-copilot.md)
- [Claude Code reference](references/claude-code.md)
- [Gemini CLI reference](references/gemini-cli.md)
- [Codex OpenAI reference](references/codex-openai.md)
- [Qwen Code reference](references/qwen-code.md)
- [Baidu Paddle reference](references/baidu-paddle.md)
- [OpenRouter reference](references/openrouter.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masks displayed API keys; may write configured credentials to .openclaw/.env.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
