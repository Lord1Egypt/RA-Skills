## Description:

Generates a talking digital-human video from a person image and either user-provided audio or text-derived speech, then returns a public video URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[focus-aim](https://clawhub.ai/user/focus-aim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create digital-human talking videos from a local person image plus audio, text-to-speech, or cloned voice input. It is suited for workflows that need a generated video URL after submitting media to the Focus AIM AEP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user media and generated speech data to AEP/TTS services and receives a public video URL.

Mitigation: Use it only for media approved for those services and for results that may be accessible through a public URL.

Risk: The aim-secret-key is required for service access.

Mitigation: Store the key through a protected local secret mechanism or carefully protected .env file, and do not paste it into chat.

Risk: Changing AEP_BASE_URL can redirect media and credentials to another endpoint.

Mitigation: Keep AEP_BASE_URL pointed at the trusted Focus AIM endpoint unless the replacement endpoint has been reviewed.

Risk: Task history can retain saved video URLs and later runs may re-contact them.

Mitigation: Periodically delete stale .task-history.jsonl entries when retained URLs are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/focus-aim/skills/aim-digital-human-video)
- [AIM skills registration](https://tools.mentarc.cn/aim-skills/)
- [FFmpeg ffprobe documentation](https://ffmpeg.org/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON script output containing a public video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .env and .task-history.jsonl files during use; generated videos are returned as public URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
