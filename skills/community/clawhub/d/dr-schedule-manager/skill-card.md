## Description:

Guides developers in designing and migrating scheduled automations that load current prompts, policies, delivery settings, and model choices at runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this playbook to design or migrate scheduled jobs so each run loads current configuration, uses an appropriate execution runner, and follows explicit delivery and verification steps. It provides architecture guidance and templates rather than a working scheduler installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scheduled job may use an unintended runner, schedule, recipient, or data permission when enabled.

Mitigation: Review the actual runner, registered schedule, recipients, data permissions, and approval gates before enabling live behavior; require user approval before live messages or production changes.

Risk: Changes to job configuration can affect the next run.

Mitigation: Protect configuration files and validate the current manifest and runtime inputs before rollout.

Risk: Deployment-specific policies and the separately named companion skill were not available for review.

Mitigation: Review the deployment's applicable policies and companion-skill behavior before relying on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/daniel-refahi-ikara/skills/dr-schedule-manager)
- [Architecture patterns](references/architecture-patterns.md)
- [Migration checklist](references/migration-checklist.md)
- [Reliability review](references/reliability-review.md)
- [Daily briefing migration example](references/example-migration-daily-briefing.md)
- [Job manifest template](references/job-manifest-template.json)

## Skill Output:

**Output Type(s):** [Text, Markdown guidance, JSON configuration, Code examples]

**Output Format:** [Markdown guidance with JSON manifest templates and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes migration steps, execution pattern recommendations, and verification checklists; does not install a scheduler.]

## Skill Version(s):

1.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
