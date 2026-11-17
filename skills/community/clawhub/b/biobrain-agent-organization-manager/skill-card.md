## Description:

Helps agents set up multi-department agent organizations with hierarchy, communication patterns, reporting, learning workflows, cron templates, and audit practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ygq19901001](https://clawhub.ai/user/ygq19901001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to design and run agent-team operating systems with department boundaries, routing rules, scheduled work, health checks, and release review practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled autonomous workflows can run with incorrect paths, timezone, budget, or message targets.

Mitigation: Confirm writable paths, timezone, model or API budget, message targets, and pause or rollback process before enabling cron templates.

Risk: Release-oriented guidance could lead an agent to commit, push, release, or publish changes without enough oversight.

Mitigation: Require manual review before any commit, push, release, or publish action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ygq19901001/skills/biobrain-agent-organization-manager)
- [Server-resolved source repository](https://github.com/Ygq19901001/biobrain-agent-organization-manager)
- [Communication Patterns for Multi-Agent Organizations](references/communication-patterns.md)
- [Cron Templates for Agent Organizations](references/cron-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with templates and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes roster, directory, cron, communication, audit, and release-review templates.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
