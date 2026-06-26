## Description: <br>
Manage Feishu and Lark tasks by creating, listing, completing, commenting on, and organizing to-dos with assignees, due dates, and checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, knowledge workers, and AI developers use this skill to manage Feishu or Lark workspace tasks from an agent workflow, including creating tasks, assigning work, checking due dates, marking tasks complete, and adding comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, complete, comment on, or assign real tasks in a Feishu or Lark workspace. <br>
Mitigation: Require user confirmation before creating, completing, bulk-assigning, or otherwise changing tasks. <br>
Risk: The skill requires a Feishu App ID and App Secret, which are sensitive credentials. <br>
Mitigation: Use a least-privilege Feishu app, protect the App Secret, and do not paste real secrets into chats or repositories. <br>
Risk: Installing the wrong package could give an unintended skill access to workspace task workflows. <br>
Mitigation: Verify the package slug and publisher profile before installation. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [ClawHub release page](https://clawhub.ai/a3152557994-ship-it/feishu-task-mgr) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Markdown] <br>
**Output Format:** [Markdown and agent actions that call the Feishu/Lark Task API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and task permissions before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
