## Description:

Generates multi-character short drama scripts from a topic, synthesizes each line with SenseAudio TTS, and concatenates the audio into a WAV file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwerty0205](https://clawhub.ai/user/qwerty0205)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a drama topic into a short multi-role script, select voices, synthesize speech through SenseAudio TTS, and return the generated audio file path with the script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructions and command-line option can expose the SenseAudio API key in terminal output or shell history.

Mitigation: Do not print the API key or pass it with --senseaudio-api-key; use a protected environment variable or secret manager.

Risk: Generated dialogue is sent to SenseAudio for cloud TTS processing and the script is saved locally as JSON.

Mitigation: Avoid sensitive or proprietary story content unless cloud TTS processing and local JSON retention are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qwerty0205/skills/generate-drama)
- [SenseAudio](https://senseaudio.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown summary with JSON script content, shell command guidance, generated file paths, and WAV audio plus JSON script files from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SenseAudio API key and sends generated dialogue text to the SenseAudio TTS service.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter says 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
