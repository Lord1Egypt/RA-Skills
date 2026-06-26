## Description: <br>
Transaction round-up helper that calculates spare change from payments and builds unsigned Solana transfer instructions for user review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nightcode112](https://clawhub.ai/user/nightcode112) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to calculate Solana transaction round-ups, request server-built unsigned transfer or swap instructions, and present them for user verification and signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsigned transfer or swap instructions can affect funds if a user signs them without review. <br>
Mitigation: Before signing, verify destinations, amounts, program IDs, token pairs, and fee breakdowns, and test with small amounts first. <br>
Risk: The skill requires a Buff API key and wallet public key. <br>
Mitigation: Use scoped, rotatable API keys, keep credentials out of prompts and logs, and never provide private keys to the agent. <br>
Risk: Security scan confidence is limited because the authoritative scan guidance reports that direct file inspection was unavailable and VirusTotal was pending. <br>
Mitigation: Review the skill files in ClawHub before installing, especially for unexpected credential use, automatic command execution, broad file access, or persistent background behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nightcode112/buff-roundup) <br>
- [Buff documentation](https://buff.finance/docs) <br>
- [Buff REST API reference](https://buff.finance/docs/api/rest) <br>
- [Buff swap documentation](https://buff.finance/docs/swaps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference unsigned Solana transaction or instruction payloads that require user review and signing outside the agent.] <br>

## Skill Version(s): <br>
2.3.5 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
