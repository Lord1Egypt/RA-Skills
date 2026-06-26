## Description: <br>
Ag-earth helps agents discover, select, validate, and execute external tools through Agent Earth for real-time news, decision support, data retrieval, and multi-step tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanminghui](https://clawhub.ai/user/shanminghui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use Ag-earth to route user requests to Agent Earth tool recommendation and execution APIs when a task needs current information, external data, or a specialized tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User requests and task context are sent to a remote Agent Earth service that can select and execute external tools with an API key. <br>
Mitigation: Use a dedicated revocable API key with quotas, avoid confidential prompts, and review the selected tool and arguments before execution. <br>
Risk: Recommended tools may return incorrect current data or perform side-effecting actions depending on the selected tool. <br>
Mitigation: Validate required parameters, ask follow-up questions for missing inputs, and require confirmation for finance, account changes, purchases, file conversion, or other side-effecting tasks. <br>


## Reference(s): <br>
- [Agent Earth API Specification](artifact/references/api-spevification.md) <br>
- [Agent Earth Website](https://agentearth.ai/) <br>
- [ClawHub Skill Page](https://clawhub.ai/shanminghui/ag-earth) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, text] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENT_EARTH_API_KEY; remote results depend on the selected Agent Earth tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
