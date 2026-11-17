## Description:

Audits one local prospectus PDF, DOC, or DOCX through PDRouter and downloads the annotated result with AutoDoc NEXT2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paodingai](https://clawhub.ai/user/paodingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other authorized users audit a single local prospectus and retrieve an annotated document after the audit completes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local prospectus is uploaded to the configured PDRouter service.

Mitigation: Audit only documents you are permitted to upload to that service.

Risk: Disclosure of the PDRouter API key could expose service access.

Mitigation: Keep the PAODINGAI_API_KEY credential private.

## Reference(s):

- [AutoDoc NEXT2.0 ClawHub listing](https://clawhub.ai/paodingai/skills/autodoc-next-prospectus-audit)
- [PDRouter service](https://platform.paodingai.com/)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Human-readable status updates and annotated PDF or DOCX]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The annotated file is downloaded only on explicit request and checked for size and SHA-256 integrity.]

## Skill Version(s):

1.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
