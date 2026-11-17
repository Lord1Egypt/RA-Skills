## Description:

Routes Amazon product-search requests through the official Gecho Bridge MCP workflow and returns product listings, prices, ratings, and links for the requested marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Amazon by keyword through a configured Gecho Bridge session, summarize useful product fields, and optionally save structured research results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a logged-in Amazon browser session, Gecho Bridge, and the Gecho Chrome extension, so it can access Amazon pages available in that session.

Mitigation: Use the skill only when comfortable with Gecho accessing the active Amazon session, manually resolve login or verification prompts in Chrome, and choose any save directory deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/amazon-search-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge GitHub repository](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Text]

**Output Format:** [Markdown with inline shell commands and concise product-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes only the most useful product fields or the top 3 to 5 results; avoids pasting full raw JSON into chat.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
