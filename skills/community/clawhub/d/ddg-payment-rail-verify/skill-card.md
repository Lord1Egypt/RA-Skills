## Description:

Prove an agent's payment path still works end to end and keep proving it: a paid smoke test, a 402-envelope pre-flight, and a buyer-side trust probe of the seller you depend on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcircuitbreaker](https://clawhub.ai/user/0xcircuitbreaker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payment engineers use this workflow to verify an x402 payment client, confirm receipts, and assess seller payment endpoints before launch or on a recurring canary schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid checks and scheduled runs can incur recurring USDC charges; preflight may also be paid.

Mitigation: Enforce the advertised spend limit and explicitly approve the schedule; treat preflight as potentially paid.

Risk: Seller URLs may expose embedded credentials or signed parameters.

Mitigation: Use public seller URLs without embedded credentials or signed parameters.

Risk: A real settlement test needs independent confirmation of its payment receipt.

Mitigation: For a deliberate real-settlement test, set X-DDG-Free-Tier: skip and independently confirm the payment receipt.

## Reference(s):

- [DDG Agent Service](https://agents.daedalusdevelopmentgroup.com)
- [ClawHub Skill Listing](https://clawhub.ai/0xcircuitbreaker/skills/ddg-payment-rail-verify)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Files]

**Output Format:** [Markdown workflow with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification results can be saved as JSON and HTTP-header files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
