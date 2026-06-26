## Description: <br>
Safely deploys Move contracts to Aptos networks, including devnet, testnet, and mainnet, with pre-deployment verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute Aptos Move contract deployments with checks for security review, test coverage, network selection, funding, publication, verification, and upgrade preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes Aptos mainnet deployment and upgrade commands that can submit transactions using the user's local signing profile, including examples with --assume-yes. <br>
Mitigation: Before mainnet deploys or upgrades, avoid --assume-yes and explicitly verify the Aptos profile, signer address, network, package, object address, and gas cost. <br>
Risk: Local Aptos profiles and environment files can contain private keys or other signing material. <br>
Mitigation: Keep private keys out of prompts, logs, command output, and version control; do not display local Aptos config or secret environment values. <br>


## Reference(s): <br>
- [Aptos CLI Publishing](https://aptos.dev/build/cli/working-with-move-contracts) <br>
- [Aptos Network Endpoints](https://aptos.dev/nodes/networks) <br>
- [Aptos Gas and Transaction Fees](https://aptos.dev/concepts/gas-txn-fee) <br>
- [Aptos Mainnet Explorer](https://explorer.aptoslabs.com/?network=mainnet) <br>
- [Aptos Testnet Explorer](https://explorer.aptoslabs.com/?network=testnet) <br>
- [ClawHub Skill Page](https://clawhub.ai/iskysun96/deploy-contracts) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and deployment checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include network-specific Aptos CLI commands for devnet, testnet, and mainnet deployment or upgrade workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
