## Description: <br>
Send the same notification across email through Himalaya and iMessage through BlueBubbles with shared markdown formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to send one user-provided notification through email and iMessage in the same workflow. It helps format the message consistently, send each configured channel, and report full or partial delivery failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real messages externally through configured email and iMessage channels. <br>
Mitigation: Verify the email address, iMessage target, subject, message body, and selected channels before sending. <br>
Risk: A partial failure can leave only one channel delivered. <br>
Mitigation: Report which channels succeeded or failed and retry only the failed channel after confirming the target and content. <br>
Risk: Notification bodies may disclose sensitive information to external recipients. <br>
Mitigation: Review message content before delivery and avoid sending secrets, credentials, or unintended private details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/cross-channel-notify) <br>
- [Channel Configuration](references/channels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and formatted notification text for email and iMessage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats a full markdown email body and a compact plain-text iMessage body truncated to 2000 characters.] <br>

## Skill Version(s): <br>
9.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
