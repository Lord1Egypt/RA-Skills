## Description:

Security self-check for Clawdbot/Moltbot that audits clawdbot.json for exposed gateway binding, missing authentication, permissive DM or group policies, weak tokens, loose file permissions, and plaintext secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterokase42](https://clawhub.ai/user/peterokase42)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to audit a local Clawdbot/Moltbot configuration for common security misconfigurations and to review optional fixes before applying them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects ~/.clawdbot/clawdbot.json, which may contain local tokens or other secrets.

Mitigation: Run it only when you intend to grant the agent access to that file, and review the generated security report before approving any fixes.

Risk: The auto-fix backup file ~/.clawdbot/clawdbot.json.bak may retain old tokens or other secrets.

Mitigation: After auto-fix, verify whether the backup is still needed and remove or protect it if it contains sensitive values.

Risk: Token replacement changes gateway credentials and can disconnect paired clients until they are updated.

Mitigation: Confirm token-changing fixes deliberately, restart the gateway, and update paired clients with the new token.

## Reference(s):

- [Dont Hack Me ClawHub Skill Page](https://clawhub.ai/peterokase42/skills/dont-hack-me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown security report with PASS, WARN, FAIL, and SKIP statuses, plus optional fix guidance after user confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect ~/.clawdbot/clawdbot.json and propose or apply targeted configuration changes only after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
