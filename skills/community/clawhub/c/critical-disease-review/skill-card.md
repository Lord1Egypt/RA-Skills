## Description:

Assesses structured inpatient medical records against 28 critical-disease insurance claim categories and returns the raw JSON result plus a natural-language conclusion with supporting evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaiccee](https://clawhub.ai/user/aaiccee)

### License/Terms of Use:

MIT-0

## Use Case:

Claims reviewers and agent workflows use this skill to evaluate structured inpatient records against critical-disease claim criteria and collect condition-level evidence for review. Its conclusions are claim-assessment support, not medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive patient and claims data may be transmitted to an external assessment service.

Mitigation: Use only after endpoint approval, explicit consent, and field minimization or redaction of patient-identifying data.

Risk: Assessment results are written to disk by default despite privacy claims that state there is no local persistence.

Mitigation: Remove default disk writes or make them opt-in with documented retention controls and secured output paths.

Risk: The natural-language conclusion can influence claims decisions but is not clinical advice.

Mitigation: Require qualified human review before relying on outputs for claims adjudication or clinical interpretation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaiccee/skills/critical-disease-review)
- [Publisher profile](https://clawhub.ai/user/aaiccee)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, guidance]

**Output Format:** [Raw JSON assessment response and plain-text natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default execution writes raw JSON and text outputs to disk and prints a preview to stdout.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
