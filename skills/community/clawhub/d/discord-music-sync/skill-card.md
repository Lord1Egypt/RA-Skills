## Description:

Sync song lyrics with music playback timing in Discord and generate timed lyric audio segments plus synchronized playback instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Discord automation users use this skill to turn timestamped lyrics into karaoke-style playback assets and timing instructions for synchronized Discord messages or audio playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided lyric files and may process sensitive or copyrighted lyrics.

Mitigation: Use only lyrics you are allowed to process and review generated Discord messages before sending them.

Risk: The skill writes generated audio assets and playback.txt to the selected output directory.

Mitigation: Use a dedicated per-project output directory instead of a broad shared folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/discord-music-sync)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and generated playback.txt text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces timestamped lyric playback guidance and local output files in the user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
