## Description:

Uses the AI Artist API to list cloned voices, create voice clones from audio, and synthesize speech with a selected voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate AI Artist voice-cloning and text-to-speech workflows, including listing available voices, creating a voice from authorized audio, and generating speech output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real-looking API key appears in the artifact documentation.

Mitigation: Use only a key from your own AI Artist account, treat the exposed key as compromised, and rotate or revoke any matching credential before use.

Risk: The skill can clone or synthesize voices without built-in consent checks.

Mitigation: Use it only with explicit authorization from the voice owner and only for lawful, non-deceptive purposes.

Risk: Creating a voice can upload local or URL-based audio to the external AI Artist service.

Mitigation: Upload only audio that is approved for that service and does not contain sensitive or unauthorized speech.

## Reference(s):

- [AI Artist Voice Clone API documentation](references/api.md)
- [ClawHub skill page](https://clawhub.ai/kukuoai/skills/deepsop-syhth-clone)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with shell commands; successful runs may return audio URLs or downloaded MP3 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AI_ARTIST_TOKEN and network access to the AI Artist API; creating a voice may upload user-provided audio.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
