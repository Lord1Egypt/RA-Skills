## Description: <br>
Automate Box cloud storage operations including file upload/download, search, folder management, sharing, collaborations, and metadata queries via Rube MCP (Composio). Always search tools first for current schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate Box through Rube MCP, including upload and download workflows, content search, folder management, sharing, collaborations, metadata queries, and Box Sign request management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real Box files and sharing settings through a connected account. <br>
Mitigation: Use the least-privileged Box account that fits the task and require explicit confirmation before recursive deletes, permanent deletes, sensitive downloads, or sharing changes. <br>
Risk: Incorrect file, folder, or collaboration identifiers can target the wrong Box resource. <br>
Mitigation: Verify file and folder IDs before changes and search current tool schemas before executing workflows. <br>


## Reference(s): <br>
- [Box Automation ClawHub Page](https://clawhub.ai/sohamganatra/box-automation) <br>
- [Rube MCP Endpoint](https://rube.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with MCP tool sequences, parameters, and operational notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active Box connection through Rube MCP and current tool schema lookup before workflow execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
