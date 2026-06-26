## Description: <br>
Checks an agent's on-chain ERC-8004 identity, trust score, and KYA credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to verify an authenticated Agnic agent's identity status, owner wallet, reputation score, categories, and KYA credential state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication tokens can grant access to Agnic identity and wallet-linked status. <br>
Mitigation: Set AGNIC_TOKEN as an environment variable when needed, avoid passing tokens on the command line, and do not share token values. <br>
Risk: Identity output can reveal wallet ownership, trust score, categories, KYA details, and agent status. <br>
Mitigation: Review output before sharing it and redact wallet or credential details when they are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/get-agent-identity) <br>
- [Agnic app](https://app.agnic.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON identity output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May expose wallet ownership, trust score, KYA details, categories, and agent status.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
