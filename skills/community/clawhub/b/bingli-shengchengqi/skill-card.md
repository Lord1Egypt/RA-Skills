## Description:

Bingli Shengchengqi collects basic case details and drafts a structured Chinese admission record.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gshatw](https://clawhub.ai/user/gshatw)

### License/Terms of Use:

MIT-0

## Use Case:

External users or clinical documentation drafters can use this skill to collect complaint, sex, age, and optional context before drafting a structured admission record. Treat the output as a draft-writing aid, not as verified clinical facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create authoritative-looking patient records with invented clinical details from incomplete input.

Mitigation: Use the output only as a draft; verify every fact and mark unsupported fields as unknown or not assessed before clinical, billing, insurance, or legal use.

Risk: The workflow may involve sensitive medical information.

Mitigation: Do not enter real patient data unless the execution environment is approved for sensitive medical information.

Risk: Default normal values can make missing history, vital signs, or examination details appear confirmed.

Mitigation: Review all defaulted fields and replace unsupported values with explicit unknown or not assessed wording.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gshatw/skills/bingli-shengchengqi)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown admission-record draft with conversational prompts for missing details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for basic patient details, confirms the collected information, and may fill unspecified fields with normal or clinical default values.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
