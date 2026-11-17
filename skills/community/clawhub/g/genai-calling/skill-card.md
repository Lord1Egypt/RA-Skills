## Description:

Unified interface for all providers and all modalities: use the `genai-calling` skill to operate the published `genai-calling` CLI/SDK across text/image/audio/video/embedding workflows, with support for authenticated local MCP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gravtice-agent](https://clawhub.ai/user/gravtice-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure provider credentials and call the `genai-calling` CLI, SDK, or MCP server for text, image, audio, video, and embedding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run the published `genai-calling` package while using provider credentials and MCP workflows.

Mitigation: Pin `genai-calling` to a reviewed version, avoid routine `--upgrade` usage, and run it with only the provider keys and files needed for the current task.

Risk: Shared environment files can expose broad provider credentials if reused across projects.

Mitigation: Keep shared env files narrow, protect API keys, and prefer task-scoped credentials or project-local overrides where practical.

Risk: MCP server exposure without authentication can allow unauthorized model and provider access.

Mitigation: Set MCP bearer-token authentication before exposing the server beyond local testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gravtice-agent/skills/genai-calling)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers provider API keys, environment files, model selection, CLI usage, SDK snippets, and local MCP server operation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
