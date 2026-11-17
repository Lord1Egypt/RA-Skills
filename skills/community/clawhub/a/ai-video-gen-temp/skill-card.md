## Description:

End-to-end AI video generation - create videos from text prompts using image generation, video synthesis, voice-over, and editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmyg11](https://clawhub.ai/user/mmyg11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate short videos from text prompts, assemble image sequences into MP4 files, and add narrated voice-over audio through local scripts and configured AI services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, narration, and media-related data may be sent to third-party cloud AI providers.

Mitigation: Avoid sensitive content and review provider data handling before use.

Risk: AI-service keys are expected to be stored in environment variables or a .env file.

Mitigation: Keep credentials out of shared repositories, restrict key permissions where possible, and rotate keys if exposed.

Risk: Provider support is overstated for Runway and ElevenLabs in this version.

Mitigation: Treat those integrations as unverified and test the selected provider path before relying on it.

Risk: Dependencies are specified with broad minimum versions.

Mitigation: Use pinned dependencies or a lockfile before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mmyg11/skills/ai-video-gen-temp)
- [OpenAI platform](https://platform.openai.com)
- [LumaAI](https://lumalabs.ai)
- [Runway](https://runwayml.com)
- [ElevenLabs](https://elevenlabs.io)
- [Replicate](https://replicate.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown instructions with Python command examples and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts, FFmpeg, environment variables, and optional cloud AI providers to create image, audio, and MP4 outputs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
