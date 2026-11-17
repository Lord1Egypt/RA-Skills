## Description:

Places user-approved phone calls to Indian (+91) numbers, asks questions in the selected language, and reports what the person said.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theindianappguy](https://clawhub.ai/user/theindianappguy)

### License/Terms of Use:

MIT

## Use Case:

External users can ask the agent to place confirmed calls to Indian contacts for reminders, appointment checks, and questions to shops, clinics, or vendors. The agent reports call outcomes and answers afterward.

### Deployment Geography for Use:

India (+91 numbers only)

## Known Risks and Mitigations:

Risk: Calls use account minutes and can create recordings and transcripts that may contain sensitive information.

Mitigation: Confirm the recipient and message before every call, share only necessary details, and review the privacy policy and retention terms before use.

Risk: The CLI installation instructions fetch code from GitHub without pinning a revision.

Mitigation: Prefer the hosted MCP connection or review and pin a CLI revision before installing it.

## Reference(s):

- [CallSimple MCP server](https://callsimple.app/mcp)
- [CallSimple information and signup](https://callsimple.app/?ref=skill)
- [CallSimple ClawHub release](https://clawhub.ai/theindianappguy/skills/callsimple)

## Skill Output:

**Output Type(s):** [API Calls, Text, Shell commands, Configuration instructions]

**Output Format:** [Phone calls with concise text summaries and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls require explicit user confirmation and support Indian (+91) numbers only; call results may include recordings and transcripts.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
