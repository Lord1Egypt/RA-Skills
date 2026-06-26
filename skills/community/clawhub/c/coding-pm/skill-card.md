## Description: <br>
Coding PM delegates coding tasks to Claude Code running in the background, reviews plans, gates approval, monitors progress, validates with three-layer testing, and reports results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Horacehxw](https://clawhub.ai/user/Horacehxw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to manage coding-agent work from request intake through planning, execution monitoring, acceptance testing, and merge cleanup while keeping the user in the approval loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a background Claude Code agent with permission prompts disabled and broader local filesystem access. <br>
Mitigation: Use it in an isolated checkout, container, VM, or restricted user account; avoid repositories containing secrets; review plans and diffs carefully; and re-enable workspace-only filesystem restrictions when finished. <br>
Risk: The background agent may modify a git worktree or run project commands during execution. <br>
Mitigation: Require plan approval before execution, monitor progress, run acceptance tests, and inspect the final diff before approving merge or cleanup. <br>


## Reference(s): <br>
- [Coding PM on ClawHub](https://clawhub.ai/Horacehxw/coding-pm) <br>
- [Supervisor Protocol](references/supervisor-prompt.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans, progress summaries, decision prompts, test reports, and merge or cleanup guidance.] <br>

## Skill Version(s): <br>
0.4.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
