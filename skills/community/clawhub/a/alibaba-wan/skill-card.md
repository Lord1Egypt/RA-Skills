## Description:

Generates AI videos and images with Alibaba Wan 2.6 and Wan 2.5 through Atlas Cloud, covering text-to-video, image-to-video, video-to-video, text-to-image, and image editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate or edit visual media from prompts, images, audio URLs, or video inputs. It supports creative, marketing, social media, product demo, and prototyping workflows that need generated image or video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The image script can automatically use a Google provider when GEMINI_API_KEY is available, which may route prompts or local images outside the declared Atlas Cloud path.

Mitigation: Use explicit provider selection, review environments that contain GEMINI_API_KEY, and apply provider allowlists before running image generation.

Risk: Prompts, image URLs, audio URLs, videos, and uploaded local media are sent to third-party generation providers.

Mitigation: Avoid sensitive prompts or private media unless third-party processing has been approved for the workflow.

Risk: Atlas Cloud API usage is billed to the configured account, with cost affected by model, resolution, and duration.

Mitigation: Confirm cost-sensitive parameters before generation and monitor the account balance or billing controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/alibaba-wan)
- [Publisher profile](https://clawhub.ai/user/xixihhhh)
- [Atlas Cloud](https://www.atlascloud.ai)
- [fal.ai Wan pricing reference](https://fal.ai/models/fal-ai/wan/v2.6/text-to-video)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with shell and Python command examples; generated artifacts are downloaded image or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY for Atlas Cloud API usage; generated media may incur provider charges.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
