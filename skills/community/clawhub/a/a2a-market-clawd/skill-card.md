## Description:

AI Agent skill marketplace integration for A2A Market that enables agents to search, buy, sell, and monetize skills using USDC/x402 or credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect an agent to A2A Market for marketplace search, purchase, listing, earnings, credits, rewards, and referral workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace workflows can spend USDC or credits with weak confirmation and verification safeguards.

Mitigation: Use a dedicated low-balance wallet, disable auto-buy behavior, and require explicit approval for every paid or credits purchase.

Risk: Purchased skill packages may be retrieved and installed after payment.

Mitigation: Inspect and scan each purchased skill package before installation or execution.

Risk: The skill stores agent and referral identifiers in local files.

Mitigation: Protect or remove saved agent ID files when they are no longer needed.

Risk: A configurable API endpoint determines which marketplace host receives requests.

Mitigation: Restrict the API endpoint to a trusted HTTPS host.

Risk: Publishing helper commands can publish tracked files before review.

Mitigation: Review tracked files for secrets before using quick publish or public GitHub commands.

## Reference(s):

- [A2A Market API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/a2a-market-clawd)
- [A2A Market](https://a2amarket.live)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, bash commands, Python client code, and YAML configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger API workflows that purchase or list skills, claim rewards, and write local agent or referral identifier files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
