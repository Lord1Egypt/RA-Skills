## Description:

Automates legal client intake in Box by checking documents against firm requirements, extracting client and matter details, routing submissions for attorney review, and generating approved engagement letters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Legal intake staff and attorneys use this skill to review client submissions against firm requirements, record intake details in Box, route matters for attorney decisions, and prepare engagement letters after firm approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prerequisite Box skills are not pinned to specific versions.

Mitigation: Verify the current sources and versions of both prerequisite skills before installation.

Risk: Intake changes or sharing could expose client information or record an unapproved decision.

Mitigation: Use only the intended intake folder; confirm attorney access, metadata writes, DocGen templates, shared-link audience and expiration before changes, and leave conflicts, PEP, sanctions, risk and legal decisions to the firm's screening process and attorneys.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/iskysun96/skills/box-legal-workflows-intake)
- [Box skills (prerequisite)](https://github.com/box/skills)

## Skill Output:

**Output Type(s):** [Text, Guidance, Files]

**Output Format:** [Markdown intake summaries and Box records or engagement letters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Box metadata and engagement letters are created only with firm-confirmed details and approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
