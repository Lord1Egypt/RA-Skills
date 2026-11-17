## Description:

Extract structured data from contracts, legal agreements, court filings, and compliance documents with pre-built schemas for parties, clauses, dates, and obligations, plus PII redaction for privilege review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Legal teams, compliance teams, and developers use this skill to extract contract metadata, clauses, dates, obligations, signatures, and other fields from legal documents. The skill also supports redacting privileged or sensitive information before documents are shared externally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected legal documents are sent to DeepRead for extraction and redaction, and may also be sent to a configured model provider when BYOK is enabled.

Mitigation: Confirm client, privilege, retention, and compliance requirements before upload.

Risk: Sample redacted-file download code may be reused in automation without production hardening.

Mitigation: Add appropriate validation, access controls, error handling, and storage controls before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-legal)
- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard)
- [DeepRead BYOK setup](https://www.deepread.tech/dashboard/byok)
- [DeepRead demo repository](https://github.com/deepread-tech/deepread-demo)
- [DeepRead service issues](https://github.com/deepread-tech/deep-read-service/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY; extracted fields may include human-in-the-loop flags for review.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
