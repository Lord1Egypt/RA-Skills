## Description:

Investigate an exact EVM token's controls, launch allocations, liquidity custody, sellability, and treasury flows, or compare findings with a prior review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Analysts and developers use this read-only workflow to assess a specific EVM token's privileges, launch distribution, liquidity custody, practical exits, and treasury flows, or to compare a new review with earlier evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blockchain data reads may consume quota on an existing provider.

Mitigation: Use an authorized read-only provider and check its quota before collecting evidence.

Risk: Exposing wallet keys or broadcast-capable endpoints could exceed the read-only workflow's scope.

Mitigation: Do not supply wallet keys or transaction-broadcast access.

Risk: An incomplete diligence report may be mistaken for proof that a token is safe or sellable.

Mitigation: Treat findings as evidence-bounded, document unknowns, and verify actual exit conditions separately.

## Reference(s):

- [Controls and dependencies](references/controls.md)
- [Liquidity custody and executable exits](references/liquidity-exits.md)
- [Launch allocations and asset flows](references/launch-flows.md)
- [Reports and repeat reviews](references/reporting.md)
- [Evidence format and local helpers](references/evidence-format.md)
- [ERC-20 token standard](https://eips.ethereum.org/EIPS/eip-20)
- [OpenZeppelin access control documentation](https://docs.openzeppelin.com/contracts/5.x/access-control)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Evidence-cited Markdown reports; optional structured JSON snapshots and comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings identify their observation time, evidence coverage, and unresolved questions; helper validation does not establish token safety.]

## Skill Version(s):

0.2.3 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
