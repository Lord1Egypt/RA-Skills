## Description:

Parses documents, images, and media into structured content and extracts schema-defined fields from documents with optional citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can convert documents, images, and media into readable or structured content and extract specified fields from documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files selected for parsing or extraction are sent to Alibaba Cloud for processing.

Mitigation: Only submit files approved for cloud processing; avoid secrets, source code, regulated data, and private documents unless policy permits the transfer.

Risk: Loading API keys with an unsafe environment-file export pattern may expose or mishandle credentials.

Mitigation: Set DASHSCOPE_API_KEY using an approved secrets manager or a safe environment-variable setup; do not use `export $(cat .env | xargs)`.

## Reference(s):

- [Alibaba Cloud Parse-X skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-parse-x)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Guidance]

**Output Format:** [Markdown, JSON, HTML, or layout data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extracted fields may include citations; results can be returned as text or saved to a file.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
