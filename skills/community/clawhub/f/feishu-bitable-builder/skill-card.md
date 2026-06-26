## Description: <br>
Helps an agent design and build Feishu Bitable systems from business requirements, including table architecture, field configuration, views, automation workflows, dashboards, permissions, testing, and handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[664624249](https://clawhub.ai/user/664624249) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, builders, and developers use this skill to turn CRM, project management, inventory, task tracking, data collection, and custom workflow requirements into Feishu Bitable app designs and configuration steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automations or outbound HTTP and webhook actions may expose business or personal data outside Feishu. <br>
Mitigation: Before enabling automations, review outbound endpoints, AI inputs, and the fields included in each action. <br>
Risk: Broad robot edit permissions may remain after setup or maintenance. <br>
Mitigation: Reduce robot edit access after handoff and confirm ownership and field-level permissions with the user. <br>
Risk: Generated table, permission, or automation plans may not match the organization's operating controls. <br>
Mitigation: Review delete actions, permission scopes, and workflow behavior before deploying to production data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/664624249/feishu-bitable-builder) <br>
- [Feishu Bitable field types reference](references/field-types.md) <br>
- [Feishu Bitable view types guide](references/view-types.md) <br>
- [Feishu Bitable automation and workflows](references/automation.md) <br>
- [Feishu Bitable dashboard design](references/dashboard.md) <br>
- [Feishu Bitable functions guide](references/functions.md) <br>
- [Feishu Bitable best practices](references/best-practices.md) <br>
- [Feishu Bitable scenarios](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline tool command examples and configuration checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu Bitable app structure, table schemas, field definitions, view plans, automation rules, dashboard recommendations, permission guidance, and delivery checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
