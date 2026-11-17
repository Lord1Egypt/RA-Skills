## Description:

Aggregate logistics information from Taobao, JD, PDD, and Douyin for multi-platform order tracking with persistent cookie storage and QR code login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpf](https://clawhub.ai/user/charles-lpf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query authenticated shopping-platform logistics, review in-transit orders, and receive CLI commands for login and tracking across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses authenticated browser automation for shopping accounts and stores sensitive session and order data locally.

Mitigation: Install only when users accept access to authenticated shopping sessions, and require review or remediation of local cookie storage before use.

Risk: Security guidance flags plaintext cookie storage, a false encryption claim, and security-disabling Chromium flags.

Mitigation: Require fixes for cookie protection claims and browser launch settings before deployment in a trusted environment.

Risk: The skill advertises JD and Douyin but evidence says those paths are unsupported, and Douyin code writes debug captures to a hard-coded local path.

Mitigation: Limit supported execution to reviewed Taobao and PDD flows until unsupported platform paths and debug capture behavior are removed or corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charles-lpf/skills/ecommerce-logistics)
- [Platform selector reference](references/selectors.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; runtime CLI output is plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write QR-code screenshots and shopping-session cookie files under the configured data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
