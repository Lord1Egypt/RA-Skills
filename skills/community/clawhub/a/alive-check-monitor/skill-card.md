## Description: <br>
提供独居用户每日签到和状态监测，长时间未签到时自动告警并通知紧急联系人。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhdryanchang](https://clawhub.ai/user/zhdryanchang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and caregivers use this skill to run a check-in service for people living alone, chronic-condition patients, travelers, or other users who need routine safety confirmation and escalation to emergency contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service is positioned as a safety-monitoring tool, but the authoritative security review says alerting is unreliable. <br>
Mitigation: Do not rely on it for real safety monitoring until emergency-alert delivery, escalation paths, and failure handling are tested end to end. <br>
Risk: The artifact includes an exposed SkillPay API key in configuration examples and skill metadata. <br>
Mitigation: Remove the embedded key, rotate it before use, and provide payment credentials only through protected environment variables or a secrets manager. <br>
Risk: The service handles sensitive user, check-in, phone, location, and emergency-contact data with inadequate data-protection evidence. <br>
Mitigation: Add authentication, authorization, encrypted storage, retention/deletion controls, and clear consent for monitored users and emergency contacts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhdryanchang/alive-check-monitor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhdryanchang) <br>
- [Skill README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Alive-check app article](https://www.bnext.com.tw/article/89759/alive-check-app) <br>
- [Product analysis article](https://www.woshipm.com/share/6323812.html) <br>
- [36Kr founder interview](https://m.36kr.com/p/3638430937910658) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API examples, shell commands, and JavaScript service configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Express service and scheduled status checks; requires Node.js, environment variables, and notifier/payment credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, skill.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
