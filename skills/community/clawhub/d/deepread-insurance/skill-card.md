## Description:

Extract structured data from insurance claims, policies, EOBs, and loss reports, with pre-built schemas for claimant information, coverage, damages, adjuster notes, and PII redaction for compliant sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance operations teams, claims reviewers, and developers use this skill to extract structured fields from claims, policy documents, EOBs, loss reports, and adjuster notes, then optionally redact claimant PII before sharing documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends complete insurance and EOB documents to a third-party cloud document-processing service.

Mitigation: Use it only when authorized to disclose those documents to DeepRead and its processing providers, and review privacy, retention, deletion, residency, subprocessor, and compliance terms before use.

Risk: Uploaded files may contain unredacted regulated, confidential, or claimant personal information.

Mitigation: Minimize data before upload where possible, redact locally when feasible, and treat use of the redaction endpoint as a third-party disclosure of the original document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-insurance)
- [Publisher profile](https://clawhub.ai/user/uday390)
- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)
- [DeepRead demo repository](https://github.com/deepread-tech/deepread-demo)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with Python, cURL, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends documents to the DeepRead API for processing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
