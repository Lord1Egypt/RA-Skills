## Description: <br>
Feishu Reading Notes helps an agent fetch shared article links, create structured Markdown reading notes, classify them by topic, and save them to Feishu Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxc168](https://clawhub.ai/user/yxc168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or personal productivity agents use this skill to archive shared WeChat, Weibo, Xueqiu, Bilibili, and public web content as categorized Markdown reading notes in Feishu Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes hardcoded Feishu credentials, fixed folder tokens, and a fixed notification recipient. <br>
Mitigation: Replace embedded Feishu secrets and destination tokens before use, and store workspace-specific configuration outside SKILL.md. <br>
Risk: The skill can delete same-named files and upload new files in configured Feishu folders. <br>
Mitigation: Require explicit user confirmation before Feishu deletion or upload actions and review the target folder before execution. <br>
Risk: The skill saves article content and reading metadata into a listed Feishu workspace. <br>
Mitigation: Use only when the user intends to store that content in the configured Feishu workspace and has rights to archive the source material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxc168/feishu-reading-notes) <br>
- [Publisher profile](https://clawhub.ai/user/yxc168) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Code, Configuration guidance] <br>
**Output Format:** [Markdown reading-note files with metadata, summaries, selected quotes, and preserved source content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local reading-note files, updates a link index, and uploads notes to configured Feishu Drive folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
