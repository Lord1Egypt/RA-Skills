## Description:

Generates AI images through the Doubao web interface using browser automation, then saves or delivers the resulting images for downstream workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanxi-ju](https://clawhub.ai/user/fanxi-ju)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate visual assets through Doubao when they need image drafts, illustrations, avatars, presentation graphics, or social media concepts without using a paid image-generation API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated images may be sent to Doubao and optionally to Feishu or another requested destination.

Mitigation: Avoid sensitive prompts or images unless the user accepts the destination service terms and the selected delivery channel.

Risk: Generated images are saved locally under the workspace image directory.

Mitigation: Review saved files and workspace retention expectations before using the skill for sensitive content.

## Reference(s):

- [Doubao Web Interface](https://www.doubao.com/chat/)
- [ClawHub Skill Page](https://clawhub.ai/fanxi-ju/skills/doubao-ai-image)
- [Publisher Profile](https://clawhub.ai/user/fanxi-ju)

## Skill Output:

**Output Type(s):** [guidance, files, text]

**Output Format:** [Markdown guidance describing browser workflow steps, prompt handling, image capture, local file paths, and optional delivery actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under the workspace image directory when the workflow completes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
