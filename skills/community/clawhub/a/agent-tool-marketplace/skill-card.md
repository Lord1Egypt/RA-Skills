## Description: <br>
Agent Tool Marketplace helps agents discover AgentPMT marketplace tools, inspect schemas and pricing, invoke selected third-party tools with wallet-signed requests, and consume responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover paid AgentPMT marketplace tools, prepare wallet authentication, sign requests, invoke matching actions, and handle marketplace responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through wallet-signed requests and paid marketplace actions. <br>
Mitigation: Confirm the selected product, action, parameters, request signature, and credit spend before invoking a paid tool. <br>
Risk: The skill requires sensitive wallet and session authentication material. <br>
Mitigation: Use only the intended wallet, protect private keys and session nonces, and generate fresh request identifiers to avoid replay errors. <br>


## Reference(s): <br>
- [AgentPMT External Agent API](https://www.agentpmt.com/external-agent-api) <br>
- [AgentPMT Marketplace](https://www.agentpmt.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/agent-tool-marketplace) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, API calls] <br>
**Output Format:** [Markdown with Python and text code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint workflow, request signing guidance, marketplace invocation steps, and error handling guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
