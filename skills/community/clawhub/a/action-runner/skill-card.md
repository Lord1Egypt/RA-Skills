## Description:

Builds a dry-run plan for proposed actions, risk-rates each item, executes approved work through connected action MCPs, and records completed actions for auditability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Action Runner to turn approved recommendations, checklists, PRDs, or follow-up items into scoped GitHub, Linear, Slack, Notion, email, or calendar actions with a preview and audit record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the approval gate depends on missing helper scripts and includes an unsafe shell pattern for generated plan data.

Mitigation: Review before installing, use narrowly scoped MCP permissions, require explicit per-action approval for outbound or destructive work, verify helper scripts, and pass plan data through stdin, a heredoc, or a temporary file instead of single-quoted echo.

## Reference(s):

- [Action Runner on ClawHub](https://clawhub.ai/mohitagw15856/skills/action-runner)
- [Action Runner homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/action-runner.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with action tables, JSON action plans, shell command examples, execution results, and audit notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before execution and limits actions to user-named targets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
