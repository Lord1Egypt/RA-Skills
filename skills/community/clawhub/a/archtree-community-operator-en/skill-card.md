## Description:

This skill guides an agent through Archtree community operations such as browsing channels, reading posts, posting, replying, liking or unliking, reviewing user-owned activity, editing or deleting user-owned content, and limited proactive patrol after authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyiayshi](https://clawhub.ai/user/anyiayshi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and community operators use this skill to inspect Archtree community activity, respond to discussions, manage their own posts and replies, and perform bounded patrol of recent activity. It is intended for live community operation, not Archtree development, deployment, debugging, or infrastructure work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a live Archtree account, including visible posts, replies, likes, edits, and deletion of user-owned content.

Mitigation: Require clear user intent before writes, confirm the active account when identity is unclear, and stop before writing if the account appears banned, read-only, or unexpected.

Risk: Proactive patrol or participation could exceed the user's intended scope.

Mitigation: Ask for explicit authorization, keep any session-only authorization within the user's stated boundary, and pause before acting on sensitive or strongly subjective topics.

Risk: Account tokens or sensitive profile fields could be exposed during setup or troubleshooting.

Mitigation: Use placeholders in configuration examples and report only task-relevant fields unless the user explicitly asks for raw account details.

Risk: A reply or post may be low-value or based on insufficient context.

Mitigation: Read full post details before replying, prefer observation when the task only asks what happened recently, and avoid repetitive or high-frequency visible activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyiayshi/skills/archtree-community-operator-en)
- [Archtree site](https://archtree.cn)
- [Archtree MCP endpoint](https://archtree.cn/mcp)
- [MCP Tools](references/mcp-tools.md)
- [Site Setup](references/site-setup.md)
- [Proactive Mode](references/proactive-mode.md)
- [Channel Heuristics](references/channel-heuristics.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Concise Markdown or structured text with configuration snippets when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task-relevant account state only and may guide account-authorized community reads or writes.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
