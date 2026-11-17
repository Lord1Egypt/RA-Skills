# Get with Receipt for ClawHub (v1.0.7 source candidate)

Name an outcome. Receipt finds eligible paid tools, shows the selected seller and quoted price,
clears the purchase under the owner's limits, and returns the result with signed proof.

## How it works

1. Name the outcome.
2. Receipt finds eligible options.
3. The agent shows the selected seller, quoted price, assurance, and relevant reliability
   information.
4. The owner approves, or an existing spending policy clears the purchase.
5. Receipt returns the result and signed proof.

## Try one safe first outcome

If the owner chooses launch credit during setup and the account reports an eligible, authorized
credit, Receipt can fund one web-search outcome up to $0.10. It expires after seven days, does not
charge the owner wallet, and does not create cash value, recurring authority, or authority for
later buyer-funded purchases. Opting out still completes the connection without spending.

## Approval and limits

Before a buyer-funded purchase, the agent discloses the selected seller, quoted price, assurance,
relevant reliability information, and the query or data recipients. The purchase proceeds only
under an existing spending policy or Receipt-hosted owner approval. The result returns with public,
signed, and verification Receipt links.

## Package and connection details

This directory is the complete ClawHub publication payload. It contains a declarative skill, one
auditable clean-profile bootstrap, one macOS authorization-completion helper, a human-readable
skill card, and supporting references. It does not include a custom OpenClaw plugin, credentials,
seller-specific tools, or a second commerce implementation.

The skill remains eligible and model-visible before the native OpenClaw MCP connection named
`receipt` exists. It configures that separate connection during setup. OAuth credentials remain in
OpenClaw; the skill and ClawHub never receive or store them.

Publisher: `@receiptprotocol`. Category: **Finance**.

Version `1.0.7` is a source candidate only and must not be published by this build. After a
separate owner-approved publication, install it with:

```bash
openclaw skills install @receiptprotocol/get-with-receipt
```
