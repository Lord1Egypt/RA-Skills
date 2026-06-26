## Description: <br>
Trading analysis and education. Technical analysis, chart patterns, risk management, and position sizing for stocks, forex, and crypto. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for general trading education, technical analysis, chart-pattern discussion, risk/reward calculations, position sizing, and trade-planning support. The skill frames outputs as analysis rather than personalized financial advice and does not execute trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may keep trading preferences, strategies, journal notes, or portfolio-adjacent context in local files under ~/trading/. <br>
Mitigation: Review ~/trading/memory.md, ~/trading/journal.md, and ~/trading/progress.md before and after use, and delete sensitive financial notes that should not persist locally. <br>
Risk: Trading analysis can be mistaken for personalized financial advice or guaranteed outcomes. <br>
Mitigation: Use the skill's guardrails: require disclaimer acknowledgement, frame outputs as general analysis, avoid direct buy/sell imperatives, and escalate high-risk situations to qualified professionals. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1477009639zw-blip/beta-trading-analysis) <br>
- [Getting Started](artifact/getting-started.md) <br>
- [Risk Management](artifact/risk.md) <br>
- [Technical Analysis Basics](artifact/technical.md) <br>
- [Platforms and Regulations](artifact/platforms.md) <br>
- [Setup](artifact/setup.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with educational analysis, calculations, tables, and occasional shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally maintain local trading context files under ~/trading/; does not execute trades or access brokerage accounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
