## Description: <br>
Expert guide for using Agent Bazaar (agent-bazaar.com), a capabilities marketplace where AI agents discover, evaluate, and purchase skills via the x402 payment protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hockeyplaya48](https://clawhub.ai/user/hockeyplaya48) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to find Agent Bazaar capabilities, inspect pricing, prepare x402 API calls, delegate USDC payment execution to lobster.cash, and chain paid capabilities into larger workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward real USDC payments for Agent Bazaar API calls. <br>
Mitigation: Use demo mode first, require explicit approval for every real payment, and set a strict per-task budget before any paid call. <br>
Risk: Requests to remote services may disclose user data or task context. <br>
Mitigation: Do not submit secrets, private keys, proprietary source code, unreleased contracts, regulated data, or sensitive portfolio details unless disclosure is explicitly approved. <br>
Risk: Endpoint responses and generated outputs may be incorrect or unsuitable for the user's workflow. <br>
Mitigation: Review endpoint selection, inputs, payment requirements, and returned outputs before acting on results or chaining additional paid calls. <br>


## Reference(s): <br>
- [Agent Bazaar Skill Page](https://clawhub.ai/hockeyplaya48/agent-bazaar) <br>
- [Agent Bazaar](https://agent-bazaar.com) <br>
- [Complete Endpoint Catalog](references/endpoints.md) <br>
- [Programmatic Integration](references/sdk-usage.md) <br>
- [x402 Payment Protocol](references/x402-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, JSON, Python, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment-flow guidance, endpoint selection, request examples, SDK usage, and workflow chaining steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
