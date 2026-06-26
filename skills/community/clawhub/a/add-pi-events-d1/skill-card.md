## Description: <br>
Add or update PI events in the Cloudflare D1 mb-events database using parsed event details, ISO 8601 dates, and SQL commands executed remotely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ababen](https://clawhub.ai/user/ababen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Site maintainers use this skill to turn event prompts, CSV rows, or event lists into Cloudflare D1 SQL updates for the babenchuk.com events database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to write to or delete from a live Cloudflare D1 database. <br>
Mitigation: Require the agent to show the exact SQL, target database, and affected event records before any write or delete, then explicitly confirm the action. <br>
Risk: Misconfigured credentials or broad Cloudflare permissions could expose more authority than the events workflow needs. <br>
Mitigation: Use a dedicated least-privilege Cloudflare token for the controlled account and keep a backup or rollback path for live-site data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ababen/add-pi-events-d1) <br>
- [Babenchuk events page](https://babenchuk.com/#events) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated SQL for inserts, updates, deletes, verification queries, and event-data normalization guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
