## Description: <br>
A customer management skill for cloud account managers that organizes customer information, records follow-up history, and generates customer profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyuanyuan1](https://clawhub.ai/user/guyuanyuan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud account managers use this skill to maintain customer profiles, update visit and communication history, classify accounts, set follow-up reminders, and produce customer reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer records may contain sensitive client information. <br>
Mitigation: Install and use only when authorized to process the customer information involved, and keep customer records in a dedicated folder. <br>
Risk: Feishu document or table updates could expose or overwrite customer records if workspace permissions are wrong. <br>
Mitigation: Verify Feishu sharing and workspace permissions before creating or updating records, and review important edits. <br>
Risk: Unknown data-processing scripts or broad email and meeting archive processing could handle more data than intended. <br>
Mitigation: Do not run unknown data-processing scripts or process broad archives without clear user direction. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or text customer records, follow-up notes, reports, Feishu document/table updates, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, create, or update customer-profile files and Feishu records when authorized.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
