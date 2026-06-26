## Description: <br>
Transcribes, extracts subtitles from, and summarizes Bilibili videos from standard URLs, BV IDs, or b23.tv short links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Markusbetter](https://clawhub.ai/user/Markusbetter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill when a Bilibili video needs a transcript, official subtitle extraction, or a concise content summary. It prefers official subtitles and falls back to downloading audio and using SiliconFlow ASR when subtitles are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bilibili media and transcripts may be downloaded or written locally. <br>
Mitigation: Use a private output directory and delete audio, transcript, and probe files after sensitive jobs. <br>
Risk: When official subtitles are unavailable, audio may be sent to SiliconFlow for ASR. <br>
Mitigation: Run only when the user accepts sending the media to SiliconFlow, and avoid using sensitive videos with the fallback transcription path. <br>
Risk: The URL handling accepts URLs beyond a strict Bilibili-only allowlist. <br>
Mitigation: Use the skill only with Bilibili video URLs, BV IDs, or b23.tv short links unless URL validation is tightened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Markusbetter/bilibili-video-transcribe-summary) <br>
- [SiliconFlow API key page](https://cloud.siliconflow.cn/me/account/ak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response with optional stdout transcript and local JSON/text output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write probe_result.json, audio.mp3, transcription_result.json, transcript.txt, and .skill-ready.json in the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
