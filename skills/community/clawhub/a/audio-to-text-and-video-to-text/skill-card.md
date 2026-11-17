## Description:

Transcribes audio and video files into text using OpenAI's Whisper API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahqazi-dev](https://clawhub.ai/user/ahqazi-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to convert uploaded or local media files into transcripts, captions, subtitles, JSON transcript data, or follow-on summaries and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media files are sent to OpenAI for transcription.

Mitigation: Use the skill only for media that the user is comfortable sending to OpenAI, and confirm any organizational data-handling requirements before transcription.

Risk: The skill asks for raw OpenAI API keys in chat or command-line arguments.

Mitigation: Configure the API key through a secure environment or secret mechanism and avoid pasting secrets into chat or shell history.

Risk: The skill can modify the Python environment at runtime with unpinned package installs.

Mitigation: Run it in a managed environment with preinstalled, pinned dependencies and ffmpeg already available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahqazi-dev/skills/audio-to-text-and-video-to-text)
- [OpenAI API keys](https://platform.openai.com/api-keys)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text, SRT, VTT, or JSON transcript files, plus setup and post-processing guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps, segment metadata, captions, summaries, action items, speaker labels, or translations when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
