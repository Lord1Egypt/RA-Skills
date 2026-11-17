## Description:

Discover, compare, buy, and retrieve Freeland prepaid travel eSIMs through x402 with native USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elvismusli](https://clawhub.ai/user/elvismusli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover, compare, purchase, recover, and privately retrieve Freeland prepaid travel eSIMs paid for with Base USDC through x402.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate an x402 payment workflow for a travel eSIM.

Mitigation: Before signing, verify the destination, plan, price, network, USDC asset, and recipient service against the live payment requirement.

Risk: Delivery tokens, QR codes, activation data, ICCIDs, and installation links can expose eSIM ownership or activation credentials.

Mitigation: Keep delivery tokens and activation credentials private, non-cacheable, and visible only to the capability holder or authenticated owner.

Risk: Timeouts or lost paid responses can create uncertainty about whether payment settled.

Mitigation: Recover with the original idempotency key, order id, and delivery token; do not create a replacement order without an explicit owner decision.

## Reference(s):

- [Freeland eSIM discovery service contract](https://api.x402card.org/api/esim/discovery)
- [Freeland eSIM readiness endpoint](https://api.x402card.org/api/esim/ready)
- [Freeland x402 eSIM ClawHub page](https://clawhub.ai/elvismusli/skills/freeland-x402-esim)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown guidance with API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes private handling guidance for payment authorization, delivery tokens, QR codes, and eSIM activation details.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
