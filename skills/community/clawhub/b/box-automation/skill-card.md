## Description:

Automate Box cloud storage operations including file upload/download, search, folder management, sharing, collaborations, and metadata queries via Rube MCP (Composio). Always search tools first for current schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide agents through Box storage workflows via Rube MCP, including file transfer, search, folder administration, sharing, collaboration management, metadata queries, and sign request handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete, permanent removal, sharing, and collaborator role changes can affect cloud files and access permissions.

Mitigation: Verify the item ID, target user or link scope, and permission level before those actions; prefer reversible trash moves unless permanent deletion is intended.

Risk: Stale Box tool schemas can lead to failed or unintended operations.

Mitigation: Search Rube tools first and confirm the current schema before executing each workflow.

## Reference(s):

- [Box Automation on ClawHub](https://clawhub.ai/sohamganatra/skills/box-automation)
- [Rube MCP endpoint](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Tool calls]

**Output Format:** [Markdown guidance with ordered MCP tool sequences, parameter notes, and operational cautions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Box connection through Rube MCP and current tool schemas from RUBE_SEARCH_TOOLS before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
