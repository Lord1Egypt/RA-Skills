## Description:

Coordinate multiple sub-agents to collaboratively complete long-horizon software engineering tasks using the CAID (Centralized Asynchronous Isolated Delegation) paradigm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncatbot](https://clawhub.ai/user/simoncatbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software engineering agents use this skill to coordinate parallel work on long-horizon, multi-file tasks with dependency-aware delegation, isolated git worktrees, test-gated integration, and final review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Git operations can alter repository history, push unintended changes, or remove worktree state.

Mitigation: Run in a dedicated, backed-up repository; review staged diffs and remotes; and require explicit approval for pushes, hard resets, and deletion.

Risk: Package installation and subagent execution can run code or commands outside the immediate review path.

Mitigation: Use a sandboxed environment, validate worktree paths, and require explicit approval before package installation or subagent-driven command execution.

Risk: Cleanup commands can delete files or expose sensitive untracked files if paths or credentials are mishandled.

Mitigation: Validate cleanup targets, avoid exposing credentials, and keep sensitive untracked files out of repositories used with this skill.

## Reference(s):

- [CAID Multi-Agent Examples](references/examples.md)
- [async-swe-agents GitHub repository](https://github.com/JiayiGeng/async-swe-agents)
- [ClawHub skill page](https://clawhub.ai/simoncatbot/skills/caid-multi-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON, bash, JavaScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coordination plans, task assignments, verification commands, and integration guidance for agent workflows.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
