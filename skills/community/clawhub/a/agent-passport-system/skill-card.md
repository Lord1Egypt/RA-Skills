## Description: <br>
Agent Passport helps agents use cryptographic identity, scoped delegation, gateway enforcement, commerce controls, trust scoring, and signed audit receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeoess](https://clawhub.ai/user/aeoess) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to issue agent identities, delegate scoped authority, enforce policy boundaries, record signed work receipts, and audit multi-agent activity. It is most relevant when agent systems need accountable delegation, commerce controls, reputation signals, or cryptographic provenance for actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated passport files can contain private key material and signed identity data. <br>
Mitigation: Protect .passport/agent.json like a private SSH key and avoid committing it to source control. <br>
Risk: Setup can modify local agent-tool configuration and connect to remote MCP or Intent Network services. <br>
Mitigation: Review Claude Desktop and Cursor configuration changes and install only when external agent identity or governance services are intended. <br>
Risk: Delegation, checkout, public Agora posting, and intent-policy changes can have authority or spending impact. <br>
Mitigation: Require explicit confirmation before delegation, checkout, public posting, or policy changes. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/aeoess/agent-passport-system) <br>
- [Agent Passport System npm package](https://www.npmjs.com/package/agent-passport-system) <br>
- [Agent Passport System MCP npm package](https://www.npmjs.com/package/agent-passport-system-mcp) <br>
- [Remote MCP endpoint](https://mcp.aeoess.com/sse) <br>
- [Intent Network API](https://api.aeoess.com) <br>
- [Agent Passport documentation](https://aeoess.com/llms-full.txt) <br>
- [Agent Passport paper](https://doi.org/10.5281/zenodo.18749779) <br>
- [Agent Passport System PyPI package](https://pypi.org/project/agent-passport-system/) <br>
- [Project repository link from artifact](https://github.com/aeoess/agent-passport-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples, TypeScript snippets, MCP setup commands, and generated identity, delegation, receipt, and proof artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to create .passport/agent.json, signed delegations, signed receipts, Merkle proofs, and Claude Desktop or Cursor MCP configuration.] <br>

## Skill Version(s): <br>
5.9.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
