## Description: <br>
APM Protocol (Agent Progressive Memory): Progressive disclosure protocol for group chat AND DM (main session) memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to give agents progressive workspace memory for direct sessions and group chats, with hooks that load context at session start and record memory flush state. It is most appropriate where persistent memory behavior is intentionally configured and reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent workspace memory hooks may expose private direct-session memory in group chats when group-name mapping is missing or the fallback path is left open. <br>
Mitigation: Configure memory/groups/group_names.json before using group chats, review the injected memory scope before deployment, and change unmapped groups to fail closed instead of falling back to direct-session memory. <br>
Risk: Automatic and scheduled flush behavior records session memory metadata and can preserve more context than intended. <br>
Mitigation: Review scheduled and precompact flush settings, inspect stored flush-state metadata, and deploy only in workspaces where persistent memory retention is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biociao/apm-agent-progressive-memory) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [HOOKS.md](artifact/HOOKS.md) <br>
- [apm_session_start hook documentation](artifact/hooks/apm_session_start/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JavaScript hook code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes memory file templates, OpenClaw hook handlers, installation commands, and configurable group-name mapping for chat-specific memory routing.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
