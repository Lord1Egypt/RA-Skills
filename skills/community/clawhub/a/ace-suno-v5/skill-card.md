## Description:

Suno V5 Music provides a local Flask web interface and Python client flow for generating AI music with the AceData Suno API, then saving generated audio, cover art, lyrics, and history locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyunnet](https://clawhub.ai/user/xiyunnet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users can use this skill to launch a local browser-based Suno V5 music generation workspace backed by the AceData API. It supports simple prompt-based generation, custom lyrics and style controls, playback, downloads, and local saving of generated assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an AceData API key in browser localStorage.

Mitigation: Use a disposable or low-scope API key and clear browser storage after use.

Risk: The skill starts a local Flask server and includes shutdown/debug patterns.

Mitigation: Run it on localhost only and remove or harden the shutdown and debug behavior before regular use.

Risk: The startup script auto-installs dependencies and the app saves generated content and history to disk.

Mitigation: Run in a virtual environment and review the local output directory and history files after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiyunnet/skills/ace-suno-v5)
- [Publisher Profile](https://clawhub.ai/user/xiyunnet)
- [AceData API Key Sign-Up](https://share.acedata.cloud/r/1uN88BrUTQ)
- [AceData Suno API Endpoint](https://api.acedata.cloud/suno)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell and Python code blocks; runtime output includes MP3 audio, image, lyric text, and JSON history files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AceData API key and runs a local Flask server on port 1688.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence, released 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
