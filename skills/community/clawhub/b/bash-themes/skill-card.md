## Description:

Bash Themes presents bash configuration and theme-management commands, but current evidence shows placeholder Oh My Bash behavior and a developer workflow CLI rather than a complete configuration framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shell users can ask an agent for bash-themes command usage, basic status/help output, and configuration guidance around BASH_THEMES_DIR. Review before installation because the security evidence says the package does not currently provide the advertised Oh My Bash configuration framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is advertised as an Oh My Bash configuration skill, but security evidence says it does not currently provide that framework.

Mitigation: Review package contents before installing and do not rely on it for production bash configuration until the functionality matches the advertised release.

Risk: A bundled developer workflow script creates local state and logs command usage under BASH_THEMES_DIR or the user's local data directory.

Mitigation: Run it in a controlled workspace and set BASH_THEMES_DIR to an expected disposable location before testing.

## Reference(s):

- [Bash Themes on ClawHub](https://clawhub.ai/xueyetianya/skills/bash-themes)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local shell command suggestions and references to BASH_THEMES_DIR; no API calls or credentials are indicated.]

## Skill Version(s):

2.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
