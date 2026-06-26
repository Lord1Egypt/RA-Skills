## Description: <br>
Use when user asks to leverage Claude or Claude Code to do something, such as implement a feature design or review code, with non-interactive automation for hands-off task execution without approval prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding, review, repository automation, and PR workflow tasks to Claude Code. It provides command patterns for quick non-interactive runs and longer managed sessions with logging, polling, and quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to run Claude Code with broad local and repository authority, including file edits, shell commands, commits, pushes, and PR creation. <br>
Mitigation: Use isolated worktrees or containers, restrict allowed tools, and manually review commands, diffs, commits, pushes, and PRs before they affect shared systems. <br>
Risk: Permission-bypassing modes can remove interactive approval checkpoints during coding work. <br>
Mitigation: Prefer read-only or acceptEdits modes for real projects and avoid skipping permissions outside intentionally isolated environments. <br>
Risk: MCP access and long-running automation can interact with external systems or continue without close supervision. <br>
Mitigation: Limit MCP configuration to trusted servers, monitor logs and task status, and require human review before external notifications or repository publication. <br>


## Reference(s): <br>
- [Example Usage Scenarios](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/feiskyer/claude-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command output, logs, task status updates, PR review notes, and workflow checklists.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
