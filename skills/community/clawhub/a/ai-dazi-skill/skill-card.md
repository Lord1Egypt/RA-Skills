## Description: <br>
AI搭子匹配平台 generates local AI-usage profiles and matching tags from user-provided usage data such as token use, model preferences, tool usage, and activity patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dory123456](https://clawhub.ai/user/dory123456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn user-approved AI usage metrics into a local profile with player level, activity score, skill tags, AI style, and matching tags. It supports personal usage analysis and AI-collaboration discovery without automatic log collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores detailed local AI-usage analytics, including active-hour patterns, model and tool preferences, and installed-skill lists. <br>
Mitigation: Use the skill only for explicit profile-generation requests, review what data is saved, and periodically inspect or delete the skill data directory. <br>
Risk: Loose activation and file-writing boundaries may retain more usage data than the user intended. <br>
Mitigation: Avoid custom JSON or custom date values for the save command, and keep data collection scoped to current, user-approved profile-generation workflows. <br>


## Reference(s): <br>
- [AI搭子 Skill - 开发与使用指南](references/guide.md) <br>
- [AI搭子 Skill - 数据格式参考](references/data-formats.md) <br>
- [ClawHub release page](https://clawhub.ai/dory123456/ai-dazi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily usage aggregates and generated profiles under the skill data directory when explicitly invoked.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
