## Description:

Authenticate AI agents with the DeepRead OCR API using OAuth device flow. The agent displays a code, the user approves it in their browser, and the agent receives a DEEPREAD_API_KEY stored as an environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to authenticate headless AI agents against DeepRead so the agent can receive a DEEPREAD_API_KEY for OCR API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional verification step can upload a document to DeepRead even though the endpoint disclosure focuses on authentication endpoints.

Mitigation: Skip verification when only authentication setup is needed, or use a non-sensitive test PDF.

Risk: The skill produces and stores a production API key in DEEPREAD_API_KEY.

Mitigation: Treat the key as a secret, keep it out of logs and source control, and use a secrets manager for long-term storage.

## Reference(s):

- [DeepRead Homepage](https://www.deepread.tech)
- [DeepRead ClawHub Skill Page](https://clawhub.ai/uday390/skills/deepread-agent-setup)
- [OAuth 2.0 Device Authorization Grant (RFC 8628)](https://datatracker.ietf.org/doc/html/rfc8628)
- [DeepRead Activation Page](https://www.deepread.tech/activate)
- [DeepRead Dashboard](https://www.deepread.tech/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for the DEEPREAD_API_KEY environment variable; does not persist secrets automatically.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
