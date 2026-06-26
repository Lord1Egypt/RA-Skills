## Description: <br>
Launch, deploy, and manage Solana tokens via the Blowfish Agent API, including status checks and claiming accrued trading fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[basedmereum](https://clawhub.ai/user/basedmereum) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to launch Solana tokens through Blowfish, monitor launch status, list launched tokens, and claim accrued trading fees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent process to use a full Solana wallet private key for real token-launch and fee-claim actions. <br>
Mitigation: Use only a dedicated low-value Solana wallet, keep the private key out of shell history, and manually confirm every launch or fee-claim action before submission. <br>
Risk: Actions are sent to an external Blowfish API endpoint and may create live on-chain effects. <br>
Mitigation: Verify the API endpoint and publisher before use, install dependencies deliberately, and review request parameters before the agent runs the bundled script. <br>


## Reference(s): <br>
- [Blowfish Agent API Reference](references/api.md) <br>
- [Blowfish Agent API](https://api-blowfish.neuko.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/basedmereum/blowfish-launch) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and API parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit authenticated token-launch, status-check, listing, and fee-claim requests through the Blowfish Agent API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
