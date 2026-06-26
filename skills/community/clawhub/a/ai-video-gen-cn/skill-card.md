## Description: <br>
End-to-end AI video generation that creates videos from text prompts using image generation, video synthesis, voice-over, and FFmpeg editing with providers such as OpenAI DALL-E, Replicate, LumaAI, and Runway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate short videos from text prompts, convert image sequences to MP4, and add voice-over narration using AI providers and FFmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, narration, and generated media may be sent to third-party AI providers. <br>
Mitigation: Use provider accounts approved for the content being processed, avoid confidential or regulated content unless policies allow it, and keep API keys out of source control. <br>
Risk: Video, image, and voice generation can incur provider API costs. <br>
Mitigation: Use dedicated API keys with spending limits and monitor provider usage before running larger batches. <br>
Risk: Generated media outputs can overwrite existing files if reused output paths are supplied. <br>
Mitigation: Write outputs to fresh filenames or directories and review generated files before sharing or deploying them. <br>
Risk: The skill depends on local Python packages and FFmpeg in addition to external services. <br>
Mitigation: Install dependencies in an isolated environment and confirm FFmpeg and required API keys are configured before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/onlyloveher/ai-video-gen-cn) <br>
- [OpenAI Platform](https://platform.openai.com) <br>
- [LumaAI](https://lumalabs.ai) <br>
- [Runway](https://runwayml.com) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [Replicate](https://replicate.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance, bash commands, and generated media files such as MP4, PNG, and MP3] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call third-party AI APIs and write generated media to user-specified output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.yaml, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
