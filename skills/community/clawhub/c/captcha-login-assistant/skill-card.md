## Description:

Assists with CAPTCHA-protected web login workflows by using Chrome DevTools MCP screenshots, AI vision recognition, and form submission guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leungbh](https://clawhub.ai/user/leungbh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized administrators use this skill to complete CAPTCHA-protected login workflows for web systems they own or are explicitly permitted to administer or test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CAPTCHA-protected login automation can weaken anti-bot protections or be misused on third-party sites.

Mitigation: Use only on systems the operator owns or is explicitly authorized to administer or test, and avoid credential lists, password guessing, rate-limit evasion, or unauthorized third-party sites.

Risk: Screenshots and form-fill workflows may expose credentials or sensitive page content.

Mitigation: Do not log passwords, and delete screenshots or logs that may contain secrets after they are no longer needed.

Risk: Rapid retries can trigger security controls or drift into abusive behavior.

Mitigation: Prefer manual CAPTCHA completion where practical, use strict retry limits, and stop when repeated verification failures occur.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leungbh/skills/captcha-login-assistant)
- [ClawHub Publisher Profile](https://clawhub.ai/user/leungbh)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with JavaScript and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on an authorized target URL, credentials, Chrome DevTools MCP access, and screenshots captured during the workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
