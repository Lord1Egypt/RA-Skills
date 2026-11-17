## Description:

Helps developers receive Alipay asynchronous payment notifications in local or CI environments by using a cloud relay and Python CLI for registration, listening, raw payload export, and local RSA2 verification.

This skill is for research and development only.

## Publisher:

[zhangke091](https://clawhub.ai/user/zhangke091)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to debug Alipay payment callbacks when their local or CI environment has no public notify_url. It supports sandbox and internal integration testing by registering a relay URL, listening for notifications, exporting raw payloads, and verifying signatures locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment notification payloads and relay credentials may pass through an unencrypted third-party HTTP relay.

Mitigation: Use only sandbox or test notification payloads unless the relay is moved to HTTPS and the operator is trusted for the data involved.

Risk: Local relay credentials and public-key configuration are stored in .alipay-notify.json.

Mitigation: Keep .alipay-notify.json out of source control, restrict local file permissions, and rotate relay credentials if exposure is suspected.

Risk: The artifact is documented for integration, sandbox, and internal debugging rather than production payment processing.

Mitigation: Do not send real customer payment data through this skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangke091/skills/alipay-notify)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .alipay-notify.json configuration and exported notify_<id>.txt payload files during agent execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
