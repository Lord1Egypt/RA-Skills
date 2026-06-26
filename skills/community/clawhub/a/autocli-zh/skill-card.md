## Description: <br>
使用 autocli CLI 访问其已支持的网站、桌面应用与外部 CLI。用于浏览、搜索、查看时间线、书签、通知、主页、热榜、文章、历史记录，或在获得用户确认时执行目标平台已支持的写操作。对 autocli 已支持的目标，优先使用 autocli，而不是浏览器自动化或手工切换执行面；仅网站支持自定义适配器。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poiskgit](https://clawhub.ai/user/poiskgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route supported website, desktop application, and external CLI tasks through the local autocli command line. It supports read workflows such as search, feeds, bookmarks, notifications, articles, history, and trend checks, and requires explicit confirmation before public or potentially irreversible write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: autocli may use existing browser sessions and expose browser bridge state, logged-in page content, or request traffic during diagnostics, interception, or custom adapter work. <br>
Mitigation: Use those flows only after the agent explains the scope and receives explicit user consent. <br>
Risk: write actions such as posting, liking, following, deleting, or commenting may be public or irreversible. <br>
Mitigation: Confirm the target object, submitted content, and external visibility before execution; use a controlled environment first for sensitive accounts or production data. <br>
Risk: custom adapters and external CLI registration can persist changes under ~/.autocli. <br>
Mitigation: Require explicit approval before creating or modifying files in ~/.autocli/adapters, ~/.autocli/plugins, or ~/.autocli/external-clis.yaml, and perform a minimal verification after changes. <br>


## Reference(s): <br>
- [AutoCLI upstream project](https://github.com/nashsu/AutoCLI) <br>
- [Bilibili target reference](references/bilibili.md) <br>
- [Google target reference](references/google.md) <br>
- [Hacker News target reference](references/hackernews.md) <br>
- [Mtime target reference](references/mtime.md) <br>
- [Twitter / X target reference](references/twitter.md) <br>
- [Wikipedia target reference](references/wikipedia.md) <br>
- [Fallback workflow guide](guides/fallbacks.md) <br>
- [Custom adapters guide](guides/custom-adapters.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Simplified Chinese prose with optional Markdown, inline shell commands, JSON summaries, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should summarize useful results first, avoid unnecessary raw command dumps, and follow target-specific display guidance when a target reference defines it.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
