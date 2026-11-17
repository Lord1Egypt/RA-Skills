## Description:

Interactive interface for the text adventure game Endless Downstairs, providing game state management and event selection handling for players who want to play a horror text adventure with an AI assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gsc578045031-cloud](https://clawhub.ai/user/gsc578045031-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to play Endless Downstairs through an AI assistant that translates player intent into local Python game commands and returns the game text. Developers can also inspect or run the included Python text adventure directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Player text can be routed into a shell-style Python command path.

Mitigation: Pass player text as a literal argument or structured parameter, avoid shell concatenation, and review the command before execution.

Risk: The assistant could continue gameplay or execute multiple game commands without a fresh player decision.

Mitigation: Require one explicit player instruction per turn and execute at most one local game command for that instruction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gsc578045031-cloud/skills/endless-downstairs)
- [README](artifact/README.md)
- [Skill instructions](artifact/skill.md)
- [Security scan source](evidence.json)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text game responses with local Python command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One command per conversation turn; game progress is persisted in local JSON save files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
