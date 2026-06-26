## Description: <br>
提供独居人群每日签到与自动监测，支持多渠道紧急通知，保障用户安全与健康状态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhdryanchang](https://clawhub.ai/user/zhdryanchang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users can run a daily safety check-in service for people living alone, chronic-care patients, travelers, or other people who need periodic wellbeing confirmation and escalation to emergency contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service handles sensitive safety, contact, location, and wellbeing data with weak documented controls. <br>
Mitigation: Use dummy data until authentication, consent, retention, storage encryption, and key-management controls are implemented and reviewed. <br>
Risk: The release includes a live-looking SkillPay API key in configuration examples and metadata. <br>
Mitigation: Treat the key as exposed, revoke or rotate it before deployment, and provide secrets only through a private runtime environment. <br>
Risk: Emergency notification behavior is safety-critical and may not send the intended alert content or reach the intended contacts. <br>
Mitigation: Test each notification channel with representative contacts and alert states before relying on it for real people. <br>
Risk: The documentation makes privacy and encryption claims that are not fully supported by the reviewed implementation evidence. <br>
Mitigation: Do not rely on those claims until the storage and privacy design is implemented, documented, and independently reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhdryanchang/daily-alive-check) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [「死了麼」被評為「痛點99分、功能1分」，為什麼中國年輕人狂下載？](https://www.bnext.com.tw/article/89759/alive-check-app) <br>
- ["死了么"App为何能火？一个产品经理的冷拆解](https://www.woshipm.com/share/6323812.html) <br>
- [估值9000万？独家对话"死了么"APP创始人](https://m.36kr.com/p/3638430937910658) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with JSON examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces service setup and API usage guidance for a Node.js daily check-in and alerting service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
