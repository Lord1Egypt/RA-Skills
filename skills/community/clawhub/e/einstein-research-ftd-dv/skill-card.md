## Description: <br>
Detects Follow-Through Day signals for market bottom confirmation using William O'Neil's methodology, with dual-index tracking and post-signal health monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze broad-market rally attempts, Follow-Through Day confirmations, and post-FTD health before considering equity exposure changes. Its outputs are informational market-timing research, not personalized financial advice or automated trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces investment-timing guidance and exposure ranges that could be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as informational market analysis, review generated reports before acting, and apply independent risk management and position sizing. <br>
Risk: The CLI can use an FMP API key to fetch market data. <br>
Mitigation: Run in a dedicated Python environment, provide only the needed API key, and avoid storing secrets in generated reports or shared logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/einstein-research-ftd-dv) <br>
- [FTD Methodology](references/ftd_methodology.md) <br>
- [Post-FTD Guide](references/post_ftd_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Console status text plus generated JSON and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an FMP API key and cached market data; reports include quality scores, market state, exposure ranges, and risk-management guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
