## Description: <br>
Coordinates autonomous coding agents by turning user requests into VibeKanban tasks, dispatching agents, tracking progress, and monitoring pull request CI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrianRWagner](https://clawhub.ai/user/BrianRWagner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to coordinate multiple coding agents, create scoped task descriptions, assign work through VibeKanban, and summarize task or CI status for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Chief of Staff mode gives the assistant broad coordination authority for the rest of a conversation. <br>
Mitigation: Confirm the target project, task scope, and agent launch actions with the user before creating or dispatching work. <br>
Risk: The artifact includes a hard-coded full-autonomy local path exception. <br>
Mitigation: Remove or override that exception before deployment unless it is explicitly intended for the deployment environment. <br>
Risk: Failed CI logs can contain sensitive data when summarized or shared. <br>
Mitigation: Treat CI output as potentially sensitive and review failed logs before posting them into shared task updates. <br>


## Reference(s): <br>
- [CoS Workflow](references/cos-workflow.md) <br>
- [Delegation Patterns](references/delegation-patterns.md) <br>
- [VibeKanban API](references/vibekanban-api.md) <br>
- [Task Templates](examples/task-templates.md) <br>
- [GitHub CLI](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown task descriptions, status tables, concise guidance, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call VibeKanban MCP tools and may provide token-efficient CI summaries when the GitHub CLI is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
