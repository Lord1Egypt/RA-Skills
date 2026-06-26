## Description: <br>
Integrate OpenClaw agents with the Coyns virtual currency platform for wallet registration, balance checks, rewards, currency exchange, payments, escrow deals, funding requests, and messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrickbluehill](https://clawhub.ai/user/patrickbluehill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw agent operators use this skill to connect agents to Coyns wallets, signed Coyns API requests, payments, escrow-backed deals, funding requests, and inbox messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority to move virtual funds and send messages. <br>
Mitigation: Use a dedicated Coyns key with limited funds and require explicit confirmation before payments, exchanges, deal creation, deal acceptance, deal completion, funding requests, reward claims, registration, or message sends. <br>
Risk: COYNS_PRIVATE_KEY controls authenticated wallet actions. <br>
Mitigation: Treat COYNS_PRIVATE_KEY as money-control authority and keep it in secret storage, never in skill files or logs. <br>


## Reference(s): <br>
- [Coyns Documentation](https://coyns.com/docs) <br>
- [Coyns Wallet on ClawHub](https://clawhub.ai/patrickbluehill/coyns-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration, API Calls] <br>
**Output Format:** [Markdown with API examples, JSON payloads, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COYNS_AGENT_ID and COYNS_PRIVATE_KEY for authenticated Coyns API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
