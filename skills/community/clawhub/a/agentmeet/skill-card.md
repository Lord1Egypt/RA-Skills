## Description:

AgentMeet coordinates meetings between agents over email by reading Google Calendar availability, generating available slots, sending protocol-formatted messages, and parsing slot-selection replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmanchu](https://clawhub.ai/user/lmanchu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to coordinate meetings by having agents read calendar availability, generate slots, send protocol-formatted email invitations, and parse slot-selection replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs unaudited code from a hard-coded Dropbox path.

Mitigation: Verify the actual source, package manifest, and lockfile before installing, and run dependency installation in an isolated environment.

Risk: The skill can send emails or create calendar events without clearly documented user confirmation.

Mitigation: Require explicit approval before sending messages or creating events, review invite contents, and set the timezone deliberately.

Risk: Outbound invite emails may include an adoption link in addition to scheduling content.

Mitigation: Review the full outgoing invite body, including links, before sending.

## Reference(s):

- [ClawHub AgentMeet skill page](https://clawhub.ai/lmanchu/skills/agentmeet)
- [AgentMeet project homepage](https://github.com/agentmeet/agentmeet)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bun plus Google Calendar and Gmail access; generated email content and calendar changes should be reviewed before sending or creating events.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
