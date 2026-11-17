## Description:

Uploads local audio files to AIOZ Stream through a three-step API workflow and returns HLS or DASH streaming playback links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, media teams, and agents use this skill to upload authorized audio files to AIOZ Stream, choose default or custom encoding settings, complete multipart upload steps, and retrieve HLS or DASH playback links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan says the skill requests broad local file and command access without tight limits on files, credentials, and callback URLs.

Mitigation: Review before installing, narrow tool permissions where possible, provide only approved file paths and callback URLs, and avoid exposing AIOZ secret keys in logs or chat output.

Risk: The skill can upload local audio to an external streaming service.

Mitigation: Use it only for audio files the user intentionally wants to upload and avoid private or copyrighted media unless authorized.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thcjp/skills/audio-stream-upload-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns upload status, execution log details, and HLS or DASH playback links when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
