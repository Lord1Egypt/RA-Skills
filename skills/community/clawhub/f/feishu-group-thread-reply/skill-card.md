## Description: <br>
Force openclaw-lark bot replies into message threads in Feishu group chats, preventing main chat noise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arianxx](https://clawhub.ai/user/Arianxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to check and apply Feishu group-chat thread reply patches after setup or plugin updates. It helps keep bot replies in message threads instead of the main group chat stream. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The patch changes local OpenClaw Feishu behavior for all group replies. <br>
Mitigation: Confirm that thread replies are desired for all Feishu group chats before applying the patch. <br>
Risk: Local plugin updates can overwrite the patched OpenClaw files. <br>
Mitigation: Run the check-only commands after updates and reapply the patch only when the check reports it is missing. <br>
Risk: Production systems may need rollback if the patched behavior is not desired. <br>
Mitigation: Back up affected files before patching production systems and restart the gateway only after reviewing the change. <br>
Risk: Heartbeat auto-reapply can restore the patch after future plugin updates. <br>
Mitigation: Add heartbeat auto-reapply steps only when persistent restoration of the patch is intentional. <br>


## Reference(s): <br>
- [How Feishu Group Thread Reply Works](references/how-it-works.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Arianxx/feishu-group-thread-reply) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and patch guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes check-only commands, patch commands, restart guidance, and optional heartbeat reapply guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
