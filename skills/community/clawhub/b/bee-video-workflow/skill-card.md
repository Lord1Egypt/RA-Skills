## Description: <br>
视频全流程自动化：下载 → 截封面 → OSS上传 → 蚁小二多平台分发 → 飞书多维表格记录。发一个视频链接就能跑完全程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and creators use this skill to automate video ingestion, cover extraction, cloud upload, optional multi-platform publishing, and Feishu tracking from a video URL or local file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can move videos to cloud storage, publishing services, and Feishu destinations with weak consent controls. <br>
Mitigation: Verify OSS, Yixiaoer, and Feishu destinations before use; prefer --no-oss, --no-feishu, or --draft until the workflow is confirmed. <br>
Risk: The workflow may use a local Douyin cookies file and an external Yixiaoer publishing script when present. <br>
Mitigation: Inspect or remove local Douyin cookies and review the external publishing script before enabling publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/bee-video-workflow) <br>
- [Yixiaoer API endpoint](https://www.yixiaoer.cn/api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [CLI output and JSON workflow result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, OSS URLs, Yixiaoer task status, and Feishu record fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
