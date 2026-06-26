## Description: <br>
Trade and monitor ApeX perpetual futures, including balances, positions, P&L, orders, market analysis, and trade reward enrollments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joshlin111](https://clawhub.ai/user/joshlin111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor ApeX perpetual futures portfolios, inspect market signals, manage orders, and execute trades through ApeX with explicit credential-based access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live ApeX futures orders and cancel existing orders. <br>
Mitigation: Use ApeX testnet first and require explicit user confirmation before every trade, close-position, cancel-all, or reward-enrollment action. <br>
Risk: Private operations require API credentials and an Omni seed. <br>
Mitigation: Keep credentials and the Omni seed out of chat and source control, and restrict API permissions where possible. <br>
Risk: Position monitoring can write trading-state.json on disk. <br>
Mitigation: Protect or delete trading-state.json on shared or backed-up machines. <br>


## Reference(s): <br>
- [ApeX Omni API Reference](references/api.md) <br>
- [ApeX Omni API](https://omni.apex.exchange) <br>
- [ApeX Omni Testnet API](https://qa.omni.apex.exchange) <br>
- [Skill page](https://clawhub.ai/joshlin111/apex-trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Private operations require ApeX API credentials and an Omni seed; public market data commands can run without credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
