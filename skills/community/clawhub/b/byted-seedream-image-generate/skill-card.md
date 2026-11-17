## Description:

Generate high-quality images from text prompts using Volcano Engine Seedream models, with support for multiple artistic styles, aspect ratios, image-to-image workflows, batch generation, and model-version selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or transform images through Volcano Engine Seedream models from text prompts, reference image URLs, or batch requests. It is suited for creative content generation where API credentials and generated image handling are acceptable for the deployment environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Console output may expose the API bearer token and prompt/request details during normal use.

Mitigation: Use only API keys and prompts that are acceptable in local console or agent logs, avoid private image URLs or confidential reference material, and rotate any key whose output may already have been captured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-seedream-image-generate)
- [Volcano Engine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON result data and Markdown image links, with optional shell command and Python usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns generated image URLs or base64 image data, success and error lists, model/version metadata, and guidance to save image URLs promptly because generated URLs are documented as temporary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
