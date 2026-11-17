## Description:

视频全流程自动化：下载、截封面、OSS上传、蚁小二多平台分发、飞书多维表格记录；发一个视频链接就能跑完全程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operations teams, and developers use this skill to turn a video link or local video into processed media, an OSS upload, optional Yixiaoer multi-platform publishing, and a Feishu Bitable record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload media and metadata to external OSS, Yixiaoer, and Feishu destinations.

Mitigation: Use trusted credentials and controlled destinations; run with --no-oss, --no-feishu, or --draft until storage, publishing, and record targets are confirmed.

Risk: Publishing depends on an external Yixiaoer script path outside this artifact.

Mitigation: Review or remove the Yixiaoer dependency before enabling publishing with YIXIAOER_TOKEN.

Risk: Feishu recording uses a fixed Bitable app token and table ID from the artifact.

Mitigation: Confirm the destination is intended before use, or run with --no-feishu.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/bee-video-workflow)
- [Publisher profile](https://clawhub.ai/user/jerryxn)
- [Yixiaoer API endpoint](https://www.yixiaoer.cn/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with CLI commands, runtime logs, generated media files, and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and ffprobe. OSS upload requires OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, OSS_BUCKET_NAME, and OSS_ENDPOINT; publishing requires YIXIAOER_TOKEN. Feishu recording targets the configured Bitable destination unless skipped.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
