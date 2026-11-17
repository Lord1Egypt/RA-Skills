## Description:

Skill to call Cloud API for Tencent Cloud (腾讯云). Used for cloud automation or resource management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2513483494](https://clawhub.ai/user/2513483494)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to work with Tencent Cloud APIs through tccli, including installation, browser-based authentication, API documentation lookup, and command construction for cloud automation or resource management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation, browser login, or cloud-changing tccli commands could affect the user's local environment or Tencent Cloud account.

Mitigation: Use trusted or reviewed tccli installation sources, require deliberate user approval before authentication or create, modify, and delete commands, and confirm the intended account and profile before execution.

Risk: SecretId, SecretKey, or stored credential output could be exposed if credential inspection commands are run or users paste secrets into chat.

Mitigation: Do not request Tencent Cloud SecretId or SecretKey values, and do not run commands that print stored credentials such as tccli configure list.

## Reference(s):

- [Tencent Cloud API reference index](https://cloudcache.tencentcs.com/capi/refs/services.md)
- [Tencent Cloud CVM best practices](https://cloudcache.tencentcs.com/capi/refs/service/cvm/practices.md)
- [Tencent Cloud CVM API actions](https://cloudcache.tencentcs.com/capi/refs/service/cvm/actions.md)
- [Tencent Cloud CVM ResizeInstanceDisks API](https://cloudcache.tencentcs.com/capi/refs/service/cvm/action/ResizeInstanceDisks.md)
- [Tencent Cloud CVM SystemDisk model](https://cloudcache.tencentcs.com/capi/refs/service/cvm/model/SystemDisk.md)
- [Install TCCLI](references/install.md)
- [Configure TCCLI credentials](references/auth.md)
- [API reference lookup steps](references/refs.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require user-approved Tencent Cloud authentication and should be executed sequentially because the skill evidence notes tccli configuration-file contention during parallel calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
