## Description:

Verifies identity documents via the Didit standalone API for passports, ID cards, driver's licenses, and residence permits, including OCR extraction, MRZ parsing, document authenticity checks, and KYC document validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and identity/KYC teams use this skill to submit passport, ID card, driver's license, or residence permit images to Didit's standalone API and interpret OCR, MRZ, authenticity, liveness, warning, and verification status results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Government ID images and verification responses can expose sensitive personal information.

Mitigation: Use the skill only with informed consent, redact sensitive response fields before sharing logs or transcripts, and avoid running the helper script in shared terminals or CI logs.

Risk: The helper script saves API requests by default, which may retain document data in the vendor console.

Mitigation: Use --no-save unless retention is explicitly required and approved for the workflow.

Risk: vendor_data may become a persistent identifier associated with a verification session.

Mitigation: Use a non-sensitive opaque identifier for vendor_data and avoid names, document numbers, addresses, or other personal data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rosasalberto/skills/didit-id-document-verification)
- [Didit documentation](https://docs.didit.me)
- [Didit ID Verification API reference](https://docs.didit.me/standalone-apis/id-verification)
- [Didit ID Verification feature guide](https://docs.didit.me/core-technology/id-verification/overview)
- [Didit supported documents](https://docs.didit.me/core-technology/id-verification/supported-documents-id-verification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API examples, shell commands, and JSON response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include helper-script output from the Didit API; responses can contain sensitive personal data from identity documents.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
