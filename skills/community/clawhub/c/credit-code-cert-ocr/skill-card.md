## Description:

Extracts text and unified social credit code certificate fields from local images, PDFs, or archives using the Sugon-Scnet OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to submit a local document path and receive structured OCR results for unified social credit code certificates. It is suited for extracting certificate fields such as organization name, address, code, issue date, and expiration date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local documents to Scnet for OCR processing.

Mitigation: Use it only with documents approved for submission to Scnet, and confirm the file path before invocation.

Risk: The API key is sent as a bearer token to a configurable endpoint.

Mitigation: Keep SCNET_API_KEY local and protected, restrict config file permissions, and leave SCNET_API_BASE at the official HTTPS endpoint unless the replacement is fully trusted.

Risk: Automatic agent invocation could process arbitrary local file paths.

Mitigation: Require explicit user intent for each file and avoid unattended bulk or arbitrary-path execution.

## Reference(s):

- [Sugon-Scnet OCR API docs](references/api-docs.md)
- [OCR field summary](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/credit-code-cert-ocr)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON on standard output, with text error messages for configuration, network, API, and file validation failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OCR type and local file path; uses SCNET_API_KEY and optional SCNET_API_BASE from local configuration.]

## Skill Version(s):

1.0.3 (source: frontmatter, skill.yaml, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
