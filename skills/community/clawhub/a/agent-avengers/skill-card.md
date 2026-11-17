## Description:

Agent Avengers decomposes complex tasks into subtasks, assigns them to specialized agents, runs them in parallel or sequence, and consolidates the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oozoofrog](https://clawhub.ai/user/oozoofrog)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to coordinate multi-agent work on complex tasks such as research, analysis, writing, coding, review, and result consolidation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates task details to multiple agents or profiles, which can expose sensitive information across sessions.

Mitigation: Review planned delegation before execution and avoid sensitive inputs unless session storage, mission files, logs, and deletion procedures are understood.

Risk: Generated execution commands and task plans may include unsafe command or path handling.

Mitigation: Inspect generated commands, subtasks JSON, mission IDs, and execution_plan.json before running scripts; execute with least privilege.

Risk: Spawned sessions, mission files, logs, and reports may persist after task completion.

Mitigation: Confirm cleanup behavior and remove retained mission directories, logs, and reports when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oozoofrog/skills/agent-avengers)
- [README](artifact/README.md)
- [Announcement](artifact/ANNOUNCEMENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON plans, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task plans, agent assignments, execution commands, monitoring summaries, and final consolidated reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
