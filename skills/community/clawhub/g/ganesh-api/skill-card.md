## Description:

Ganesh Image Hosting API for image hosting. Use when user mentions "Ganesh", "upload image", "image hosting", or asks about image sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidbergman121](https://clawhub.ai/user/davidbergman121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to upload images to Ganesh and obtain shareable URLs for articles, Markdown, documentation, or image sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends users to mutable API instructions through a shortened URL.

Mitigation: Verify the current Ganesh API destination and parameters before using generated guidance or uploading files.

Risk: The skill may lead to images being uploaded to an external hosting service without clear consent handling.

Mitigation: Use the skill only when the user explicitly intends to upload an image, and avoid sensitive or private images unless the hosting service's storage and sharing behavior is understood.

## Reference(s):

- [Ganesh Official API Documentation](https://ishortn.ink/ganesh-official-api)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls]

**Output Format:** [Markdown or text instructions with API usage details and shareable image URLs when an upload is performed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The linked API documentation changes frequently, so generated guidance should be checked against the current Ganesh documentation before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
