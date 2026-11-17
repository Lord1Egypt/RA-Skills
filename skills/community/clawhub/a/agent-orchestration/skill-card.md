## Description:

Master the art of spawning and managing sub-agents. Write prompts that actually work, track running agents, and learn from every outcome. Part of the Hal Stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdnw](https://clawhub.ai/user/clawdnw)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to structure prompts for research, build, and review agents, track active sub-agents, and capture learnings from agent outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Builder and orchestration prompts can lead agents to create files, run commands, or affect external systems outside the user's intended scope.

Mitigation: Use narrow output paths, explicit technical constraints, and manual confirmation before running commands that could modify important files or external systems.

Risk: Agent tracking and learning notes can persist sensitive prompt details if users record secrets or confidential context.

Mitigation: Avoid recording secrets or confidential details in tracking logs, and review persistent notes before sharing or publishing them.

Risk: Session-management guidance includes investigating stalled agents and potentially killing running agents.

Mitigation: Manually confirm the target session and expected impact before stopping an agent or restarting work.

## Reference(s):

- [Agent Orchestration on ClawHub](https://clawhub.ai/clawdnw/skills/agent-orchestration)
- [Builder Agent Template](artifact/templates/builder-agent.md)
- [Research Agent Template](artifact/templates/research-agent.md)
- [Review Agent Template](artifact/templates/review-agent.md)
- [Active Agents Tracking Template](artifact/examples/active-agents.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prompt templates, checklists, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are structured for direct agent prompting and workspace tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
