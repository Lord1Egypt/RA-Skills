## Description: <br>
当需要查询阿里云日志（SLS）时使用此技能，支持 CLI 查询日志、分析数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeweis](https://clawhub.ai/user/jeweis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Aliyun Log Service CLI access, query SLS logs with bounded SQL searches, and inspect returned log data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to work with Aliyun SLS access credentials. <br>
Mitigation: Use dedicated read-only RAM or temporary credentials scoped to the required projects and logstores, and avoid passing long-lived keys in chat or shell command arguments. <br>
Risk: The skill includes broader SLS command guidance that could be used for create, update, or delete operations. <br>
Mitigation: Approve only log-query operations unless resource changes are explicitly intended and reviewed. <br>
Risk: Unbounded log queries can expose excessive data or overload the agent context. <br>
Mitigation: Keep time ranges narrow and use LIMIT clauses, following the skill's default limit guidance. <br>


## Reference(s): <br>
- [Project mapping reference](references/project_mapping.md) <br>
- [ClawHub skill page](https://clawhub.ai/jeweis/aliyun-log-query) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries should use limited time ranges and LIMIT clauses to avoid excessive output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
