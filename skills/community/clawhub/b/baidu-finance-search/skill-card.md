## Description:

百度财经搜索 skill。基于超哥方法论定制，支持雪球/知乎/东方财富/同花顺等站点的财经舆情搜索，适合短线情绪博弈和事件驱动分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangrichao2020](https://clawhub.ai/user/huangrichao2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial-analysis agents use this skill to query Baidu Qianfan AI Search for Chinese finance sentiment, announcements, policy news, earnings discussion, and sector rotation signals across sites such as Xueqiu, Eastmoney, 10jqka, Zhihu, and Sina Finance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill disables TLS certificate checks while sending the Baidu API key and user queries.

Mitigation: Review before installing and remove the disabled certificate verification before use.

Risk: User prompts may include confidential trading plans, personal data, or sensitive business research sent to the Baidu API.

Mitigation: Avoid submitting confidential or personal data, and use the skill only with data approved for third-party API processing.

Risk: A Baidu API key may be exposed or abused if this version is used on untrusted networks.

Mitigation: Keep the API key low-privilege and rotate it if the skill has already been used in an untrusted environment.

## Reference(s):

- [Baidu Qianfan AI Search web_summary endpoint](https://qianfan.baidubce.com/v2/ai_search/web_summary)
- [ClawHub skill page](https://clawhub.ai/huangrichao2020/skills/baidu-finance-search)
- [ClawHub publisher profile](https://clawhub.ai/user/huangrichao2020)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Console text with Markdown-style sections plus a summarized JSON block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and sends user queries to the Baidu Qianfan web_summary API; AI analysis text is truncated to 3000 characters in the human-readable output and 500 characters in the summarized JSON block.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and _meta.json report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
