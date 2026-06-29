## Description: <br>
Agent Payment helps autonomous agents create an EVM wallet through AgentAddress, buy USDC-denominated AgentPMT credits via x402, sign authenticated requests, and check balances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and autonomous-agent operators use this skill to connect agents to AgentPMT payment workflows, including wallet creation, credit purchase, request signing, and balance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can create wallets, purchase credits, and spend credits on AgentPMT tools or workflows. <br>
Mitigation: Install only for intended payment workflows, keep spending limits small, and monitor credit purchases and tool invocations. <br>
Risk: Wallet private keys, mnemonics, session nonces, signatures, and payment authorization data are sensitive financial material. <br>
Mitigation: Store secrets outside prompts and logs, avoid returning them to users, and use a secret manager or equivalent protected storage. <br>
Risk: Incorrect signing inputs or reused request identifiers can cause failed requests or replay protections to trigger. <br>
Mitigation: Lowercase wallet addresses in signed messages, use a fresh request_id for each signed request, and follow the documented recovery guidance for signature errors. <br>


## Reference(s): <br>
- [AgentPMT External Agent API](https://www.agentpmt.com/external-agent-api) <br>
- [AgentPMT Marketplace](https://www.agentpmt.com) <br>
- [Agent Payment on ClawHub](https://clawhub.ai/agentpmt/agent-payment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment flow guidance, request-signing message formats, and secret-handling rules.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
