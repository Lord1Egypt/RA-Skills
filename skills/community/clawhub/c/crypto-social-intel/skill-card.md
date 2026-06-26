## Description: <br>
Crypto Social Intel helps agents retrieve crypto social trends, sentiment scores, KOL proxy signals, mention-surge alerts, and the Crypto Fear & Greed Index through remote MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackxun520](https://clawhub.ai/user/jackxun520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for crypto market-research workflows such as checking social trend rankings, token sentiment, mention surges, KOL proxy movement, and the Fear & Greed Index. Outputs should be used as informational social-intelligence signals, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market-research prompts are sent to the Antalpha MCP service. <br>
Mitigation: Avoid sharing private portfolio details, wallet secrets, API keys, or other sensitive financial information. <br>
Risk: Outputs may be mistaken for investment advice. <br>
Mitigation: Treat results as informational social-intelligence signals and pair them with independent review before acting. <br>
Risk: Santiment free-tier social data may lag by about 35 days. <br>
Mitigation: Disclose the lag when Santiment-backed tools are used and avoid relying on those results for real-time decisions. <br>
Risk: The KOL signal is a social-dominance proxy rather than direct Twitter KOL data. <br>
Mitigation: Label KOL outputs as proxy signals and avoid presenting them as direct influencer activity. <br>


## Reference(s): <br>
- [Crypto Social Intel ClawHub listing](https://clawhub.ai/jackxun520/crypto-social-intel) <br>
- [jackxun520 ClawHub publisher profile](https://clawhub.ai/user/jackxun520) <br>
- [Antalpha MCP endpoint](https://mcp-skills.ai.antalpha.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with JSON tool outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only remote MCP lookups; Santiment-backed social data may lag about 35 days on the free tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
