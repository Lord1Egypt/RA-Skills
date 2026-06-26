## Description: <br>
Enables AI agents to interact with AISP (Agent Inference Sharing Protocol) for renting or providing DIEM API capacity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DaveO280](https://clawhub.ai/user/DaveO280) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to rent or provide DIEM/Venice API capacity through AISP, including listing capacity, funding rentals with USDC escrow, retrieving scoped API keys, and settling rentals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can initiate USDC escrow transactions. <br>
Mitigation: Use an external or hardware signer, verify contract addresses, test read-only listing calls first, and require explicit approval before funding, settling, or refund actions. <br>
Risk: The workflow can handle scoped Venice API keys. <br>
Mitigation: Use inference-only, revocable, minimal-scope API keys and require explicit approval before storing or retrieving credentials. <br>
Risk: A misconfigured backend URL could route transactions or credential requests to the wrong service. <br>
Mitigation: Verify BACKEND_URL before use and avoid pasting raw private keys into the agent. <br>


## Reference(s): <br>
- [AISP on ClawHub](https://clawhub.ai/DaveO280/aisp) <br>
- [AISP homepage](https://github.com/DaveO280/Diem-Marketplace-V2-) <br>
- [ClawHub documentation](https://docs.openclaw.ai/tools/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference BACKEND_URL, wallet signer configuration, contract addresses, API endpoints, and scoped Venice API keys.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
