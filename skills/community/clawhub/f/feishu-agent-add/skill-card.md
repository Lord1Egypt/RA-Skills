## Description:

Helps OpenClaw users add a Feishu-connected agent through a guided prompt flow or a generated one-command setup path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyecho-io](https://clawhub.ai/user/cyecho-io)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to add a Feishu bot-backed agent without manually editing OpenClaw configuration. It collects the agent name, purpose, app credentials, and setup preferences, previews the plan, then runs the bundled configurator or provides a ready-to-run command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu App Secret values during setup.

Mitigation: Prefer interactive secret entry, avoid pasting secrets into command lines or shared chats, and review generated configuration before use.

Risk: The security summary says the skill deserves review before installation because it handles secrets and user-supplied agent instructions.

Mitigation: Review the skill before installing, run with --dry-run first, and inspect generated SOUL.md and BOOTSTRAP.md files before using the new agent.

Risk: Agent-to-agent access may broaden what the new agent can reach.

Mitigation: Disable agent-to-agent access unless the workflow specifically requires it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyecho-io/skills/feishu-agent-add)
- [README](artifact/README.md)
- [SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON summaries from the setup script when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or preview OpenClaw configuration entries, Feishu account bindings, workspace files, and next-step guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
