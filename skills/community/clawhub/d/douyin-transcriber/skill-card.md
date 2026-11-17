## Description:

Transcribes speech from audio or video files, automatically extracting audio and converting it to text using Docker Whisper ASR for Douyin/TikTok media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[don068589](https://clawhub.ai/user/don068589)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up local transcription workflows for Douyin/TikTok or other audio/video media. It guides extraction, transcription, language selection, model choice, and result parsing with Docker Whisper ASR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party Docker Whisper ASR service.

Mitigation: Use a pinned image digest and verify the container source before processing recordings.

Risk: The Docker port mapping may expose the local transcription endpoint more broadly than intended.

Mitigation: Bind the service to 127.0.0.1 and apply network and resource controls before use.

Risk: Sensitive recordings could be processed by a container whose logging behavior has not been verified.

Mitigation: Avoid sensitive recordings until container behavior, logging, and retention are reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces transcription workflow instructions; actual transcription output depends on the local Whisper ASR container and selected model.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
