## Description:

通过官方 Gecho Bridge MCP 采集 Amazon 商品评论，包括评论文本、评分、日期和可用的评论者信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, ecommerce researchers, and agent operators use this skill to collect Amazon product reviews through the official Gecho Bridge MCP workflow when they provide a product URL or ASIN. It helps summarize useful review fields and report saved result paths without pasting full raw JSON into the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Gecho Bridge and a Chrome extension connected to the user's logged-in Amazon browser session.

Mitigation: Use it only for review collection the user intentionally requests, and confirm the user is comfortable trusting the Gecho extension and MCP package before running setup commands.

Risk: Amazon may present login, CAPTCHA, regional, cookie, or blocking pages that prevent reliable collection.

Mitigation: Ask the user to resolve browser prompts manually in Chrome, then retry only when the Gecho extension and Amazon session are ready.

Risk: Running setup commands adds the Gecho Bridge MCP service to OpenClaw or Hermes.

Mitigation: Present configuration commands only when the tool is missing or setup is requested, and avoid changing MCP settings on the user's behalf.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gecho-ai/skills/amazon-reviews-zh-cn)
- [Gecho Website](https://gecho.ai/)
- [Gecho Bridge GitHub](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw Configuration Video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes Configuration Video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional shell command blocks and summarized structured review data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs summarize the most useful fields or the first 3 to 5 review records and may include a saved result path; full raw JSON is not pasted into the conversation.]

## Skill Version(s):

1.1.38 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
