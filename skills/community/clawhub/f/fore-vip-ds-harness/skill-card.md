## Description:

Guides an agent through local DeepSeek Harness setup by explaining DSH, helping configure a DeepSeek API key, installing Node.js and the DSH npm package for the detected operating system, starting the local web UI, and creating a desktop launcher.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onsoul](https://clawhub.ai/user/onsoul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to install and launch DeepSeek Harness locally, configure access to the DeepSeek platform, and create a reusable desktop shortcut for the local web UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent system and npm changes, including global package installation and possible sudo package installation.

Mitigation: Ask the agent to show each command before execution, confirm the package source, and proceed only when the requested system changes are acceptable.

Risk: The install flow uses unpinned external npm packages and may use npx -y.

Mitigation: Prefer pinned package versions, use a trusted registry, and avoid npx -y unless the user explicitly accepts running the latest package.

Risk: The skill creates desktop launcher files that can run local commands later.

Mitigation: Review generated launcher file contents before making them executable or using them.

Risk: DeepSeek API keys could be exposed if written into shared files, logs, or replies.

Mitigation: Keep API keys in the local web UI or environment variables only, and do not echo or store the key in generated documentation.

## Reference(s):

- [DeepSeek Harness GitHub repository](https://github.com/deepseek-ai/deepseek-harness)
- [DeepSeek Platform](https://platform.deepseek.com)
- [Node.js China download site](https://nodejs.cn)
- [npmmirror registry](https://registry.npmmirror.com)
- [ClawHub skill page](https://clawhub.ai/onsoul/skills/fore-vip-ds-harness)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, PowerShell, batch, and desktop-entry code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OS-specific commands and files at runtime; no executable files are bundled with the skill artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
