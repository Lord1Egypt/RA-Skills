## Description: <br>
A crypto trading decision agent for BTC, ETH, and SOL that uses layered macro, liquidity, consensus, execution, and risk checks to return EXECUTE or NO TRADE decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericn26-star](https://clawhub.ai/user/ericn26-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to structure crypto trade analysis for BTC, ETH, and SOL, with a strong bias toward rejecting trades unless the supplied market data satisfies strict risk and liquidity criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce risky crypto trade suggestions that may be mistaken for financial advice or direct execution instructions. <br>
Mitigation: Treat outputs as informational analysis, independently verify all market data, and require human confirmation before any trade. <br>
Risk: Connecting the skill to exchange credentials or automated trading could turn advisory text into account-impacting action. <br>
Mitigation: Do not provide exchange credentials or connect outputs to automatic trading without separate risk controls and approval gates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ericn26-star/christy-minimax-crypto-trading) <br>
- [Publisher profile](https://clawhub.ai/user/ericn26-star) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown] <br>
**Output Format:** [Markdown text with strict EXECUTE_LONG, EXECUTE_SHORT, or NO TRADE decision formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied market data such as price, RSI, funding, open interest, and key levels; does not execute trades or access accounts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
