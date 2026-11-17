## Description:

Directoryahu is an end-to-end multi-agent pipeline for creating faceless Islamic short-form story videos, coordinating story research, scriptwriting, image generation, voice narration, and video assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohamedzeidan2021](https://clawhub.ai/user/mohamedzeidan2021)

### License/Terms of Use:


## Use Case:

External creators and developers use this skill to produce educational faceless Islamic story videos for TikTok, Instagram Reels, and YouTube Shorts. The pipeline is intended to generate story research, scripts, image prompts and outputs, narration assets, subtitles, and final video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable orchestrator can write state files outside its intended output folder if story identifiers are not constrained.

Mitigation: Run the skill in a constrained workspace account, validate story_id values from users and agents, and confine writes to a dedicated output directory.

Risk: The artifact claims a face-detection gate, but the security evidence says that gate is not implemented.

Mitigation: Implement real fail-closed face detection and block video generation whenever a generated image violates the faceless constraint.

Risk: Narration and images may be sent to external TTS, image-generation, or cloud-detection providers.

Mitigation: Require explicit user consent and review provider handling before sending narration text, images, or generated media to external services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohamedzeidan2021/skills/director)
- [SKILL.md](artifact/SKILL.md)
- [Visual Style Guide](artifact/visual_style_guide.md)
- [Global Config](artifact/global_config.json)
- [Story Research Agent](artifact/story_agent.md)
- [Script Writer Agent](artifact/script_agent.md)
- [Visual Generation Agent](artifact/visual_agent.md)
- [Voice Narration Agent](artifact/voice_agent.md)
- [Video Assembly Agent](artifact/assembly_agent.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON schemas, shell command examples, configuration snippets, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces story JSON, scene scripts, image and audio paths, subtitle files, thumbnails, and final MP4 video paths when connected to the required tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
