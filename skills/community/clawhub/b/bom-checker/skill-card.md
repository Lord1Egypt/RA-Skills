## Description:

Validate visual inspection device BOM completeness to prevent missing components. Use when checking BOM integrity, auditing bill of materials, verifying AOI device components, or preventing assembly line stoppages from missing parts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, automation, and procurement teams use this skill to review visual inspection equipment BOMs before purchasing or assembly. It checks expected camera, lighting, control, motion, electrical, mechanical, sensor, pneumatic, and software components and reports critical, high-risk, and medium-risk gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated BOM reports may be used to support purchasing or production decisions.

Mitigation: Review generated reports before relying on pass/fail conclusions for purchasing or production decisions.

Risk: BOMs can contain confidential supplier, part, or pricing information.

Mitigation: Confirm where the agent saves report files before using the skill with confidential BOM data.

Risk: The skill is written for Chinese-language BOM reports.

Mitigation: Install only when Chinese-language BOM reports are acceptable for the team reviewing the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/bom-checker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text BOM completeness report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes missing-item lists, included components, warnings, recommendations, and a pass/fail conclusion.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
