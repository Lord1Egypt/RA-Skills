## Description:

A crypto trading decision skill for BTC, ETH, and SOL that applies layered market, liquidity, consensus, and risk checks to return EXECUTE or NO TRADE decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericn26-star](https://clawhub.ai/user/ericn26-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for informational crypto market analysis and structured BTC, ETH, or SOL trade-decision filtering. It is designed to reject ambiguous setups and return either a structured EXECUTE decision or a NO TRADE rejection reason.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce direct crypto trade instructions that may lead to real financial loss.

Mitigation: Use outputs only as informational analysis, require explicit user intent before invocation, and do not treat EXECUTE decisions as professional financial advice.

Risk: The security scan notes broad market terms may activate the skill.

Mitigation: Invoke the skill only in clearly scoped crypto trading contexts and review any trade decision before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericn26-star/skills/christy-minimax-crypto-trading)
- [ClawHub publisher profile](https://clawhub.ai/user/ericn26-star)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style decision text with structured trade fields or a rejection reason]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are limited to EXECUTE_LONG, EXECUTE_SHORT, or NO TRADE decisions.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
