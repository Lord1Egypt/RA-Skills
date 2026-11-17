## Description:

Provides a one-time patch workflow for openclaw-lark so Feishu tool calls from non-webhook agent paths can preserve the current agent's account and sender identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zouxiao7777](https://clawhub.ai/user/zouxiao7777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to patch an OpenClaw openclaw-lark installation when Control UI or sessions_send Feishu tool calls lose the current agent's Feishu identity. It guides code changes, restart requirements, validation, and rollback for that one-time patching workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the patch changes Feishu authorization and session handling in ways that can confuse identities and expose session keys.

Mitigation: Install or run it only in a reviewed development workflow, back up the openclaw-lark plugin, confirm every diff, and smoke test Feishu DM and Control UI behavior before using a shared gateway.

Risk: The security guidance flags the session-key fallback, persistent sessions.json lookup, and full session-key logging as unsuitable for shared gateway deployment.

Mitigation: Fix or remove those behaviors before shared or production deployment, and avoid logging complete session keys.

Risk: The fallback reinstall command can overwrite local plugin edits and is unpinned when written as npx -y @larksuite/openclaw-lark install.

Mitigation: Use rollback first, get explicit operator confirmation before reinstalling, and pin and verify the package before any production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zouxiao7777/skills/agent-feishu-direct-tools-patch)
- [Agent Direct Feishu Tool Patch guide](artifact/doc/OpenClaw-Multi-Agent-Feishu-Direct-Tools-Patch-Guide-(openclaw-lark).en.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code blocks and file-level patch instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit operator confirmation before edits, gateway restart after edits, and Feishu DM plus Control UI smoke tests.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
