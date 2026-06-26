## Description: <br>
Read Feishu work-report data through the Report v1 API and turn it into daily or weekly summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taype](https://clawhub.ai/user/taype) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workplace automation users use this skill to fetch Feishu report entries by date, rule, or reporter and draft daily or weekly digests that highlight themes, completed work, blockers, next actions, and follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored Feishu/OpenClaw credentials to read sensitive workplace report data. <br>
Mitigation: Install only for trusted publishers and confirm the Feishu account, date range, report rule, and reporter filters before running the script. <br>
Risk: Raw report exports may expose workplace content if written to shared or temporary locations. <br>
Mitigation: Choose output paths deliberately, avoid shared temp locations for sensitive exports, and delete raw exports when they are no longer needed. <br>
Risk: Generated summaries may omit context or expose sensitive details when posted to Feishu chat or documents. <br>
Mitigation: Review the drafted digest before publishing it and remove confidential or unnecessary personal details. <br>


## Reference(s): <br>
- [Summary Template](references/summary-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/taype/feishu-report-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON report export plus a concise human-facing digest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write fetched report exports to a file; filters include date range, report rule, reporter ID, account, page size, and maximum item count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, created 2026-03-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
