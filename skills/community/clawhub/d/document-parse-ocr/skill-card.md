## Description:

Submits public document URLs to Scnet's asynchronous OCR service and returns structured JSON with recognized text, tables, titles, layout elements, and page Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to send publicly accessible documents to Scnet for asynchronous OCR and document-structure extraction, especially for batch document processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and document URLs are sent to Scnet for external OCR processing.

Mitigation: Use only documents approved for external processing; avoid confidential, regulated, internal-only, or signed-URL documents unless that processing is explicitly approved.

Risk: The skill depends on an API token stored in configuration.

Mitigation: Protect the config/.env token file, avoid pasting API keys into chat, and rotate the token if exposure is suspected.

Risk: The API base can be configured and may direct requests to an unintended network destination.

Mitigation: Keep SCNET_API_BASE pointed at the official HTTPS Scnet endpoint before running the skill.

Risk: Runtime dependencies are not pinned in the artifact evidence.

Mitigation: Pin and review Python dependencies before deployment in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/skills/document-parse-ocr)
- [Scnet Website](https://www.scnet.cn)
- [Sugon-Scnet OCR API Docs](references/api-docs.md)
- [Document Parsing Output Fields](assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON document parsing results with recognized text, layout blocks, tables, images, and page Markdown content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY, accepts a public HTTP or HTTPS file URL, polls asynchronously for up to 600 seconds, and returns errors as user-facing text.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, skill.yaml, and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
