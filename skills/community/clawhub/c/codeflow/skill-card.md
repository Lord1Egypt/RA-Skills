## Description:

Codeflow streams coding-agent CLI sessions to Discord or Telegram, showing tool calls, file writes, shell commands, results, and session summaries without additional LLM calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subjadeites](https://clawhub.ai/user/subjadeites)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use Codeflow to make local coding-agent runs observable in Discord or Telegram. It is suited for relaying implementation, debugging, code review, and parallel task sessions where teammates need to see agent activity and results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed development-session content may be sent to Discord or Telegram and stored in local stream logs by default.

Mitigation: Use only approved channels, enable CODEFLOW_SAFE_MODE=true for shared channels, and set CODEFLOW_STREAM_LOG=redacted or off when sensitive content may appear.

Risk: Agent permission boundaries can be weakened when users enable unrestricted agent modes or install persistent enforcement hooks.

Mitigation: Review the workflow before installation, avoid global bypassPermissions or --dangerously-skip-permissions unless explicitly accepted, and treat enforcer installation as an administrative action.

Risk: The enforcer install path changes OpenClaw plugin configuration and may restart the gateway.

Mitigation: Limit install or update actions to trusted operators and expect the current conversation or thread to be interrupted during a gateway restart.

## Reference(s):

- [Codeflow ClawHub Page](https://clawhub.ai/subjadeites/skills/codeflow)
- [First-Time Setup](references/setup.md)
- [Advanced Modes](references/advanced-modes.md)
- [Discord and Telegram Output](references/discord-output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured Discord or Telegram relay messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can stream detailed development-session content; safe mode can suppress file previews and command output bodies.]

## Skill Version(s):

2.0.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
