## Description: <br>
Generate videos using Seedance models. Invoke when user wants to create videos from text prompts, images, or reference materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to ask an agent to generate Seedance videos from text prompts, first or last frame images, and reference image, video, or audio URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt the agent to store video-provider API keys in a workspace environment file. <br>
Mitigation: Use a scoped provider API key through the platform secret manager and avoid committing or sharing workspace environment files. <br>
Risk: Prompts and media URLs are sent to the configured remote video provider for processing. <br>
Mitigation: Avoid private prompts or sensitive media URLs unless the user accepts provider-side processing for that content. <br>


## Reference(s): <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Video generation implementation](artifact/scripts/video_generate.py) <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-seedance-video-generate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with video embeds, downloadable video URLs, JSON status objects, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return success, partial_success, error, or pending task status with video URLs, error details, or task IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
