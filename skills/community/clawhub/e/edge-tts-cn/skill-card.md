## Description:

Converts text into speech audio with Microsoft Edge neural voices through node-edge-tts, with configurable language, voice, speed, pitch, volume, output format, and subtitle generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn requested text into spoken MP3 audio with selected voices and languages, and to configure TTS preferences or subtitles when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text may be sent to Microsoft Edge's online TTS service.

Mitigation: Do not submit secrets, credentials, private business data, or sensitive personal content unless the data-handling implications have been reviewed.

Risk: Broad TTS triggers may cause unintended text to be converted to speech.

Mitigation: Confirm user intent before conversion and remove trigger words from the text that is sent for synthesis.

Risk: Generated MP3 and subtitle JSON files can remain on disk.

Mitigation: Clean up generated files from the temporary directory or use an explicit managed output path.

Risk: The skill depends on npm packages and carries supply-chain risk.

Mitigation: Review or update dependencies before use and prefer pinned, reproducible installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/edge-tts-cn)
- [node-edge-tts Reference](references/node_edge_tts_guide.md)
- [Voice Testing Preview](https://tts.travisvn.com/)

## Skill Output:

**Output Type(s):** [audio files, subtitle JSON, shell commands, configuration, guidance]

**Output Format:** [MP3 audio files, optional JSON subtitles, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Microsoft Edge's online TTS service; generated media may be written to temporary or user-specified output paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, target metadata, and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
