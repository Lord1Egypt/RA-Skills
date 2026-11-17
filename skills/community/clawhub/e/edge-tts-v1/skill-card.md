## Description:

Text-to-speech conversion using node-edge-tts for generating audio from text with configurable voices, languages, speed, pitch, and subtitle generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert requested text into spoken audio, choose Microsoft Edge neural voices, adjust prosody, and optionally produce subtitle timing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted text is sent to Microsoft Edge's online TTS service.

Mitigation: Avoid converting secrets, personal data, or proprietary text unless the user has permission and the service use is acceptable.

Risk: Generated audio can remain in a temporary directory or user-selected output path.

Mitigation: Clean temporary audio files after use or choose a trusted output location with appropriate access controls.

Risk: The release relies on npm dependencies and was flagged for dependency-pattern review.

Mitigation: Review, update, or pin dependencies before using the skill in shared or production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/edge-tts-v1)
- [node-edge-tts Reference](references/node_edge_tts_guide.md)
- [Voice Testing](https://tts.travisvn.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline JavaScript and bash examples; generated artifacts are MP3 audio files and optional JSON subtitles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access to Microsoft Edge's online TTS service; generated audio may be retained locally until cleaned up.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
