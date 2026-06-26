## Description: <br>
Fast, affordable automatic speech-to-text transcription supporting 100 languages, speaker diarization, word timestamps, and customizable output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilyakam](https://clawhub.ai/user/ilyakam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents, developers, and media-processing workflows use this skill to submit audio files or media URLs to Speech is Cheap for transcription, status checks, and optional formats such as JSON, SRT, VTT, and WebVTT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio, media URLs, transcript data, and job metadata are sent to Speech is Cheap for processing. <br>
Mitigation: Use this skill only for data that may be processed by Speech is Cheap, and enable --private for sensitive recordings when using the transcription command. <br>
Risk: The skill depends on SIC_API_KEY for authenticated API calls. <br>
Mitigation: Keep SIC_API_KEY secret, store it only in trusted environment configuration, and avoid sharing logs or command output that might expose credentials. <br>
Risk: Webhook callbacks can send job completion data to a configured URL. <br>
Mitigation: Configure webhook URLs only for endpoints you control and trust. <br>
Risk: API usage may affect the user's Speech is Cheap account. <br>
Mitigation: Confirm account limits and expected usage before running high-volume transcription jobs. <br>


## Reference(s): <br>
- [Speech is Cheap](https://speechischeap.com) <br>
- [Speech is Cheap API Documentation](https://docs.speechischeap.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/ilyakam/asr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the skill command returns JSON by default and can request SRT, VTT, or WebVTT transcript formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIC_API_KEY; supports URL transcription, local file upload, job status checks, speaker diarization, word timestamps, audio labels, streaming, privacy mode, language selection, confidence threshold, webhook callback, and segment duration.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence.release.version, manifest.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
