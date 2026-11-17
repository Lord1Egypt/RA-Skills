## Description:

CI release engineer skill for validation gating, release-readiness checks, and automation-safe delivery criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to assess CI gates, release readiness, automation-safe validation evidence, and blockers before merge or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad CI or pipeline discussions.

Mitigation: Confirm the user is asking for release gating, CI readiness, or pre-merge validation before applying the checklist.

Risk: Referenced source-material paths may not exist in every project.

Mitigation: Verify the project has equivalent CI, testing, planning, and documentation guidance before treating missing local files as blockers.

Risk: Release-readiness recommendations can be misleading when validation evidence is incomplete.

Mitigation: Require repeatable unit, E2E or HTTP, documentation, and environment evidence where relevant, and report missing evidence as a blocker or explicit risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/ci-ci)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown release-readiness recommendation with validation checks, missing gates, blockers, and follow-up actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is produced by the skill itself; outputs should be grounded in repeatable validation evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
