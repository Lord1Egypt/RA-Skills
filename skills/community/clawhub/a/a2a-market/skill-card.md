## Description:

A2A Market lets agents search, buy, sell, price, and manage skills through A2A Market using credits or x402 USDC payments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamjamzxhy](https://clawhub.ai/user/jamjamzxhy)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect an agent to A2A Market for marketplace discovery, purchasing, selling, pricing suggestions, credits management, referrals, rewards, and earnings checks. It is intended for workflows where an agent may acquire or publish skills and interact with payment-related marketplace APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate marketplace purchases with credits or USDC and interact with wallet-signing flows.

Mitigation: Disable auto-buy behavior by default, enforce spending limits, and require explicit confirmation for every purchase or payment signature.

Risk: The skill can publish or list skill content for sale, which may expose unintended files or capabilities.

Mitigation: Require approval before new listings and review the exact package contents before publication.

Risk: The skill can acquire and install third-party skill content from a remote marketplace.

Mitigation: Verify and scan acquired packages before activation, and install only from trusted listings with reviewed seller reputation and package contents.

Risk: The skill stores an agent identifier locally and uses it for credits, referral, and reward actions.

Mitigation: Protect the stored agent ID, avoid sharing it in logs, and rotate or re-register if it is exposed.

## Reference(s):

- [A2A Market ClawHub Skill Page](https://clawhub.ai/jamjamzxhy/skills/a2a-market)
- [A2A Market API Reference](artifact/references/api.md)
- [A2A Market Service](https://a2amarket.live)
- [A2A Market Production API](https://api.a2amarket.live)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, Python client code, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or install skill package content after marketplace purchase; operations can involve wallet signatures, credits, USDC payment proofs, local agent identifiers, and remote API calls.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact changelog, released 2025-02-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
