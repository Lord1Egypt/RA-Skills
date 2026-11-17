## Description:

Douyin Video Transcribe helps agents extract audio from Douyin/TikTok China video links or local files, transcribe speech with Whisper, and produce structured summaries and notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[don068589](https://clawhub.ai/user/don068589)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content analysts use this skill to process Douyin/TikTok China links, local videos, or image notes into transcripts, summaries, key points, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start a persistent Docker Whisper service from an unpinned third-party image and expose it on the host network.

Mitigation: Pin the Docker image to a reviewed digest, bind the ASR service to 127.0.0.1, restrict network exposure, and stop or remove the container when transcription is complete.

Risk: The skill downloads external media and processes local audio or video files, which can expose sensitive or unauthorized content.

Mitigation: Use it only with media the user is authorized to process, keep temporary files in a controlled location, and review generated transcripts before sharing them.

Risk: Configured cloud transcription fallbacks may send audio content to external ASR providers.

Mitigation: Require explicit user approval before cloud transcription, confirm which provider and account will be used, and prefer local transcription for sensitive media.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown transcripts and summaries with inline shell commands and JSON-like transcription results from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transcript text, detected language, timestamped segments, summaries, key points, tags, troubleshooting guidance, and saved Markdown files.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
