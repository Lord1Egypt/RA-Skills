## Description: <br>
Connects multiple REST APIs, fetches and transforms data, and pushes it to a live Google Sheets dashboard that auto-updates on a schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to configure an automated pipeline that pulls selected REST API data, transforms it, and syncs it into Google Sheets dashboards on a schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pipeline uses Google service-account credentials and connected API credentials. <br>
Mitigation: Confirm service-account permissions, target Sheet sharing, and connected API scopes before installation; store credentials only in the configured secrets manager. <br>
Risk: Selected API data is written to Google Sheets and may be buffered locally after failed writes. <br>
Mitigation: Avoid regulated or highly sensitive data unless Google Sheets storage and temporary local buffering are acceptable under the user's data policy. <br>
Risk: Frequent scheduled syncs can exceed source API limits or write malformed data if upstream schemas change. <br>
Mitigation: Set a schedule that matches API rate limits and validate response schemas before writing rows to Sheets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neo1307/argus-api-pipeline) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/neo1307) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code, shell commands, and configuration snippets for a scheduled API-to-Google-Sheets pipeline.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a live Google Sheets dashboard, pipeline run logs, and failure alerts when implemented by the agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
