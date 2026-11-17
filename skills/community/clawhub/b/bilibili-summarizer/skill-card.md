## Description:

Extracts subtitles from Bilibili, Douyin, YouTube, Xiaohongshu, and local video files, then helps agents produce structured summaries, information-density ratings, danmaku analysis, key-frame screenshots, speaker diarization, and SRT exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangligong0826](https://clawhub.ai/user/zhangligong0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs to process video links or local media from Bilibili, Douyin, YouTube, Xiaohongshu, and local files into transcripts, summaries, credibility notes, information-density scores, optional danmaku analysis, screenshots, and saved subtitle exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted or untrusted URLs can cause unintended network fetches while resolving, downloading, or caching media.

Mitigation: Use trusted URLs and local files, and run with network egress controls that block loopback, private, and metadata-service addresses.

Risk: Downloaded media, generated transcripts, screenshots, and subtitle records may remain in a local cache and contain sensitive content.

Mitigation: Avoid confidential media unless local retention is acceptable, and review or clear the cache after processing sensitive transcripts.

Risk: ASR engines and media tools may download or execute model and dependency code in the runtime environment.

Mitigation: Pin dependencies and ASR models in a controlled environment before serious or commercial use.

Risk: Author and key-person background analysis can be misleading if the agent lacks reliable background information.

Mitigation: Require explicit uncertainty notices for unknown backgrounds and add extra trustworthiness warnings for medical, legal, financial, or other sensitive domains.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangligong0826/skills/bilibili-summarizer)
- [Bilibili video metadata API](https://api.bilibili.com/x/web-interface/view)
- [Bilibili player subtitle API](https://api.bilibili.com/x/player/v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown summaries plus JSON processing results, SRT/TXT subtitle files, and JPG key-frame files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache downloaded audio, generated transcripts, frame images, and subtitle records locally under the skill cache.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
