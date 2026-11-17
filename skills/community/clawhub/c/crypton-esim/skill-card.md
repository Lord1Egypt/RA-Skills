## Description:

Purchase anonymous eSIMs with BTC/XMR/card - no account required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajarmoszuk](https://clawhub.ai/user/ajarmoszuk)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to browse eSIM data plans, create Crypton guest checkouts with BTC, XMR, or card, and check order status from chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Country searches, package IDs, payment-method choices, and order IDs are sent to Crypton.

Mitigation: Install only in environments where sending those values to Crypton is acceptable.

Risk: Checkout and status responses can include payment links, payment addresses, order UUIDs, ICCIDs, activation codes, or QR payloads.

Mitigation: Treat these values as sensitive and avoid sharing logs or screenshots that contain them.

Risk: Checkout creation can initiate a purchase flow from a chat command.

Mitigation: Add or require an explicit confirmation step before checkout creation in sensitive environments.

Risk: The dependency requirement allows newer requests releases to be resolved at install time.

Mitigation: Pin dependencies for controlled deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajarmoszuk/skills/crypton-esim)
- [Crypton Guest eSIM API documentation](https://crypton.sh/esim/guest)
- [Crypton website](https://crypton.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls]

**Output Format:** [Markdown chat text with plan listings, checkout details, payment links or addresses, order IDs, ICCIDs, and activation codes when returned by Crypton.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive payment links, order UUIDs, ICCIDs, activation codes, and QR payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
