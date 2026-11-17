## Description:

Guides Uniswap swap quoting, approval review, unsigned handoff preparation, and reconciliation across AMM and UniswapX routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and other users can compare Uniswap swap quotes, check wallet approvals, prepare unsigned transactions or order handoffs, and reconcile existing swaps without granting the skill signing authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect token, chain, recipient, route, or slippage settings could lead to an unintended swap.

Mitigation: Confirm token addresses, chain IDs, recipient, route, and slippage against the current quote before wallet use.

Risk: A wallet signature or transaction submission can authorize a transfer of funds.

Mitigation: Keep handoffs unsigned; require explicit user authorization for the exact wallet action before any signing or submission.

Risk: Exposed API keys or signatures could compromise access or authorization.

Mitigation: Use an existing secret mechanism for API keys and never include keys or signatures in reports.

## Reference(s):

- [Trading API recipes and sources](artifact/references/recipes.md)
- [Uniswap Trading API overview](https://developers.uniswap.org/docs/trading/overview)
- [Uniswap swap integration guide](https://developers.uniswap.org/docs/trading/swapping-api/start-building/integration-guide)
- [Uniswap Permit2 lifecycle](https://developers.uniswap.org/docs/trading/swapping-api/concepts/permit2)
- [ClawHub skill listing](https://clawhub.ai/galleonlabs/skills/galleon-uniswap-swap)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands]

**Output Format:** [Markdown with quote details and optional JSON or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote-only or unsigned handoff; does not sign or submit transactions.]

## Skill Version(s):

0.3.1 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
