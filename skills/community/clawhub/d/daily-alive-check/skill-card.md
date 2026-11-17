## Description:

Provides a daily check-in monitoring service for people living alone, with scheduled status checks and emergency-contact notifications after extended inactivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhdryanchang](https://clawhub.ai/user/zhdryanchang)

### License/Terms of Use:

MIT

## Use Case:

Developers and service operators can run this skill as an API-backed welfare check service for users who need daily safety confirmation and escalation to emergency contacts. It is intended for solo residents, chronic-disease patients, and travelers, but requires security review before real users are onboarded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published artifacts expose a SkillPay credential.

Mitigation: Remove the credential from artifacts, rotate the key, and load payment secrets only from a managed secret store or deployment environment.

Risk: Sensitive welfare-check, location, phone, and emergency-contact data can be accessed or changed without documented authentication or per-user authorization.

Mitigation: Require authentication on all user endpoints and enforce per-user authorization before registration, check-in, status, history, or contact changes.

Risk: Stored user data may not match the documented privacy claims.

Mitigation: Encrypt or otherwise protect stored data, define retention and deletion behavior, and document user consent before production use.

Risk: Emergency-alert delivery may fail or send mismatched notification content.

Mitigation: Fix and test each notifier path with realistic emergency-contact data before relying on the service for safety escalation.

Risk: Broad CORS and flagged dependencies increase deployment exposure.

Mitigation: Restrict allowed origins to trusted clients and update dependencies before exposing the service to real users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhdryanchang/skills/daily-alive-check)
- [「死了麼」被評為「痛點99分、功能1分」，為什麼中國年輕人狂下載？](https://www.bnext.com.tw/article/89759/alive-check-app)
- ["死了么"App为何能火？一个产品经理的冷拆解](https://www.woshipm.com/share/6323812.html)
- [估值9000万？独家对话"死了么"APP创始人](https://m.36kr.com/p/3638430937910658)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown documentation, shell command examples, configuration values, Node.js service code, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs an HTTP service with registration, check-in, status, history, and emergency-contact endpoints plus scheduled monitoring.]

## Skill Version(s):

1.0.1 (source: evidence release, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
