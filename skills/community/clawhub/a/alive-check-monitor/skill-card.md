## Description:

Provides a daily check-in and status monitoring service for people living alone, with automatic alerts to emergency contacts after prolonged inactivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhdryanchang](https://clawhub.ai/user/zhdryanchang)

### License/Terms of Use:

MIT

## Use Case:

Developers and service operators can use this skill to run a check-in API for people living alone, allowing users to register emergency contacts, submit daily check-ins, review status history, and trigger inactivity alerts. The service should be treated as an isolated prototype until the documented security controls and alert reliability requirements are addressed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive user, location, phone, and emergency-contact data may be exposed because the security evidence reports missing authentication and per-user authorization.

Mitigation: Add authenticated endpoints, per-user authorization checks, HTTPS deployment guidance, and least-privilege access controls before handling real users.

Risk: Stored personal data and operational secrets may be exposed if local files or configured tokens are not protected.

Mitigation: Use encrypted and access-controlled storage, keep secrets out of committed files, rotate exposed or shared credentials, and define consent and retention policies.

Risk: Emergency notifications may be unreliable, which could create false confidence in a safety-monitoring workflow.

Mitigation: Verify alert delivery for each configured channel, add delivery acknowledgements and escalation handling, and avoid relying on the service for real safety monitoring until tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhdryanchang/skills/alive-check-monitor)
- [Business Next article on alive-check apps](https://www.bnext.com.tw/article/89759/alive-check-app)
- [Woshipm product analysis of alive-check apps](https://www.woshipm.com/share/6323812.html)
- [36Kr interview about an alive-check app](https://m.36kr.com/p/3638430937910658)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation, JSON API examples, shell commands, and JavaScript service code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs an Express-based check-in service, persists user and check-in records locally, and sends notifications through configured Telegram, Discord, and email channels.]

## Skill Version(s):

1.0.1 (source: server release metadata, artifact skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
