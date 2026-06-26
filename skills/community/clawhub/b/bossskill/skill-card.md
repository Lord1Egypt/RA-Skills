## Description: <br>
Startup coaching and boss secretary workflow for founders, small business owners, customer follow-up, team management, task review, business diagnosis, and operating checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanfanscoin](https://clawhub.ai/user/fanfanscoin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, small business owners, sales leaders, and project managers use this skill to turn natural-language business updates into CRM-style records, task follow-ups, operating checklists, customer follow-up plans, team management advice, and daily business review guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store customer, team, task, and business notes in a local SQLite database. <br>
Mitigation: Store only business-necessary records, avoid passwords, payment details, government IDs, trade secrets, and unnecessary private details, and protect the database and exported files. <br>
Risk: Licensed features may send the current command input plus license and device information to the vendor service. <br>
Mitigation: Use licensed cloud commands only when needed, review the current input before sending it, and avoid including sensitive or unrelated business data. <br>
Risk: Endpoint and license behavior can be influenced by BOOSKILL_* environment variables. <br>
Mitigation: Run the skill only in an environment you control and verify BOOSKILL_* variables before using license or cloud-core features. <br>
Risk: Public Word/PDF download links require uploading user-selected documents. <br>
Mitigation: Upload documents only when explicitly requested and remove secrets, private data, and unauthorized third-party information before upload. <br>


## Reference(s): <br>
- [BossSkill ClawHub listing](https://clawhub.ai/fanfanscoin/bossskill) <br>
- [SQLite business database reference](references/sqlite-database.md) <br>
- [Task reminder system reference](references/task-reminder-system.md) <br>
- [Team and customer schemas reference](references/team-customer-schemas.md) <br>
- [Checklists reference](references/checklists.md) <br>
- [Privacy notice](PRIVACY.md) <br>
- [License notice](LICENSE_NOTICE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON records and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or query a user-selected local SQLite database and may call licensed cloud endpoints only for explicit licensed commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
