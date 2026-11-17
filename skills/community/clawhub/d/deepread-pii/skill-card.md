## Description:

Redacts PII from PDFs, scanned images, and text files using DeepRead's context-aware document redaction API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to redact personal data from documents before sharing them, sending them to other APIs or LLMs, or storing cleaned copies for business workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Original, unredacted documents are uploaded to DeepRead for processing, which creates privacy and compliance risk for sensitive or regulated records.

Mitigation: Use the skill only when authorized to send the source documents to DeepRead, and review DeepRead privacy, retention, compliance, and webhook handling terms before production use.

Risk: The skill depends on the DEEPREAD_API_KEY credential and calls a third-party cloud API.

Mitigation: Keep the API key secret, rotate it if compromised, and test workflows with non-sensitive documents before sending confidential files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/uday390/skills/deepread-pii)
- [DeepRead Homepage](https://www.deepread.tech)
- [DeepRead Privacy Policy](https://www.deepread.tech/privacy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash, JSON, Python, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to call the DeepRead API, poll or receive webhook results, and retrieve a redacted document with a detection report.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
