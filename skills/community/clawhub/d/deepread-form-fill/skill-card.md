## Description:

AI-powered PDF form filling that uploads a PDF form and JSON data to DeepRead, detects fields visually, maps values semantically, performs quality checks, and returns a completed PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation teams use this skill to fill existing PDF forms from structured JSON data through DeepRead's remote form-fill API, including scanned forms and templates without AcroForm fields. The returned report helps users review filled, verified, and human-review fields before relying on the completed PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends PDFs, form-field data, and optional webhook destinations to DeepRead's remote service.

Mitigation: Install only when that data transfer is acceptable, review DeepRead's retention and compliance terms, and avoid sending sensitive SSNs, tax, financial, medical, or employment data unless the use case has appropriate approval.

Risk: Generated filled-PDF download URLs may expose completed documents if they are logged or shared.

Mitigation: Shorten signed URL expiry where possible and keep generated download URLs out of logs, shared transcripts, and tickets.

Risk: Command-line examples can place sensitive form-field values in shell history or process logs.

Mitigation: Prefer secure files or application-managed request bodies for sensitive data, and avoid putting real sensitive values directly on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-form-fill)
- [DeepRead homepage](https://www.deepread.tech)
- [DeepRead dashboard](https://www.deepread.tech/dashboard/?utm_source=clawhub)
- [DeepRead BYOK setup](https://www.deepread.tech/dashboard/byok)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY; submits PDF files and form-field JSON to DeepRead's API and returns status, a signed filled-PDF URL, and a quality report.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
