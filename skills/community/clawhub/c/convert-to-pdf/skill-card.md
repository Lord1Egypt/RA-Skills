## Description:

Convert one or multiple documents to PDF by uploading them to Cross-Service-Solutions, polling until completion, then returning download URL(s) for the converted PDF(s) or a ZIP if multiple files are converted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossservicesolutions](https://clawhub.ai/user/crossservicesolutions)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to convert one or more documents into PDF output through the Cross-Service-Solutions API and return download URLs for the resulting PDFs or ZIP archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user documents and an API key to a remote conversion service.

Mitigation: Use it only for documents approved for Cross-Service-Solutions processing, protect the API key, and avoid passing the key through shell history.

Risk: The helper script can be redirected with SOLUTIONS_BASE_URL or --base-url.

Mitigation: Leave the default endpoint in place unless the alternate destination is fully trusted and controlled.

Risk: Sensitive, regulated, or confidential files may require additional approval before third-party processing.

Mitigation: Confirm privacy, retention, and compliance requirements before converting those files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossservicesolutions/skills/convert-to-pdf)
- [Cross-Service-Solutions API key registration](https://login.cross-service-solutions.com/register)
- [Solutions API base URL](https://api.xss-cross-service-solutions.com/solutions/solutions)
- [Local skill definition](artifact/SKILL.md)
- [Local README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON result examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script prints structured JSON containing job status, output file metadata, download URL fields, input file names, and error details when conversion fails.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
