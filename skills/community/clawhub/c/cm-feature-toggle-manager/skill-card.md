## Description:

Audit, manage, and clean up feature flags across codebases to reduce toggle debt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inventory feature flags, assess toggle debt, identify stale or orphaned flags, and plan safe cleanup or rollout work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for querying external feature-flag services and removing or editing flag configuration.

Mitigation: Require explicit approval before API calls, deletion steps, or configuration edits, and prefer read-only or least-privilege credentials.

Risk: A generated cleanup plan could select the wrong branch or remove a flag that still controls active behavior.

Mitigation: Review the plan in code review, validate the expected flag state, run tests, and verify changes in staging before production rollout.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, checklists, command templates, and code or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated cleanup plans and service changes should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
