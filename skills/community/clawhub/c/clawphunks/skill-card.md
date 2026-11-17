## Description:

Mint and trade ClawPhunks NFTs. The first collection designed for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jefdiesel](https://clawhub.ai/user/jefdiesel)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to inspect the ClawPhunks collection, mint NFTs with x402 USDC payment, and obtain trading instructions for Ethereum L1 escrow flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to handle real wallet keys and sign payments.

Mitigation: Use only a low-balance wallet dedicated to this skill, never reuse a primary wallet private key, and verify every USDC amount and recipient before signing.

Risk: Mutable remote scripts or service responses may change after review.

Mitigation: Review fetched scripts and instructions before execution and pin audited code when operating the skill in production workflows.

Risk: The server security guidance calls out facilitator, Supabase policy, and dependency issues for public operation.

Mitigation: Resolve those issues and repeat security review before deploying or relying on the service as a public production backend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jefdiesel/skills/clawphunks)
- [ClawPhunks homepage](https://clawphunks.vercel.app)
- [ClawPhunks skills documentation](https://clawphunks.vercel.app/skills)
- [Escrow contract on Etherscan](https://etherscan.io/address/0x3e67d49716e50a8b1c71b8dEa0e31755305733fd)
- [Ethscriptions collection](https://ethscriptions.com/collections/0xb432d8c446afefb98651e05c8eee22a8617bd7a0b239dfab70e1fb3a02aa9e8a)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON responses with inline TypeScript, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet, payment, minting, collection, rarity, and trading guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
