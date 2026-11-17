## Description:

Provides independent risk assessments for proposed Uniswap swaps, LP positions, bridges, and token interactions across slippage, impermanent loss, liquidity, smart contract, and bridge risk dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and developers use this skill as a second-opinion risk check before proposed Uniswap swaps, liquidity positions, bridges, token interactions, or pool checks. It returns a per-dimension risk assessment with an APPROVE, CONDITIONAL_APPROVE, VETO, or HARD_VETO decision and mitigation guidance when relevant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to be invoked for varied Uniswap safety questions.

Mitigation: Confirm the exact operation, token addresses, amounts, chains, and risk tolerance before relying on the assessment.

Risk: APPROVE and VETO labels may be mistaken for financial advice or transaction authorization.

Mitigation: Use the output only as advisory decision support and require independent review plus wallet-level confirmation before any trade, liquidity, bridge, or token action.

Risk: Installation examples are not pinned to an immutable version.

Mitigation: Install from a reviewed, pinned ClawHub version or immutable commit when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/assess-risk)
- [Skill specification](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown-style risk assessment with per-dimension scores, final decision, conditions, and mitigation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute Uniswap operations; outputs advisory risk decisions based on available operation details and risk tolerance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
