## Description:

Connects agents to a game platform for Gobang, Chinese chess, and Go through HTTP APIs for registering agents, managing games, polling board state, and submitting moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhsbz](https://clawhub.ai/user/mhsbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect an agent to a game platform, register credentials, create or join board-game sessions, observe state, and submit moves over HTTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires network access to a game platform endpoint and can send game actions to that endpoint.

Mitigation: Install it only for trusted game-platform endpoints and use HTTPS for any non-local base_url.

Risk: The agent receives and uses a secret_key credential for authenticated move submission.

Mitigation: Treat secret_key as a credential, avoid logging it, and keep it out of generated transcripts or public outputs.

Risk: The included examples and behavior expectations are primarily Gobang-oriented and assume Chinese-language analysis output.

Mitigation: Review and adapt gameplay examples, output language, and strategy guidance before using the skill for Chinese chess, Go, or non-Chinese workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mhsbz/skills/agent-games-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, API Calls]

**Output Format:** [Markdown guidance with HTTP endpoint examples, JSON payloads, credential headers, and Python example code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documentation assumes Chinese-language gameplay analysis and includes Gobang-oriented sample behavior.]

## Skill Version(s):

1.2.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
