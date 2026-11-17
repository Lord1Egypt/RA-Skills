## Description:

Use the Meshy.ai REST API to generate assets: text-to-2D images and image-to-3D models, then download outputs locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabatesduran](https://clawhub.ai/user/sabatesduran)

### License/Terms of Use:


## Use Case:

Developers and creative technical users use this skill to generate Meshy text-to-image assets and image-to-3D OBJ assets from prompts, local images, or public image URLs, then save the generated outputs locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, local image contents converted to data URIs, and image URLs are sent to Meshy.ai for generation.

Mitigation: Use the skill only when the Meshy account and data policy allow sharing those inputs; avoid confidential prompts and images.

Risk: A custom MESHY_BASE_URL can send the Meshy API key and payloads to a non-default endpoint.

Mitigation: Leave MESHY_BASE_URL unset unless the endpoint is trusted and intended.

Risk: Generated files are downloaded from URLs returned by the external service and saved locally.

Mitigation: Review output locations and scan generated assets before using them in downstream workflows.

## Reference(s):

- [Meshy API notes](artifact/references/api-notes.md)
- [Meshy API documentation](https://docs.meshy.ai/en)
- [Meshy Text to Image API](https://docs.meshy.ai/en/api/text-to-image)
- [Meshy Image to 3D API](https://docs.meshy.ai/en/api/image-to-3d)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; generated assets are saved as PNG, OBJ, and optional MTL files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MESHY_API_KEY; sends prompts, images, or image URLs to Meshy.ai and may use MESHY_BASE_URL when configured.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
