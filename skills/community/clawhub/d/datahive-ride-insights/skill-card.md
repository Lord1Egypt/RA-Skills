## Description: <br>
Fetches ride-sharing receipt emails from Gmail, extracts structured ride records through a local loopback OpenClaw Gateway, stores results in JSON and SQLite, and can produce ride insights plus an anonymized CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datahiveai](https://clawhub.ai/user/datahiveai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to build a local ride receipt database, review spending and travel patterns, and export a shareable anonymized ride report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches Gmail ride receipts and stores raw receipt email content locally, which can include sensitive travel, financial, and HTML receipt data. <br>
Mitigation: Limit the Gmail account and date scope before fetching, protect the generated local files, and delete raw email exports when they are no longer needed. <br>
Risk: Extraction sends raw per-email JSON and HTML receipt content to the active local Gateway-backed model. <br>
Mitigation: Confirm user consent before extraction and use only a loopback Gateway host such as localhost, 127.0.0.1, or ::1. <br>
Risk: The anonymized CSV excludes direct identifiers but remains a derived mobility dataset that may still be sensitive. <br>
Mitigation: Review the CSV before sharing it and retain or upload it only when the user is comfortable with the remaining disclosure risk. <br>


## Reference(s): <br>
- [Ride Insights on ClawHub](https://clawhub.ai/datahiveai/datahive-ride-insights) <br>
- [ClawHub](https://clawhub.com) <br>
- [DataHive AI](https://datahive.ai) <br>
- [DataHive Missions Blog](https://datahive.ai/blog/) <br>
- [Provider Gmail Queries](references/provider_queries.json) <br>
- [Ride SQLite Schema](references/schema_rides.sql) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, SQLite database, CSV, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands; generated local artifacts include JSON, SQLite, and CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default extraction is capped at 50 emails unless the user approves more; raw receipt JSON persists locally until deleted.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
