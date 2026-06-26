## Description: <br>
Deploy NFT collections on Base. AI agents can deploy via API key or x402 USDC payment. Humans mint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nrlartt](https://clawhub.ai/user/nrlartt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to register an agent, verify a human owner, and deploy ERC-721 NFT collections on Base through Clawdmint APIs or x402 USDC payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may initiate real NFT deployments or x402 payment actions that have financial and public-chain consequences. <br>
Mitigation: Require explicit human approval for each deployment or payment action before sending requests. <br>
Risk: Incorrect collection parameters can route funds incorrectly or publish unintended mint terms. <br>
Mitigation: Verify payout addresses, mint prices, supply limits, royalty settings, and target Base network details before execution. <br>
Risk: The skill relies on a private API key and optional webhook endpoint configuration. <br>
Mitigation: Keep the API key private, regenerate it if exposed, set wallet spending limits where possible, and use only trusted HTTPS webhook endpoints under user control. <br>


## Reference(s): <br>
- [Clawdmint Homepage](https://clawdmint.xyz) <br>
- [Clawdmint Skill Documentation](https://clawdmint.xyz/skill.md) <br>
- [Clawdmint API Base](https://clawdmint.xyz/api/v1) <br>
- [Clawdmint x402 Pricing](https://clawdmint.xyz/api/x402/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/nrlartt/clawdmint) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides API-key and x402 payment flows for NFT collection deployment on Base.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
