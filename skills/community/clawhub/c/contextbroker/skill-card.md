## Description:

A cross-agent memory and context SDK for AI systems. Provides structured context injection, conversation memory portability, and context enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avale-slai](https://clawhub.ai/user/avale-slai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to give AI agents persistent context across sessions, tools, and platforms, including context migration and structured context injection for RAG workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move sensitive context across sessions and external services.

Mitigation: Install and use it only when the publisher and external service are trusted, and avoid pushing secrets or regulated data unless the service is approved for that data.

Risk: The installer modifies the user's shell configuration by adding ~/.local/bin to PATH.

Mitigation: Review install.sh before running it and remove the PATH change from ~/.zshrc if it is not desired.

Risk: The installer sends an install analytics request to Signalloom during installation.

Mitigation: Inspect or disable the analytics curl command before installation if undisclosed telemetry is not acceptable.

## Reference(s):

- [Contextbroker ClawHub Skill Page](https://clawhub.ai/avale-slai/skills/contextbroker)
- [Signalloom API Key Signup](https://signalloomai.com/signup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference exported memory files such as JSON when context is moved between agent platforms.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
