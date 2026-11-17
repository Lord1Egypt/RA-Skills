## Description:

Replaces an image’s background scene through Flyelep’s AI API, optionally using a reference image and text prompt to guide the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and agents use this skill to request a new environment for a product or subject while retaining the main subject. It returns the generated image URL for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images may be uploaded to Flyelep to obtain a URL for processing; the documented upload links are described as temporary (24 hours).

Mitigation: Upload only images the user has chosen to process, and avoid retaining or reusing the temporary URL beyond the current task.

Risk: The documented Windows example writes a request payload to a local temporary JSON file.

Mitigation: Keep credentials out of saved files and remove the temporary payload after the API call, as the instructions specify.

## Reference(s):

- [Scene Replace on ClawHub](https://clawhub.ai/flyelepai/skills/flyelep-scene-replace)
- [Flyelep scene replacement API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/sceneReplace)
- [Flyelep image upload API](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)

## Skill Output:

**Output Type(s):** [Image URL, Text]

**Output Format:** [A generated image URL with brief status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to present the result URL without retrieving the image contents.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
