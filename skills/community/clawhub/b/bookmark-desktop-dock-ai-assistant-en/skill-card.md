## Description:

Bookmark & Desktop Dock AI Assistant works with the Command Compass Windows app to turn prompts, skill files, local files, folders, app shortcuts, web links, and browser bookmarks into searchable, copy-ready, open-ready cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create Command Compass CardSchema v1 cards for prompts, local resources, web favorites, app shortcuts, and quick-launch workflows. It is intended for organizing user-selected resources into cards that can be copied, searched, or opened from the Command Compass desktop app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplemental files may be loaded as active instructions and steer an agent toward external website changes or package replacement.

Mitigation: Use only SKILL.md as the active skill instructions, treat supplemental files as reference evidence, and remove or clearly quarantine WEBSITE_AGENT_INSTRUCTIONS.md before broad distribution.

Risk: Cards can point to local files, shortcuts, executables, scripts, or private paths selected by the user.

Mitigation: Require user confirmation before opening executable or script-like targets, avoid inventing local paths or secrets, and keep local resource organization limited to user-selected or confirmed items.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/skills/bookmark-desktop-dock-ai-assistant-en)
- [Publisher profile](https://clawhub.ai/user/addogiavara-tech)
- [Command Compass download page](https://www.wboke.com/zh/download)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Configuration]

**Output Format:** [JSON arrays or objects containing Command Compass CardSchema v1 cards, with concise Markdown guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cards should keep copied content in instruction, openable targets in openTarget, and conservative permissions for local files, shortcuts, executables, and scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
