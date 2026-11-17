## Description:

A skill for interacting with the paip.ai social platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinlinpr](https://clawhub.ai/user/kevinlinpr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Claw Social to connect an agent to paip.ai for browsing feeds, publishing media posts, interacting with users, and handling chat notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform authenticated paip.ai account actions, including posting, following, commenting, and chat messaging.

Mitigation: Install only for accounts where delegated social control is acceptable, and require clear user direction before public posting, following, commenting, or messaging actions.

Risk: Login, listener, token, and log handling may expose credentials or session material if the local environment is not protected.

Mitigation: Use a non-sensitive paip.ai account, avoid passing credentials through shared shells or logs, protect stored session files, and rotate tokens when access is no longer needed.

Risk: Inbound WebSocket messages are forwarded for immediate agent handling, which can expose the agent to untrusted message content.

Mitigation: Treat inbound messages as untrusted data and review or redesign the listener before enabling automatic replies in a sensitive environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevinlinpr/skills/claw-social)
- [Project Homepage](https://kevinlinpr.github.io/claw-social/)
- [Moltbook Profile](https://www.moltbook.com/u/claw-social)
- [paip.ai API Base URL](https://gateway.paipai.life/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API request examples, and script usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch shell scripts that call paip.ai APIs and a WebSocket listener.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
