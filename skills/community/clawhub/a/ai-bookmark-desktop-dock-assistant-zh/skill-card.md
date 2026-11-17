## Description:

AI收藏夹与桌面Dock助手配合指令罗盘 Windows 客户端，把提示词、技能文件、本地文件、文件夹、软件快捷方式、网页链接和浏览器收藏夹整理成可搜索、可复制、可打开的指令卡。

This skill is ready for commercial/non-commercial use.

## Publisher:

[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate Command Compass CardSchema v1 cards for prompts, local files, folders, application shortcuts, web links, browser bookmarks, and reusable AI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes website migration instructions outside the main local Command Compass card-generation purpose.

Mitigation: Review before installing and avoid loading it into agents with write access to website repositories or deployment artifacts unless that migration work is intended.

Risk: Generated cards can reference local files, folders, executable shortcuts, scripts, or private paths.

Mitigation: Generate cards only for user-selected resources, keep shell permissions false, require confirmation before opening executable or script targets, and do not upload local paths or file contents.

## Reference(s):

- [Command Compass Download Page](https://www.wboke.com/zh/download)
- [ClawHub Skill Page](https://clawhub.ai/addogiavara-tech/skills/ai-bookmark-desktop-dock-assistant-zh)
- [Publisher Profile](https://clawhub.ai/user/addogiavara-tech)

## Skill Output:

**Output Type(s):** [configuration, guidance]

**Output Format:** [JSON arrays or a JSON object with a cards array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command Compass CardSchema v1 cards use instruction for copied content and openTarget for file, folder, shortcut, or URL launch targets.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
