## Description:

通过官方 Gecho Bridge MCP 搜索 Amazon 商品、获取已知商品详情并采集商品评论。适用于市场发现、商品库调研、商品比较、评论分析和 ASIN 级研究。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, market researchers, and developers use this skill to discover Amazon products, inspect known ASINs or product URLs, and summarize review themes through configured Gecho MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can read Amazon pages available in the active browser session through Gecho Bridge and the Gecho Chrome extension.

Mitigation: Use it only with the intended Gecho and Amazon accounts, and resolve login, CAPTCHA, region, or consent pages manually before invoking tools.

Risk: Research results may be saved to a local directory selected during use.

Mitigation: Choose the save directory intentionally and review generated JSON files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/amazon-zh-cn)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Bridge GitHub repository](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [Gecho website](https://gecho.ai/)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, File paths]

**Output Format:** [Markdown summaries with inline shell commands and optional JSON result file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured Gecho MCP tools serially; saved raw results may be written to a user-selected directory.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
