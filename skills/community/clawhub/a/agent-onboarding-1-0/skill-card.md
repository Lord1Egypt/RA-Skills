## Description:

Provides a standard onboarding process for new agents joining a collaboration network, covering required general skills, `_config/` setup, cron registration, and capability declaration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royrollpapa](https://clawhub.ai/user/royrollpapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent maintainers use this skill to onboard a new agent into an existing collaboration network with shared skills, local configuration records, recurring synchronization tasks, and a capability announcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and update dependent skills, which can introduce unreviewed behavior if dependency versions or sources are not controlled.

Mitigation: Install only pinned, trusted skill versions in an authorized environment and perform integrity checks before updates.

Risk: The skill directs agents to register recurring cron jobs, which can create persistent automation without adequate documentation or removal paths.

Mitigation: Document each cron command, owner, schedule, and removal step before enabling the jobs.

Risk: The onboarding flow can overwrite `_config/` during synchronization, which may replace local configuration unexpectedly.

Mitigation: Require confirmation or backup before overwriting `_config/` files.

Risk: The skill includes folder tokens whose sensitivity is not established by the evidence.

Mitigation: Treat folder tokens as sensitive unless the service confirms they are non-secret identifiers protected by separate authentication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/royrollpapa/skills/agent-onboarding-1-0)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with configuration filenames, dependency names, and cron expressions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes required dependent skills, `_config/` file expectations, daily cron schedules, and operational best practices.]

## Skill Version(s):

1.0.0 (source: server release metadata; skill frontmatter declares 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
