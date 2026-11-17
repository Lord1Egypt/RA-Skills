## Description:

Manage and automate DuoPlus Android cloud phones through the official OpenAPI and the synchronous HTTP Gateway. Use when an AI needs to discover cloud phones, inspect status/details, initialize a proxy, start/stop/restart a phone, wait until it is controllable, read UI state or screenshots, complete Android UI actions, or run an explicitly authorized shell command on a cloud phone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duoplusofficial](https://clawhub.ai/user/duoplusofficial)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this agent skill to manage DuoPlus cloud-phone lifecycle and perform explicitly authorized Android UI automation on running phones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed when supplied in conversation or command-line arguments.

Mitigation: Use a protected credential method when available, and do not echo or persist the key.

Risk: The security scan is partial, flags broad environment and network capabilities, and could not resolve three local references.

Mitigation: Review the unresolved references before installation and limit use to explicitly requested phone operations.

## Reference(s):

- [Automation actions](references/automation-actions.md)
- [DuoPlus control API and routing](references/control-api.md)
- [DuoPlus interface introduction](https://help.duoplus.cn/docs/introduction)
- [DuoPlus cloud phone list API](https://help.duoplus.cn/docs/cloud-phone-list)
- [DuoPlus cloud phone status API](https://help.duoplus.cn/docs/cloud-phone-status)
- [DuoPlus proxy initialization](https://help.duoplus.cn/docs/proxy-init)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, JSON, UI observations and screenshots]

**Output Format:** [Command-line invocations, JSON responses, and Android UI observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshots when requested for visual verification.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
