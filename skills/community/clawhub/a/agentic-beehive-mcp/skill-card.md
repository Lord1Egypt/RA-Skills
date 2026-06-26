## Description: <br>
Agentic Beehive MCP Server provides situational awareness, branch scheduling, and external colony management for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hon27hon](https://clawhub.ai/user/hon27hon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this MCP server to track agent branch state, choose task-delivery or state-maintenance patterns, register external endpoints, and summarize active alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server stores branch, colony, alert, and evolution state in a local SQLite database. <br>
Mitigation: Avoid storing secrets in metadata or alerts, and periodically review or clear the local beehive.db state. <br>
Risk: Registered external endpoints can be contacted for colony status checks. <br>
Mitigation: Register only trusted endpoints and review endpoint behavior before polling. <br>
Risk: The runtime depends on fastmcp, which is installed separately. <br>
Mitigation: Pin or review the fastmcp dependency before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hon27hon/agentic-beehive-mcp) <br>
- [Publisher Profile](https://clawhub.ai/user/hon27hon) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [JSON responses from MCP tools plus Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and pip; runtime behavior depends on fastmcp and locally registered endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README version entry) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
