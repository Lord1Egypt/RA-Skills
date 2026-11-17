## Description:

End-to-end AI video generation - create videos from text prompts using image generation, video synthesis, voice-over, and editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matttgx](https://clawhub.ai/user/matttgx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate short AI videos from text prompts, image sequences, and optional narration through Python CLI scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generated media, and narration can be sent to third-party AI providers.

Mitigation: Use only non-sensitive prompts and media, and verify which provider will receive each request before running the scripts.

Risk: Provider support is overstated; the Runway option is advertised but does not provide an independent Runway workflow in the artifact.

Mitigation: Avoid the Runway option until it is fixed, and test the selected provider path before using the skill for real work.

Risk: Dependency versions are ranged rather than pinned.

Mitigation: Run the skill in an isolated environment and pin dependencies before production or team use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matttgx/skills/ai-video-gen-1-0-0)
- [OpenAI Platform](https://platform.openai.com)
- [LumaAI](https://lumalabs.ai)
- [Runway](https://runwayml.com)
- [ElevenLabs](https://elevenlabs.io)
- [Replicate](https://replicate.com)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python CLI commands and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PNG, MP4, and MP3 files; uses configured third-party API keys and FFmpeg.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
