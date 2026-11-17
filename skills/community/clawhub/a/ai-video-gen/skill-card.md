## Description:

End-to-end AI video generation - create videos from text prompts using image generation, video synthesis, voice-over, and editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhanbourinajd](https://clawhub.ai/user/rhanbourinajd)

### License/Terms of Use:


## Use Case:

External developers and creators use this skill to generate short AI-assisted videos from text prompts, image sequences, and optional narration. It helps agents propose setup steps and run scripts for image generation, video synthesis, voice-over creation, and FFmpeg assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generated images, and narration may be sent to cloud AI providers.

Mitigation: Avoid sensitive prompts or media, review each provider's terms, and use only API keys approved for the intended data.

Risk: The skill requires paid or quota-limited API keys and stores them through environment variables or a .env file.

Mitigation: Use a virtual environment, keep .env files out of version control, rotate exposed keys, and monitor provider billing.

Risk: Some documented provider features and helper scripts are incomplete or missing from the artifact.

Mitigation: Verify provider support and available scripts before relying on Runway, ElevenLabs, multi-scene, or editing workflows.

Risk: The scripts read and write local media files and invoke FFmpeg.

Mitigation: Run the skill in a private working directory with trusted input files and review generated outputs before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rhanbourinajd/skills/ai-video-gen)
- [Publisher profile](https://clawhub.ai/user/rhanbourinajd)
- [README](artifact/README.md)
- [Quick Start](artifact/QUICK_START.md)
- [OpenAI platform](https://platform.openai.com)
- [Luma Labs](https://lumalabs.ai)
- [Runway](https://runwayml.com)
- [ElevenLabs](https://elevenlabs.io)
- [Replicate](https://replicate.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local media files when the referenced scripts are executed with configured API keys and FFmpeg.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
