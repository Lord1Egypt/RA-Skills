## Description:

Transcribes local audio or video files and public audio URLs with Volcengine Doubao ASR Flash, returning transcripts with optional JSON utterance timestamps or SRT subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackcorvu](https://clawhub.ai/user/blackcorvu)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and agents use this skill to turn recordings, meetings, podcasts, interviews, videos, voice messages, or public audio URLs into text transcripts, meeting notes, JSON timestamp data, or SRT subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio recordings or public audio URLs are sent to Volcengine/ByteDance for transcription.

Mitigation: Use the skill only for recordings that are approved for that external processing path, and avoid submitting sensitive content unless the account, region, and data handling terms are acceptable.

Risk: The API key can be exposed if passed on the command line or stored with permissive file permissions.

Mitigation: Prefer an environment secret or a config file with restrictive permissions, and avoid passing the API key directly in shell history.

Risk: The implementation copies the API key into the request body's user.uid field when no uid is supplied.

Mitigation: Prefer a patched version or pass a non-secret uid so the API key is not duplicated outside the authentication header.

Risk: Using the service can incur usage-based transcription charges.

Mitigation: Confirm billing expectations before processing recordings, especially long files or repeated batch use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blackcorvu/skills/doubao-asr-flash)
- [Volcengine Doubao ASR Flash Documentation](https://www.volcengine.com/docs/6561/1631584)
- [Volcengine Speech Console](https://console.volcengine.com/speech/app)
- [artifact/README.md](artifact/README.md)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, files]

**Output Format:** [Plain text transcript, JSON response with utterance timestamps, SRT subtitle file, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write transcript or subtitle files when the user provides an output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
