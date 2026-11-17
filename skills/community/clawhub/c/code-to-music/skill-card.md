## Description:

Converts a code file into music by analyzing code structure, mapping those features to musical parameters, and using the MiniMax music-2.6 API to generate a code-inspired MP3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besty0121](https://clawhub.ai/user/besty0121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to turn a local source-code file into an MP3 composition for creative presentation, documentation, or experimentation with code-derived music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends code-derived counts, prompts, and generated lyrics to MiniMax, which may be inappropriate for sensitive proprietary code.

Mitigation: Use the skill only with code that is acceptable to process through MiniMax, or review and redact sensitive source material before running it.

Risk: The skill downloads an audio URL returned by the external API and writes the response body directly to disk.

Mitigation: Use trusted MiniMax API responses and consider adding URL validation and response-size limits before routine use.

Risk: Music generation depends on a configured MiniMax API key and account quota for music-2.6.

Mitigation: Configure MINIMAX_API_KEY for an account with music-2.6 access before use and monitor quota or billing impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/besty0121/skills/code-to-music)
- [MiniMax API host](https://api.minimaxi.com)
- [MiniMax music generation endpoint](https://api.minimaxi.com/v1/music_generation)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, files]

**Output Format:** [Console status output and an MP3 audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local input code file, sends derived prompts and generated lyrics to MiniMax, and writes the returned audio to a user-specified path or code_symphony.mp3.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
