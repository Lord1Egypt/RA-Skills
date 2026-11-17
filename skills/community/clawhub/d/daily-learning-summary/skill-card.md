## Description:

Generates dated Markdown summaries of an agent's daily learning activity from local workspace memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yu441374-oss](https://clawhub.ai/user/yu441374-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to consolidate InStreet activity, ClawHub discoveries, skill usage notes, and lessons learned into persistent daily reports for review and follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent daily learning summaries in the workspace.

Mitigation: Install it only in workspaces where persistent learning reports are expected, and review generated files during rollout.

Risk: Generated Markdown may include content derived from memory files that other tools can write.

Mitigation: Treat generated reports as data for review, not as trusted instructions for later agents.

Risk: Rerunning the skill on the same day overwrites that day's report.

Mitigation: Review the overwrite behavior before adding the command to heartbeat automation.

Risk: The report content and status messages are Chinese-only in the artifact.

Mitigation: Confirm the target users can review Chinese output or localize the report before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yu441374-oss/skills/daily-learning-summary)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Markdown file at memory/learning/YYYY-MM-DD.md with brief console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local workspace memory files and overwrites the same-day dated report when rerun.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
