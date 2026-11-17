## Description:

Processes image prompts or image datasets in bulk by generating images, upscaling them, removing backgrounds, or creating short videos through Apify Actors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxouf](https://clawhub.ai/user/maxouf)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, developers, and commerce teams can use this skill to generate or transform batches of images and turn images into short video clips. It also helps chain processing steps and track each result and its cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, or dataset contents may be sent to external services.

Mitigation: Avoid sending sensitive material unless you have authorization, and consider whether the external services are appropriate for that data.

Risk: Making a Drive file available to anyone with its link can broaden access to that file.

Mitigation: Review any suggestion to broaden Drive sharing before applying it; use only files you are authorized to share with the intended service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/maxouf/skills/apify-bulk-image-pipeline)
- [Actor index](artifact/references/actor-index.md)
- [Cost guardrails and recovery](artifact/references/gotchas.md)
- [Apify image generator Actor](https://apify.com/sherwood/image-generator-batch)
- [Apify image upscaler Actor](https://apify.com/sherwood/image-upscaler-batch)
- [Apify background remover Actor](https://apify.com/sherwood/background-remover-batch)
- [Apify video generator Actor](https://apify.com/sherwood/video-generator-batch)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Image and video URLs, Result data]

**Output Format:** [Apify Actor inputs and dataset results in JSON, with generated image and video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include per-item status and errors; generated media is delivered by URL.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
