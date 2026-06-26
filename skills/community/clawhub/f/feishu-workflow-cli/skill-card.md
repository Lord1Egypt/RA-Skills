## Description: <br>
Orchestrate complex Feishu/Lark workflows using the official lark CLI for reporting, project management, meeting automation, document collaboration, and cross-domain operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and operations teams use this skill to plan and execute Feishu/Lark workflows that combine chat, docs, Base, Sheets, calendar, mail, tasks, meetings, wiki, drive, and approvals. It helps an agent choose workflow templates, compose command chains, and apply safety checks before performing authenticated business actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated workflows can send messages or email, share links, update records, create approvals, and join or monitor meetings. <br>
Mitigation: Require explicit user confirmation before send, share, meeting, approval, record-update, or external-email actions, and verify recipients and link permissions before execution. <br>
Risk: Automating reports or meeting workflows may expose confidential business content. <br>
Mitigation: Avoid confidential meetings or reports unless the organization has approved the automation controls and the agent is operating under appropriate access permissions. <br>


## Reference(s): <br>
- [Feishu Workflow CLI on ClawHub](https://clawhub.ai/lm203688/feishu-workflow-cli) <br>
- [Lark CLI Changelog](https://github.com/larksuite/cli/blob/main/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workflow steps, command examples, prerequisite checks, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
