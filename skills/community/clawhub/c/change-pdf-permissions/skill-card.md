## Description:

Change a PDF's permission flags for editing, printing, copying, forms, annotations, and related controls by uploading it to the Solutions API, polling until completion, then returning a download URL for the updated PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossservicesolutions](https://clawhub.ai/user/crossservicesolutions)

### License/Terms of Use:

MIT

## Use Case:

Developers and document workflow operators use this skill to change PDF permission flags through the Solutions API and receive a structured job result with the updated file link and final permission settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected PDF and Solutions API bearer token are sent to an external PDF-processing service.

Mitigation: Use the skill only when the provider's privacy and retention practices are acceptable, prefer a scoped API key, and avoid highly sensitive PDFs unless approved.

Risk: The base URL can be changed, which could send PDFs and credentials to an unintended service.

Mitigation: Do not set --base-url or SOLUTIONS_BASE_URL unless it is a trusted HTTPS endpoint you control.

Risk: PDF permission flags may be enforced differently by different PDF viewers.

Mitigation: Test the updated PDF in the target viewer or workflow before relying on the permissions for access control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossservicesolutions/skills/change-pdf-permissions)
- [Solutions API registration](https://login.cross-service-solutions.com/register)
- [Solutions API base URL](https://api.xss-cross-service-solutions.com/solutions/solutions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON result examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces job status, download URL, original file name when available, and the final permission settings sent to the API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
