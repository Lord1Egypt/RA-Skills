## Description:

从用户提供的抖音公开视频链接、分享文案或 aweme_id 中提取视频信息、简介与口播逐字稿，并整理成可复制文案和摘要；也可通过已有 job_id 查询任务状态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和自媒体运营者可提交抖音公开视频链接、分享文案或 aweme_id，获取视频信息、简介和口播逐字稿，并整理成可复制文案与摘要；也可继续查询已有任务。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated use of an unpinned latest CLI release creates a supply-chain risk, and partial scanner coverage leaves the evidence incomplete.

Mitigation: Postpone installation until the CLI version is fixed and reviewed. Resolve the local references the scan could not analyze, and do not treat another scanner's clean result as proof of safety.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/douyin-copy-extract-v2)
- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown containing video details, source description, transcript, copy-ready text, summary, or task status when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fields returned by the task; missing details are not invented.]

## Skill Version(s):

0.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
