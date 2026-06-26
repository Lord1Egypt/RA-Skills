## Description: <br>
Get笔记炼金术 helps an agent turn Get笔记录音 notes into privacy-reviewed, distilled, structured knowledge assets archived to Feishu Bitable, with optional IMA and Feishu wiki sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingclaw](https://clawhub.ai/user/qingclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External professionals such as lawyers, consultants, trainers, and sales teams use this skill to process private recording notes into searchable, reusable knowledge records. It supports single-recording, batch, scheduled, search, and statistics workflows around Get笔记, Feishu Bitable, and optional knowledge-base destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads private Get笔记录音 and can archive distilled content into Feishu or optional knowledge bases. <br>
Mitigation: Install it only for workspaces where that access is intended, verify the destination Feishu workspace and permissions, and keep optional sync targets disabled until configured. <br>
Risk: Scheduled scanning can automatically process new recordings. <br>
Mitigation: Keep scheduled scanning off unless automatic processing is desired, and review configuration before enabling batch or cron-style workflows. <br>
Risk: Legal, client, financial, medical, or business-strategy recordings may contain sensitive information even after automated redaction. <br>
Mitigation: Manually review privacy reports and redaction results before syncing high-sensitivity recordings to shared destinations. <br>


## Reference(s): <br>
- [Privacy Rules](references/privacy-rules.md) <br>
- [Distillation Prompt Templates](references/distill-prompts.md) <br>
- [Feishu Bitable Setup Guide](references/bitable-setup.md) <br>
- [Get笔记 Homepage](https://biji.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/qingclaw/getnote-alchemy) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries and structured records, with JSON-backed configuration and processing state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces privacy review reports, distilled knowledge fields, Feishu Bitable records, and optional IMA or Feishu wiki entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
