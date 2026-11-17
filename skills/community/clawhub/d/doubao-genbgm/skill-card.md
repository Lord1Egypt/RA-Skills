## Description:

Based on the Volcano Engine Doubao Music Generation API, this skill supports instrumental background music generation from text descriptions and vocal song generation from prompts or lyrics with controls for genre, mood, timbre, key, tempo, instruments, and related settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fackee](https://clawhub.ai/user/fackee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to generate instrumental background music, soundtracks, and vocal songs through Volcano Engine's Doubao Music Generation API. It supports prompt-based and lyrics-based workflows with configurable audio format, duration, billing mode, musical style, and local file output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, and task data are sent to Volcano Engine for generation.

Mitigation: Use only data appropriate for that external service and review prompts or lyrics before submission.

Risk: The skill requires VOLC_ACCESS_KEY and VOLC_SECRET_KEY credentials.

Mitigation: Keep credentials out of repositories and shared logs, and load them from a local environment or protected secret store.

Risk: The script installs and imports the requests dependency and writes generated audio to a local output path.

Mitigation: Prefer a virtual environment, consider pinning dependencies, and choose an output path that will not overwrite important files.

## Reference(s):

- [Doubao Music Generation Parameter Quick Reference](artifact/references/params.md)
- [Volcano Engine Key Management](https://console.volcengine.com/iam/keymanage/)
- [Volcano Engine Music Generation API Endpoint](https://open.volcengineapi.com/?Action=XXX&Version=2024-08-12)
- [ClawHub Skill Page](https://clawhub.ai/fackee/skills/doubao-genbgm)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown instructions with bash commands and local audio file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates mp3 or wav audio files after polling the remote task result.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
