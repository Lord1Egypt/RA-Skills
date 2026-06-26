## Description: <br>
Search chats, list/read messages, and send messages via Beeper Desktop using the beeper-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foeken](https://clawhub.ai/user/foeken) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to search Beeper chats, review messages, send or edit messages, manage chats, and transfer attachments through the Beeper Desktop CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose Beeper chat contents to an agent during search and message review. <br>
Mitigation: Use read-only commands when only search or review is needed, and quote only the minimum message content required for the task. <br>
Risk: The skill can send, edit, archive, create, upload, download, and delete messaging-related content. <br>
Mitigation: Review recipients, message text, chat identifiers, and file paths before executing any command that changes chats, messages, reminders, or assets. <br>
Risk: The BEEPER_ACCESS_TOKEN grants access to the Beeper Desktop API. <br>
Mitigation: Keep BEEPER_ACCESS_TOKEN private, store it securely, and install the skill only when the publisher is trusted. <br>


## Reference(s): <br>
- [Beeper CLI release page](https://clawhub.ai/foeken/beeper-cli) <br>
- [beeper-cli](https://github.com/foeken/beeper-cli) <br>
- [beeper-cli releases](https://github.com/foeken/beeper-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the beeper binary, Beeper Desktop with API access enabled, and a BEEPER_ACCESS_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
