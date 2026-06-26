## Description: <br>
Use this skill when a user wants to browse, compare, buy, pay for, query orders, track logistics, manage addresses, cancel/refund eligible orders, or apply after-sale service on Filtalgo through the bundled Agent Tool Gateway CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bvcg204](https://clawhub.ai/user/bvcg204) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to shop on Filtalgo through a bundled CLI, including product search, cart management, checkout preparation, wallet payment handoff, order lookup, logistics tracking, address management, cancellations, refunds, and after-sale requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Filtalgo account state, including cart, address, checkout, order, refund, and after-sale data. <br>
Mitigation: Require explicit user confirmation before purchase, payment preparation, address changes, cancellations, refunds, or after-sale submissions. <br>
Risk: Security evidence reports disabled TLS verification and broad credential/API controls. <br>
Mitigation: Use only in trusted environments until TLS verification is fixed, and avoid exposing access tokens, refresh tokens, or client secrets in user-facing output. <br>
Risk: The release is an internal beta with a small live catalog focused on sunscreen products. <br>
Mitigation: Set user expectations about limited catalog coverage and verify item, variant, quantity, and payment details before checkout. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bvcg204/filtalgo-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-producing command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an OAuth-backed Filtalgo account session; purchase, payment, address, cancellation, refund, and after-sale actions should require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
