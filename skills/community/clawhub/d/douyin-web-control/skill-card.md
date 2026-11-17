## Description:

Use this skill when the user wants an Agent to operate Douyin web through the douyin-web CLI, including launching or focusing Douyin, login checks, feed navigation, search, current video info, playback control, comments, likes, following the current author, favorites, sharing, danmaku, screenshots, or screen/audio recording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billwang233](https://clawhub.ai/user/billwang233)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to control Douyin Web through the douyin-web CLI for browser launch, login checks, navigation, search, playback, screenshots, recording, and user-approved interactions. Developers and testers can also use it to validate or extend the CLI while preserving manual handling for login, captcha, and account-risk checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can execute an unreviewed local or installed CLI that controls an authenticated Douyin browser session.

Mitigation: Use a pinned, reviewed CLI revision in an isolated virtual environment, set DOUYIN_WEB_CLI or DOUYIN_CLI_ROOT to a trusted absolute path, and avoid untrusted workspaces.

Risk: The skill can trigger public or account-affecting actions such as likes, follows, favorites, shares, comments, danmaku, or recording.

Mitigation: Require explicit user confirmation before account-affecting actions or recording, and use isolated --profile or --home values for separate sessions.

Risk: Login, captcha, SMS verification, and account-risk checks require human handling.

Mitigation: Pause automation when these checks appear, have the user complete them manually, and resume only after status or wait-login confirms the session state.

## Reference(s):

- [Feature Matrix](references/feature-matrix.md)
- [douyin-web CLI project](https://github.com/billwang233/douyin-web-cli)
- [ClawHub skill page](https://clawhub.ai/billwang233/skills/douyin-web-control)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to inspect CLI JSON fields and screenshot paths, and to require user confirmation before account-affecting actions.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
