## Description:

Extracts structured fields from consented Chinese national ID cards, bank cards, driver's licenses, and vehicle licenses for human-reviewed KYC workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carochen112233-commits](https://clawhub.ai/user/carochen112233-commits)

### License/Terms of Use:

MIT-0

## Use Case:

KYC onboarding and identity-operations teams use this skill to extract document fields from authorized images for human-reviewed verification workflows. OCR extraction does not establish document authenticity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity and bank-card images and extracted fields contain sensitive personal data.

Mitigation: Process only authorized documents through a trusted HTTPS backend; apply masking, access controls, and retention limits.

Risk: OCR results can be incomplete or mistaken and do not prove document authenticity.

Mitigation: Request clearer images for uncertain fields and require authorized human review before high-impact decisions.

## Reference(s):

- [eKYC Suite Document OCR on ClawHub](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite-document-ocr)
- [Related eKYC Suite Document OCR MCP package](https://www.npmjs.com/package/@wefi-ai/ekyc-suite-document-ocr-mcp)
- [eKYC Suite parent skill](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured JSON fields or a concise, masked text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports four document categories; missing or unreadable fields should not be guessed.]

## Skill Version(s):

1.0.20 (source: server-resolved ClawHub release metadata; bundled skill frontmatter says 1.0.19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
