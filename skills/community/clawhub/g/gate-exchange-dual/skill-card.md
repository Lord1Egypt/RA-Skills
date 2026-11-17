## Description:

Gate dual investment skill for product discovery, settlement simulation, position management, balance queries, and confirmation-gated dual order placement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Gate dual investment products, model settlement outcomes, review positions and balances, and prepare dual investment orders through a Gate MCP session. Write actions require explicit confirmation and should be used only with appropriate Gate credentials and user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place non-cancelable financial orders through Gate dual investment.

Mitigation: Use a Gate MCP credential limited to the minimum Earn:Write scope the user accepts, and require explicit immediate confirmation before every order placement.

Risk: Financial output can mislead users if APY, minimum amount, guarantee wording, or raw error messages are handled incorrectly.

Mitigation: Review displayed APY calculations, product terms, and user-facing wording against Gate data before relying on responses or placing orders.

Risk: Dual investment is not principal-protected and settlement may occur in a different currency than the initial investment.

Mitigation: Show both settlement scenarios and the non-principal-protected risk note before any investment decision or order confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-exchange-dual)
- [ClawHub Publisher Profile](https://clawhub.ai/user/gate-exchange)
- [ClawHub Metadata Homepage](https://github.com/gate/gate-skills)
- [Gate MCP Dependency](https://github.com/gate/gate-mcp)
- [README](artifact/README.md)
- [MCP Execution Specification](artifact/references/mcp.md)
- [Product Query Workflows](artifact/references/product-query.md)
- [Subscription and Order Placement Workflows](artifact/references/subscription.md)
- [Settlement and Assets Workflows](artifact/references/settlement-assets.md)
- [Runtime Rules](artifact/references/gate-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with tables, order drafts, settlement scenarios, and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Gate MCP tools with required API credentials; order placement is confirmation-gated.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
