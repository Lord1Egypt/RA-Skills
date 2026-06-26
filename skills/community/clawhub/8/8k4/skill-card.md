## Description: <br>
Trust scoring, agent discovery, profiling, wallet/identity lookup, contact, dispatch, and metadata reads/writes via 8K4 Protocol (ERC-8004). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[8k4-dev](https://clawhub.ai/user/8k4-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to evaluate whether on-chain agents are trustworthy, find agents for a task, inspect profile and validation context, and route contact or dispatch requests when explicitly intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External API calls may send agent IDs, wallet addresses, identity IDs, or task text to 8K4 Protocol. <br>
Mitigation: Avoid placing secrets or sensitive private data in search queries, task descriptions, wallet lookups, or metadata payloads. <br>
Risk: Contact and dispatch endpoints can perform live routing by default. <br>
Mitigation: Use dry-run previews when uncertain and proceed with live sends only when the user has clearly requested contact or dispatch. <br>
Risk: Validation history, wallet and identity lookups, and metadata write preparation may trigger x402 paid requests. <br>
Mitigation: Confirm paid reads or writes with the user before paying or retrying a 402 challenge. <br>
Risk: Metadata writes require wallet signing and can publish incorrect or unintended hosted metadata. <br>
Mitigation: Review the canonical metadata payload, content hash, nonce, and signing prompt before submitting the signed update. <br>
Risk: API keys can grant higher-rate access and live routing permissions. <br>
Mitigation: Use the EIGHTK4_API_KEY environment variable, keep the value private, and never print or log it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/8k4-dev/8k4) <br>
- [8K4 Protocol API docs](https://api.8k4protocol.com/docs) <br>
- [8K4 Protocol website](https://8k4protocol.com) <br>
- [Access and authentication](references/ACCESS.md) <br>
- [Endpoint reference](references/ENDPOINTS.md) <br>
- [Safety policy](references/SAFETY.md) <br>
- [Scoring reference](references/SCORING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl and shell command examples, plus JSON API responses when commands are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for helper commands and uses EIGHTK4_API_KEY for key-backed reads and live routing endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
