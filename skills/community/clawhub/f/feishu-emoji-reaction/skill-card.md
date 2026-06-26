## Description: <br>
Enables an agent to add Feishu emoji reactions, interpret user reaction events, decide when to reply or stay silent, and maintain learned emoji mappings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chargiie](https://clawhub.ai/user/chargiie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents using Feishu through OpenClaw use this skill to acknowledge messages with emoji reactions, respond appropriately to user reaction events, and learn Feishu-specific emoji meanings over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials may be required for standalone scripts. <br>
Mitigation: Use a least-privileged Feishu app and store app IDs and secrets only in secure environment or configuration storage. <br>
Risk: Broad reaction notifications can expose more conversation activity than the agent needs. <br>
Mitigation: Keep reaction notifications limited to own messages unless broader monitoring is intentional. <br>
Risk: Learned emoji notes may retain user-specific communication patterns. <br>
Mitigation: Periodically review or clear learned emoji memory files. <br>
Risk: Reaction event message IDs include suffixes that can cause Feishu API failures if reused directly. <br>
Mitigation: Strip the ':reaction:' suffix and call the API with the pure om_xxx message ID. <br>


## Reference(s): <br>
- [Feishu message reaction API documentation](https://open.feishu.cn/document/server-docs/im-v1/message-reaction/emojis-introduce) <br>
- [Feishu emoji list](references/emoji-list.md) <br>
- [OpenClaw messaging tool documentation](https://docs.openclaw.ai/tools/messaging) <br>
- [OpenClaw Feishu channel configuration](https://docs.openclaw.ai/channels/feishu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript message-tool examples, shell command examples, and JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to emit Feishu reaction API calls and use NO_REPLY when a text response is not needed.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
