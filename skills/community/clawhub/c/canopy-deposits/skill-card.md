## Description:

Helps merchants create crypto deposit intents, retrieve funding options and addresses, and check deposit settlement through Canopy's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gkwxz4h9s8-ai](https://clawhub.ai/user/gkwxz4h9s8-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and their agents use this skill to prepare Canopy crypto deposits, provide customers with funding details, and check detection and settlement status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing OAuth credentials or secret keys in chat or configuration can compromise the merchant account.

Mitigation: Connect through the MCP client's secure credential system and never request or paste secrets into chat.

Risk: Creating an intent or issuing an address changes merchant account state and may present unintended deposit terms.

Mitigation: Request user authorization and review the destination wallet, network, token, minimum, and fees before creating or issuing deposit details.

Risk: An incorrect network, token, or interpretation of deposit detection could mislead a payer about funding or settlement.

Mitigation: Show the exact returned network and token alongside any address, and distinguish deposit detection from confirmed settlement.

## Reference(s):

- [Canopy MCP documentation](https://www.canopypay.io/agents/mcp)
- [Canopy MCP plain-text contract](https://www.canopypay.io/agents/mcp/raw)
- [Canopy Deposits ClawHub release](https://clawhub.ai/gkwxz4h9s8-ai/skills/canopy-deposits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text with deposit details, funding instructions, links, and status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a hosted checkout URL or a network-specific deposit address with token and minimum, as returned by Canopy.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
