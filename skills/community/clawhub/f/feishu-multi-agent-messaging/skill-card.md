## Description: <br>
Helps OpenClaw agents coordinate Feishu group and direct messages across multiple bot accounts using accountId routing and user open_id mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wulinsquarelikui](https://clawhub.ai/user/wulinsquarelikui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators configuring OpenClaw multi-agent workflows use this skill to route Feishu group chat and direct messages through the correct bot identity, maintain user ID mappings, and support group handoff between agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu bot credentials and appSecret values could be exposed if copied into repositories or shared documents. <br>
Mitigation: Keep appSecret values out of repositories and shared docs, and store production credentials only in approved secret-management locations. <br>
Risk: Incorrect accountId, target, or user open_id mappings can send messages to the wrong bot, user, or chat. <br>
Mitigation: Verify accountId bindings, target IDs, allowlists, and user mapping files before sending messages through Feishu bots. <br>
Risk: Feishu messages may include personal data, secrets, or sensitive document links in real group chats. <br>
Mitigation: Avoid posting secrets, personal data, or sensitive document links into group chats and restrict bot permissions to the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wulinsquarelikui/feishu-multi-agent-messaging) <br>
- [Architecture design](docs/architecture.md) <br>
- [User ID mapping](docs/id-mapping.md) <br>
- [Collaboration workflow](docs/workflow.md) <br>
- [Troubleshooting](docs/troubleshooting.md) <br>
- [Message samples](examples/message-samples.md) <br>
- [OpenClaw configuration example](examples/openclaw.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; outputs operational messaging guidance and example configuration rather than executable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
