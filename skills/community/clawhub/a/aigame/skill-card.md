## Description:

AI能力试炼游戏 — 5章推理冒险，考验AI的推理、记忆、计算和决策能力。说「开始游戏」即可开始。

This skill is ready for commercial/non-commercial use.

## Publisher:

[val1813](https://clawhub.ai/user/val1813)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw agent play the AgentWorld five-chapter reasoning adventure through the hosted HTTP API, narrating observations, dialogue, and puzzle-solving as it progresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a throwaway remote game account and sends tokens, gameplay actions, nicknames, and session data to a raw IP address over unencrypted HTTP.

Mitigation: Use non-sensitive nicknames and gameplay text, review the network calls before enabling the skill, and prefer a future HTTPS version with explicit confirmation before registration.

Risk: Broad game-related triggers can start remote gameplay behavior when a user only makes a casual game request.

Mitigation: Require an explicit user confirmation before account registration or other network calls, and narrow triggers where the deployment platform allows it.

## Reference(s):

- [ClawHub aigame skill page](https://clawhub.ai/val1813/skills/aigame)
- [val1813 publisher profile](https://clawhub.ai/user/val1813)
- [aigame repository link listed in artifact](https://github.com/val1813/aigame)
- [AgentWorld game API base URL](http://111.231.112.127:9000)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown narrative with inline shell commands and summarized API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill contacts a remote HTTP game server and should summarize gameplay responses for the user instead of showing raw JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
