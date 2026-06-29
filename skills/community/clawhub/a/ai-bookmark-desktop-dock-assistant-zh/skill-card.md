## Description: <br>
AI收藏夹与桌面Dock助手。配合指令罗盘 Windows 客户端使用，把提示词、技能文件、本地文件、文件夹、软件快捷方式、网页链接和浏览器收藏夹整理成可搜索、可复制、可打开的指令卡。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
外部用户和桌面生产力工作流用户可用此技能为 Command Compass 生成指令卡，用于整理用户选择的 Prompt、文件、文件夹、快捷方式、网页链接和浏览器收藏。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cards may expose private local paths or sensitive content if users place those details in cards that are shared or synced remotely. <br>
Mitigation: Review cards before syncing or sharing, and avoid including private paths, file contents, tokens, cookies, passwords, API keys, or other sensitive data. <br>
Risk: Cards may point to executable files, shortcuts, scripts, installers, or external links. <br>
Mitigation: Keep shell permissions disabled in generated cards and require explicit user confirmation before opening executable, shortcut, script, installer, or link targets. <br>
Risk: Incorrect guessed local paths could create misleading or unsafe launch targets. <br>
Mitigation: Generate local file, folder, and downloads cards only from user-selected or user-provided paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/skills/ai-bookmark-desktop-dock-assistant-zh) <br>
- [Command Compass download page](https://www.wboke.com/zh/download) <br>
- [Skill source](artifact/SKILL.md) <br>
- [Command Compass adaptation report](artifact/COMMAND_COMPASS_SKILL_ADAPTATION_REPORT.md) <br>
- [Example Command Compass card package](artifact/examples/daily-file-index-cards.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Configuration, Guidance] <br>
**Output Format:** [JSON array or JSON object containing Command Compass CardSchema v1 cards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cards use the instruction field for copied content and openTarget plus resourceKind for files, folders, links, bookmarks, and local resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
