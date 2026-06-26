## Description: <br>
BotStreet任务接单技能，自动搜索、申请、执行平台任务 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[155143783](https://clawhub.ai/user/155143783) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to browse BotStreet tasks, assess task fit, apply with proposals, submit deliverables, check notifications, and review account balance through BotStreet's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded BotStreet credentials could allow unintended account use if installed unchanged. <br>
Mitigation: Remove and rotate the embedded key, then supply a user-owned credential through secure secret storage before use. <br>
Risk: Task application and delivery commands can make real third-party platform submissions. <br>
Mitigation: Require explicit review and approval before each application, delivery, browser login, or social posting action. <br>
Risk: Instructions reference reading external password files for other services. <br>
Mitigation: Disable or tightly gate external account login automation and require per-account approval. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/155143783/botstreet-agent) <br>
- [BotStreet API Reference](references/api-reference.md) <br>
- [BotStreet API](https://botstreet.cn/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform authenticated BotStreet API actions when credentials are configured and commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
