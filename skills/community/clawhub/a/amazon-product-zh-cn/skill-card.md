## Description:

通过官方 Gecho Bridge MCP 获取完整的 Amazon 商品详情，包括标题、价格、变体、规格、描述、评分和链接。用户提供 Amazon 商品 URL 或 ASIN 时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, ecommerce researchers, and agents use this skill to fetch and summarize structured Amazon product details from a provided product URL or ASIN through the Gecho Bridge MCP workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Gecho Bridge, a Gecho Chrome extension, and logged-in Gecho and Amazon browser sessions.

Mitigation: Install and configure the required components only after reviewing the Gecho package and extension provenance, and use the skill only with browser pages you are comfortable exposing to that workflow.

Risk: Amazon login, CAPTCHA, region, cookie, or other blocking pages can prevent complete or accurate product capture.

Mitigation: Resolve browser prompts manually in Chrome before running the workflow, and stop when the tool reports an error, timeout, or empty result.

Risk: Returned product details may be incomplete or stale because they depend on the visible browser session and marketplace state.

Mitigation: Review summarized fields and saved outputs before using them for purchasing, research, or downstream decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/amazon-product-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge repository](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with concise summaries, setup commands, links, and saved-result paths when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs summarize the most useful 3 to 5 fields and avoid pasting complete raw JSON.]

## Skill Version(s):

1.1.38 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
