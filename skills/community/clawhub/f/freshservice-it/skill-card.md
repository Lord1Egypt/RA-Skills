## Description: <br>
Access Freshservice via the Freshservice API to manage tickets, requesters, agents, assets, changes, problems, and service catalog data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT service management teams and agents use this skill to inspect Freshservice resources and perform ticket or resource changes through a connected Freshservice account after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a Freshservice account and can access sensitive IT service data using the connected account's permissions. <br>
Mitigation: Use a Freshservice account with appropriate permissions and review the connected account scope before use. <br>
Risk: Create, update, or delete operations can change Freshservice tickets, assets, changes, or related resources. <br>
Mitigation: Review write or delete previews carefully and approve only actions that match the user's intent. <br>


## Reference(s): <br>
- [Freshservice API Documentation](https://api.freshservice.com/) <br>
- [Freshservice Ticket API](https://api.freshservice.com/v2/tickets.html) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live Freshservice tool catalog exposed through ClawLink; write and destructive actions require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
