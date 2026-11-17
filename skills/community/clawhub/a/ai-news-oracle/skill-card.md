## Description:

Fetch real-time AI news briefings from the AI News Oracle API (Hacker News, TechCrunch, The Verge). Uses a10m.work registry for discovery and Paymaster for gasless transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swimmingkiim](https://clawhub.ai/user/swimmingkiim)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to fetch current AI news briefings from Hacker News, TechCrunch, and The Verge without doing their own web browsing. The skill is intended for agents that need concise news summaries with timestamps and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command references a GitHub repository without pinning a commit or reviewed release.

Mitigation: Install from a pinned commit or reviewed release, and review the artifact before deployment.

Risk: The skill interacts with a third-party API and optional payment flow.

Mitigation: Review service trust, data handling, and payment requirements before enabling the skill in production agents.

## Reference(s):

- [AI News Oracle API](https://api.ai-news.swimmingkiim.com)
- [a10m.work Project #3](https://a10m.work/project/3)
- [a10m.work Registry](https://a10m.work)
- [ClawHub Skill Page](https://clawhub.ai/swimmingkiim/skills/ai-news-oracle)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Structured briefing JSON with concise human-readable summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamps and source links; no user-supplied parameters are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
