## Description: <br>
Crypto News Ranked by AI helps agents fetch NS3 crypto news feeds, ranked stories, daily briefings, and breaking headlines with structured market context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assembleai-crypto](https://clawhub.ai/user/assembleai-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, trading workflow builders, and agent operators use this skill to retrieve crypto market news, coin-specific updates, top story rankings, daily briefings, and breaking headlines from NS3 feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill sends requested coin symbols, language choices, and feed filters to NS3. <br>
Mitigation: Use it only for crypto news and market briefings when that external API contact is acceptable. <br>
Risk: Users may include sensitive wallet, account, balance, or private portfolio details in requests. <br>
Mitigation: Avoid sharing wallet addresses, account details, balances, or private portfolio data when asking the agent to use the skill. <br>
Risk: Crypto news and market context can be mistaken for trading, investment, tax, or financial advice. <br>
Mitigation: Present outputs as informational news summaries and preserve the artifact's disclaimer that users are responsible for their own decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/assembleai-crypto/crypto-news-ns3) <br>
- [NS3 homepage](https://ns3.ai) <br>
- [NS3 RSS documentation](https://docs.ns3.ai/ns3-rss) <br>
- [NS3 API documentation](https://docs.ns3.ai/ns3-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with RSS-derived text and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NS3 RSS endpoints; News RSS responses can be large, so the artifact recommends limit and filter parameters.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
