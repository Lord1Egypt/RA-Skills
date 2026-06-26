## Description: <br>
Fetch real-time AI news briefings from the AI News Oracle API (Hacker News, TechCrunch, The Verge). Uses a10m.work registry for discovery and Paymaster for gasless transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swimmingkiim](https://clawhub.ai/user/swimmingkiim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to fetch concise AI news briefings from the AI News Oracle API without browsing multiple news sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to an external API and optional payment flow. <br>
Mitigation: Confirm trust in the API provider before installation, use the free tier for basic briefings, and only configure wallet or payment headers when premium access is intentional. <br>
Risk: AI news briefings may be incomplete, stale, or affected by upstream source availability. <br>
Mitigation: Review included timestamps and source links before relying on a briefing for business decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/swimmingkiim/ai-news-oracle) <br>
- [Live API](https://api.ai-news.swimmingkiim.com) <br>
- [a10m.work registry project](https://a10m.work/project/3) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Text briefing with timestamps and source links; the source skill also describes structured briefing JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No tool parameters; optional premium usage can require a Base Wallet payment header.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
