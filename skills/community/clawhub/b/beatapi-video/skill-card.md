## Description:

Guides agents to discover, inspect, and use BeatAPI capabilities for AI models, social and web research, and media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatapi](https://clawhub.ai/user/beatapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and creators use this skill to select BeatAPI capabilities, run authorized model and research requests, create media, and track task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented REST workflow may return shell commands that are unsafe to execute without review.

Mitigation: Prefer MCP or structured client calls; never directly execute API-returned shell command strings.

Risk: Agent actions can upload selected media and initiate paid jobs on the user's account.

Mitigation: Upload only user-selected files and start paid work only when explicitly requested; check account balance and pricing first.

Risk: Account credentials and one-time secrets could be exposed in agent-visible outputs.

Mitigation: Keep API keys in private host configuration and create secret-bearing sessions or webhooks only in trusted server-side code.

## Reference(s):

- [BeatAPI API documentation](https://docs.beatapi.io/)
- [BeatAPI model catalog](https://beatapi.io/model)
- [BeatAPI pricing](https://beatapi.io/pricing)
- [Capability discovery and execution](artifact/references/capabilities.md)
- [Account setup and credentials](artifact/references/setup.md)
- [BeatAPI OpenAPI contract](artifact/references/beatapi.openapi.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration guidance, Shell commands]

**Output Format:** [Markdown or structured JSON with capability results, task status, and media links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media generation can return asynchronous task IDs; results require a completed task.]

## Skill Version(s):

0.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
