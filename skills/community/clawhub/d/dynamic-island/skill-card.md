## Description:

Dynamic Island is a macOS desktop widget that monitors OpenClaw agents in real time and shows idle, alert, thinking, done, and error states in a frosted-glass pill UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhixiangshon-cell](https://clawhub.ai/user/zhixiangshon-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, configure, and run a macOS desktop status widget that monitors multiple local OpenClaw agents, previews recent messages, and opens configured Feishu or Lark chat links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local desktop process reads OpenClaw session logs and displays recent prompt and response snippets.

Mitigation: Use it only on trusted Macs and avoid running it against agents or sessions that contain sensitive information.

Risk: The local WebView and WebSocket path is underprotected.

Mitigation: Keep the services bound to loopback and add authentication, origin checks, HTML escaping, and URL allowlists before broader use.

Risk: The install and startup flow can install dependencies, compile a widget, start local processes, and configure login auto-start.

Mitigation: Review setup and startup commands first, prefer a pinned virtual environment, and avoid LaunchAgent auto-start until the launch configuration is present and reviewed.

## Reference(s):

- [Dynamic Island on ClawHub](https://clawhub.ai/zhixiangshon-cell/skills/dynamic-island)
- [OpenClaw Dynamic Island project homepage](https://github.com/zhixiangshon-cell/openclaw-dynamic-island)
- [OpenClaw](https://github.com/nicepkg/openclaw)
- [emolog](https://apps.apple.com/app/emolog/id6443809191)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS 13+ with Python 3.9+, Swift, and the websockets package.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
