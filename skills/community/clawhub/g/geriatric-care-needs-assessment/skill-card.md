## Description:

Drafts a structured geriatric care needs assessment for older adult clients, covering functional status, cognitive and behavioral observations, safety, supports, environment, financial and legal status, and prioritized care recommendations for licensed professional review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External care managers, licensed social workers, eldercare coordinators, and discharge planners use this skill to turn sensitive intake information into a draft multi-domain care needs assessment. The draft supports professional review before care planning, service authorization, sharing, or billing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment content may contain sensitive health and personal information.

Mitigation: Avoid entering unnecessary identifiers, store drafts securely, and confirm authorization before sharing assessment content.

Risk: Draft recommendations could be mistaken for final clinical, care-planning, billing, or authorization decisions.

Mitigation: Keep the output labeled as a draft and require review by a licensed Aging Life Care Manager or social worker before operational use.

Risk: Elder abuse, neglect, or exploitation indicators may create mandatory reporting obligations.

Mitigation: Surface urgent concerns clearly and remind the care manager that any required Adult Protective Services report must be filed directly under the applicable jurisdiction's rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/geriatric-care-needs-assessment)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown draft assessment with tables, priority labels, urgent concern alerts, and licensed professional review block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is labeled as a draft and requires licensed professional review before sharing, billing, service authorization, or care-plan use.]

## Skill Version(s):

0.1.0 (source: release evidence and changelog, released 2026-05-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
