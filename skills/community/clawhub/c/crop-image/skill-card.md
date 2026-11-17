## Description:

Use this skill when an AI agent needs to crop images through the deployed Crop Image service, including URL-based cropping and file-upload cropping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effimail](https://clawhub.ai/user/effimail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to crop images through ImageClaw's hosted API, either from reachable image URLs or from selected local image uploads, and return cropped image URLs plus metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs or uploaded local image files are sent to ImageClaw's hosted API.

Mitigation: Use the skill only for images that can be shared with that external service, and avoid private, sensitive, internal-only, or credential-bearing image URLs unless data handling terms have been confirmed.

Risk: Remote API failures or validation errors can prevent cropping from completing.

Mitigation: Return the original API status code and detail to the caller, ask for corrected input on 400 or 422 responses, and retry only transient 500 responses or network timeouts.

## Reference(s):

- [Crop Image skill page](https://clawhub.ai/effimail/skills/crop-image)
- [ImageClaw homepage](https://imageclaw.net)
- [ImageClaw API documentation](https://api.imageclaw.net/docs)
- [ImageClaw API base URL](https://api.imageclaw.net)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns cropped image URLs, original image size metadata, face-detection status, and API error details when failures occur.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
