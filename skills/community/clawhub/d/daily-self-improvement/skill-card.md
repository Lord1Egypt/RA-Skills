## Description:

Daily Self Improvement collects daily failure and correction signals, analyzes recurring issues, suggests relevant ClawHub skills, writes a Markdown reflection report, and can send the report to Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and operators use this skill to summarize recent failures, daily-note issues, and corrections into a daily self-improvement report with suggested follow-up skills and actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships unsafe defaults that can send local operational summaries to a preset Discord destination using an embedded gateway credential.

Mitigation: Remove the embedded gateway token, disable Discord notifications by default, replace the bundled channel ID with a confirmed destination, and inspect the outgoing report payload before scheduling.

Risk: Failure logs, daily notes, corrections, and memory files may contain sensitive operational or user-specific information.

Mitigation: Review and minimize configured data sources before running the skill, and avoid sending generated summaries to external services unless the destination is approved.

Risk: The generated report recommends skill install commands that could introduce additional unreviewed packages.

Mitigation: Review each recommended package separately before running any generated install command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/daily-self-improvement)
- [Publisher profile](https://clawhub.ai/user/sunnyhot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with suggested actions, skill install commands, optional Discord message text, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated report under memory/self-improvement and may append a daily-note summary when those workspace files are present.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
