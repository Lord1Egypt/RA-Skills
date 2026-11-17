## Description:

Deploy NFT collections on Base. AI agents can deploy via API key or x402 USDC payment. Humans mint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nrlartt](https://clawhub.ai/user/nrlartt)

### License/Terms of Use:


## Use Case:

External developers and agent builders use Clawdmint to register an agent, verify human ownership, deploy ERC-721 NFT collections on Base, configure minting parameters, and monitor collection activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can authorize account actions if exposed or sent to the wrong service.

Mitigation: Store the API key carefully, send it only to clawdmint.xyz, and regenerate it if compromised.

Risk: Webhook configuration can expose mint activity or agent events to unintended receivers.

Mitigation: Configure only webhook endpoints you control and protect webhook tokens.

Risk: x402 payments and NFT deployments can create real USDC spending and on-chain actions.

Mitigation: Require explicit wallet approval and spending limits before x402 payment or collection deployment.

Risk: Manual curl installation can fetch unreviewed skill content.

Mitigation: Prefer a reviewed ClawHub release or verify the downloaded SKILL.md before manual installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nrlartt/skills/clawdmint)
- [Clawdmint homepage](https://clawdmint.xyz)
- [Clawdmint skill documentation](https://clawdmint.xyz/skill.md)
- [Clawdmint API base](https://clawdmint.xyz/api/v1)
- [x402 pricing](https://clawdmint.xyz/api/x402/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API request examples, OpenClaw configuration, webhook setup, and x402 payment guidance.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
