## Description:

Creates a feature flag management guide and lifecycle playbook covering taxonomy, creation, rollout, monitoring, cleanup, and governance for a service or team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and product teams use this skill to document feature flag practices or produce a per-flag rollout plan. It helps define ownership, approvals, monitoring, rollback, cleanup, and governance expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated rollback, cleanup, or API examples may be applied without adapting them to the team's actual feature flag platform or authorization model.

Mitigation: Adapt examples to the deployed platform, use scoped credentials, require authorized production flag changes, and keep audit logging enabled.

Risk: Generated playbooks may contain placeholders or defaults that do not match a team's compliance, privacy, or contractual rollout constraints.

Mitigation: Review and customize required inputs, rollout constraints, monitoring thresholds, approvals, and rollback commands before adopting the guide.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/feature-flag-guide)
- [Feature Flag Guide homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/feature-flag-guide.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, checklists, templates, decision trees, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-adaptable examples for feature flag rollout, monitoring, rollback, cleanup, and governance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
