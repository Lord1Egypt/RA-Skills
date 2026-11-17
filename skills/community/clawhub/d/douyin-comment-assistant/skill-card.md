## Description:

抖音评论获取助手 retrieves public Douyin search results, trending topics, creator posts, and video or image-post comments as structured JSON for content research and social media analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to collect public Douyin data for short-video topic research, competitor monitoring, sentiment review, trend tracking, and follow-on reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a Review verdict because the tool sends GUAIKEI_API_TOKEN in URL parameters.

Mitigation: Install only if sending the token to guaikei.com is acceptable, and prefer a release that transmits tokens in authorization headers.

Risk: The security guidance says generated logs may contain usernames, IDs, comment text, and research targets.

Mitigation: Protect or delete generated logs after use, and prefer explicit save/no-save or output-path controls when available.

Risk: The tool sends Douyin keywords, URLs, identifiers, and the API token to a third-party API service.

Mitigation: Confirm the intended data-sharing and authorization scope before use, especially for commercial or customer-facing analysis.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/why20261/douyin-comment-assistant)
- [Server-resolved source commit](https://github.com/why20261/douyin-comment-assistant/commit/a1b26a241a1f2b8ab2d5232c0635912f01419519)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-comment-assistant)
- [抖音数据获取官网](https://www.guaikei.com)
- [完整选项说明](references/options.md)
- [更新日志](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful CLI runs write JSON to stdout and may save local logs.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact metadata and changelog report 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
