## Description:

Meta-agent skill for orchestrating complex tasks through autonomous sub-agents by decomposing work into subtasks, spawning specialized agents, coordinating file-based communication, consolidating results, and dissolving agents upon completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to split complex work into independent sub-agent tasks, create task-specific agent workspaces, coordinate file-based handoffs, and consolidate results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous sub-agents can create workspaces, copy task files, and proceed with limited oversight.

Mitigation: Limit the input scope, exclude confidential or regulated data, and require explicit approval or redaction before dispatching agents.

Risk: Sub-agent templates can send task content to a third-party AI API through SKILLBOSS_API_KEY.

Mitigation: Use only approved data, manage the API key as a secret, and add consent, redaction, or local-only controls before processing sensitive material.

Risk: Parallel agents can produce conflicting or incorrect outputs during consolidation.

Mitigation: Validate deliverables against success criteria and review merged results before relying on them.

## Reference(s):

- [File-Based Communication Protocol](references/communication-protocol.md)
- [Sub-Agent Templates](references/sub-agent-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/abeltennyson/skills/abel-agent-orchestrator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline code, shell commands, JSON examples, and file layout templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create task-specific SKILL.md files, inbox/outbox workspaces, status.json tracking files, and consolidated summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
