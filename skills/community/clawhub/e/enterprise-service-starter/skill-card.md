## Description: <br>
企服助手一键初始化技能会在用户请求初始化或安装企服助手时，协助安装一组企业服务相关依赖技能并引导用户配置项目知识库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators setting up the 企服助手 workflow use this skill to bootstrap the required enterprise-service skills and prepare user-specific project knowledge-base configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change the local skills setup by installing or copying dependent skills. <br>
Mitigation: Install only when the publisher is trusted, review the dependency installation script first, and confirm each skill before adding it to the local environment. <br>
Risk: The workflow asks users to handle an Enterprise WeChat webhook URL, which is sensitive configuration. <br>
Mitigation: Store webhook values as secrets or environment variables and avoid committing them to project files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/enterprise-service-starter) <br>
- [Publisher profile](https://clawhub.ai/user/perrykono-debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation of dependent skills and setup of a user-specific project knowledge-base file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
