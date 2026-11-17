## Description:

Reviews user-supplied indicators of electronic evidence authenticity, legality, relevance, and integrity and returns a JSON decision-support result for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Legal professionals and developers use this skill to screen electronic evidence indicators against a four-property checklist in a Chinese civil-litigation context. Its formal review supports, but does not replace, human legal assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented evidence-package input and automatic audit-log archival do not clearly match the local CLI's data handling.

Mitigation: Before using confidential legal evidence, confirm what files are read, what logs are written and retained, and which permissions the runtime grants.

Risk: A formal checklist result may be mistaken for a legal conclusion or verified court-admission decision.

Mitigation: Have a qualified reviewer verify the applicable rules, underlying evidence, and any missing-input assumptions before relying on the result.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/evid-four-check)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dimension findings, missing-input warnings, remediation, and a clause-review checklist; requires human verification.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; bundled SKILL.md lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
