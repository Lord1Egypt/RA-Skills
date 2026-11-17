## Description:

Cron orchestration and mutual-exclusion guidance for separating coordinator, team broadcast, and side-collection tasks with single-task rounds, five-minute spacing, and lock files to prevent concurrent execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[managernet](https://clawhub.ai/user/managernet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to define cron-agent responsibilities, ordering, locking, notification behavior, and isolated execution contexts for scheduled repository automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated cron agents can modify files, push changes, send notifications, and dispatch agents with broad authority.

Mitigation: Install or invoke the skill only in repositories where that automation is approved, and add branch isolation or explicit review gates before pushes.

Risk: Secrets or sensitive repository content could be exposed through automated outputs or pushes.

Mitigation: Confirm secret-scanning and publication controls before enabling automated commits, pushes, or notification messages.

Risk: Dependency ordering is known to need stronger enforcement, and older cron flows may overlap with the new orchestration rules.

Mitigation: Fix dependency enforcement and disable or separate the legacy side_research_run.sh flow before relying on the orchestration in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/managernet/skills/cron-orchestration)
- [Publisher profile](https://clawhub.ai/user/managernet)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, markdown]

**Output Format:** [Markdown guidance with task tables, cron rules, lock-file conventions, and notification formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions; it does not include executable scripts in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
