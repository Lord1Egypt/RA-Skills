## Description:

CamScanner-Image2Office helps an agent convert user-selected images containing text, tables, or complex layouts into editable Word (.docx) or Excel (.xlsx) documents using CamScanner's service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need OCR-based conversion from an image into an editable Office document. It is suited for images that contain text, tables, or complex layouts that should become Word or Excel files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are sent to CamScanner's external OCR conversion service.

Mitigation: Avoid regulated, confidential, identity, financial, customer, or otherwise sensitive documents unless organizational policy permits that service.

Risk: Converted files are written to a local path chosen during use.

Mitigation: Choose output paths deliberately and verify the target directory and extension before downloading the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/camscanner-ai/skills/camscanner-image2office-office)
- [CamScanner homepage](https://www.camscanner.com)
- [CamScanner AI tools API base](https://ai-tools.camscanner.com)
- [Publisher profile](https://clawhub.ai/user/camscanner-ai)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown with bash and JSON examples; downloaded .docx or .xlsx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; sends selected images to CamScanner's external service and saves output to a user-chosen local path.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
