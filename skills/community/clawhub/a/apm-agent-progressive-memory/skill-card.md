## Description:

APM Protocol (Agent Progressive Memory): Progressive disclosure protocol for group chat AND DM (main session) memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to structure agent memory for private sessions and group chats, with progressive loading, memory write-back rules, and hooks for session bootstrap and flush tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private DM memory can be exposed in group sessions when chat mapping or detection fails.

Mitigation: Avoid group use until the DM fallback fails closed, keep group_names.json mappings complete, and review behavior before installing in workspaces with private notes or group chats.

Risk: Automatic memory bootstrap and persistence can surface or retain sensitive workspace context.

Mitigation: Install only in workspaces where automatic memory loading and persistence are acceptable, and review the bundled hooks before enabling them.

Risk: Flush-state handling can blur DM and group boundaries in the current hook design.

Mitigation: Avoid group workflows until flush-state separation is fixed and verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biociao/skills/apm-agent-progressive-memory)
- [SKILL.md](artifact/SKILL.md)
- [HOOKS.md](artifact/HOOKS.md)
- [ADDENDUM.md](artifact/ADDENDUM.md)
- [apm_session_start hook documentation](artifact/hooks/apm_session_start/HOOK.md)
- [remem-flush hook documentation](artifact/hooks/remem-flush/HOOK.md)
- [precompact-remem hook documentation](artifact/hooks/precompact-remem/HOOK.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file templates, hook installation commands, and JavaScript hook code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bootstrap and flush hooks that can read or update workspace memory state when installed.]

## Skill Version(s):

1.6.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
