## Description: <br>
Use Agent Wormhole for one-time sealed handoffs between autonomous agents, including encrypted mission briefs, scoped secrets, temporary artifacts, receipts, config drops, CLI/API usage, ECHO holder access, and Bankr x402 paid opens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to send or receive one-time encrypted handoffs containing mission briefs, scoped secrets, files, receipts, or configuration drops. It also guides CLI/API usage, ECHO holder access checks, Bankr x402 paid opens, and operation of the backing service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wormhole codes can allow anyone who has the code to claim the one-time payload. <br>
Mitigation: Keep codes private unless public claiming is intended, and prefer short TTLs for sensitive payloads. <br>
Risk: Handoffs may contain scoped secrets, artifacts, receipts, or configuration data. <br>
Mitigation: Avoid logging plaintext payloads or secrets, clean up received artifacts when no longer needed, and verify package and service endpoints before use. <br>
Risk: Wallet and x402 payment flows can depend on sensitive wallet configuration or spend authority. <br>
Mitigation: Use separate owner and payer wallet configs, set explicit payment limits, and do not validate paid execution with the endpoint owner's wallet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/builtbyecho/agent-wormhole) <br>
- [Agent Wormhole direct API route](https://storage.builtbyecho.xyz/agent-wormhole) <br>
- [Agent Wormhole health endpoint](https://storage.builtbyecho.xyz/agent-wormhole/health) <br>
- [Bankr x402 paid open endpoint](https://x402.bankr.bot/0x2a16625fad3b0d840ac02c7c59edea3781e340ae/agent-wormhole-open) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive handoff, wallet, and payment handling guidance; use short TTLs and avoid logging secrets.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
