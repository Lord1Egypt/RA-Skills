## Description: <br>
Integrate apps with blockchain providers, wallets, and contract calls safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Web3 provider setup, wallet connection, chain validation, and contract-call wrappers to frontend or backend applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wallet or contract-call code can expose private keys or sensitive credentials if secrets are pasted into chat or committed to source control. <br>
Mitigation: Keep keys in a secrets manager or environment variables, never paste private keys into agent prompts or outputs, and scan repositories before deployment. <br>
Risk: Write-capable contract calls can spend gas or assets and may be irreversible on mainnet. <br>
Mitigation: Start on a local chain or testnet, require explicit chain gating, avoid defaulting to mainnet, and review transaction previews before signing. <br>
Risk: Server-side signing creates high-impact custody and authorization risks. <br>
Mitigation: Use server signers only when explicitly required and approved, with externally secured keys and audit logging for write operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzfshark/axodus-web3-integration) <br>
- [Publisher Profile](https://clawhub.ai/user/mzfshark) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with code paths, environment variable contracts, and validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe wrapper module paths, required environment variables, wallet flow choices, and test or build commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
