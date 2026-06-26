## Description: <br>
Provides strict guidance for occasional HEARTBEAT.md updates, requiring a single replacement status block at most once per hour. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quratus](https://clawhub.ai/user/quratus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to keep HEARTBEAT.md concise by replacing it with a single short status block when an update is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Updating HEARTBEAT.md replaces the file and can remove useful context if the wrong path or stale state is used. <br>
Mitigation: Confirm the target file path and use normal safeguards such as version control or backups before allowing the overwrite. <br>
Risk: Frequent or appended heartbeat updates can clutter the status file and confuse downstream heartbeat handling. <br>
Mitigation: Check the last update time, update at most once per hour, and keep only one short status block. <br>


## Reference(s): <br>
- [Breadcrumb Writer on ClawHub](https://clawhub.ai/quratus/breadcrumb-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files] <br>
**Output Format:** [Markdown status block or concise editing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No hidden code, installs, credentials, or network behavior found in server security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
