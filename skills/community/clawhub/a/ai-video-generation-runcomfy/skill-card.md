## Description:

Routes text-to-video, image-to-video, and video-extension requests through the RunComfy CLI and provides model-specific prompting and invocation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to select an appropriate RunComfy video model, structure prompts and input JSON, and run generation jobs from text, images, or existing clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party RunComfy CLI that can execute local code under the user's account.

Mitigation: Use a reviewed and pinned @runcomfy/cli version instead of unpinned npx or global installs.

Risk: RunComfy API tokens and uploaded media can expose account access or sensitive prompt, image, audio, or video content.

Mitigation: Keep tokens narrowly scoped where possible, avoid logging or committing credentials, and submit only media URLs and prompts suitable for RunComfy processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/ai-video-generation-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy video models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy)
- [Kling model collection](https://www.runcomfy.com/models/collections/kling?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy)
- [Seedance model collection](https://www.runcomfy.com/models/collections/seedance?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy)
- [Veo 3 model collection](https://www.runcomfy.com/models/collections/veo-3?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-video-generation-runcomfy)
- [RunComfy publisher profile](https://clawhub.ai/user/permew)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RunComfy model identifiers, input schemas, prompt patterns, and CLI commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
