## Description: <br>
Generates Android configuration-pull code templates for configuration center, whitelist, standalone API, and push-pull integration flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hefuwei-95](https://clawhub.ai/user/hefuwei-95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Android configuration retrieval code, including managers, task or service interfaces, notification registration, and PluginModule lifecycle hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated code can edit Android project files and PluginModule lifecycle hooks. <br>
Mitigation: Review the generated diff before committing and confirm lifecycle hook names, call timing, and module placement. <br>
Risk: Generated integrations may include API URLs, push keys, credential references, or logging of configuration values. <br>
Mitigation: Validate URLs, keys, credential references, and logging behavior before accepting the changes. <br>


## Reference(s): <br>
- [配置拉取代码生成](https://clawhub.ai/hefuwei-95/config-pull-template) <br>
- [配置中心 Manager 模板](references/config-center-template.md) <br>
- [白名单 Manager 模板](references/whitelist-template.md) <br>
- [单独接口 Manager 模板](references/api-template.md) <br>
- [推拉结合 Manager 模板](references/push-pull-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Kotlin and Java code written into workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Android configuration integration code and PluginModule lifecycle hooks based on user-supplied configuration details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
