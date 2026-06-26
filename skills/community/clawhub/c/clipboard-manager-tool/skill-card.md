## Description: <br>
Clipboard history management for saving, searching, restoring, clearing, and reading clipboard items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yushimohuang](https://clawhub.ai/user/yushimohuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to inspect, set, save, search, restore, and clear local clipboard history across Windows, macOS, and Linux. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clipboard history can contain passwords, API keys, private messages, or proprietary text and is stored in a local plaintext workspace file. <br>
Mitigation: Avoid saving sensitive clipboard contents, ignore or delete clipboard-history.md regularly, and review it before sharing or committing workspace files. <br>
Risk: Set and restore actions can replace the current system clipboard content. <br>
Mitigation: Confirm the intended text or history item before running clipboard set or restore commands. <br>


## Reference(s): <br>
- [Skill definition](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes clipboard-history.md in the workspace root and trims saved history to 50 items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
