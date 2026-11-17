## Description:

Agent Commerce Engine lets autonomous agents connect to compatible headless e-commerce backends for product discovery, cart operations, account flows, and order creation with final payment handed to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowloady](https://clawhub.ai/user/nowloady)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to connect shopping agents to compatible commerce APIs, search catalog data, manage carts and profiles, and create pending orders for human payment handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles passwords, tokens, profile data, and orders, and server security evidence flags credential-transport and local credential-safety weaknesses.

Mitigation: Use it only with commerce backends you trust, and avoid entering real passwords until URL validation, redirect handling, and credential-file creation issues are fixed.

Risk: The create-order flow can submit shipping details and create a pending order even though final payment is handed back to the user.

Mitigation: Confirm the merchant URL, cart contents, and shipping details before order creation, then provide the payment link to the user for manual completion.

## Reference(s):

- [Server-Side Implementation Specification](artifact/SERVER_SPEC.md)
- [ClawHub skill page](https://clawhub.ai/nowloady/skills/agent-commerce-engine)
- [Project homepage](https://github.com/NowLoadY/agent-commerce-engine)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI output, JSON API responses, and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commerce commands may read or write per-store tokens and visitor IDs under the local OpenClaw credentials directory.]

## Skill Version(s):

1.7.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
