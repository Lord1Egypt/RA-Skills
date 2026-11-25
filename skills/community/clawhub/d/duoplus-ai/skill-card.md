## Description:

Manage and automate DuoPlus Android cloud phones through the official OpenAPI and the synchronous HTTP Gateway. Use when an AI needs to discover cloud phones, inspect status/details, initialize a proxy, start/stop/restart a phone, wait until it is controllable, read UI state or screenshots, complete Android UI actions, or run an explicitly authorized shell command on a cloud phone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duoplusofficial](https://clawhub.ai/user/duoplusofficial)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage authorized DuoPlus cloud phones and complete requested Android UI tasks through DuoPlus services. It provides lifecycle, status, proxy, UI automation, and explicitly authorized device-shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured API endpoint could receive an API key or bearer token.

Mitigation: Use the documented DuoPlus production endpoint and review any DUOPLUS_API_BASE override before sending credentials.

Risk: Passing an API key as a command-line argument may expose it in process listings or logs.

Mitigation: Use secure DUOPLUS_API_KEY injection or a private key file with --api-key-file; do not pass the key as an argument or paste it into chat.

## Reference(s):

- [Credential setup](references/credentials.md)
- [HTTP Gateway automation actions](references/automation-actions.md)
- [DuoPlus control API and routing](references/control-api.md)
- [DuoPlus interface introduction](https://help.duoplus.cn/docs/introduction)
- [DuoPlus cloud phone API documentation](https://help.duoplus.cn/docs/cloud-phone-list)
- [DuoPlus execute command documentation](https://help.duoplus.cn/docs/execute-the-adb-command)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Screenshots]

**Output Format:** [JSON responses, screenshots, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform cloud phone lifecycle or UI actions when explicitly requested; actions return status and result data.]

## Skill Version(s):

1.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
