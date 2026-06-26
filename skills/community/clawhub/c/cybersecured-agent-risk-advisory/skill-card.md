## Description: <br>
为 AI智能体配置龙行无忧风险管家服务，协助用户完成认证、智能体绑定、安全扫描、风险评估、服务申请和事故信息提交，并在服务生效后协助保障查询和事故处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cybersecured-cn](https://clawhub.ai/user/cybersecured-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure Cybersecured's risk advisory service for AI agents, including authentication, agent binding, security scanning, risk assessment submission, service application, coverage lookup, and incident submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and transmit detailed agent-environment and security assessment data to the service provider. <br>
Mitigation: Use it only with explicit user approval, review generated assessment content before submission, and submit only the intended assessment directory to a trusted Cybersecured service account. <br>
Risk: The skill depends on sensitive credentials and stores API key configuration locally. <br>
Mitigation: Protect the local configuration file, avoid sharing workspaces that contain credential material, and run the documented logout flow or remove the stored API key when access is no longer needed. <br>
Risk: The artifact includes test-environment commands that can bypass SSL verification and references cloud metadata probes. <br>
Mitigation: Use the production endpoint for normal operation, do not use SSL-bypass options in production, and avoid metadata probing in production environments unless explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cybersecured-cn/cybersecured-agent-risk-advisory) <br>
- [Cybersecured AI service website](https://www.cybersecured.cn/ai) <br>
- [Questionnaire guide](artifact/references/questionnaire-guide.md) <br>
- [Questionnaire schema](artifact/references/questionnaire-schema.json) <br>
- [Risk factors format](artifact/references/risk-factors-format.md) <br>
- [Data storage specification](artifact/references/data-storage.md) <br>
- [Status handling guide](artifact/references/status-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON file instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local assessment and questionnaire JSON files for submission through the cybersecured-agent CLI.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
