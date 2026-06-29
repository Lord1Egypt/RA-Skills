## Description: <br>
Bookmark & Desktop Dock AI Assistant works with the Command Compass Windows app to turn prompts, skill files, local files, folders, app shortcuts, web links, and browser bookmarks into searchable, copy-ready, open-ready cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize selected prompts, skill files, local resources, app shortcuts, web links, and bookmarks into Command Compass cards for fast copying, searching, and opening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local files, folders, shortcuts, and bookmarks can expose private paths or resource names if users add sensitive resources to cards. <br>
Mitigation: Only add resources the user intentionally selects, and keep local paths, file contents, and private data out of public website or market data. <br>
Risk: Opening executable, shortcut, installer, or script-like targets can trigger local actions outside the agent response. <br>
Mitigation: Keep shell permission disabled in generated cards and require user confirmation before opening executable or script-like targets. <br>
Risk: Website or command-market matches could sync resources the user did not intend to add. <br>
Mitigation: Use confirmation-based sync and review matches before adding them to the local Command Compass library. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/skills/bookmark-desktop-dock-ai-assistant-en) <br>
- [Command Compass download page](https://www.wboke.com/zh/download) <br>


## Skill Output: <br>
**Output Type(s):** [json, guidance, configuration] <br>
**Output Format:** [JSON object or array containing Command Compass CardSchema v1 cards.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cards use instruction as the copy field and openTarget as the openable resource address.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
