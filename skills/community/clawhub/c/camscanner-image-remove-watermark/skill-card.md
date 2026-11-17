## Description:

Uses CamScanner's hosted image enhancement service to remove watermarks, stamps, and translucent logos from images while preserving the underlying content and layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create curl and jq workflows that upload an image to CamScanner, remove a watermark, and save the cleaned JPG locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images processed with this skill are sent to CamScanner's servers.

Mitigation: Avoid using it on IDs, contracts, confidential business documents, copyrighted media you do not control, or other sensitive files.

Risk: Watermark or stamp removal can alter the meaning or authenticity of official or protected documents.

Mitigation: Use the workflow only when you have the right to modify the image, and review the resulting file before relying on or sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/camscanner-ai/skills/camscanner-image-remove-watermark)
- [CamScanner homepage](https://www.camscanner.com)
- [CamScanner AI tools API base URL](https://ai-tools.camscanner.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; generated commands upload selected images to CamScanner servers and save processed JPG files locally.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
