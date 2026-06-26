## Description: <br>
飞书任务（Bot身份）：使用Bot/应用身份管理飞书任务，创建任务、查询任务列表、更新状态、分配成员等。本Skill专门使用v1 API，Bot身份可直接调用，解决了lark-task官方Skill使用v2接口无法支持Bot身份的问题。当需要以Bot身份（应用身份）操作任务时使用本Skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiang92229](https://clawhub.ai/user/lixiang92229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill when an agent needs to read Feishu/Lark task data through a bot or application identity instead of a user login. It is suited for listing tasks assigned to the bot through Feishu task v1 APIs using app credentials supplied by the host environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu app-level credentials to call Feishu APIs. <br>
Mitigation: Install only when the publisher is trusted with those credentials and provide only the least-privilege Feishu scopes needed for the task. <br>
Risk: Granting task write permission expands the potential impact of credential misuse even though the observed helper lists tasks. <br>
Mitigation: Avoid granting task write permission unless future write features are required, and review the referenced lark-shared authentication guidance before deployment. <br>


## Reference(s): <br>
- [lark-task-bot-get-my-tasks](references/lark-task-bot-get-my-tasks.md) <br>
- [Project homepage](https://github.com/lixiang92229/feishu-bot-task) <br>
- [ClawHub skill page](https://clawhub.ai/lixiang92229/feishu-bot-task) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON task results from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script emits JSON containing Feishu task items and a total count.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
