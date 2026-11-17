## Description:

Manages the OpenClaw agent lifecycle, including agent configuration, Matrix account registration, and account binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxlhyx](https://clawhub.ai/user/cxlhyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw use this skill to add or remove agents, register Matrix accounts, bind accounts to agents, and run one-command setup against a configured homeserver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Matrix credentials in ways that could expose or weaken them.

Mitigation: Review before installing, use only against a trusted local Matrix server unless HTTPS is enforced, and rotate accounts created by the setup flow.

Risk: Access tokens may be printed or stored in OpenClaw configuration.

Mitigation: Avoid logging access-token output and restrict permissions on ~/.openclaw/openclaw.json because it stores bearer tokens.

Risk: Predictable account passwords can reduce account security.

Mitigation: Replace or rotate any accounts created with the predictable password pattern before normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxlhyx/skills/agent-manager-hxx)
- [Publisher profile](https://clawhub.ai/user/cxlhyx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that create Matrix accounts and modify ~/.openclaw/openclaw.json.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
