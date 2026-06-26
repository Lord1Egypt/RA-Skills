## Description: <br>
Provides cryptocurrency and precious-metals market data plus technical-analysis indicators for assets such as BTC, ETH, BNB, ZEC, SOL, and gold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[burceasn](https://clawhub.ai/user/burceasn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch crypto market data, calculate technical indicators, and structure market-analysis or trading-plan guidance without granting trade-execution authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes external market-data requests to public providers. <br>
Mitigation: Install and run it in an isolated Python environment and disclose that market queries may be sent to public data providers. <br>
Risk: Trading-plan or leverage guidance may be mistaken for financial advice. <br>
Mitigation: Present outputs as educational market analysis, require human review, and avoid granting agents authority to trade. <br>
Risk: Users may expose wallet keys, exchange API keys, or other credentials while discussing crypto workflows. <br>
Mitigation: Do not request or store wallet keys or exchange API keys, and remind users to keep credentials outside the agent workflow. <br>
Risk: Unpinned or broad Python dependencies can change behavior over time. <br>
Mitigation: Use an isolated environment and consider pinning dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/burceasn/crypto-watch-skill) <br>
- [Technical indicator guide](references/INDICATORS.md) <br>
- [Trading strategy guide](references/STRATEGY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market data depends on public provider availability and network access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
