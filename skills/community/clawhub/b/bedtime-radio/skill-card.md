## Description:

Generate a complete bedtime story audio program from a keyword, with intro, narration, character voices, and a sleepy outro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use this skill to create age-appropriate bedtime story programs for children, including story text, voice planning, SenseAudio synthesis commands, and playback order guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated story text is sent to SenseAudio using the user's API key.

Mitigation: Avoid including children's full names, addresses, school details, or other sensitive personal information in prompts.

Risk: The sample shell command builds JSON around user-generated text.

Mitigation: Harden the script with proper JSON encoding before operational use.

## Reference(s):

- [Bedtime Radio on ClawHub](https://clawhub.ai/scikkk/skills/bedtime-radio)
- [SenseAudio](https://senseaudio.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, audio files, guidance]

**Output Format:** [Markdown with story text, segment tables, Bash synthesis commands, generated MP3 filenames, and assembly instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and local curl, jq, and xxd for audio synthesis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
