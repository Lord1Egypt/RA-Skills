## Description:

Converts Word and PDF drug application documents into draft eCTD 4.0/3.2.2 XML skeletons for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Regulatory operations teams, submission publishers, and developers can use this skill to draft eCTD module XML, index files, and checksums from Word or PDF application documents before independent regulatory validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated XML may not be validated eCTD-compliant output and should be treated as a draft skeleton.

Mitigation: Run independent regulatory and schema validation before relying on generated submission artifacts.

Risk: The skill processes potentially sensitive drug application documents and writes outputs to the workspace.

Mitigation: Use isolated, approved workspaces and non-production or redacted documents unless data handling has been reviewed.

Risk: The security verdict is suspicious and notes dependency and scoping issues.

Mitigation: Pin and review dependencies before installation, and perform security review before production use.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ICH eCTD Specification](https://www.ich.org/page/ectd)
- [FDA eCTD Technical Conformance Guide](https://www.fda.gov/drugs/electronic-regulatory-submission-and-review/ectd-technical-conformance-guide)
- [EMA Electronic Application Forms](https://www.ema.europa.eu/en/human-regulatory/marketing-authorisation/application-procedures/electronic-application-forms)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance plus generated XML and checksum files when the packaged script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Word/PDF inputs and independent regulatory/schema validation of generated XML.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
