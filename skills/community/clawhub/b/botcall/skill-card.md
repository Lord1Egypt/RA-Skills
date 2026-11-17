## Description:

Phone numbers for AI agents. Provision numbers, receive SMS, extract verification codes. Use when you need to sign up for services, receive 2FA codes, or handle phone verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danecodes](https://clawhub.ai/user/danecodes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide agents through Botcall CLI and MCP workflows for provisioning phone numbers, receiving SMS messages, extracting verification codes, and managing plan or billing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may run signup, 2FA, upgrade, or billing commands without enough user control.

Mitigation: Require explicit confirmation before executing phone verification, plan upgrade, or billing commands.

Risk: The skill requires a Botcall API key for phone-number and SMS workflows.

Mitigation: Use a minimally scoped Botcall API key and avoid exposing the key in logs, prompts, or shared configuration.

Risk: Phone numbers and SMS codes can be misused for account workflows the user does not own or control.

Mitigation: Use the skill only for phone numbers, SMS codes, and account workflows the user owns or is authorized to manage.

## Reference(s):

- [Botcall Website](https://botcall.io)
- [botcall npm CLI](https://www.npmjs.com/package/botcall)
- [Botcall MCP npm Package](https://www.npmjs.com/package/@botcallio/mcp)
- [ClawHub Publisher Profile](https://clawhub.ai/user/danecodes)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that can affect phone-number allocation, SMS access, plan upgrades, and billing; require explicit user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
