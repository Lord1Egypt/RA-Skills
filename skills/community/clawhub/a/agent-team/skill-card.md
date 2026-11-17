## Description:

Manages and invokes a team of role-specific AI agents for task execution and interactive chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to list, inspect, spawn, and chat with role-specific OpenClaw agents for coding, writing, analysis, research, and review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running spawn or chat sends agent persona content and user task or chat text to configured OpenClaw models.

Mitigation: Review the configured model providers and avoid sending sensitive prompts, SOUL.md content, or tasks unless that routing is acceptable.

Risk: The greeting helper includes placeholder API-key handling and has incomplete disclosure of its DashScope network calls.

Mitigation: Use environment variables for credentials, do not hardcode real API keys, and document or review outbound model API calls before use.

Risk: The skill documentation and command output are primarily Chinese-language, which may reduce reviewability for some teams.

Mitigation: Have a Chinese-reading reviewer inspect the skill behavior, configuration, and prompts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/skills/agent-team)
- [ClawHub publisher profile](https://clawhub.ai/user/jiangzhiyu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output depends on the configured agents, local OpenClaw setup, and selected model providers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
