## Description:

Communicate with a CoPaw instance through its HTTP API to inspect agents or chats, create chat sessions, send messages, and understand auth, scoping, and SSE behavior before integration work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erview](https://clawhub.ai/user/erview)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate agents with CoPaw over HTTP, including chat/session creation, agent-scoped console chat requests, SSE response handling, and related auth or API-surface decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and chat content may be sent to the configured CoPaw HTTP host.

Mitigation: Install and use this skill only when interaction with that CoPaw host is intended, and treat chat content as data disclosed to that service.

Risk: Workspace, MCP, cron, skills, tools, and file-management API surfaces can inspect or change administrative state.

Mitigation: Use those API groups only for explicit administrative or inspection tasks, and prefer the chat/session flow for ordinary CoPaw conversations.

Risk: Implicit agent selection can send requests to an unintended CoPaw agent.

Mitigation: Prefer agent-scoped routes or set X-Agent-Id explicitly when building automation.

## Reference(s):

- [Overview / Auth / Scoping](references/overview-auth-scoping.md)
- [Chats / Console Chat / SSE](references/chats-console-sse.md)
- [Agents / Models / Skills / Tools](references/agents-models-skills-tools.md)
- [Workspace / MCP / Cron](references/workspace-mcp-cron.md)
- [Practical Recipes](references/practical-recipes.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with JSON payload examples and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on minimal endpoint sequences, payload shape, auth and scoping caveats, and task-relevant API groups.]

## Skill Version(s):

0.1.0 (source: release evidence, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
