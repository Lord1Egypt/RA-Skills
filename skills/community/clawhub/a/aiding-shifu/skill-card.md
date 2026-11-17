## Description:

Aiding Shifu helps agents find installation workers, manage login, and dispatch or review home decoration installation work orders on the Aiding Shifu platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinhuihua](https://clawhub.ai/user/yinhuihua)

### License/Terms of Use:

MIT-0

## Use Case:

External service teams, dealers, and operations staff use this skill to search for home decoration installation technicians, authenticate to the Aiding Shifu platform, dispatch work orders, and review order details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged credentials or account tokens may expose user accounts and related personal data.

Mitigation: Do not install until the packaged config secret is removed, the exposed token is revoked, and credentials are stored in a protected secret store with clear user consent.

Risk: Login flows may disclose raw tokens through displays, logs, clipboard handling, wildcard postMessage transfer, or third-party QR services.

Mitigation: Review the login flow before deployment, avoid logging or displaying raw tokens, restrict message targets, and stop sending login payloads to third-party QR services.

Risk: Work-order and technician workflows process names, phone numbers, addresses, and other service data.

Mitigation: Keep personal data masked in agent responses, collect only necessary fields, and confirm user consent before sending or storing work-order information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinhuihua/skills/aiding-shifu)
- [Aiding Shifu homepage](https://asf.dderp.cn)
- [Aiding Shifu API documentation](https://mes.dderp.cn/mob/swagger-ui/index.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline commands and structured API or work-order summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local login and token configuration when the user authenticates.]

## Skill Version(s):

3.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
