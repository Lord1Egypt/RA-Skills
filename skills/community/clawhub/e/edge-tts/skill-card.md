## Description:

Edge TTS converts text to speech through node-edge-tts with configurable voices, languages, rate, pitch, output format, and subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[i3130002](https://clawhub.ai/user/i3130002)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to turn requested text into spoken audio, including voice notes, accessible reading, summaries, and multilingual speech output. It also supports direct script usage for configuring voices, prosody, subtitles, proxy settings, and output paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech synthesis is sent to Microsoft's online TTS service.

Mitigation: Avoid using the skill with sensitive, private, or regulated text unless that external service use is acceptable.

Risk: Helper scripts can write audio, subtitle, or configuration files to caller-specified paths.

Mitigation: Use a dedicated output directory and review custom --output, --config-path, and --reset targets before running commands.

Risk: The package relies on npm dependencies and example npx execution.

Mitigation: Install reviewed dependency versions and avoid unpinned npx usage in production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/i3130002/skills/edge-tts)
- [node-edge-tts Reference](references/node_edge_tts_guide.md)
- [Voice Testing](https://tts.travisvn.com/)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [Audio files and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce MP3 audio, optional JSON subtitle files, MEDIA paths, and persisted TTS configuration.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill-info.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
