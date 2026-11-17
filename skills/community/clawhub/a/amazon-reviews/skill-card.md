## Description:

Collect Amazon product reviews with the official Gecho Bridge MCP tool, including review text, ratings, dates, and reviewer metadata when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect and summarize review data for a supplied Amazon product URL or ASIN through the Gecho Bridge MCP workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Gecho's third-party MCP bridge and Chrome extension with a logged-in Amazon browser session.

Mitigation: Install only if comfortable with that bridge and extension model, keep the browser session under user control, and resolve login, CAPTCHA, verification, region, or cookie prompts manually.

Risk: Default setup commands use an npm package through npx, which can change if installed without a pinned version.

Mitigation: For stronger reproducibility, pin or review the Gecho Bridge package version before configuring the MCP server.

Risk: Amazon pages may return no data, time out, or block collection behind manual prompts.

Mitigation: Run only one Gecho job per turn, stop on failures, report the exact error, and avoid unofficial scraping or browser automation fallbacks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gecho-ai/skills/amazon-reviews)
- [Gecho Website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw Setup Video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes Setup Video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured review summaries and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the top 3 to 5 useful fields or items; may include review counts and saved file paths when available.]

## Skill Version(s):

1.1.38 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
