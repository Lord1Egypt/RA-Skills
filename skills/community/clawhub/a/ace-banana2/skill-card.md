## Description:

Ace Banana2 generates and edits images through the AceData Nano Banana API, supporting text-to-image, image-to-image, batch generation, local image upload, custom aspect ratios, and 2K/4K resolutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyunnet](https://clawhub.ai/user/xiyunnet)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate new images from prompts or edit local and remote images with AceData Nano Banana models. The skill can upload local images to AceData CDN, submit generation requests, and save returned image files locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store the AceData API key in a plaintext .env file and includes backup code that could copy that file to a predictable D:/backup location if invoked.

Mitigation: Set ACEDATA_API_KEY in the environment instead of passing --api_key or entering it interactively, and remove or disable backup_skill_files before use.

Risk: Local images used for editing may be uploaded to AceData CDN or sent to AceData services.

Mitigation: Avoid sensitive images unless the user accepts sending them to AceData/CDN services.

## Reference(s):

- [Nano Banana Images API Documentation](references/api_docs.md)
- [AceData Cloud Platform](https://share.acedata.cloud/r/1uN88BrUTQ)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated image files saved locally]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AceData API key, may upload local input images to AceData CDN, prints JSON API responses, and saves output PNG files to a dated desktop folder.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
