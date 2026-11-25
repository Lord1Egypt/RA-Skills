## Description:

Give this agent its own US or Canadian phone number, read the verification codes texted to it, and have an AI voice assistant phone a business for your human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perqele](https://clawhub.ai/user/perqele)

### License/Terms of Use:

MIT-0

## Use Case:

An agent uses Dial to obtain a US or Canadian phone number, receive verification codes, and place AI voice calls to businesses on a human's behalf.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: Setup may send an accessible email address to an external provider during signup without first warning the user or getting approval.

Mitigation: Before calling sign_up, confirm the user approves sharing the chosen email address with the provider; use an inbox selected for this purpose.

## Reference(s):

- [Dial by Aloha Labs](https://alohalabshq.com/dial/)
- [Dial pricing](https://alohalabshq.com/dial/#pricing)
- [Dial MCP server](https://aloha-dial-api.onrender.com/mcp)
- [Help and project page linked in the skill](https://github.com/perqele/dial-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Text responses containing phone numbers, verification codes, messages, call results, and account information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the Dial account, available numbers, and received messages or call outcomes.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
