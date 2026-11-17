## Description:

Installs, tests, and monitors free language models for WorkBuddy and Claude Code, with optional model switching and image-reading support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other WorkBuddy or Claude Code users can configure free model providers, check whether models remain usable, and optionally route image-reading requests through a supported provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model settings can persistently route Claude Code requests through local proxies and external AI providers.

Mitigation: Review configuration changes and provider destinations before installation; disable unneeded proxy behavior.

Risk: Prompts and images can reach third-party providers, while failure dumps may retain sensitive content locally.

Mitigation: Avoid sensitive inputs unless the destination provider has been reviewed; disable unneeded image forwarding, watch, and failure-dump behavior.

## Reference(s):

- [Free LLM Installer on ClawHub](https://clawhub.ai/oracis/skills/free-llm-installer)
- [Zhipu BigModel platform](https://open.bigmodel.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce model health reports and update local model settings when run.]

## Skill Version(s):

1.1.9 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
