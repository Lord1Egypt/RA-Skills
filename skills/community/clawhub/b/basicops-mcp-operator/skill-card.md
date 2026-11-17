## Description:

Operate BasicOps through an available BasicOps MCP server. Use when the user wants to read from or update BasicOps tasks, projects, notes, messages, assignments, statuses, subtasks, reviews, or related work in an MCP-capable environment. Trigger on requests like "update this BasicOps task", "assign this in BasicOps", "summarize this BasicOps thread", "request review", "create subtasks", or "mark this complete". Prefer safe context gathering before writes, ask one concise clarifying question when the target is ambiguous, and summarize completed changes briefly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjhlarsen](https://clawhub.ai/user/hjhlarsen)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and teams use this skill to read, summarize, and update BasicOps tasks, projects, notes, and discussions through an existing MCP connection. It supports careful, scoped changes and concise follow-up summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit shared tasks and post messages in BasicOps.

Mitigation: Use a trusted MCP connection scoped to intended workspaces, and make the target and requested change clear before writing.

## Reference(s):

- [Using agents with BasicOps](https://basicops.com/agent-users)
- [BasicOps](https://basicops.com)
- [Setup checks](artifact/references/setup.md)
- [Workflow patterns](artifact/references/workflow-patterns.md)
- [Write safety](artifact/references/write-safety.md)
- [Common requests](artifact/references/common-requests.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Concise natural-language summaries and BasicOps task or thread updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or update BasicOps work through the available MCP connection; writes should stay within the clear user-requested scope.]

## Skill Version(s):

0.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
