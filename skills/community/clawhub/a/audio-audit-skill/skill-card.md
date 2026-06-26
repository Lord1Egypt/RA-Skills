## Description: <br>
音频/视频内容质检与审核工具 — 自动识别语音内容，检测敏感词、违规信息，生成结构化审核报告 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QWERTY0205](https://clawhub.ai/user/QWERTY0205) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operations teams, and reviewers use this skill to transcribe audio or video, scan for sensitive or prohibited content, and produce structured audit reports for manual review. It supports individual files and batch directories for scenarios such as short-video moderation, podcast review, meeting audits, and educational content checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose the SenseAudio API key if an agent follows the artifact's plain environment-variable echo check. <br>
Mitigation: Use a redacted presence check for `SENSEAUDIO_API_KEY` and never print, log, or paste the secret value. <br>
Risk: Audio and video content may contain private or regulated information and is uploaded to SenseAudio for transcription. <br>
Mitigation: Process only recordings the user is authorized to upload, obtain required consent, and avoid broad batch directories that may include unrelated private media. <br>
Risk: Generated transcripts and audit reports may preserve sensitive speech, matched keywords, timestamps, and speaker information. <br>
Mitigation: Store outputs in a controlled location, restrict access, and delete or redact transcripts and reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QWERTY0205/audio-audit-skill) <br>
- [SenseAudio website](https://senseaudio.cn) <br>
- [SenseAudio transcription API endpoint](https://api.senseaudio.cn/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, text summaries, and transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include risk levels, matched keywords, timestamps, speaker labels, sentiment markers, audit summaries, and full transcripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
