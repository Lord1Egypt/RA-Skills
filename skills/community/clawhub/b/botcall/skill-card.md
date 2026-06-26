## Description: <br>
Phone numbers for AI agents. Provision numbers, receive SMS, extract verification codes. Use when you need to sign up for services, receive 2FA codes, or handle phone verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danecodes](https://clawhub.ai/user/danecodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to provision Botcall phone numbers, receive SMS messages, extract verification codes, and configure Botcall MCP access for phone verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose SMS messages and verification codes to an agent. <br>
Mitigation: Require explicit approval before retrieving, displaying, or entering codes, and use it only for accounts or services the user owns or is authorized to verify. <br>
Risk: Number provisioning, release, plan upgrades, and billing actions can change account state or incur charges. <br>
Mitigation: Require explicit approval before provisioning or releasing numbers, opening billing, or upgrading plans. <br>
Risk: BOTCALL_API_KEY and received SMS codes are sensitive credentials. <br>
Mitigation: Store the API key in an environment or secret manager, avoid logging secrets or codes, and rotate credentials if exposed. <br>


## Reference(s): <br>
- [Botcall website](https://botcall.io) <br>
- [botcall npm CLI](https://www.npmjs.com/package/botcall) <br>
- [Botcall MCP npm package](https://www.npmjs.com/package/@botcallio/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/danecodes/botcall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOTCALL_API_KEY and the botcall CLI; may output phone numbers, SMS messages, and verification codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
