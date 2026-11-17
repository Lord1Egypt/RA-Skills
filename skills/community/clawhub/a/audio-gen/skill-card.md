## Description:

Generates audiobooks, podcasts, and educational audio content by drafting a script and converting it to an MP3 with ElevenLabs text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udiedrichsen](https://clawhub.ai/user/udiedrichsen)

### License/Terms of Use:


## Use Case:

Users and developers use this skill to create short-form narrated content such as audiobook chapters, podcast episodes, and educational audio lessons from a requested topic, length, and style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated script text or topic-derived filenames may be placed into a shell command.

Mitigation: Use only trusted prompts, or change execution to pass arguments without a shell and sanitize all generated filenames before audio generation.

Risk: Audio files may be written to a shared temporary path.

Mitigation: Store generated audio in a private temporary directory with restrictive permissions and remove files when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/udiedrichsen/skills/audio-gen)
- [Project homepage](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown response with generated script text, optional shell command invocation, and a MEDIA path for an MP3 audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ANTHROPIC_API_KEY and ELEVENLABS_API_KEY; the artifact describes MP3 output saved under /tmp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
