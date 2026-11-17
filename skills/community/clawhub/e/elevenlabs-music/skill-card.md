## Description:

Generate music from text prompts using ElevenLabs Eleven Music API. Use when creating songs, soundtracks, jingles, lullabies, or any audio music from descriptions. Supports vocals with AI-generated lyrics, instrumental tracks, and multiple genres/styles. Requires paid ElevenLabs plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdbotborges](https://clawhub.ai/user/clawdbotborges)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate songs, instrumental tracks, soundtracks, jingles, lullabies, and other music from text prompts through the ElevenLabs Eleven Music API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script requires an ElevenLabs API key, which could be exposed if run in an overly broad environment.

Mitigation: Run it in a limited environment with only ELEVENLABS_API_KEY available and avoid sharing logs or shells that may expose credentials.

Risk: Music generation can incur paid ElevenLabs API usage.

Mitigation: Confirm plan access and usage budget before repeated generation, and choose duration settings deliberately.

Risk: The script installs Python dependencies at runtime through uv.

Mitigation: Pin or lock dependencies before repeated or production use.

Risk: Prompts that reference protected artists or bands may be rejected by the API or create copyright concerns.

Mitigation: Describe musical style, genre, era, mood, and instrumentation instead of naming artists or bands directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdbotborges/skills/elevenlabs-music)
- [ClawHub publisher profile](https://clawhub.ai/user/clawdbotborges)
- [ElevenLabs pricing](https://elevenlabs.io/pricing)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated audio is saved as an MP3 file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY, uv, and a paid ElevenLabs plan; supports 3-600 second duration and instrumental-only mode.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
