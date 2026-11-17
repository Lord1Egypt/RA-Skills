## Description:

教育培训机构专家 covers four education-training reconciliation checks: lesson-hour write-off review, lesson consumption versus teacher-hour-pay review, training-hour consumption versus prepaid tuition review, and tuition-refund review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Education and finance operators use this skill to paste tabular training-institution records, route them to one of four local reconciliation checks, and receive line-referenced findings or missing-column notices. It is intended for operational review support, not legal, tax, attendance, or policy advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local CLI writes a hidden usage-count file in the user's home directory.

Mitigation: Disclose the local persistence behavior before installation and run it only in environments where this local state is acceptable.

Risk: The skill may stop after five runs and request a subscription despite local-only and no-promotion claims.

Mitigation: Tell users about the trial limit before routine use and avoid depending on the free release for uninterrupted operational workflows.

Risk: Users may paste sensitive education or finance records into the tool.

Mitigation: Use sanitized or approved records unless the local workstation and skill package have been reviewed for the relevant data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-education-pub)
- [Publisher profile: chenqg618](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON from a local Node.js CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes pasted table text by headers; JSON output includes subSkill, subSkillName, and result when --json is used.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
