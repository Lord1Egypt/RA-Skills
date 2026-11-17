## Description:

Self-driven AI worker that reads goals, generates tasks, executes them, and logs progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changye01](https://clawhub.ai/user/changye01)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to maintain persistent goals, generate concrete tasks, run one round of work per wake-up, and log progress across runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hourly unattended runs can repeatedly modify workspace files while pursuing persistent goals.

Mitigation: Review the agents/ files and working directory before enabling scheduled execution, and remove or disable the cron job when autonomous changes are no longer wanted.

Risk: Persistent goals and task memory may continue driving work after the initial setup.

Mitigation: Keep AUTONOMOUS.md, memory/tasks.md, and memory/backlog.md scoped to intended work, and require user input when goals are empty instead of inventing new goals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/changye01/skills/autonomous-tasks)
- [Publisher profile](https://clawhub.ai/user/changye01)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown task lists, logs, file changes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update persistent agents/ state files and produce workspace outputs for each task.]

## Skill Version(s):

10.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
