## Description:

Agent Swarm Dev Team coordinates multiple AI coding agents, including Codex, Claude Code, and Gemini, to work on development tasks in isolated worktrees and tmux sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multiple coding agents across feature branches, code review, monitoring loops, and completion checks for software development tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default agent arguments can bypass approval and sandbox boundaries.

Mitigation: Remove the dangerous default agent arguments and run the skill only in an isolated workspace or container.

Risk: The initializer writes to a hard-coded /Users/xufan65 install path.

Mitigation: Change the install path to the intended workspace before running the initializer.

Risk: Long-running coding agents can continue changing branches, files, or pull requests after launch.

Mitigation: Monitor tmux sessions, pull request status, CI status, and review outputs before merging any changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/agent-swarm-dev-team)
- [ClawHub publisher profile](https://clawhub.ai/user/sunnyhot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The initializer may create local workflow folders, logs, helper scripts, and a README for agent orchestration.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
