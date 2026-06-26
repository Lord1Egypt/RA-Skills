## Description: <br>
Transcribes recorded audio files to speaker-labeled text, JSON, or SRT subtitles using ByteDance Volcengine Doubao Seed-ASR 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahnxu](https://clawhub.ai/user/vahnxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to transcribe recorded meetings, voice memos, and other audio files through Doubao ASR, including speaker diarization and subtitle export when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio content is processed by Volcengine/Doubao, and local files are uploaded to the configured TOS bucket. <br>
Mitigation: Use a dedicated TOS bucket, least-privilege credentials, and a retention or deletion policy for sensitive recordings. <br>
Risk: Misconfigured TOS permissions can cause upload failures or broaden access to uploaded audio. <br>
Mitigation: Use the documented bucket policy approach instead of broad IAM permissions, and verify the bucket policy before processing sensitive files. <br>
Risk: Incorrect TOS region selection can make uploads very slow for servers outside mainland China. <br>
Mitigation: Choose a TOS region close to the runtime environment, such as cn-hongkong or ap-southeast-1 for overseas servers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vahnxu/doubao-asr) <br>
- [Volcengine Doubao audio file recognition docs](https://www.volcengine.com/docs/6561/1354868) <br>
- [Volcengine Speech console](https://console.volcengine.com/speech/new/) <br>
- [Volcengine IAM user management](https://console.volcengine.com/iam/usermanage) <br>
- [Volcengine TOS console](https://console.volcengine.com/tos) <br>
- [Skill guide insights](references/skill-guide-insights.md) <br>
- [Trigger tests](references/trigger-tests.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcripts, JSON API results, SRT subtitles, and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include speaker labels; off-peak mode can return a request ID for later query.] <br>

## Skill Version(s): <br>
0.19.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
