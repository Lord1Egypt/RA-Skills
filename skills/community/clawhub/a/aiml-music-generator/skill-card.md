## Description:

Generate high-quality music or songs via AIMLAPI using Suno, Udio, Minimax, and ElevenLabs models for requested lyrics, styles, or soundtracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aimlapihello](https://clawhub.ai/user/aimlapihello)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate instrumental tracks or songs with custom prompts, lyrics, model choices, and length settings through AIMLAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, the AIMLAPI API key, and generated audio are handled through external network calls.

Mitigation: Use the skill only when external AIMLAPI processing is acceptable, avoid private or sensitive text in prompts and lyrics, and keep the API key in the environment.

Risk: API use may create cost exposure during generation and polling.

Mitigation: Use spending limits on the AIMLAPI key and tune polling interval and maximum wait settings for the task.

Risk: Downloaded MP3 files may need review before redistribution or commercial use.

Mitigation: Review generated audio and applicable AIMLAPI or model terms before publishing, sharing, or using it in production content.

## Reference(s):

- [AIML Music Generator on ClawHub](https://clawhub.ai/aimlapihello/skills/aiml-music-generator)
- [AIMLAPI audio generation API endpoint](https://api.aimlapi.com/v2)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Command-line guidance and downloaded MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY and writes generated music files to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
