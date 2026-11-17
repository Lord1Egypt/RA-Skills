## Description:

Extracts text and structured fields from business qualification documents, including business licenses, social organization registrations, trade union registrations, religious activity registrations, private non-enterprise registrations, institution legal registrations, and unified social credit code certificates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to call the Sugon-Scnet OCR service for authorized business qualification images or PDFs and return structured OCR results. It is suited for extracting certificate identifiers, names, addresses, dates, representatives, capital, and other fields from supported Chinese enterprise and organization documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads provided documents to a remote OCR service, which can expose sensitive business qualification data.

Mitigation: Use it only for documents you are authorized to process and confirm the user understands that OCR processing occurs through Scnet's remote service.

Risk: A readable local path can cause the skill to upload any file the runtime can access.

Mitigation: Run the skill in a restricted workspace containing only the intended input document, and verify the file path before execution.

Risk: The API base URL is configurable, so documents and the API token could be sent to an unintended endpoint.

Mitigation: Verify config/.env uses the intended HTTPS api.scnet.cn endpoint before invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/enterprise-qualification-ocr)
- [Scnet website](https://www.scnet.cn)
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [OCR field summary](assets/templates/fields-summary.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON emitted to standard output, with setup and usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Scnet API key, an OCR type, and a readable local file path; the remote API may rate limit requests.]

## Skill Version(s):

1.0.5 (source: frontmatter, skill.yaml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
