## Description:

Deep Current helps agents maintain long-running research threads with a local Python CLI for topics, notes, sources, findings, and dated markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madebydia](https://clawhub.ai/user/madebydia)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to track ongoing research topics, keep local research state, and guide an agent through scheduled or manual research digest workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains local research state and report files.

Mitigation: Use a workspace where deep-current/currents.json and deep-current-reports/ are acceptable write targets, and review generated reports before relying on them.

Risk: The optional nightly workflow can cause the agent to search the web and write reports on a schedule.

Mitigation: Review the cron prompt, selected model, timeout, and scheduling policy before enabling unattended runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/madebydia/skills/deep-current)
- [Project homepage](https://github.com/madebydia/deep-current)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text output, JSON state files, and markdown research reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local research state under deep-current/ and dated reports under deep-current-reports/ when configured by the user.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
