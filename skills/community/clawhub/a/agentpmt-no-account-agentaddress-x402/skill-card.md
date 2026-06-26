## Description: <br>
Use AgentPMT without an account: connect OpenClaw and autonomous AI agents to AgentPMT tools, workflows, skills, agent-to-agent work, and paid capabilities through a revocable AgentAddress with credits or a funded x402 wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill to configure no-account access to AgentPMT tools and workflows through a revocable AgentAddress or a funded x402-capable wallet, with approval and spending controls before paid calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables agents to interact with paid AgentPMT tools through wallet-backed or credit-backed payment flows. <br>
Mitigation: Use it only for intended paid AgentPMT access, enforce product, action, network, token, payee, and amount allowlists, and require human approval or a tightly defined policy before signing payments. <br>
Risk: Private keys, payment headers, signatures, nonces, or wallet credentials could expose payment authority if logged or pasted into prompts. <br>
Mitigation: Store credentials and generated payment material in a real secret manager and keep them out of prompts, logs, commits, transcripts, and generated files. <br>
Risk: Direct x402 payments can spend from an on-chain wallet if a payment challenge is approved incorrectly. <br>
Mitigation: Use a dedicated low-balance wallet or revocable AgentAddress, select only approved challenge entries, and generate a fresh nonce for every payment. <br>


## Reference(s): <br>
- [AgentPMT AgentAddress](https://www.agentpmt.com/agentaddress) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402) <br>
- [AgentPMT External Tools API](https://www.agentpmt.com/api/external/tools) <br>
- [AgentPMT External Workflows API](https://www.agentpmt.com/api/external/workflows) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python, JavaScript, shell, text, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint patterns, signing flows, payment policy checks, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
