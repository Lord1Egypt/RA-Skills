## Description: <br>
A crypto trading decision agent for BTC, ETH, and SOL that applies layered macro, consensus, liquidity, committee, execution, and risk checks to return EXECUTE or NO TRADE decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericn26-star](https://clawhub.ai/user/ericn26-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate BTC, ETH, and SOL trading setups with a conservative decision workflow that favors rejecting ambiguous trades. It produces structured trade parameters only when the provided market context satisfies its macro, liquidity, consensus, and risk gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce actionable crypto trade parameters. <br>
Mitigation: Treat outputs as analysis rather than financial advice, verify market data independently, size risk separately, and do not connect the skill to exchange, wallet, or automation tools without separate review and explicit controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericn26-star/eric-minimax-crypto-trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown decision output with EXECUTE_LONG, EXECUTE_SHORT, or NO TRADE and structured reason fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include entry, stop, take-profit levels, Expected R, and a concise rejection or execution rationale.] <br>

## Skill Version(s): <br>
11.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
