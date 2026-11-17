## Description:

Builds OpenClaw agent workspaces end-to-end, including persona, operating rules, guardrails, heartbeat behavior, memory options, skill roster guidance, and iteration support for existing agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to design new OpenClaw agents or refine existing ones. It helps produce tailored workspace files, operating rules, guardrails, memory guidance, heartbeat behavior, and acceptance test scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workspace, memory, heartbeat, operating rule, and skill roster changes can shape future agent behavior and may persist across sessions.

Mitigation: Review generated MEMORY.md, HEARTBEAT.md, AGENTS.md, and skill roster changes before use.

## Reference(s):

- [Agent Builder on ClawHub](https://clawhub.ai/plgonzalezrx8/skills/agent-builder)
- [OpenClaw agent workspace (cheat sheet)](references/openclaw-workspace.md)
- [OpenClaw agent file templates (snippets)](references/templates.md)
- [Agent Architecture Patterns](references/architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with generated file contents and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed contents for IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, optional memory files, skill roster changes, and acceptance test prompts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
