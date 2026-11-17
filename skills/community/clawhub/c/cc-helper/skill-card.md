## Description:

Cc Helper guides developers through Claude Code environment checks, CLI installation, third-party API provider selection, local configuration, and setup verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallyface0](https://clawhub.ai/user/sallyface0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up Claude Code with supported third-party API providers, especially when they need platform-specific installation guidance, environment variables, settings JSON, and troubleshooting help.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides shell installation commands, including remote installer patterns, that users may execute in their local environment.

Mitigation: Review commands before execution, prefer official installer documentation, and avoid piping remote scripts directly into a shell.

Risk: The skill asks users to configure API keys and provider credentials for Claude Code.

Mitigation: Store API keys in environment variables or a secret store, avoid committing project configuration files that contain credentials, and rotate keys if they are exposed.

Risk: The skill discusses changing Claude Code credential files and provider routing.

Mitigation: Back up credential files or use supported logout and reset flows before modifying authentication state.

## Reference(s):

- [Installation Guide](references/install-guide.md)
- [Provider Configuration Matrix](references/provider-table.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Node.js](https://nodejs.org/)
- [Git for Windows](https://git-scm.com/download/win)
- [DeepSeek API Keys](https://platform.deepseek.com/api_keys)
- [Kimi Platform](https://platform.moonshot.cn)
- [OpenRouter API Keys](https://openrouter.ai/keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific commands, provider-specific environment variables, settings.local.json examples, and troubleshooting steps.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter and changelog list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
