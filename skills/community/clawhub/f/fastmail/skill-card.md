## Description: <br>
Manages Fastmail email and calendar via JMAP and CalDAV APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[witooh](https://clawhub.ai/user/witooh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent read, search, send, organize, and delete Fastmail email, and to view or change Fastmail calendar events, reminders, and invitation responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to Fastmail email and calendar data, including message contents and calendar events. <br>
Mitigation: Install only in trusted agent environments and use revocable app-specific Fastmail credentials. <br>
Risk: The skill supports high-impact actions such as sending email, reply-all, deleting or bulk deleting email, changing calendar events, and responding to invitations. <br>
Mitigation: Require explicit manual approval before send, reply-all, delete, bulk email, calendar change, or RSVP actions. <br>
Risk: Fastmail tokens, usernames, and app passwords can be exposed if stored carelessly. <br>
Mitigation: Keep credentials out of committed files and avoid committing .env files. <br>


## Reference(s): <br>
- [Fastmail Skill Page](https://clawhub.ai/witooh/fastmail) <br>
- [Fastmail Tools Reference](references/TOOLS.md) <br>
- [Fastmail](https://www.fastmail.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool results with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Fastmail credentials through environment variables for email and calendar operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
