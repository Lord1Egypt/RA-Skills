## Description:

Use CamScanner to extract mathematical formulas from images by sending an image to CamScanner's OCR service, detecting formula regions, and producing a stitched PNG result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to extract equations or mathematical expressions from photos, screenshots, and scanned documents into a clean PNG image for downstream use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are sent to CamScanner's servers for formula extraction.

Mitigation: Use the skill only when the transfer of those images to CamScanner is acceptable; avoid confidential, regulated, or personal information unless the third-party processing is approved.

Risk: The workflow depends on a third-party OCR service and local command-line tools.

Mitigation: Confirm curl and jq are available and review service responses before relying on the downloaded PNG output.

## Reference(s):

- [CamScanner Homepage](https://www.camscanner.com)
- [CamScanner AI Tools API Base](https://ai-tools.camscanner.com)
- [ClawHub Skill Page](https://clawhub.ai/camscanner-ai/skills/camscanner-extract-formula)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and JSON examples; the workflow downloads a PNG file locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; sends selected images to CamScanner servers for processing.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
