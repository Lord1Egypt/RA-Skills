## Description:

Generate full songs and instrumental tracks with ElevenLabs Music on RunComfy via the runcomfy CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to generate vocal songs, instrumental beds, jingles, podcast intros, game loops, and soundtrack-style music from structured text prompts through RunComfy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance may lead users to install or execute an unpinned third-party CLI that can change after review.

Mitigation: Review the RunComfy CLI package before installing, use a pinned reviewed version, and avoid unpinned npx or global installs in controlled environments.

Risk: The skill requires a RunComfy token and local RunComfy configuration.

Mitigation: Run the CLI with only the RunComfy token and project directories needed for music generation, and avoid logging or committing credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/permew/skills/elevenlabs-music-generation)
- [RunComfy](https://www.runcomfy.com)
- [ElevenLabs Music model on RunComfy](https://www.runcomfy.com/models/elevenlabs/elevenlabs/music-generation?utm_source=clawhub&utm_medium=skill&utm_campaign=elevenlabs-music-generation)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=elevenlabs-music-generation)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=elevenlabs-music-generation)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to call the RunComfy CLI, prepare JSON inputs, and save generated audio files to an output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
