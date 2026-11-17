## Description:

批量采集抖音公开视频的互动指标和视频文案，并导出 CSV 供投放复盘与内容分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户和营销分析人员可批量查询公开视频的点赞、评论、收藏、分享和播放量，并导出 CSV，用于投放结案与内容复盘。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default service address uses plaintext HTTP, exposing authentication tokens in transit.

Mitigation: Review before installing; use a trusted HTTPS service address before logging in or sending requests, if available.

Risk: Locally saved credentials and settings may be reused from an older service configuration.

Mitigation: Keep the token configuration private and check whether an existing ~/.xhs-convert token should be reused before running the skill.

Risk: Persisted insecure TLS settings can disable certificate checks.

Mitigation: Avoid enabling insecure TLS except for a trusted test endpoint; review any inherited setting before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cuiyunhai/skills/dy-collect)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [JSON task results and CSV export; agent summaries in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing metrics are empty strings, not zero; CSV uses a BOM for spreadsheet compatibility.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
