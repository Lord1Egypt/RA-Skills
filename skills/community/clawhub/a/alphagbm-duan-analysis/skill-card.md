## Description:

Duan-Yongping-style seller playbook for any ticker: Sell Put at a willing-buy price, Covered Call for yield enhancement, and Panic-Buy context from current VIX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request a ticker-level Duan Yongping-style options-selling analysis with sell-put, covered-call, and VIX panic-buy context. Outputs are educational decision support, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat options-selling analysis as personalized financial advice.

Mitigation: Present outputs as educational decision support and require the user to make independent suitability, risk, and compliance judgments.

Risk: Broad market prompts may receive options-specific framing.

Mitigation: Use this skill only when Duan-style options-selling analysis is intended; route general market questions to a broader market-analysis skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-duan-analysis)
- [AlphaGBM](https://alphagbm.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style analysis cards with structured option metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sell_put, covered_call, and panic_buy panels plus ticker, stock price, expiry, DTE, and timestamp metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-06-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
