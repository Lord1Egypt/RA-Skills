## Description:

Smart multi-model routing for Claude, GPT, Gemini, and local Ollama models with cost optimization, fallback chains, and usage tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mackding](https://clawhub.ai/user/mackding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start or integrate a local OpenAI-compatible gateway that routes chat completion requests across multiple model providers with configurable routing, fallback, cost tracking, and health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable external code through an unpinned npx command.

Mitigation: Prefer a pinned, verified CLI version or lockfile-managed install before running the gateway command.

Risk: Provider API keys and prompts may be sent to the selected cloud model providers.

Mitigation: Use only provider keys and prompts appropriate for the configured provider routing, and review provider selection before sending sensitive requests.

Risk: The reviewed artifact does not contain the actual gateway implementation.

Mitigation: Review the external CLI package and its dependencies before deployment.

## Reference(s):

- [Agent Gateway on ClawHub](https://clawhub.ai/mackding/skills/agent-gateway)
- [Publisher profile: mackding](https://clawhub.ai/user/mackding)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct users to run an external CLI and configure provider API-key environment variables.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
