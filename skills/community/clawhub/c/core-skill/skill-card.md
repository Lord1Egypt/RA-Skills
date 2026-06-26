## Description: <br>
The base layer an AI agent runs on to be verifiable, accountable, and able to work with the world by adding a controlled Ed25519 identity, narrowed delegated authority, signed action receipts, and approval-gated connection workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeoess](https://clawhub.ai/user/aeoess) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill to give an AI agent a verifiable identity, scoped authority, signed receipts, and a controlled connection layer for approved interactions with people, companies, and other agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated identity keys, signed receipts, and optional tokens can expose sensitive identity or authorization data if mishandled. <br>
Mitigation: Store keys, receipts, and tokens as sensitive material; limit access and review any tool or package that handles them. <br>
Risk: External actions such as publishing, searching for matches, introductions, delegation, commerce, or identity sharing can affect third parties or disclose the principal's intent. <br>
Mitigation: Require explicit principal approval for each external action and use double opt-in before introductions exchange contact details. <br>
Risk: The skill depends on npm packages and remote services including MCP and API endpoints outside NVIDIA ownership. <br>
Mitigation: Review the package sources, endpoint behavior, and network permissions before deployment in a sensitive environment. <br>


## Reference(s): <br>
- [APS protocol surface](references/aps.md) <br>
- [Connection layer](references/connect.md) <br>
- [Durable accountable continuity](references/continuity.md) <br>
- [Agent Passport System on npm](https://www.npmjs.com/package/agent-passport-system) <br>
- [Agent Passport System MCP on npm](https://www.npmjs.com/package/agent-passport-system-mcp) <br>
- [Agent Passport System on PyPI](https://pypi.org/project/agent-passport-system/) <br>
- [Agent Passport System GitHub repository](https://github.com/aeoess/agent-passport-system) <br>
- [Remote MCP endpoint](https://mcp.aeoess.com/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and reference-module instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs the agent to load reference modules on demand and to require explicit approval for publishing, searching, introductions, delegation, commerce, identity sharing, and other external actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
