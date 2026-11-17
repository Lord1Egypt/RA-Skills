## Description:

Automate ActiveCampaign tasks via Rube MCP (Composio), including contact management, tag changes, list subscriptions, automation enrollment, and task creation while prompting agents to search current tool schemas first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide ActiveCampaign CRM workflows through Rube MCP, including contact lookup and creation, tag changes, list subscription changes, automation enrollment, and contact task creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live ActiveCampaign operations can change customer records, list subscriptions, tags, automation enrollment, and tasks.

Mitigation: Use a least-privilege ActiveCampaign account and require explicit confirmation before any mutation or bulk operation.

Risk: Incorrect contact, list, automation, or task IDs can apply changes to the wrong record or workflow.

Mitigation: Verify contacts and IDs before mutation, and search current tool schemas before running workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sohamganatra/skills/activecampaign-automation)
- [Rube MCP Server](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands]

**Output Format:** [Markdown with inline tool names, parameters, and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Rube MCP and an active ActiveCampaign connection.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
