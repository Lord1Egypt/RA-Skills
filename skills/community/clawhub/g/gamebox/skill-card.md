## Description:

Gamebox provides a dependency-free Python framework for shared-directory multiplayer agent games with script-managed turns, state, actions, and messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use Gamebox to coordinate multiplayer text games between agents through a shared filesystem. Python scripts enforce game state and protocol while agents provide narration, moderation, puzzle content, or gameplay guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared files and private game data are not safely scoped or access-controlled.

Mitigation: Install only for trusted local or sandboxed multi-agent play, use a dedicated game directory with restrictive filesystem permissions, and do not store secrets in messages or game state.

Risk: Private and role channels may not protect information from untrusted participants until path containment and authentication are added.

Mitigation: Use private and role channels only with trusted participants and avoid confidential information in game messages.

## Reference(s):

- [Gamebox ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/gamebox)
- [Protocol reference](references/protocol.md)
- [RPG prompt template](references/games/rpg.md)
- [Werewolf prompt template](references/games/werewolf.md)
- [Story relay prompt template](references/games/story_relay.md)
- [CTF prompt template](references/games/ctf.md)
- [Civilization prompt template](references/games/civilization.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command examples and JSON script responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script outputs follow a status/data or status/error JSON protocol and use local shared-directory game state.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
