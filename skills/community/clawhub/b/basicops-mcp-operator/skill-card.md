## Description: <br>
Operate BasicOps through an available BasicOps MCP server for reading or updating tasks, projects, notes, messages, assignments, statuses, subtasks, reviews, and related work in an MCP-capable environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjhlarsen](https://clawhub.ai/user/hjhlarsen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and teams using BasicOps use this skill to let an agent perform careful BasicOps reads and writes through an authenticated MCP server. It is suited for concise task updates, thread summaries, subtask creation, review requests, and other scoped workflow changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make BasicOps changes through MCP, including assignments, statuses, subtasks, reviews, and messages. <br>
Mitigation: Confirm the target object, workspace, assignee, reviewer, and requested mutation when ambiguity exists; use the smallest valid write and summarize exactly what changed. <br>
Risk: A missing, unauthorized, or misidentified BasicOps MCP connection can block the requested work or point the agent at the wrong tool surface. <br>
Mitigation: Check for an authenticated BasicOps MCP server or clearly named BasicOps tool surface before acting, and stop with setup guidance rather than inventing a fallback. <br>
Risk: The security review notes powerful maintainer-focused automation in the bundle even though the verdict is clean. <br>
Mitigation: Review the disclosed behavior before deployment and use the skill only in environments where local access and workflow automation are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjhlarsen/basicops-mcp-operator) <br>
- [BasicOps MCP setup checks](references/setup.md) <br>
- [BasicOps workflow patterns](references/workflow-patterns.md) <br>
- [BasicOps write safety](references/write-safety.md) <br>
- [Common BasicOps requests](references/common-requests.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown summaries, clarifying questions, setup guidance, and concise completion notes after MCP-mediated BasicOps operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an available and authenticated BasicOps MCP tool surface; writes should stay scoped to the clear target object and requested change.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
