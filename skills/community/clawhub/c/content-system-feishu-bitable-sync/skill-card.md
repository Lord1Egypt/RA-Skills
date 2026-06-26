## Description: <br>
Sync a local `wechat-report` result into Feishu Bitable after the user has reviewed the report and confirmed the sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill after reviewing a local WeChat report to sync article records into a configured Feishu Bitable. It is intended for workflows that need source_url-based deduplication, update-in-place behavior, and a CSV fallback when direct sync fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mutate configured Feishu Bitable records, including updating rows and clearing previous record contents during deduplication. <br>
Mitigation: Use least-privileged Feishu credentials, verify FEISHU_BITABLE_APP_TOKEN and FEISHU_BITABLE_TABLE_ID before running, and run only after explicit review and confirmation. <br>
Risk: Markdown input can direct the skill to a local raw JSON path, which may be unexpected if the Markdown came from an untrusted source. <br>
Mitigation: Use trusted report files only and inspect the raw JSON path before execution. <br>
Risk: Direct sync failures produce CSV fallback files that may contain article metadata and should be handled as operational data. <br>
Mitigation: Review generated CSV files before manual import and store or delete them according to the workspace data-handling policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abigale-cyber/content-system-feishu-bitable-sync) <br>
- [Publisher profile](https://clawhub.ai/user/abigale-cyber) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [runtime.py](artifact/runtime.py) <br>
- [skill.json](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, API calls] <br>
**Output Format:** [Markdown sync report, optional CSV fallback, and updated local JSON status metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Feishu Bitable rows using source_url deduplication and records sync status in local output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
