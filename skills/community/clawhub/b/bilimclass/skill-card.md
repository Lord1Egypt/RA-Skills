## Description: <br>
Accesses the BilimClass school platform for Kazakhstan students to retrieve schedules, homework, grades, and diary entries through API-backed CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[podberezovk](https://clawhub.ai/user/podberezovk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, especially Kazakhstan students using BilimClass, use this skill to ask an agent for their school schedule, homework, diary details, and grade summaries. Developers or OpenClaw users can also run the bundled CLI commands directly after configuring their own BilimClass credentials. <br>

### Deployment Geography for Use: <br>
Kazakhstan <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived BilimClass JWTs and school account data. <br>
Mitigation: Keep ~/.openclaw/.env.json private, do not commit or paste credentials into chats, and refresh or revoke tokens if they are exposed. <br>
Risk: Broad auto-triggering can cause unintended schedule, diary, homework, or grade lookups. <br>
Mitigation: Prefer explicit BilimClass requests and review trigger behavior before installing the skill for routine agent use. <br>
Risk: The skill is intended for access to the user's own BilimClass data. <br>
Mitigation: Install only when the agent should access the user's own BilimClass schedule, homework, diary, and grades. <br>


## Reference(s): <br>
- [ClawHub BilimClass release page](https://clawhub.ai/podberezovk/bilimclass) <br>
- [BilimClass platform](https://bilimclass.kz) <br>
- [BilimClass schedule API endpoint](https://api.bilimclass.kz/api/v4/os/clientoffice/schedule) <br>
- [BilimClass journal API endpoint](https://journal-service.bilimclass.kz/diary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown prose with inline shell commands and JSON examples; CLI output is formatted text or raw JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include school schedule, homework, diary, and grade data for the configured BilimClass account.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
