## Description:

Orchestrates coding work across planning, implementation, TDD, review, security checks, hooks, worktrees, and multi-agent review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure coding tasks from requirements through implementation, validation, review, and iteration. It is intended to guide agent behavior and produce code, review findings, test plans, shell commands, and configuration-oriented workflow artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill force-loads unreviewed external skill files through absolute paths.

Mitigation: Replace absolute-path loading with packaged, reviewed, and pinned dependencies before use.

Risk: The security scan reports unsafe command execution paths, including a shell execution gate.

Mitigation: Harden command execution by removing shell=True paths, validating command arguments, and requiring explicit review for high-risk commands.

Risk: The skill can persist task, archive, command log, memory, and auto-commit data beyond a narrow coding task.

Mitigation: Make persistence features opt-in, document retention behavior, and redact or disable command logging where sensitive data may appear.

Risk: The artifact includes permissive external-agent modes.

Mitigation: Disable permissive external-agent execution by default and require sandboxing plus scoped tool permissions for delegated work.

Risk: The artifact includes broad project file-reading and workflow orchestration behavior.

Mitigation: Restrict reads and workflow operations to the active project workspace and require human approval before expanding scope.

## Reference(s):

- [Agent System](references/agent-system.md)
- [Hook System](references/hook-system.md)
- [External Agents](references/external-agents.md)
- [Iteration Patterns](references/iteration-patterns.md)
- [Security Patterns Detail](references/security-patterns-detail.md)
- [TDD Anti-Patterns](references/tdd-anti-patterns.md)
- [Workflow Examples](references/workflow-examples.md)
- [Worktree Guide](references/worktree-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, JSON reports, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit review reports, task plans, validation steps, and workflow commands depending on the coding stage.]

## Skill Version(s):

13.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
