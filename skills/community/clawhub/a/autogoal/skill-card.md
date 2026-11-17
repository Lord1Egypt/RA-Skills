## Description:

Automates ongoing progress on user-defined long-term goals with periodic check-ins, adaptive strategies, and progress reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandongraves08](https://clawhub.ai/user/brandongraves08)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Autogoal to turn open-ended long-term objectives into recurring agent check-ins that evaluate progress, take concrete actions, adapt strategy, and report status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous check-ins can continue acting after the user has lost context or after the goal is no longer appropriate.

Mitigation: Require explicit confirmation for each cron job, set expiration and cleanup rules, and review scheduled payloads before enabling them.

Risk: Scheduled runs may have broader tool authority than the goal requires.

Mitigation: Restrict scheduled check-ins to read-only or narrowly allowed tools and require human approval before irreversible external actions.

Risk: Financial goals can lead to harmful live trading or market actions.

Mitigation: Use paper or simulation mode by default, configure risk rules, and avoid live financial actions without explicit human approval.

Risk: Stored goal text and strategy notes may include untrusted or stale instructions.

Mitigation: Treat stored goal content as untrusted data and revalidate instructions, permissions, and user intent during check-ins.

## Reference(s):

- [Autogoal ClawHub Page](https://clawhub.ai/brandongraves08/skills/autogoal)
- [Goal Lifecycle Patterns](references/goal-lifecycle.md)
- [Planning Depth & Strategy Reference](references/planning-depth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON cron configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes progress reports, strategy updates, goal lifecycle commands, and recurring check-in configuration.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
