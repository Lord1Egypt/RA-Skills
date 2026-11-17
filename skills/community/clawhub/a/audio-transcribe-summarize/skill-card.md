## Description:

Transcribes audio and video files to text and generates structured summaries using the SenseAudio ASR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q1lin570](https://clawhub.ai/user/q1lin570)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to transcribe recordings, meetings, lectures, podcasts, interviews, or video files, then turn the transcript into structured notes, summaries, action items, and quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings are uploaded to SenseAudio for transcription.

Mitigation: Use only recordings the user is permitted to send to SenseAudio, and avoid confidential, regulated, or third-party recordings unless the service's data handling is acceptable.

Risk: Transcript text and raw JSON results are stored locally and a preview is printed to stdout.

Mitigation: Protect the generated .txt and .json files, choose an appropriate output location, and avoid running where stdout is centrally logged for sensitive content.

## Reference(s):

- [SenseASR API Reference](api-reference.md)
- [SenseAudio API Key Setup](https://senseaudio.cn/platform/api-key)
- [SenseASR Transcription Endpoint](https://api.senseaudio.cn/v1/audio/transcriptions)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples, transcript text files, and raw JSON transcription results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a .txt transcript and a companion .json API response file next to the input or configured output path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
