## Description:

免费版 helps developers and teams manage and call free OpenRouter AI models for AI conversations, agent orchestration, and automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and automation workflow users use this skill to configure and invoke free OpenRouter models, continue interrupted tasks, and collect model outputs and status for agent workflows. It is not intended for decisions requiring complete determinism or unsupervised high-stakes judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local file and command tools for general automation.

Mitigation: Run it only in a constrained agent environment with explicit approval for file writes and shell commands.

Risk: The skill may use external AI APIs and can expose private prompts or data if sensitive inputs are provided.

Mitigation: Avoid secrets and private data unless the calling agent enforces data handling boundaries and user confirmation.

Risk: The artifact documents API key setup and model/API failure modes.

Mitigation: Store API keys in environment variables, keep them out of source control and logs, and review generated outputs before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/free-resource-finder)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JSON output examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include model results, execution logs, status fields, and retry or resume metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
