## Description:

Uses the AnyParse API to extract structured content, layout information, and text from documents and images in many common formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyforge](https://clawhub.ai/user/anyforge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse local documents through a configured AnyParse API endpoint when they need extracted text, OCR-like document conversion, layout analysis, orientation classification, or layout-preserving structured output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files submitted for parsing are uploaded to the configured AnyParse endpoint, which may expose private document contents if the endpoint is untrusted or not approved for the data.

Mitigation: Use only an AnyParse endpoint you control or trust, prefer HTTPS, and avoid submitting confidential files unless the service is approved for that data.

Risk: The AnyParse API key is read from environment variables or configuration and sent as a bearer token to the configured endpoint.

Mitigation: Use a narrowly scoped and revocable API key, store it outside shared files when possible, and rotate it if endpoint or workspace exposure is suspected.

Risk: The dependency list is unpinned, so installing dependencies later may resolve to newer package versions than those reviewed.

Mitigation: Pin dependency versions before deployment and review dependency changes during installation or release updates.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the parser script returns JSON containing metadata, page layout, extracted text, status code, and message fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured AnyParse API URL and API key; layout analysis is enabled by default and can be adjusted with CLI flags.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
