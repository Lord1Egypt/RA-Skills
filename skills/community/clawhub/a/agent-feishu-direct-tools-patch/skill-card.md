## Description: <br>
One-time/on-demand patch for openclaw-lark that enables Feishu tool calls from non-webhook agent paths by propagating session identity into the tool runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zouxiao7777](https://clawhub.ai/user/zouxiao7777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to patch openclaw-lark so Feishu tools invoked through Control UI, sessions_send, or other non-webhook paths use the current executing agent's Feishu account identity. It is intended for short-term patch application, validation, and rollback-aware maintenance rather than permanent always-on loading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies openclaw-lark source files and can affect Feishu tool behavior if applied to the wrong directory or version. <br>
Mitigation: Use a git branch or backup, confirm the runtime install path before editing, review the final diff, and apply the patch only when intentionally updating openclaw-lark. <br>
Risk: Patched files do not take effect until the OpenClaw Gateway or the Node process loading the plugin is restarted. <br>
Mitigation: Restart the Gateway after patching, then run low-impact Feishu DM and Control UI smoke tests before normal use. <br>
Risk: Leaving this patch skill permanently enabled may expose operational patch instructions during routine agent use. <br>
Mitigation: Remove or disable the skill after patching and validation are complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zouxiao7777/agent-feishu-direct-tools-patch) <br>
- [Agent Direct Feishu Tool Patch Guide](artifact/doc/OpenClaw-Multi-Agent-Feishu-Direct-Tools-Patch-Guide-(openclaw-lark).en.md) <br>
- [Agent Direct Tool Invocation Without Feishu Ticket](artifact/SKILL.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit operator confirmation before file edits and a gateway restart after patching.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
