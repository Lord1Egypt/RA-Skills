## Description: <br>
App Rank Monitor fetches Apple and Diandian app ranking data, generates daily Markdown reports, and sends them to DingTalk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cfans731](https://clawhub.ai/user/cfans731) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to collect app store ranking data, generate daily monitoring reports, and send ranking summaries and report files to a DingTalk group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes DingTalk credentials and can send reports automatically. <br>
Mitigation: Replace or rotate all DingTalk credentials before use and verify the destination chat or webhook. <br>
Risk: The skill can use stored Diandian login secrets and persist browser sessions. <br>
Mitigation: Replace Diandian credentials, use a dedicated account when possible, and clear persisted browser sessions when they are no longer needed. <br>
Risk: The skill can delete local data during cleanup and transmit generated reports. <br>
Mitigation: Run cleanup and report sending manually first, confirm what will be removed or transmitted, then enable scheduled automation. <br>
Risk: Debug screenshot or HTML capture can retain sensitive session or page data. <br>
Mitigation: Disable debug capture unless actively troubleshooting and remove captured files after review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cfans731/app-rank-monitor) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Scheduled task configuration](artifact/docs/定时任务配置说明.md) <br>
- [Platform mapping guide](artifact/docs/平台映射说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, DingTalk messages, Excel files, configuration snippets, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send generated reports to DingTalk and may write local ranking data, logs, browser state, screenshots, or downloaded files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
