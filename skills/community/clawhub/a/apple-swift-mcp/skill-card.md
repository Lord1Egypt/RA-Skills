## Description: <br>
This skill should be used when the user asks about Apple app data via the native Swift MCP, including Calendar, Reminders, Contacts, Maps, Mail, Messages, or Notes on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to let an agent interact with Apple app data and personal productivity workflows through a native Swift MCP server. It covers calendar and reminder management, contact and map lookup, email and note workflows, and message sending or history queries on macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive local app data such as email, messages, notes, contacts, calendar data, reminders, and message history. <br>
Mitigation: Install it only when this local macOS automation is intended, grant permissions narrowly, and review sensitive reads before using their results. <br>
Risk: The skill can send outgoing mail or messages through macOS applications. <br>
Mitigation: Require explicit user confirmation before any outgoing email, iMessage, SMS, reply, or forwarded message is sent. <br>
Risk: Security evidence flags insufficient scoping and user-control guarantees for sensitive local data and messaging authority. <br>
Mitigation: Confirm what each tool will access before use and avoid broad local permissions unless the access need is clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/apple-swift-mcp) <br>
- [Project repository linked in skill documentation](https://github.com/chrischall/apple-swift-mcp) <br>
- [GitHub releases linked in skill documentation](https://github.com/chrischall/apple-swift-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger MCP-backed actions against local macOS apps when the user grants required permissions.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
