## Description:

Agent Benchmark evaluates AI agent task completion across file operations, data processing, system operations, robustness, and code quality using standardized benchmark tasks and Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to run lightweight AI agent benchmark tasks, compare behavior before releases, diagnose capability gaps, and generate evaluation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run custom local code with inherited environment access, which may expose secrets or affect the host workspace.

Mitigation: Run it only in an isolated sandbox with trusted task files, a scrubbed environment, and no valuable workspace or credentials available.

Risk: Server security evidence reports unsafe file and persistence behavior that should be reviewed before installation.

Mitigation: Validate task IDs and paths, disclose executable custom tasks, avoid writes to agent memory, and use a real container or restricted account before normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/agent-benchmark)
- [Publisher profile](https://clawhub.ai/user/yuyonghao-123)
- [Artifact skill documentation](artifact/SKILL.md)
- [Default benchmark tasks](artifact/tasks/default-tasks.json)
- [First-run test summary](artifact/TEST_SUMMARY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown reports, console text, task definitions, and executable command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scored benchmark results by task and category; custom task files can change executed behavior.]

## Skill Version(s):

0.1.0 (source: server release metadata, target metadata, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
