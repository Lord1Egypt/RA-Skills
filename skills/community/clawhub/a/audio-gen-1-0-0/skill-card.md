## Description:

Generate audiobook, podcast, or educational audio scripts from a user topic and convert approved scripts into MP3 audio with ElevenLabs text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matttgx](https://clawhub.ai/user/matttgx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to draft narrated content such as audiobooks, podcasts, and educational lessons, revise the script, and generate an MP3 after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated script text may be passed through command examples in a way that could allow crafted content to run unintended shell commands.

Mitigation: Review before installing and run only in an environment that passes script text and output paths to the TTS tool without shell parsing.

Risk: Script text is sent to external providers and generated audio can incur API costs.

Mitigation: Avoid sensitive content and confirm provider usage, credentials, and cost expectations before generating audio.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matttgx/skills/audio-gen-1-0-0)
- [Publisher profile](https://clawhub.ai/user/matttgx)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown and plain text script output, with a MEDIA path to an MP3 file after audio generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ANTHROPIC_API_KEY and ELEVENLABS_API_KEY; requests are intended for single-narrator audio up to about 30 minutes per file.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
