## Description:

Checks UIBC contest submissions against TH-EVT-001 requirements and returns structured decision-support results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Contest participants and reviewers use this skill to check required submission materials and file formats before submitting UIBC code, theory, or design entries. Results support review rather than determining final eligibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A checklist result may be mistaken for an official eligibility decision or reflect rules that need confirmation.

Mitigation: Treat results as decision support and check the current contest rules with a human reviewer before adjudication.

Risk: The skill declares broader tool access than its local checker needs.

Mitigation: Grant only minimal local Python execution permissions; do not grant web access or write access without a separate need.

Risk: Published license metadata conflicts with the artifact's code license and documentation rights statements.

Mitigation: Confirm licensing for code and documentation separately before redistribution.

## Reference(s):

- [Contest Submission Portal on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/contest-submission-portal)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports required and missing items, format checks, warnings, and a result code (0: no warnings; 1: warnings; 2: invalid input).]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact declares 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
