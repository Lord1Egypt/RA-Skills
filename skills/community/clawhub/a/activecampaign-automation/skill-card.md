## Description: <br>
Automate ActiveCampaign tasks via Rube MCP (Composio): manage contacts, tags, list subscriptions, automation enrollment, and tasks. Always search tools first for current schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through ActiveCampaign CRM and marketing workflows, including contact management, tagging, list subscription changes, automation enrollment, and contact task creation through Rube MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real changes to ActiveCampaign contacts, tags, list subscriptions, automations, and tasks. <br>
Mitigation: Confirm exact contacts, list IDs, tags, automation IDs, and marketing consent before mutating actions; use a limited or test account where practical. <br>
Risk: Tool schemas or ActiveCampaign IDs may be stale or account-specific. <br>
Mitigation: Call RUBE_SEARCH_TOOLS first for current schemas and verify IDs in ActiveCampaign before executing workflows. <br>
Risk: Bulk changes may hit ActiveCampaign account rate limits. <br>
Mitigation: Batch operations with reasonable delays and backoff on rate-limit responses. <br>


## Reference(s): <br>
- [Rube MCP](https://rube.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with MCP tool names, parameter notes, and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agent use of Rube MCP tools for ActiveCampaign workflows.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
