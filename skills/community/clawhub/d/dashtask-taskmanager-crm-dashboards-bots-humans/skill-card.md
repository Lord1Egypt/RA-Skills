## Description: <br>
Manage tasks, CRM leads, contacts, and settings via the DashTask REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sstrohl223](https://clawhub.ai/user/sstrohl223) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, sales and operations teams, and AI agent developers use this skill to manage DashTask tasks, projects, CRM records, notifications, dimensions, and related emails through the DashTask API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real changes to tasks, CRM records, settings, notifications, and outbound emails. <br>
Mitigation: Use a dedicated DashTask API key with only the scopes needed, and require clear user approval before deleting records, changing dimensions or settings, creating notifications, or sending emails. <br>
Risk: Requests sent to the wrong endpoint could affect the wrong DashTask organization. <br>
Mitigation: Verify DASHTASK_ENDPOINT belongs to the intended DashTask organization before enabling the skill. <br>


## Reference(s): <br>
- [DashTask](https://dashtask.ai) <br>
- [ClawHub skill page](https://clawhub.ai/sstrohl223/dashtask-taskmanager-crm-dashboards-bots-humans) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown API reference with JSON payload examples and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHTASK_API_KEY and DASHTASK_ENDPOINT; API key scopes determine available actions.] <br>

## Skill Version(s): <br>
1.9.1 (source: SKILL.md frontmatter and clawfile.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
