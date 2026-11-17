## Description:

Intelligent log analysis CLI tool powered by DeepSeek API with 30+ built-in tools for file operations, system diagnostics, and log pattern recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xin9min9](https://clawhub.ai/user/xin9min9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and incident responders use this skill to analyze application, system, security, JSON, CSV, and plain-text logs with natural-language queries through the EdithAI CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global third-party npm CLI that can process sensitive logs, use a DeepSeek API key, access files, and run diagnostic commands.

Mitigation: Prefer a pinned and reviewed CLI version, avoid administrative privileges, and configure command allowlists and blocklists before analyzing logs.

Risk: Logs selected for analysis may contain secrets, incident details, or regulated data that could be sent to DeepSeek or retained in local EdithAI history.

Mitigation: Redact sensitive values before analysis, use a narrowly scoped API key, and review or clear ~/.edithai/history.json when working with sensitive incidents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xin9min9/skills/edithai-clawhub-skill)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [CAPABILITIES.md](artifact/CAPABILITIES.md)
- [INSTALL.md](artifact/INSTALL.md)
- [QUICK-REFERENCE.md](artifact/QUICK-REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with CLI commands, configuration snippets, and analysis outputs; the underlying CLI may also produce JSON or report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and DEEPSEEK_API_KEY; CLI history may be stored under ~/.edithai/history.json.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
