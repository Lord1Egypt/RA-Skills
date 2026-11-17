## Description:

Extract structured data from pay stubs and earnings statements, including employer, employee, pay period, gross and net pay, taxes, deductions, and year-to-date totals, as typed JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

External users, lending teams, tenant-screening teams, HR auditors, and benefits reviewers use this skill to extract pay stub fields and support income verification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pay stubs may contain highly sensitive personal and financial information that is sent to DeepRead's external API.

Mitigation: Review DeepRead's privacy, retention, deletion, and compliance terms before use, and only upload documents when external processing is acceptable.

Risk: The skill's redaction guidance is incomplete and may leave unnecessary personal data in uploaded documents.

Mitigation: Redact unnecessary PII before upload and verify redaction quality before sending documents externally.

Risk: Related DeepRead install commands reference separate packages that are outside this skill's security review.

Mitigation: Review and scan each related skill independently before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-pay-stubs)
- [Publisher profile](https://clawhub.ai/user/uday390)
- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell setup commands, and Python verification code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends pay stub documents to the DeepRead external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
