## Description:

Generates images with Doubao Seedream through Volcano Engine ARK when users invoke Maliang or request Doubao, Seedream, or Volcano ARK image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joannaxing](https://clawhub.ai/user/joannaxing)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate AI images from text prompts with Doubao Seedream, return the image to chat, and save local image outputs with a manifest and gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's API key to a configurable image-generation endpoint.

Mitigation: Use only trusted Volcano Engine ARK endpoints and do not let prompts or untrusted configuration set SEEDREAM_API_ENDPOINT or --endpoint.

Risk: Prompt text is sent to the configured remote image service and stored locally in manifest.json.

Mitigation: Avoid sensitive prompt content unless sending it to the remote service and storing it locally is acceptable.

Risk: Generated image URLs returned by the configured endpoint are downloaded without independent URL validation.

Mitigation: Review the skill before installing and use a narrowly scoped API key with quota limits.

## Reference(s):

- [Project homepage](https://github.com/JoannaXing/doubao-maliang-image-gen)
- [Volcano Engine ARK Console](https://console.volcengine.com/ark/)
- [Volcano Engine ARK image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [Images, Files, JSON, HTML, Shell commands]

**Output Format:** [Generated image files with manifest JSON, an HTML gallery, and terminal text listing saved file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Volcano Engine API key; defaults to Seedream 5.0, 2K output size, and one to four images per request.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
