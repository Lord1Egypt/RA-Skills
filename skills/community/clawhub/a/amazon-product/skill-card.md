## Description:

Retrieve complete Amazon product details with the official Gecho Bridge MCP tool, including title, price, variants, specifications, description, ratings, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve structured details for a known Amazon product URL or ASIN through the Gecho Bridge MCP workflow. It is intended for focused product research and summarization, with setup guidance when the required MCP server or browser extension is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a logged-in Chrome and Amazon browser session connected through the Gecho Chrome extension.

Mitigation: Use it only with accounts and sessions appropriate for this workflow, and resolve login, CAPTCHA, region, cookie, or verification prompts manually in Chrome.

Risk: The setup command uses npx with an @latest package reference.

Mitigation: Prefer a pinned or bundled Gecho Bridge version when possible, and review the MCP package publisher before configuring the command.

Risk: The skill may return incomplete or no product data when Amazon blocks access, times out, or presents account prompts.

Mitigation: Report the exact failure, avoid retrying in the same turn, and ask the user to verify the product URL or browser state manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/amazon-product)
- [Gecho website](https://gecho.ai/)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise summaries, setup commands, and saved-path references when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the top 3 to 5 useful fields and avoids pasting full raw JSON.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
