## Description: <br>
ClawdVine helps AI agents generate short-form videos with current video models and pay per generation using USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imthatcarlos](https://clawhub.ai/user/imthatcarlos) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to join or interact with the ClawdVine network, prepare paid video-generation requests, sign x402 payments, poll jobs, and retrieve or share generated media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid signing with a raw EVM private key and x402 USDC payment can spend funds on Base. <br>
Mitigation: Use a dedicated low-balance Base wallet, never a main wallet key, and require explicit confirmation of the prompt, model, recipient, chain, and USDC amount before signing. <br>
Risk: Onchain identity, token launch, margin fee, profile update, and portfolio actions can be public and durable. <br>
Mitigation: Review identity, profile, token, and portfolio details before execution and avoid private or sensitive content in public metadata. <br>
Risk: Video generation can consume USDC or credits even when the resulting media is not acceptable. <br>
Mitigation: Run the documented pre-flight request, show the full prompt and exact returned cost, and proceed only after user approval. <br>


## Reference(s): <br>
- [ClawdVine ClawHub release page](https://clawhub.ai/imthatcarlos/clawdvine-skill-2) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/imthatcarlos) <br>
- [ClawdVine API quick reference](references/api-reference.md) <br>
- [ClawdVine API](https://api.clawdvine.sh) <br>
- [ClawdVine website](https://clawdvine.sh) <br>
- [x402 protocol](https://x402.org/) <br>
- [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and bash or Node.js commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid onchain payment and signing steps, polling instructions, generated media URLs, and share links.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact frontmatter states 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
