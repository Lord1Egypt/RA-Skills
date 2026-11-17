## Description:

粘贴抖音视频链接，用抖评岛（ExportDou）导出评论和回复，保存为 CSV 或 Excel，也可先预览少量评论，分析用户反馈、产品问题和选题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenny-shaw](https://clawhub.ai/user/kenny-shaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to export comments and replies from publicly accessible Douyin videos through ExportDou for download, preview, or feedback analysis. It is suitable when the user has an ExportDou account and available credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends public Douyin links or share text to the third-party ExportDou API.

Mitigation: Use it only when the user is comfortable with ExportDou processing those public links or share text.

Risk: The ExportDou CLI may save service credentials locally or use an API key from the environment.

Mitigation: Do not paste API keys into chat; provide keys only through secure environment variables and avoid printing credentials.

Risk: Exports can consume paid credits or require paid features for replies and Excel output.

Mitigation: Confirm requested row counts, reply export, Excel format, and credit availability before creating or resuming export tasks.

## Reference(s):

- [抖评岛官网](https://exportdou.cn)
- [CLI 使用说明](https://exportdou.cn/developers#agent)
- [API 文档](https://exportdou.cn/developers)
- [套餐和积分](https://exportdou.cn/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files, Analysis]

**Output Format:** [Markdown with inline bash commands and local CSV or Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preview structured JSON samples and download verified CSV or XLSX exports from ExportDou tasks.]

## Skill Version(s):

1.0.3 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
