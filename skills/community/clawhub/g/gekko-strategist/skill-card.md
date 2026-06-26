## Description: <br>
Gekko Strategist is an AI-powered DeFi strategy development agent that designs, backtests, adapts, and evaluates yield farming strategies based on market conditions, risk profiles, and capital allocation goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gekkoai001](https://clawhub.ai/user/gekkoai001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and DeFi developers use this skill to design, backtest, adapt, and compare yield farming strategies on Base using market conditions, risk profiles, and capital allocation goals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strategy prompts or market context are sent to the disclosed external GekkoTerminal API. <br>
Mitigation: Install only if this external API use is acceptable, and avoid sending seed phrases, private keys, exchange credentials, or wallet access. <br>
Risk: Yield strategy recommendations may be informational and may not match future market conditions. <br>
Mitigation: Independently review and backtest recommendations before using them for any separate transaction or allocation decision. <br>
Risk: The skill discusses DeFi vault allocations but does not execute transactions itself. <br>
Mitigation: Require explicit user approval and wallet signing in any separate execution flow. <br>


## Reference(s): <br>
- [Gekko Strategist ClawHub Page](https://clawhub.ai/gekkoai001/gekko-strategist) <br>
- [GekkoTerminal Strategist A2A Endpoint](https://gekkoterminal.ai/api/a2a?agent=strategist) <br>
- [Publisher Profile](https://clawhub.ai/user/gekkoai001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces strategy recommendations, backtest summaries, adapted allocation guidance, and side-by-side strategy comparisons; it does not execute trades or sign wallet transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
