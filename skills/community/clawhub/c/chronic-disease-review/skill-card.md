## Description:

Reviews outpatient chronic disease OCR records for diabetes or hypertension and returns raw review JSON plus a natural-language decision and reasoning summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaiccee](https://clawhub.ai/user/aaiccee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare operations teams use this skill to submit OCR text arrays for outpatient chronic disease audit support, focused on diabetes and hypertension review outcomes. It returns the service response and a readable conclusion with supporting reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical OCR text may be sent to the configured remote review service.

Mitigation: Confirm the service destination, legal basis, and data-sharing controls before use; provide only approved minimum-necessary inputs.

Risk: Review results are saved to disk by default despite the skill's no-persistence claim.

Mitigation: Write outputs only to approved or ephemeral locations and handle all response files as sensitive medical records.

Risk: Audit conclusions may be mistaken for medical diagnosis or treatment advice.

Mitigation: Use the output as administrative review support and require appropriate human review for clinical or eligibility decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaiccee/skills/chronic-disease-review)
- [Chronic disease review service](https://shangbao.yunzhisheng.cn/skills/chronic-disease)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON response plus natural-language text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes response JSON and summary text files to configurable paths; default paths are under ../runs/med-chronic-disease-review.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
